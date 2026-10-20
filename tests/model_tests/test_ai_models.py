#!/usr/bin/env python3
"""Tests for AI Models"""

import pytest
import numpy as np
import pandas as pd
import sys
import os

sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..', 'ai_models'))


class TestGDPForecaster:
    """Tests for GDP forecasting model"""
    
    def test_model_initialization(self):
        from macro_forecasting.gdp_forecasting import GDPForecaster
        forecaster = GDPForecaster()
        assert forecaster is not None
        assert isinstance(forecaster.models, dict)
    
    def test_prepare_features(self):
        from macro_forecasting.gdp_forecasting import GDPForecaster
        forecaster = GDPForecaster()
        
        # Create sample data
        df = pd.DataFrame({
            'gdp': [2.5, 2.6, 2.4, 2.7, 2.5],
            'inflation': [3.1, 3.0, 3.2, 2.9, 3.0],
            'interest_rate': [5.25, 5.25, 5.5, 5.5, 5.5]
        })
        
        features = forecaster.prepare_features(df)
        assert len(features) == len(df) - 4  # Due to lagging
        assert 'gdp_lag_1' in features.columns
    
    def test_forecast_generation(self):
        from macro_forecasting.gdp_forecasting import GDPForecaster
        forecaster = GDPForecaster()
        
        # Generate forecasts (without training - will use defaults)
        result = forecaster.forecast(horizon=12)
        
        assert len(result['forecasts']) == 12
        assert isinstance(result['confidence_intervals'], list)
        assert len(result['confidence_intervals']) == 12
        assert result['horizon_months'] == 12
        
        # Check reasonable values
        assert all(isinstance(f, float) for f in result['forecasts'])
        assert all(0 <= fc <= 10 for fc in result['forecasts'])  # GDP growth shouldn't exceed 10%


class TestRecessionPredictor:
    """Tests for recession prediction model"""
    
    def test_model_initialization(self):
        from recession_prediction.recession_detector import RecessionPredictor
        predictor = RecessionPredictor()
        assert predictor is not None
        assert predictor.probability_threshold == 0.5
    
    def test_warning_signals_detection(self):
        from recession_prediction.recession_detector import RecessionPredictor
        predictor = RecessionPredictor()
        
        current_data = {
            'yield_curve': 0.45,  # Positive = inverted
            'unemployment_change': 0.3,
            'credit_spread_widening': 1.2,
            'pmi_contraction': 1,
            'volatility': 0.04
        }
        
        signals = predictor._identify_warning_signals(current_data)
        
        assert len(signals) >= 1
        signal_types = [s['signal'] for s in signals]
        assert any('yield_curve' in st for st in signal_types)


@pytest.mark.parametrize("horizon", [1, 6, 12, 24, 60])
def test_gdp_horizons(horizon):
    """Test different forecast horizons"""
    from macro_forecasting.gdp_forecasting import GDPForecaster
    forecaster = GDPForecaster()
    result = forecaster.forecast(horizon=horizon)
    assert len(result['forecasts']) == horizon


def test_invalid_forecast_horizon():
    """Test invalid horizon raises error"""
    from macro_forecasting.gdp_forecasting import GDPForecaster
    forecaster = GDPForecaster()
    
    try:
        forecaster.forecast(horizon=0)
        assert False, "Should have raised ValueError"
    except ValueError:
        pass
    
    try:
        forecaster.forecast(horizon=100)
        assert False, "Should have raised ValueError"
    except ValueError:
        pass
