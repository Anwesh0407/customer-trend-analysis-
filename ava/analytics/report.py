"""
AVA Market Report Generator
Outputs reports/market_summary.json and reports/market_report.md.
"""

import json
import os
import pandas as pd
from typing import Optional
from ava.models import Niche
from ava.analytics.market import compute_market_analytics
from ava.analytics.opportunities import generate_preliminary_insights, STANDING_LIMITATIONS

def generate_market_report(
    df: pd.DataFrame,
    niche: Optional[Niche] = None,
    output_dir: str = "data/reports"
) -> str:
    os.makedirs(output_dir, exist_ok=True)
    market = compute_market_analytics(df, niche)
    opps = generate_preliminary_insights(df, niche)

    # 1. market_summary.json
    json_path = os.path.join(output_dir, "market_summary.json")
    summary_data = {
        "market": market,
        "opportunities": opps,
        "standing_limitations": STANDING_LIMITATIONS
    }
    with open(json_path, "w", encoding="utf-8") as f:
        json.dump(summary_data, f, indent=2)

    # 2. market_report.md
    md_path = os.path.join(output_dir, "market_report.md")
    lines = [
        "# AVA Market Analysis Report",
        "",
        "> **Notice:** This report is based on public catalog observations. Review counts reflect customer attention, not unit sales.",
        "",
        "## Executive Summary",
        f"- **Sample Size:** {market['sample_size']} products analyzed",
        f"- **Median Price:** ₹{market['price_metrics']['median']} (Range: ₹{market['price_metrics']['min']} – ₹{market['price_metrics']['max']})",
        f"- **Median Customer Rating:** {market['rating_metrics']['median']} ★ (Mean: {market['rating_metrics']['mean']} ★)",
        f"- **Brand Competition:** Top 5 brands control {market['brand_metrics']['top_5_share_pct']}% of observed listings",
        "",
        "## Price Band Distribution",
        "| Price Band | Count | Share (%) | Avg Rating |",
        "| :--- | :---: | :---: | :---: |"
    ]

    for pb in market["price_bands"]:
        lines.append(f"| {pb['band_name']} | {pb['product_count']} | {pb['share_pct']}% | {pb['avg_rating']} ★ |")

    lines.extend([
        "",
        "## Preliminary Insights & Hypotheses",
        ""
    ])

    if opps.get("insights_suppressed"):
        lines.append(f"> *{opps['reason']}*")
    else:
        for ins in opps.get("insights", []):
            lines.append(f"### {ins['title']} (Confidence: {ins['confidence']})")
            lines.append(f"- **Observation [Actual]:** {ins['observation']}")
            lines.append(f"- **Hypothesis [Estimate]:** {ins['hypothesis']}")
            lines.append(f"- **Evidence:** {ins['evidence']}")
            lines.append(f"- **Limitations:** {ins['limitations']}")
            lines.append("")

    lines.extend([
        "## Standing Limitations",
        ""
    ])
    for lim in STANDING_LIMITATIONS:
        lines.append(f"- {lim}")

    lines.append("")

    with open(md_path, "w", encoding="utf-8") as f:
        f.write("\n".join(lines))

    return md_path
