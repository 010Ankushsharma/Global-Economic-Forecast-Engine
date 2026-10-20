-- GEFE Database Schema
-- PostgreSQL 15+ Required

-- Countries table
CREATE TABLE countries (
    country_id VARCHAR(10) PRIMARY KEY,
    country_name VARCHAR(100) NOT NULL,
    region VARCHAR(50),
    continent VARCHAR(50),
    iso_code VARCHAR(3),
    population_millions DECIMAL(12,2),
    gdp_trillions_usd DECIMAL(12,4),
    gdp_growth_rate DECIMAL(5,2),
    inflation_rate DECIMAL(5,2),
    unemployment_rate DECIMAL(5,2),
    interest_rate DECIMAL(5,2),
    debt_to_gdp DECIMAL(8,2),
    credit_rating VARCHAR(10),
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

-- Economic indicators table
CREATE TABLE economic_indicators (
    indicator_id SERIAL PRIMARY KEY,
    country_id VARCHAR(10) REFERENCES countries(country_id),
    indicator_type VARCHAR(50) NOT NULL,
    value DECIMAL(15,4) NOT NULL,
    date DATE NOT NULL,
    source VARCHAR(100),
    frequency VARCHAR(20), -- daily, monthly, quarterly, annual
    unit VARCHAR(50),
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    UNIQUE(country_id, indicator_type, date)
);

CREATE INDEX idx_indicators_country_date ON economic_indicators(country_id, date);
CREATE INDEX idx_indicators_type ON economic_indicators(indicator_type);

-- GDP data specifically
CREATE TABLE gdp_data (
    gdp_id SERIAL PRIMARY KEY,
    country_id VARCHAR(10) REFERENCES countries(country_id),
    gdp_value_trillions DECIMAL(12,4),
    gdp_growth_rate DECIMAL(5,2),
    quarter VARCHAR(10),
    year INTEGER,
    gdp_per_capita DECIMAL(12,2),
    purchasing_parity_adjusted DECIMAL(12,4),
    nominal_gdp_flag BOOLEAN DEFAULT TRUE,
    real_gdp_flag BOOLEAN DEFAULT TRUE,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

CREATE INDEX idx_gdp_country_year ON gdp_data(country_id, year);

-- Inflation data
CREATE TABLE inflation_data (
    inflation_id SERIAL PRIMARY KEY,
    country_id VARCHAR(10) REFERENCES countries(country_id),
    cpi_value DECIMAL(8,2),
    core_cpi DECIMAL(8,2),
    inflation_rate_annual DECIMAL(5,2),
    inflation_rate_monthly DECIMAL(5,2),
    date DATE NOT NULL,
    base_year VARCHAR(10),
    source VARCHAR(100),
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

CREATE INDEX idx_inflation_country_date ON inflation_data(country_id, date);

-- Interest rates
CREATE TABLE interest_rates (
    rate_id SERIAL PRIMARY KEY,
    country_id VARCHAR(10) REFERENCES countries(country_id),
    central_bank VARCHAR(100),
    policy_rate DECIMAL(5,3),
    rate_type VARCHAR(50),
    effective_date DATE,
    next_meeting_date DATE,
    decision VARCHAR(20), -- hike, cut, hold
    source VARCHAR(100),
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

-- Market data
CREATE TABLE market_data (
    market_id SERIAL PRIMARY KEY,
    asset_symbol VARCHAR(20),
    asset_type VARCHAR(30), -- equity, bond, commodity, currency
    price DECIMAL(15,4),
    change_percent DECIMAL(8,2),
    volume BIGINT,
    high DECIMAL(15,4),
    low DECIMAL(15,4),
    open DECIMAL(15,4),
    close DECIMAL(15,4),
    timestamp TIMESTAMP NOT NULL,
    exchange VARCHAR(50),
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

CREATE INDEX idx_market_symbol_timestamp ON market_data(asset_symbol, timestamp);
CREATE INDEX idx_market_type ON market_data(asset_type);

-- Forecasts
CREATE TABLE forecasts (
    forecast_id SERIAL PRIMARY KEY,
    forecast_type VARCHAR(50) NOT NULL, -- gdp, inflation, recession, sector
    target_entity VARCHAR(100),
    country_id VARCHAR(10) REFERENCES countries(country_id),
    forecast_value DECIMAL(10,4),
    lower_bound DECIMAL(10,4),
    upper_bound DECIMAL(10,4),
    confidence_level DECIMAL(3,2),
    forecast_horizon_months INTEGER,
    model_used VARCHAR(50),
    generated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    actual_value DECIMAL(10,4),
    forecast_accuracy DECIMAL(5,2),
    status VARCHAR(20) DEFAULT 'PENDING'
);

CREATE INDEX idx_forecasts_type_entity ON forecasts(forecast_type, target_entity);
CREATE INDEX idx_forecasts_generated ON forecasts(generated_at);

-- News events
CREATE TABLE news_events (
    news_id SERIAL PRIMARY KEY,
    title VARCHAR(500),
    source VARCHAR(100),
    url TEXT,
    published_at TIMESTAMP,
    content TEXT,
    sentiment_score DECIMAL(5,3),
    sentiment_label VARCHAR(20),
    impact_score DECIMAL(5,3),
    risk_level VARCHAR(20),
    affected_sectors TEXT[],
    key_entities TEXT[],
    keywords TEXT[],
    processed_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    vector_embedding VECTOR(768)
);

CREATE INDEX idx_news_published ON news_events(published_at);
CREATE INDEX idx_news_sentiment ON news_events(sentiment_score);
CREATE INDEX idx_news_sectors ON news_events USING GIN(affected_sectors);

-- Sector performance
CREATE TABLE sector_performance (
    sector_id SERIAL PRIMARY KEY,
    sector_name VARCHAR(100) NOT NULL,
    sector_code VARCHAR(20),
    period_start DATE,
    period_end DATE,
    return_percent DECIMAL(8,2),
    volatility DECIMAL(8,2),
    sharpe_ratio DECIMAL(5,3),
    max_drawdown DECIMAL(8,2),
    beta DECIMAL(5,3),
    pe_ratio DECIMAL(8,2),
    dividend_yield DECIMAL(5,2),
    market_cap_trillions DECIMAL(12,4),
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

-- Risk scores
CREATE TABLE risk_scores (
    risk_id SERIAL PRIMARY KEY,
    country_id VARCHAR(10) REFERENCES countries(country_id),
    risk_type VARCHAR(50), -- recession, inflation, market, liquidity
    probability DECIMAL(5,3),
    confidence_interval_lower DECIMAL(5,3),
    confidence_interval_upper DECIMAL(5,3),
    risk_level VARCHAR(20),
    contributing_factors JSONB,
    warning_signals JSONB,
    assessment_date DATE,
    horizon_months INTEGER,
    model_version VARCHAR(20),
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

CREATE INDEX idx_risk_country_date ON risk_scores(country_id, assessment_date);
CREATE INDEX idx_risk_type ON risk_scores(risk_type);

-- Recession predictions
CREATE TABLE recession_predictions (
    prediction_id SERIAL PRIMARY KEY,
    country_id VARCHAR(10) REFERENCES countries(country_id),
    timestamp TIMESTAMP NOT NULL,
    recession_probability DECIMAL(5,3),
    risk_level VARCHAR(20),
    yield_curve_spread DECIMAL(6,3),
    credit_spread_widening DECIMAL(6,3),
    unemployment_change DECIMAL(5,3),
    pmi_manufacturing DECIMAL(5,2),
    volatility_index DECIMAL(8,2),
    models_used TEXT[],
    ensemble_model VARCHAR(50),
    warning_signals JSONB,
    interpretation TEXT,
    historical_accuracy DECIMAL(5,3),
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

CREATE INDEX idx_recession_country_timestamp ON recession_predictions(country_id, timestamp);

-- System logs and audit
CREATE TABLE system_logs (
    log_id SERIAL PRIMARY KEY,
    log_level VARCHAR(10),
    component VARCHAR(50),
    message TEXT,
    metadata JSONB,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

CREATE INDEX idx_logs_created ON system_logs(created_at);
CREATE INDEX idx_logs_level ON system_logs(log_level);

-- Materialized views for common queries
CREATE MATERIALIZED VIEW mv_country_overview AS
SELECT 
    c.country_id,
    c.country_name,
    c.region,
    c.population_millions,
    g.gdp_value_trillions,
    g.gdp_growth_rate,
    i.inflation_rate_annual,
    ir.policy_rate,
    r.risk_level as recession_risk,
    r.recession_probability
FROM countries c
LEFT JOIN gdp_data g ON c.country_id = g.country_id AND g.year = EXTRACT(YEAR FROM CURRENT_DATE)
LEFT JOIN inflation_data i ON c.country_id = i.country_id AND i.date = CURRENT_DATE - INTERVAL '30 days'
LEFT JOIN interest_rates ir ON c.country_id = ir.country_id AND ir.effective_date >= CURRENT_DATE
LEFT JOIN (
    SELECT country_id, risk_level, recession_probability 
    FROM risk_scores 
    WHERE risk_type = 'recession' 
    ORDER BY assessment_date DESC LIMIT 1
) r ON c.country_id = r.country_id;

REFRESH MATERIALIZED VIEW CONCURRENTLY mv_country_overview;

-- Views for forecasting
CREATE VIEW vw_recent_forecasts AS
SELECT 
    f.forecast_id,
    f.forecast_type,
    f.target_entity,
    f.forecast_value,
    f.lower_bound,
    f.upper_bound,
    f.confidence_level,
    f.forecast_horizon_months,
    f.model_used,
    f.generated_at,
    f.actual_value,
    f.forecast_accuracy,
    CASE 
        WHEN f.actual_value IS NOT NULL THEN ABS(f.forecast_value - f.actual_value) / NULLIF(f.actual_value, 0) * 100
        ELSE NULL
    END as accuracy_percent
FROM forecasts f
ORDER BY f.generated_at DESC
LIMIT 100;

-- Create full-text search index on news
ALTER TABLE news_events ADD COLUMN ts_vector TSVECTOR;

UPDATE news_events 
SET ts_vector = to_tsvector('english', title || ' ' || COALESCE(content, ''));

CREATE INDEX idx_news_search ON news USING GIN(ts_vector);

-- Update trigger for auto-populating ts_vector
CREATE OR REPLACE FUNCTION update_news_ts_vector()
RETURNS TRIGGER AS $$
BEGIN
    NEW.ts_vector := to_tsvector('english', COALESCE(NEW.title, '') || ' ' || COALESCE(NEW.content, ''));
    RETURN NEW;
END;
$$ LANGUAGE plpgsql;

CREATE TRIGGER trg_update_news_ts_vector
BEFORE INSERT OR UPDATE ON news_events
FOR EACH ROW EXECUTE FUNCTION update_news_ts_vector();
