# 1. Project Task List: FCM Trader (v2)

This document outlines the development tasks for the FCM Trader application, updated based on the detailed design in `docs/detailed_design.md`.

---

## 2. Epic 1: Project Foundation & Environment Setup

**Objective:** Establish the project's technical foundation, including the development environment, database connectivity, and core application structure.

-   [x] **1.1. Initialize Project Directory Structure**: Create `app`, `tests`, `logs`, `scripts`, `data`, and `models` directories.
-   [x] **1.2. Define Project Dependencies**: Configure `pyproject.toml` with all necessary libraries.
-   [x] **1.3. Configure Docker Environment**: Create `Dockerfile` and `docker-compose.yml`.
-   [x] **1.4. Create Database Session Manager**: Implement `app/core/database.py`.
-   [x] **1.5. Implement Core Data Models**:
    -   [x] 1.5.1. Define SQLAlchemy models for `Instrument`, `MarketData`, and `Signal` in their respective feature modules (e.g., `app/features/data_ingestion/models.py`) based on the DDL in `detailed_design.md`.
    -   [x] 1.5.2. Define corresponding Pydantic schemas for API validation and serialization.
-   [x] **1.6. Setup Core Configuration & Logging**:
    -   [x] 1.6.1. Implement a Pydantic-based settings management module in `app/core/config.py`.
    -   [x] 1.6.2. Configure a structured logging service (e.g., Structlog) for the application.
-   [x] **1.7. Initialize FastAPI Application**:
    -   [x] 1.7.1. Set up the main `app/main.py` with a health check endpoint and API routers.
    -   [x] 1.7.2. Implement a startup event to create initial database tables from the SQLAlchemy models.

---

## 3. Epic 2: Feature - Data Ingestion

**Objective:** Build the service responsible for reliably fetching, cleaning, and storing market data.

-   [ ] **2.1. Implement Data Ingestion Repository**:
    -   [ ] 2.1.1. Create `app/features/data_ingestion/repository.py` to handle all database operations for instruments and market data, following the Repository Pattern.
-   [ ] **2.2. Implement Data Ingestion Service**:
    -   [ ] 2.2.1. Create `app/features/data_ingestion/service.py` containing the business logic for the ingestion process.
    -   [ ] 2.2.2. Implement the data source connector to fetch OHLCV data from an external API.
    -   [ ] 2.2.3. Develop data validation and cleaning functions.
-   [ ] **2.3. Develop Tests (TDD)**:
    -   [ ] 2.3.1. Write unit tests for the repository methods and service logic.
    -   [ ] 2.3.2. Write integration tests for the end-to-end data ingestion flow, mocking the external API.
-   [ ] **2.4. Create API Endpoint**:
    -   [ ] 2.4.1. Implement the `/instruments/` endpoints in `app/features/data_ingestion/router.py`.
    -   [ ] 2.4.2. Expose an endpoint to manually trigger the data ingestion process.

---

## 4. Epic 3: Feature - Signal Generation

**Objective:** Implement the core trading strategy logic to generate buy/sell signals.

-   [ ] **4.1. Implement Signal Generation Repository**:
    -   [ ] 4.1.1. Create `app/features/signal_generation/repository.py` to handle database operations for signals.
-   [ ] **4.2. Implement Indicator Calculation Library**:
    -   [ ] 4.2.1. Create a library in `app/features/signal_generation/indicators.py` to calculate MACD, RSI, Stochastic, etc.
    -   [ ] 4.2.2. Write unit tests for each indicator calculation (TDD).
-   [ ] **4.3. Implement Signal Generation Service**:
    -   [ ] 4.3.1. Create `app/features/signal_generation/service.py` to orchestrate the signal generation process.
    -   [ ] 4.3.2. Implement the composite signal logic and relative strength gauge.
    -   [ ] 4.3.3. Implement the layered exit strategy logic.
-   [ ] **4.4. Develop Tests (TDD)**:
    -   [ ] 4.4.1. Write unit tests for the composite signal and exit logic.
    -   [ ] 4.4.2. Write integration tests to verify signal generation from raw data.
-   [ ] **4.5. Create API Endpoint**:
    -   [ ] 4.5.1. Implement the `/signals/{instrument_id}` endpoint in `app/features/signal_generation/router.py`.

---

## 5. Epic 4: Feature - Portfolio & Execution

**Objective:** Develop services to manage trades, positions, and portfolio state.

-   [ ] **5.1. Implement Portfolio Repository**:
    -   [ ] 5.1.1. Create `app/features/portfolio/repository.py` for trade and position data.
-   [ ] **5.2. Implement Portfolio Service**:
    -   [ ] 5.2.1. Create `app/features/portfolio/service.py`.
    -   [ ] 5.2.2. Implement position sizing logic.
    -   [ ] 5.2.3. Implement trade management and portfolio tracking logic.
-   [ ] **5.3. Develop Tests (TDD)**:
    -   [ ] 5.3.1. Write unit tests for position sizing and portfolio metric calculations.
-   [ ] **5.4. Create API Endpoints**:
    -   [ ] 5.4.1. Implement `/portfolio` and `/trades` endpoints in `app/features/portfolio/router.py`.

---

## 6. Epic 5: Presentation Tier (Frontend)

**Objective:** Build an interactive dashboard for visualizing data and managing trades.

-   [ ] **6.1. Setup Frontend Application**:
    -   [ ] 6.1.1. Initialize a Streamlit application in `frontend/app.py`.
-   [ ] **6.2. Develop API Client Service**:
    -   [ ] 6.2.1. Create a service to handle communication with the FastAPI backend.
-   [ ] **6.3. Develop Dashboards (US-1, US-2, US-5)**:
    -   [ ] 6.3.1. Create the Signal Dashboard view.
    -   [ ] 6.3.2. Create the Portfolio Dashboard view.
    -   [ ] 6.3.3. Create the Interactive Charting view.

---

## 7. Epic 6: Deployment & Operations

**Objective:** Automate testing, deployment, and monitoring.

-   [ ] **7.1. Configure CI/CD Pipeline**:
    -   [ ] 7.1.1. Set up a GitHub Actions workflow to run Pytest on every push.
-   [ ] **7.2. Implement System Monitoring (US-3)**:
    -   [ ] 7.2.1. Integrate an alerting mechanism for critical application errors.
-   [ ] **7.3. Prepare for Deployment**:
    -   [ ] 7.3.1. Create deployment scripts (e.g., using AWS CDK or Terraform).
    -   [ ] 7.3.2. Finalize production configuration for Docker and AWS Fargate.
