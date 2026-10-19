.PHONY: help up down build test lint deploy-k8s clean docs shell migrate seed backup restore

help: ## Show this help message
	@echo 'Usage: make [target]'
	@echo ''
	@echo 'Available targets:'
	@awk 'BEGIN {FS = ":.*?## "} /^[a-zA-Z_-]+:.*?## / {printf "  %-15s %s\n", $$1, $$2}' $(MAKEFILE_LIST)

up: ## Start all services
	docker-compose up -d

down: ## Stop all services
	docker-compose down

build: ## Build all Docker images
	docker-compose build --no-cache

clean: ## Remove all containers and volumes
	docker-compose down -v --remove-orphans
	find . -type d -name "__pycache__" -exec rm -rf {} +
	find . -type d -name "*.pyc" -delete

test: ## Run all tests
	cd backend && pytest tests/ -v --cov=app --cov-report=html
	cd data_pipeline && pytest tests/ -v

lint: ## Run code quality checks
	flake8 backend/ data_pipeline/ ai_models/ analytics/ || true
	mypy backend/app/ || true
	isort --check-only backend/ data_pipeline/ ai_models/ || true

format: ## Format code
	black backend/ data_pipeline/ ai_models/ analytics/
	isort backend/ data_pipeline/ ai_models/ analytics/

shell: ## Open bash shell in backend container
	docker-compose exec backend bash

docs: ## Generate documentation
	pdoc3 app --output-dir docs/html
	@echo "Documentation generated in docs/html/"

migrate: ## Run database migrations
	docker-compose exec backend alembic upgrade head

seed: ## Seed database with sample data
	docker-compose exec backend python scripts/seed_data.py

deploy-k8s: ## Deploy to Kubernetes
	cd infra/kubernetes && kubectl apply -f .

terraform-plan: ## Plan Terraform infrastructure
	cd infra/terraform && terraform plan

terraform-apply: ## Apply Terraform infrastructure
	cd infra/terraform && terraform apply -auto-approve

monitoring: ## Start monitoring stack only
	docker-compose up prometheus grafana

logs: ## View logs from all services
	docker-compose logs -f

db-shell: ## Open PostgreSQL shell
	docker-compose exec postgres psql -U gefe_user -d gefe_db

backup-db: ## Backup database
	docker-compose exec postgres pg_dump -U gefe_user gefe_db > backup_$(shell date +%Y%m%d_%H%M%S).sql

restore-db: ## Restore database from backup
	@if [ -z "$(FILE)" ]; then echo "Error: FILE variable required"; exit 1; fi
	docker-compose exec postgres psql -U gefe_user gefe_db < $(FILE)

setup-dev: ## Setup development environment
	@echo "Setting up development environment..."
	npm install --prefix frontend
	pip install -r backend/requirements.txt
	mkdir -p backend/__pycache__
	docker-compose pull
	@echo "Development environment setup complete!"

check-deps: ## Check if dependencies are available
	@which docker || (echo "Docker not found" && exit 1)
	@which kubectl 2>/dev/null || echo "Note: kubectl not installed"
	@which terraform 2>/dev/null || echo "Note: terraform not installed"
	@which python3 || (echo "Python3 required" && exit 1)

install-hooks: ## Install pre-commit hooks
	pre-commit install
