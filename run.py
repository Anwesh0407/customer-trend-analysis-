#!/usr/bin/env python3
"""AVA (Amazon Vendor Assist) CLI Entry Point.

Commands:
  collect   - Ingest data from CSV/JSON sources into data/raw/
  clean     - Process, validate, and deduplicate raw data into data/cleaned/
  analyze   - Compute market insights and write data/reports/
  load      - Load cleaned data idempotently into the database
  pipeline  - Execute collect -> clean -> analyze -> load end to end
  serve     - Start the FastAPI integration server
"""
from __future__ import annotations

import argparse
import json
import logging
import os
import sys
from pathlib import Path
from typing import Optional

from ava.config import get_settings
from ava.logging_setup import configure_logging

logger = logging.getLogger("ava.cli")


def cmd_collect(args: argparse.Namespace) -> int:
    """Collect data from source adapters and save timestamped raw files."""
    from ava.collectors.product_collector import ProductCollector
    from ava.collectors.review_collector import ReviewCollector
    from ava.sources.csv_source import CSVSource
    from ava.sources.json_source import JSONSource

    limit: Optional[int] = args.limit
    input_prod: Optional[str] = args.input_products
    input_rev: Optional[str] = args.input_reviews

    # Default to synthetic sample data if no inputs provided
    if not input_prod:
        default_csv = Path("data/sample/sample_products.csv")
        default_json = Path("data/sample/sample_products.json")
        if default_csv.exists():
            input_prod = str(default_csv)
        elif default_json.exists():
            input_prod = str(default_json)

    if not input_rev:
        default_rev_csv = Path("data/sample/sample_reviews.csv")
        if default_rev_csv.exists():
            input_rev = str(default_rev_csv)

    print("=== [AVA] Collecting Raw Data ===")
    prod_raw_path = None
    if input_prod:
        print(f"Product source: {input_prod} (limit={limit})")
        if input_prod.endswith(".json") or input_prod.endswith(".jsonl"):
            source = JSONSource(input_prod)
        else:
            source = CSVSource(input_prod)

        collector = ProductCollector(raw_dir="data/raw")
        items = collector.collect(source, limit=limit)
        print(f"Products collected: {len(items)}")

    if input_rev:
        print(f"Review source: {input_rev} (limit={limit})")
        if input_rev.endswith(".json") or input_rev.endswith(".jsonl"):
            source = JSONSource(input_rev)
        else:
            source = CSVSource(input_rev)

        collector = ReviewCollector(raw_dir="data/raw")
        items = collector.collect(source, limit=limit)
        print(f"Reviews collected: {len(items)}")

    print("=== Collection Complete ===")
    return 0


def cmd_clean(args: argparse.Namespace) -> int:
    """Clean, parse, normalize, and validate raw data into data/cleaned/."""
    from ava.processing.cleaning import run_cleaning_pipeline

    print("=== [AVA] Cleaning Data ===")
    res = run_cleaning_pipeline(
        raw_product_path=args.input_products,
        raw_review_path=args.input_reviews,
        output_dir="data/cleaned",
        limit=args.limit,
    )
    print(f"Products in: {res['products_in']}, out: {res['products_out']}, rejected: {res['products_rejected']}, deduped: {res['duplicates_removed']}")
    print(f"Reviews in: {res['reviews_in']}, out: {res['reviews_out']}")
    print(f"Reports saved to: data/cleaned/cleaning_report.json")
    print("=== Cleaning Complete ===")
    return 0


def cmd_analyze(args: argparse.Namespace) -> int:
    """Compute market statistics and preliminary insights."""
    import pandas as pd
    from ava.analytics.market import compute_market_analytics
    from ava.analytics.opportunities import generate_preliminary_insights
    from ava.analytics.report import generate_market_report

    print("=== [AVA] Running Analytics ===")
    clean_csv = Path("data/cleaned/products_clean.csv")
    if not clean_csv.exists():
        print(f"Error: {clean_csv} does not exist. Run 'python run.py clean' first.", file=sys.stderr)
        return 1

    df = pd.read_csv(clean_csv)
    if args.limit:
        df = df.head(args.limit)

    niche = None
    if args.niche:
        try:
            from ava.models import Niche
            niche_dict = json.loads(args.niche)
            niche = Niche(**niche_dict)
        except Exception:
            print(f"Warning: could not parse niche JSON: {args.niche}")

    md_path = generate_market_report(df, niche=niche, output_dir="data/reports")
    market = compute_market_analytics(df, niche=niche)
    opps = generate_preliminary_insights(df, niche=niche)

    print(f"Summary: {market['sample_size']} listings analyzed across {len(market['price_bands'])} price bands.")
    print(f"Opportunities detected: {len(opps.get('insights', []))}")
    print(f"Report written to: data/reports/market_summary.json and {md_path}")
    print("=== Analytics Complete ===")
    return 0


