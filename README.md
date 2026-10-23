# Global Economic Forecast Engine (GEFE)

## AI-Powered Macroeconomic Intelligence & Forecasting Platform

A production-grade system that continuously analyzes macroeconomic indicators, financial markets, commodities, and global news to predict economic trends, sector performance, recession risks, inflation cycles, market regime shifts, and country-level economic outlooks.

### 🎯 Core Capabilities

- **Global Macro Data Ingestion**: Real-time ingestion of GDP, CPI, interest rates, unemployment, industrial production
- **Financial Markets Analysis**: Equities, Forex, Bonds, Derivatives tracking
- **Commodity Monitoring**: Oil, Gold, Natural Gas, Agricultural products
- **News Intelligence**: NLP-powered analysis of financial news, central bank statements, geopolitical events
- **Economic Forecasting**: LSTM, TFT, XGBoost, Prophet models for multi-horizon predictions
- **Recession Risk Detection**: Early warning signals with probability scores
- **Sector Performance Prediction**: Technology, Healthcare, Energy, Finance, Manufacturing forecasts
- **Regime Detection**: Market state identification (expansion, recession, high/low inflation, volatility shocks)
- **Causal Economic Analysis**: Relationship mapping between economic variables

### 🏗️ Architecture Overview

```
Data Sources → Ingestion Pipeline (Kafka) → Feature Engineering → AI Model Layer
→ Forecasting Engine → Risk Engine → News Intelligence → Analytics → API → Dashboard
```

### 🚀 Quick Start

```bash
# Clone and setup
git clone <repository-url>
cd global_economic_forecast_engine

# Copy environment variables
cp .env.example .env

# Start all services
make up

# Run tests
make test
```

### 📊 Dashboards

- **Macro Overview**: Global economic health indicators
- **Country Analysis**: GDP, inflation, risk per country
- **Sector Forecasts**: Sector performance predictions
- **Commodity Trends**: Raw material price movements
- **Recession Risk**: Probability scores and early warnings
- **News Intelligence**: Real-time sentiment and impact analysis

### 🛠️ Tech Stack

- **Frontend**: React, Next.js, TypeScript, TailwindCSS, Recharts
- **Backend**: FastAPI, Python
- **AI Models**: PyTorch, TensorFlow, Scikit-learn, Statsmodels, XGBoost
- **Time Series**: Prophet, Temporal Fusion Transformer, LSTM, ARIMA
- **Streaming**: Kafka
- **Database**: PostgreSQL
- **Vector DB**: Qdrant
- **Infrastructure**: Docker, Kubernetes, Terraform
- **Monitoring**: Prometheus, Grafana

### 📈 Performance Targets

- Real-time data ingestion from global streams
- Sub-5 second prediction updates
- Multi-country support (200+ countries)
- 99.99% uptime
- Billion-scale data handling

### 📁 Project Structure

```
global_economic_forecast_engine/
├── frontend/          # React/Next.js dashboard
├── backend/           # FastAPI REST API
├── data_pipeline/     # Data ingestion and processing
├── ai_models/         # Machine learning models
├── analytics/         # Economic analytics engine
├── vector_db/         # Vector embeddings
├── database/          # PostgreSQL schema and migrations
├── tests/             # Comprehensive test suite
├── infra/            # Infrastructure as code
└── docs/             # Documentation
```

### 🔧 Development Commands

```bash
make up              # Start all services
make down            # Stop all services
make build           # Build Docker images
make test            # Run tests
make lint            # Code quality checks
make deploy-k8s      # Deploy to Kubernetes
```

### 📄 License


### 👥 Contact

For questions or support, contact the GEFE development team.
