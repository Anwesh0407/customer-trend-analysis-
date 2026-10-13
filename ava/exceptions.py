"""
AVA Domain Exceptions
"""

class AvaException(Exception):
    """Base exception for all AVA domain errors."""
    pass

AVABaseException = AvaException

class SourceUnavailable(AvaException):
    """Raised when an external or conditional data source is missing credentials or inaccessible."""
    pass

class ComplianceViolation(AvaException):
    """Raised when a request violates crawling compliance, robots.txt, or domain bans."""
    pass

class DomainBlockedError(ComplianceViolation):
    """Raised when an attempted fetch targets a prohibited marketplace domain."""
    pass

class RateLimitExceeded(AvaException):
    """Raised when requests exceed configured frequency limits."""
    pass

class ValidationError(AvaException):
    """Raised when data fails schema validation rules."""
    pass

class NicheNotFoundError(AvaException):
    """Raised when a requested niche ID does not exist."""
    pass

class ProductNotFoundError(AvaException):
    """Raised when an ASIN lookup fails."""
    pass

class StorageError(AvaException):
    """Raised on repository or database connection failures."""
    pass

class VerifierError(AvaException):
    """Raised when assistant response verifier detects unsupported numerical claims."""
    pass