def cmd_load(args: argparse.Namespace) -> int:
    """Load cleaned data into database using repository and verify counts."""
    from ava.storage.sql_repository import SQLAlchemyRepository
    from ava.storage.files import load_cleaned_data_to_db

    print("=== [AVA] Loading Data to Database ===")
    repo = SQLAlchemyRepository()
    repo.init_db()

    res = load_cleaned_data_to_db(repo, cleaned_dir=args.cleaned_dir or "data/cleaned")
    print(f"Database: {repo.db_url}")
    print(f"Products loaded: {res['products_loaded']} (Saved/Updated: {res['products_saved']})")
    print(f"Reviews loaded: {res['reviews_loaded']} (Saved: {res['reviews_saved']})")
    print(f"Verification against report: {'PASSED' if res['verified_against_report'] else 'FAILED/SKIPPED'}")
    if res["expected_rows_out"] is not None:
        print(f"Expected: {res['expected_rows_out']}, Actual: {res['products_loaded']}")
    print(f"Data mode: {res['data_mode']}")
    print("=== Load Complete ===")
    return 0


def cmd_pipeline(args: argparse.Namespace) -> int:
    """Run full pipeline: collect -> clean -> analyze -> load."""
    print("###############################################")
    print("### RUNNING FULL AVA DATA PIPELINE END TO END ###")
    print("###############################################")
    ret = cmd_collect(args)
    if ret != 0:
        return ret
    ret = cmd_clean(args)
    if ret != 0:
        return ret
    ret = cmd_analyze(args)
    if ret != 0:
        return ret
    ret = cmd_load(args)
    if ret != 0:
        return ret
    print("###############################################")
    print("### PIPELINE COMPLETED SUCCESSFULLY ###")
    print("###############################################")
    return 0


def cmd_serve(args: argparse.Namespace) -> int:
    """Start FastAPI server."""
    import uvicorn
    settings = get_settings()
    host = args.host or settings.HOST
    port = args.port or settings.PORT
    reload = args.reload

    print(f"Starting AVA FastAPI Server on http://{host}:{port} (reload={reload})...")
    uvicorn.run("api.main:app", host=host, port=port, reload=reload)
    return 0


def main() -> int:
    configure_logging()
    parser = argparse.ArgumentParser(description="AVA (Amazon Vendor Assist) CLI")
    subparsers = parser.add_subparsers(dest="command", help="Available subcommands")

    # collect
    p_collect = subparsers.add_parser("collect", help="Collect raw data from sources")
    p_collect.add_argument("--input-products", "-ip", help="Path to input products file")
    p_collect.add_argument("--input-reviews", "-ir", help="Path to input reviews file")
    p_collect.add_argument("--limit", "-l", type=int, help="Max records to collect")

    # clean
    p_clean = subparsers.add_parser("clean", help="Clean, validate, and deduplicate data")
    p_clean.add_argument("--input-products", "-ip", help="Path to raw products file")
    p_clean.add_argument("--input-reviews", "-ir", help="Path to raw reviews file")
    p_clean.add_argument("--limit", "-l", type=int, help="Max records to clean")

    # analyze
    p_analyze = subparsers.add_parser("analyze", help="Compute analytics and market reports")
    p_analyze.add_argument("--niche", "-n", help="Niche filter JSON string")
    p_analyze.add_argument("--limit", "-l", type=int, help="Max records to analyze")

    # load
    p_load = subparsers.add_parser("load", help="Load cleaned data into database")
    p_load.add_argument("--cleaned-dir", "-cd", default="data/cleaned", help="Cleaned data directory")

    # pipeline
    p_pipe = subparsers.add_parser("pipeline", help="Run collect -> clean -> analyze -> load")
    p_pipe.add_argument("--input-products", "-ip", help="Path to input products file")
    p_pipe.add_argument("--input-reviews", "-ir", help="Path to input reviews file")
    p_pipe.add_argument("--limit", "-l", type=int, help="Max records")
    p_pipe.add_argument("--niche", "-n", help="Niche filter JSON string")
    p_pipe.add_argument("--cleaned-dir", "-cd", default="data/cleaned", help="Cleaned data directory")

    # serve
    p_serve = subparsers.add_parser("serve", help="Start the FastAPI backend server")
    p_serve.add_argument("--host", default=None, help="Host address")
    p_serve.add_argument("--port", type=int, default=None, help="Port")
    p_serve.add_argument("--reload", action="store_true", default=False, help="Enable auto-reload")

    args = parser.parse_args()
    if not args.command:
        parser.print_help()
        return 1

    commands = {
        "collect": cmd_collect,
        "clean": cmd_clean,
        "analyze": cmd_analyze,
        "load": cmd_load,
        "pipeline": cmd_pipeline,
        "serve": cmd_serve,
    }

    try:
        return commands[args.command](args)
    except Exception as e:
        logger.exception("Error executing command '%s': %s", args.command, e)
        print(f"Error: {e}", file=sys.stderr)
        return 1


if __name__ == "__main__":
    sys.exit(main())
