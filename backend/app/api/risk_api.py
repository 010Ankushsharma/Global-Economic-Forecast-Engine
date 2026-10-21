#!/usr/bin/env python3
"""Risk Analysis API Routes for GEFE"""

from fastapi import APIRouter, Depends, HTTPException
from pydantic import BaseModel, Field
from typing import List, Optional, Dict, Any
import logging
from datetime import datetime

logger = logging.getLogger(__name__)

router = APIRouter()


class RecessionRiskRequest(BaseModel):
    """Recession risk analysis request"""
    country_ids: List[str]
    indicators: Optional[List[str]] = None
    include_factors: bool = True


class VolatilityAnalysisRequest(BaseModel):
    """Market volatility analysis request"""
    asset_class: str = "equities"
    market_region: str = "global"
    lookback_days: int = Field(90, ge=30, le=365)


@router.post("/recession")
async def analyze_recession_risk(request: RecessionRiskRequest):
    """Analyze recession probability and early warning signals"""
    try:
        from collections import defaultdict
        
        results = []
        
        # Sample analysis for requested countries
        for country_id in request.country_ids:
            recession_analysis = {
                "country_id": country_id,
                "recession_probability": {
                    "current": 0.28,  # 28%
                    "1_month": 0.32,
                    "3_months": 0.35,
                    "6_months": 0.31
                },
                "confidence_interval": {
                    "lower_90": 0.22,
                    "upper_90": 0.38
                },
                "risk_level": "MODERATE",
                "warning_signals": [],
                "contributing_factors": {},
                "yield_curve": {
                    "spreads": {
                        "2y_10y": -0.45,  # basis points
                        "inverted": True
                    },
                    "status": "INVERTED"
                },
                "credit_spreads": {
                    "investment_grade": 1.2,
                    "high_yield": 3.8,
                    "widening_trend": True
                },
                "labor_market": {
                    "unemployment_trend": "rising",
                    "jobless_claims": 225000,
                    "trend_direction": "worsening"
                },
                "leading_indicators": {
                    "pmi_manufacturing": 47.8,  # below 50 = contraction
                    "consumer_confidence": 102.5,
                    "housing_starts": "declining"
                },
                "historical_accuracy": 0.84,
                "last_updated": datetime.now().isoformat()
            }
            
            if request.include_factors:
                recession_analysis["contributing_factors"] = {
                    "yield_curve_inversion": {"weight": 0.30, "impact": "high"},
                    "credit_spread_widening": {"weight": 0.25, "impact": "moderate"},
                    "labor_softening": {"weight": 0.20, "impact": "moderate"},
                    "manufacturing_weakness": {"weight": 0.15, "impact": "low"},
                    "consumer_sentiment": {"weight": 0.10, "impact": "low"}
                }
                
                recession_analysis["warning_signals"] = [
                    {
                        "signal": "Yield Curve Inversion",
                        "severity": "HIGH",
                        "description": "10Y-2Y Treasury spread has been inverted for 18 months",
                        "historical_predictive_power": 0.89
                    },
                    {
                        "signal": "Credit Spread Widening",
                        "severity": "MODERATE",
                        "description": "High-yield spreads widened by 45bps over past quarter",
                        "historical_predictive_power": 0.72
                    },
                    {
                        "signal": "Manufacturing Contraction",
                        "severity": "MODERATE",
                        "description": "PMI has remained below 50 for 3 consecutive months",
                        "historical_predictive_power": 0.65
                    }
                ]
            
            results.append(recession_analysis)
        
        return {
            "analysis_type": "RECESSION_RISK",
            "request_timestamp": datetime.now().isoformat(),
            "countries_analyzed": len(request.country_ids),
            "results": results
        }
        
    except Exception as e:
        logger.error(f"Error analyzing recession risk: {e}")
        raise HTTPException(status_code=500, detail="Failed to analyze recession risk")


@router.post("/volatility")
async def analyze_volatility(request: VolatilityAnalysisRequest):
    """Analyze market volatility patterns and risks"""
    try:
        volatility_metrics = {
            "asset_class": request.asset_class,
            "market_region": request.market_region,
            "lookback_period_days": request.lookback_days,
            "current_vix": 14.5,
            "volatility_metrics": {
                "historical_volatility_30d": 12.8,
                "historical_volatility_60d": 15.2,
                "historical_volatility_90d": 16.5,
                "realized_volatility": 13.4,
                "implied_volatility": 14.8
            },
            "volatility_clusters": [
                {"start_date": "2024-01-01", "end_date": "2024-01-15", "avg_vol": 18.5},
                {"start_date": "2024-01-16", "end_date": "2024-01-30", "avg_vol": 12.3}
            ],
            "extreme_events": [
                {
                    "date": "2024-01-05",
                    "magnitude": 4.2,  # standard deviations
                    "impact": "SIGNIFICANT",
                    "cause": "Central bank announcement"
                }
            ],
            "forecasted_volatility": {
                "next_7d": {"mean": 13.2, "std": 2.1},
                "next_30d": {"mean": 14.5, "std": 3.8}
            },
            "regime_status": {
                "current": "LOW_VOLATILITY",
                "probability": 0.72,
                "duration_days": 45
            },
            "stress_scenarios": [
                {
                    "scenario": "Geopolitical Crisis",
                    "impact_on_vix": "+8.5",
                    "probability": 0.15
                },
                {
                    "scenario": "Economic Data Disappointment",
                    "impact_on_vix": "+5.2",
                    "probability": 0.25
                }
            ],
            "generated_at": datetime.now().isoformat()
        }
        
        return volatility_metrics
        
    except Exception as e:
        logger.error(f"Error analyzing volatility: {e}")
        raise HTTPException(status_code=500, detail="Failed to analyze volatility")


@router.get("/credit-spreads")
async def get_credit_spreads(
    sector: Optional[str] = None,
    rating: Optional[str] = None
):
    """Get current credit spread data"""
    try:
        spreads_data = {
            "investment_grade": {
                "AAA": 0.45,
                "AA": 0.65,
                "A": 0.95,
                "BBB": 1.45
            },
            "high_yield": {
                "BB": 3.25,
                "B": 4.85,
                "CCC": 7.50
            },
            "trend": "widening",
            "change_1m": "+12 bps",
            "timestamp": datetime.now().isoformat()
        }
        return spreads_data
    except Exception as e:
        logger.error(f"Error fetching credit spreads: {e}")
        raise HTTPException(status_code=500, detail="Failed to fetch credit spreads")


@router.get("/liquidity-risk")
async def assess_liquidity_risk(asset_class: str = "bonds"):
    """Assess liquidity risk in markets"""
    try:
        liquidity_assessment = {
            "asset_class": asset_class,
            "overall_rating": "MODERATE_RISK",
            "metrics": {
                "bid_ask_spread": 0.15,
                "market_depth": "ADEQUATE",
                "turnover_ratio": 0.85,
                "settlement_time_hours": 24
            },
            "risk_factors": [
                {"factor": "Market Size", "impact": "LOW"},
                {"factor": "Trading Volume", "impact": "MEDIUM"},
                {"factor": "Number of Participants", "impact": "LOW"}
            ],
            "recommendations": [
                "Monitor trading volumes closely",
                "Consider limit orders during volatile periods",
                "Maintain diversified positions"
            ],
            "timestamp": datetime.now().isoformat()
        }
        return liquidity_assessment
    except Exception as e:
        logger.error(f"Error assessing liquidity risk: {e}")
        raise HTTPException(status_code=500, detail="Failed to assess liquidity risk")
