# GEFE - Quick Start Guide

## Prerequisites

- Docker & Docker Compose (v20+)
- Python 3.9+ (for local development)
- Node.js 18+ (for frontend development)
- Git
- Optional: Kubernetes cluster for production deployment

## Installation & Setup

### Option 1: Docker Compose (Recommended for Development)

```bash
# 1. Clone or navigate to project directory
cd global_economic_forecast_engine

# 2. Configure environment variables
cp .env.example .env
# Edit .env with your actual credentials

# 3. Build and start all services
make up

# 4. Wait for services to be healthy
sleep 30

# 5. Verify health
curl http://localhost:8000/health
curl http://localhost:3000
```

**Access Points:**
- Backend API: http://localhost:8000/docs
- Frontend Dashboard: http://localhost:3000
- Grafana Monitoring: http://localhost:3001 (admin/admin123)
- Prometheus: http://localhost:9090
- Qdrant Vector DB: http://localhost:6333

### Option 2: Local Development Setup

```bash
# 1. Install backend dependencies
cd backend
pip install -r requirements.txt
uvicorn main:app --reload --host 0.0.0.0 --port 8000

# 2. Install frontend dependencies (new terminal)
cd frontend
npm install
npm run dev

# 3. Set up PostgreSQL locally
# Use docker-compose up postgres only
docker-compose up postgres qdrant kafka
```

### Option 3: Production Kubernetes Deployment

```bash
# 1. Ensure you have kubectl configured
kubectl config get-contexts

# 2. Deploy infrastructure
cd infra/kubernetes
kubectl apply -f namespace.yaml
kubectl apply -f persistent-volumes.yaml

# 3. Deploy applications
make deploy-k8s

# 4. Run database migrations
kubectl exec -it gefe-backend-0 -- alembic upgrade head

# 5. Access services via Ingress (configured separately)
```

## Testing

```bash
# Run all tests
make test

# Run specific test suites
pytest backend/tests/unit/
pytest backend/tests/model_tests/
pytest data_pipeline/tests/

# Test with coverage
pytest --cov=backend/app --cov-report=html
open htmlcov/index.html
```

## Database Setup

```bash
# Initialize database schema
docker-compose exec postgres psql -U gefe_user -d gefe_db -f /docker-entrypoint-initdb.d/schemas.sql

# Or use migrations
make migrate

# Seed sample data
make seed
```

## Data Pipeline Configuration

The data pipeline automatically:
- Ingests macroeconomic data from FRED API
- Fetches market data from Alpha Vantage/Yahoo Finance
- Processes financial news streams
- Updates vector embeddings in Qdrant

Configuration in `.env`:
```
FRED_API_KEY=your_fred_key
ALPHA_VANTAGE_KEY=your_alpha_key
NEWS_API_KEY=your_news_key
```

## API Usage Examples

### Get GDP Forecasts

```bash
curl -X POST "http://localhost:8000/api/v1/forecast/gdp"   -H "Content-Type: application/json"   -d '{
    "country_id": "US",
    "forecast_horizon": 12,
    "confidence_level": 0.95,
    "include_scenarios": true
  }'
```

### Analyze Recession Risk

```bash
curl -X POST "http://localhost:8000/api/v1/risk/recession"   -H "Content-Type: application/json"   -d '{
    "country_ids": ["US", "EU", "CN"],
    "include_factors": true
  }'
```

### News Analysis

```bash
curl -X POST "http://localhost:8000/api/v1/news/analyze"   -H "Content-Type: application/json"   -d '{
    "keywords": ["inflation", "interest rates", "recession"],
    "date_range_days": 7
  }'
```

## Monitoring & Observability

### Prometheus Metrics
Available at `/metrics` endpoint on port 8000

### Grafana Dashboards
Pre-configured dashboards:
- System Resource Usage
- API Performance
- Model Prediction Quality
- Data Pipeline Health

### Log Aggregation
View logs: `make logs`

Individual container logs:
```bash
docker-compose logs backend
docker-compose logs data-pipeline
docker-compose logs ai-models
```

## Scaling Considerations

### Horizontal Scaling
Use Kubernetes HPA configuration provided in `infra/kubernetes/hpa.yaml`

### Database Scaling
- Add read replicas via PostgreSQL streaming replication
- Implement connection pooling with PgBouncer

### Kafka Scaling
- Increase partition count for high-throughput topics
- Add consumer group instances

## Troubleshooting

### Services won't start
```bash
# Check logs
docker-compose logs <service-name>

# Restart specific service
docker-compose restart <service-name>

# Rebuild images
docker-compose build --no-cache
```

### Database connection errors
```bash
# Wait for database to be ready
docker-compose exec postgres pg_isready -U gefe_user

# Check connection string in .env
cat .env | grep DATABASE_URL
```

### Kafka messages not processing
```bash
# Check Kafka status
docker-compose exec kafka kafka-topics.sh --bootstrap-server localhost:9092 --list

# Inspect consumer lag
docker-compose exec kafka kafka-consumer-groups.sh --bootstrap-server localhost:9092 --describe
```

## Security Checklist

- [ ] Change default passwords in `.env`
- [ ] Enable HTTPS/TLS for production
- [ ] Configure firewall rules
- [ ] Set up API rate limiting
- [ ] Enable audit logging
- [ ] Rotate API keys regularly
- [ ] Backup database daily
- [ ] Monitor for security alerts

## Next Steps

1. **Customize Data Sources**: Integrate additional economic data providers
2. **Train Models**: Use historical data to improve prediction accuracy
3. **Configure Alerts**: Set up notifications for risk thresholds
4. **User Management**: Implement authentication and authorization
5. **Performance Tuning**: Optimize based on load testing results

## Support & Documentation

- Full documentation: `docs/` directory
- API reference: http://localhost:8000/docs
- Architecture diagram: `docs/architecture.md`
- Model documentation: `docs/ai_models.md`

## License

Proprietary - ABB Internal Use Only

For questions, contact the GEFE development team.
