# -*- coding: utf-8 -*-
"""
GenPark Sales Agent Client
Zero-dependency BANT/MEDDIC multi-criteria sales qualification evaluator,
price elasticity discount hurdle solver, and pipeline velocity & slippage forecaster.
"""

import math
from typing import Dict, List, Any, Optional

class GenParkSalesAgent:
    """
    Evaluates enterprise B2B sales lead qualification, solves allowable discount ceilings
    against gross margin thresholds, and forecasts sales pipeline velocity.
    """

    def evaluate_bant_meddic_qualification(
        self,
        lead_profile: Dict[str, Any]
    ) -> Dict[str, Any]:
        """
        Evaluates BANT (Budget, Authority, Need, Timeline) and MEDDIC criteria to produce a composite lead score.
        """
        # BANT evaluation (weight: 40%)
        budget_allocated = lead_profile.get("has_budget_allocated", False)
        authority_is_c_level = lead_profile.get("is_economic_buyer", False)
        need_urgency = lead_profile.get("need_urgency_score", 0.5)  # 0 to 1
        timeline_months = lead_profile.get("implementation_timeline_months", 12)

        bant_b = 25.0 if budget_allocated else 5.0
        bant_a = 25.0 if authority_is_c_level else 10.0
        bant_n = max(0.0, min(25.0, need_urgency * 25.0))
        bant_t = 25.0 if timeline_months <= 3 else (15.0 if timeline_months <= 6 else 5.0)
        bant_score = bant_b + bant_a + bant_n + bant_t

        # MEDDIC evaluation (weight: 60%)
        # Metrics, Economic Buyer, Decision Criteria, Decision Process, Identify Pain, Champion
        meddic_metrics = 16.6 if lead_profile.get("clear_roi_metrics_defined", False) else 5.0
        meddic_econ_buyer = 16.6 if authority_is_c_level else 5.0
        meddic_criteria = 16.6 if lead_profile.get("technical_criteria_documented", False) else 5.0
        meddic_process = 16.6 if lead_profile.get("procurement_steps_mapped", False) else 5.0
        meddic_pain = 16.6 if lead_profile.get("critical_business_pain_identified", False) else 5.0
        meddic_champion = 17.0 if lead_profile.get("internal_champion_identified", False) else 5.0
        meddic_score = meddic_metrics + meddic_econ_buyer + meddic_criteria + meddic_process + meddic_pain + meddic_champion

        composite_score = round(0.40 * bant_score + 0.60 * meddic_score, 1)

        if composite_score >= 80.0:
            tier = "SQL (Sales Qualified Lead - Fast Track)"
            action = "Schedule Executive Commercial Proposal & Technical POC Review"
        elif composite_score >= 60.0:
            tier = "SAL (Sales Accepted Lead - High Potential)"
            action = "Secure Economic Buyer introduction and map procurement timeline"
        elif composite_score >= 40.0:
            tier = "Marketing Nurture Lead"
            action = "Enroll in automated industry case study email sequence"
        else:
            tier = "Disqualified"
            action = "Archive lead or route to self-serve freemium tier"

        return {
            "lead_id": lead_profile.get("lead_id", "lead_unnamed"),
            "composite_qualification_score": composite_score,
            "qualification_tier": tier,
            "bant_score": round(bant_score, 1),
            "meddic_score": round(meddic_score, 1),
            "recommended_next_action": action,
            "risk_factors": [
                k for k, v in [
                    ("No allocated budget", not budget_allocated),
                    ("No internal champion", not lead_profile.get("internal_champion_identified", False)),
                    ("Long timeline (>6 months)", timeline_months > 6)
                ] if v
            ]
        }

    def calculate_price_elasticity_and_discount_ceiling(
        self,
        deal_size_usd: float,
        customer_tier: str = "enterprise",
        competitor_pressure_score: float = 0.5,
        gross_margin_pct: float = 75.0,
        max_discount_cap_pct: float = 30.0
    ) -> Dict[str, Any]:
        """
        Calculates allowable discount ceiling preserving minimum gross margin hurdles.
        Formula: Gross Margin at Discount d = (Price * (1 - d) - COGS) / (Price * (1 - d))
        """
        if deal_size_usd <= 0:
            raise ValueError("Deal size must be positive.")

        # Baseline cost of goods sold (COGS)
        cogs = deal_size_usd * (1.0 - gross_margin_pct / 100.0)

        # Minimum required gross margin threshold (e.g. 55%)
        min_margin_threshold = 0.55
        # Max theoretical discount: 1 - COGS / ((1 - min_margin) * Price)
        theoretical_max_discount = max(0.0, 1.0 - (cogs / ((1.0 - min_margin_threshold) * deal_size_usd)))
        max_allowed_pct = min(max_discount_cap_pct, round(theoretical_max_discount * 100.0, 1))

        # Recommended discount based on competitor pressure and customer tier
        tier_multiplier = 1.0 if customer_tier == "enterprise" else (0.75 if customer_tier == "midmarket" else 0.5)
        recommended_discount_pct = min(max_allowed_pct, round(competitor_pressure_score * max_allowed_pct * tier_multiplier, 1))

        discounted_price = round(deal_size_usd * (1.0 - recommended_discount_pct / 100.0), 2)
        realized_gross_profit = round(discounted_price - cogs, 2)
        realized_margin_pct = round(100.0 * realized_gross_profit / discounted_price, 2)

        return {
            "original_deal_size_usd": deal_size_usd,
            "discounted_deal_size_usd": discounted_price,
            "recommended_discount_pct": recommended_discount_pct,
            "maximum_allowable_discount_pct": max_allowed_pct,
            "cogs_usd": round(cogs, 2),
            "realized_gross_profit_usd": realized_gross_profit,
            "realized_gross_margin_pct": realized_margin_pct,
            "margin_health": "HEALTHY" if realized_margin_pct >= 60.0 else "MARGIN_WARNING"
        }

    def forecast_pipeline_velocity_and_slippage(
        self,
        deals: List[Dict[str, Any]],
        target_quarter_days: int = 90
    ) -> Dict[str, Any]:
        """
        Forecasts B2B pipeline velocity: Velocity = (Deals * WinRate * AvgDealSize) / SalesCycleDays
        and identifies deals at risk of quarter slippage.
        """
        if not deals:
            return {"pipeline_velocity_usd_per_day": 0.0, "deals_analyzed": 0, "slippage_risk_deals": []}

        total_value = sum(d.get("amount_usd", 0.0) for d in deals)
        n = len(deals)
        avg_deal_size = total_value / max(1, n)

        win_rates = [d.get("win_probability", 0.3) for d in deals]
        avg_win_rate = sum(win_rates) / max(1, n)

        cycle_durations = [d.get("sales_cycle_days", 45) for d in deals]
        avg_cycle_days = sum(cycle_durations) / max(1, n)

        # Pipeline Velocity formula
        velocity_usd_per_day = round((n * avg_win_rate * avg_deal_size) / max(1.0, avg_cycle_days), 2)
        expected_quarter_revenue = round(velocity_usd_per_day * target_quarter_days, 2)

        # Slippage risk detection: deals where current stage dwell time exceeds 1.5x expected stage duration
        slippage_alerts = []
        for d in deals:
            dwell_days = d.get("days_in_current_stage", 0)
            expected_days = d.get("expected_stage_days", 14)
            if dwell_days > 1.5 * expected_days:
                slippage_alerts.append({
                    "deal_id": d.get("id", "deal"),
                    "deal_name": d.get("name", "Enterprise Contract"),
                    "amount_usd": d.get("amount_usd", 0.0),
                    "days_in_stage": dwell_days,
                    "expected_stage_days": expected_days,
                    "slippage_severity": "HIGH" if dwell_days > 2.5 * expected_days else "MEDIUM"
                })

        return {
            "total_pipeline_value_usd": round(total_value, 2),
            "deals_analyzed": n,
            "average_deal_size_usd": round(avg_deal_size, 2),
            "average_win_probability": round(avg_win_rate, 3),
            "average_sales_cycle_days": round(avg_cycle_days, 1),
            "pipeline_velocity_usd_per_day": velocity_usd_per_day,
            "expected_quarter_revenue_usd": expected_quarter_revenue,
            "slippage_alerts_count": len(slippage_alerts),
            "slippage_risk_deals": slippage_alerts
        }
