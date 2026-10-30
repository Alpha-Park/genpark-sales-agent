# -*- coding: utf-8 -*-
"""
GenPark Sales Agent FastMCP Server
"""

import json
from typing import Dict, List, Any, Optional
from mcp.server.fastmcp import FastMCP
from client import GenParkSalesAgent

mcp = FastMCP("genpark-sales-agent")
sales = GenParkSalesAgent()

@mcp.tool()
def evaluate_bant_meddic_qualification(lead_profile_json: str) -> str:
    """
    Evaluates BANT and MEDDIC criteria to produce a composite sales qualification score.
    """
    profile = json.loads(lead_profile_json)
    res = sales.evaluate_bant_meddic_qualification(profile)
    return json.dumps(res, indent=2)

@mcp.tool()
def calculate_price_elasticity_and_discount_ceiling(
    deal_size_usd: float,
    customer_tier: str = "enterprise",
    competitor_pressure_score: float = 0.5,
    gross_margin_pct: float = 75.0,
    max_discount_cap_pct: float = 30.0
) -> str:
    """
    Calculates allowable discount ceiling preserving minimum gross margin hurdles.
    """
    res = sales.calculate_price_elasticity_and_discount_ceiling(deal_size_usd, customer_tier, competitor_pressure_score, gross_margin_pct, max_discount_cap_pct)
    return json.dumps(res, indent=2)

@mcp.tool()
def forecast_pipeline_velocity_and_slippage(
    deals_json: str,
    target_quarter_days: int = 90
) -> str:
    """
    Forecasts B2B pipeline velocity and identifies deals at risk of quarter slippage.
    """
    deals = json.loads(deals_json)
    res = sales.forecast_pipeline_velocity_and_slippage(deals, target_quarter_days)
    return json.dumps(res, indent=2)

def main():
    print("Testing Sales Agent:")
    lead = {"has_budget_allocated": True, "is_economic_buyer": True, "need_urgency_score": 0.9, "implementation_timeline_months": 2}
    print(evaluate_bant_meddic_qualification(json.dumps(lead)))

if __name__ == "__main__":
    main()
