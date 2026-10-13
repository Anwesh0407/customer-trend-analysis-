"""
AVA Compliant HTTP Client
Strictly implements compliance safeguards:
- Hard domain blocking (Amazon domains refused by default)
- Robots.txt enforcement
- Per-host rate limiting
- Immediate stop on 401, 403, and CAPTCHAs
- Exponential backoff on transient errors (429, 5xx) with Retry-After respect
"""

import time
import urllib.parse
import urllib.robotparser
from typing import Optional, Dict, Any
import requests
from ava.config import settings
from ava.exceptions import DomainBlockedError, ComplianceViolation, RateLimitExceeded
from ava.logging_setup import logger

class CompliantHttpClient:
    def __init__(self, time_provider=time.time, sleep_provider=time.sleep):
        self._time = time_provider
        self._sleep = sleep_provider
        self._last_request_per_host: Dict[str, float] = {}
        self._robots_cache: Dict[str, urllib.robotparser.RobotFileParser] = {}
        self.session = requests.Session()
        self.session.headers.update({"User-Agent": settings.USER_AGENT})

    def is_domain_blocked(self, url: str) -> bool:
        hostname = urllib.parse.urlparse(url).hostname or ""
        hostname = hostname.lower()
        for blocked in settings.BLOCKED_DOMAINS:
            if hostname == blocked or hostname.endswith("." + blocked):
                return True
        return False

    def can_fetch_robots(self, url: str) -> bool:
        parsed = urllib.parse.urlparse(url)
        base = f"{parsed.scheme}://{parsed.netloc}"
        if base not in self._robots_cache:
            rp = urllib.robotparser.RobotFileParser()
            rp.set_url(f"{base}/robots.txt")
            try:
                rp.read()
            except Exception as e:
                logger.warning(f"Failed to fetch robots.txt for {base}: {e}. Conservative fallback: refusing fetch.")
                return False
            self._robots_cache[base] = rp
        return self._robots_cache[base].can_fetch(settings.USER_AGENT, url)

    def get(self, url: str, check_robots: bool = True, max_retries: int = 2) -> requests.Response:
        # 1. Enforce Domain Block
        if self.is_domain_blocked(url):
            raise DomainBlockedError(
                f"Compliance Violation: Fetch to {url} blocked. Prohibited marketplace domain in settings.BLOCKED_DOMAINS."
            )

        # 2. Check robots.txt if requested
        if check_robots and not self.can_fetch_robots(url):
            raise ComplianceViolation(f"Robots.txt disallows crawling {url} for user agent {settings.USER_AGENT}")

        # 3. Rate limiting per host
        parsed = urllib.parse.urlparse(url)
        host = parsed.netloc
        now = self._time()
        last_req = self._last_request_per_host.get(host, 0.0)
        elapsed = now - last_req
        if elapsed < settings.RATE_LIMIT_DELAY:
            delay = settings.RATE_LIMIT_DELAY - elapsed
            self._sleep(delay)

        attempts = 0
        backoff = 1.0

        while attempts <= max_retries:
            attempts += 1
            self._last_request_per_host[host] = self._time()
            try:
                resp = self.session.get(url, timeout=settings.REQUEST_TIMEOUT)

                # 4. Immediate stop on 401, 403
                if resp.status_code in (401, 403):
                    raise ComplianceViolation(
                        f"Aborting fetch: Access denied ({resp.status_code}) on {url}. Bypassing authentication is strictly prohibited."
                    )

                # 5. Immediate stop on CAPTCHA detection
                text_sample = resp.text[:2000].lower()
                if "captcha" in text_sample or "robot check" in text_sample or "enter the characters" in text_sample:
                    raise ComplianceViolation(
                        f"Aborting fetch: CAPTCHA detected on {url}. Anti-bot bypass is strictly prohibited."
                    )

                # 6. Retry-After / 429 / 5xx handling
                if resp.status_code == 429:
                    retry_after = resp.headers.get("Retry-After")
                    sleep_sec = float(retry_after) if retry_after and retry_after.isdigit() else backoff
                    if attempts <= max_retries:
                        logger.warning(f"Rate limited (429) on {host}. Backing off for {sleep_sec}s...")
                        self._sleep(sleep_sec)
                        backoff *= 2.0
                        continue
                    else:
                        raise RateLimitExceeded(f"Rate limit exceeded (429) on {url} after {max_retries} retries.")

                if resp.status_code >= 500:
                    if attempts <= max_retries:
                        logger.warning(f"Server error ({resp.status_code}) on {url}. Retrying with backoff {backoff}s...")
                        self._sleep(backoff)
                        backoff *= 2.0
                        continue

                return resp

            except requests.RequestException as e:
                if attempts <= max_retries:
                    self._sleep(backoff)
                    backoff *= 2.0
                    continue
                raise e

        raise requests.RequestException(f"Failed to fetch {url} after {max_retries} attempts.")

http_client = CompliantHttpClient()
