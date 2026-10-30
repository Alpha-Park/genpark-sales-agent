# -*- coding: utf-8 -*-
import json
from client import GenParkSalesAgent

agent = GenParkSalesAgent()

# 1. BANT + MEDDIC Enterprise Lead Qualification
lead = {
    "lead_id": "opp_90210",
    "has_budget_allocated": True,
    "is_economic_buyer": True,
    "need_urgency_score": 0.85,
    "implementation_timeline_months": 3,
    "clear_roi_metrics_defined": True,
    "technical_criteria_documented": True,
    "procurement_steps_mapped": True,
    "critical_business_pain_identified": True,
    "internal_champion_identified": True
}
qualification = agent.evaluate_bant_meddic_qualification(lead)
print(f"Lead Qualification: Score={qualification['composite_qualification_score']} | Tier: {qualification['qualification_tier']}")
print(f"  Recommended Action: {qualification['recommended_next_action']}")

# 2. Price Elasticity & Margin Hurdle Solver
discount = agent.calculate_price_elasticity_and_discount_ceiling(
    deal_size_usd=120000.0,
    customer_tier="enterprise",
    competitor_pressure_score=0.7,
    gross_margin_pct=80.0
)
print()
print(f"Deal Discounting: Original=${discount['original_deal_size_usd']} -> Proposed=${discount['discounted_deal_size_usd']} ({discount['recommended_discount_pct']}% off)")
print(f"  Gross Profit: ${discount['realized_gross_profit_usd']} (Margin: {discount['realized_gross_margin_pct']}%, Status: {discount['margin_health']})")

# 3. Pipeline Velocity & Slippage Risk Modeling
pipeline = [
    {"id": "d1", "name": "Fintech Tier-1 Migration", "amount_usd": 150000, "win_probability": 0.7, "sales_cycle_days": 60, "days_in_current_stage": 10, "expected_stage_days": 14},
    {"id": "d2", "name": "HealthCorp AI Audit", "amount_usd": 85000, "win_probability": 0.4, "sales_cycle_days": 75, "days_in_current_stage": 35, "expected_stage_days": 14}, # stalled
    {"id": "d3", "name": "Logistics Route Engine", "amount_usd": 200000, "win_probability": 0.5, "sales_cycle_days": 90, "days_in_current_stage": 12, "expected_stage_days": 20}
]
velocity = agent.forecast_pipeline_velocity_and_slippage(pipeline)
print()
print(f"Pipeline Velocity: ${velocity['pipeline_velocity_usd_per_day']}/day | Expected QTR Rev: ${velocity['expected_quarter_revenue_usd']}")
print(f"Slippage Alerts: {velocity['slippage_alerts_count']} deals stalled")
for s in velocity["slippage_risk_deals"]:
    print(f"  Stalled Deal '{s['deal_name']}': {s['days_in_stage']} days in stage (expected {s['expected_stage_days']})")
