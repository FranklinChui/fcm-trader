# 1. System Architecture

This document outlines the architecture for the FCM Trader application, a decision-support and portfolio tracking tool designed to generate trade signals and help users manage their manually executed trades. The architecture is modular, scalable, maintainable, and follows a 3-tier system design and a feature-centric development approach.

---

## 2. Architectural Approach

### 2.1. 3-Tier System

The application is structured into three logical tiers to separate concerns and enhance scalability:

1.  **Presentation Tier (Frontend)**: A user-facing interface for visualizing data, signals, and performance. This tier will be built using a Python-native framework like Streamlit or Gradio for rapid development and ease of integration.
2.  **Application Tier (Backend)**: The core logic of the system, responsible for data processing, signal generation, and portfolio management. It exposes a RESTful API for the frontend to consume.
3.  **Data Tier**: Manages the storage and retrieval of all data, including market data, signals, and trade records.

### 2.2. Feature-Centric Design

The codebase will be organized by feature to promote modularity and parallel development. Each feature (e.g., `data_ingestion`, `signal_generation`, `portfolio_management`) will be a self-contained module with its own logic, models, and services.

---

## 3. Technology Stack

The technology stack is chosen to be robust, scalable, and primarily Python-oriented.

| Tier          | Technology                               | Purpose                                                      |
|---------------|------------------------------------------|--------------------------------------------------------------|
| **Presentation** | Streamlit / Gradio                       | Interactive dashboards, data visualization, and user controls. |
| **Application**  | FastAPI                                  | High-performance, asynchronous API for core services.        |
|               | Pydantic                                 | Data validation and settings management.                     |
|               | SQLAlchemy / SQLModel                    | Object-Relational Mapping (ORM) for database interaction.    |
|               | Celery / Dramatiq                        | Background task processing for long-running jobs (e.g., backtesting). |
| **Data**         | PostgreSQL                               | Primary relational database for persistent data storage.     |
|               | Redis                                    | In-memory data store for caching and message brokering.      |
| **Deployment**   | Docker                                   | Containerization for consistent development and deployment.  |
|               | Docker Compose                           | Orchestrating multi-container local development environments. |

---

## 4. Component Design & Data Flow

The system is composed of several interconnected services, each corresponding to a core feature.

```mermaid
graph TD
    subgraph Presentation Tier
        A[Frontend UI - Streamlit/Gradio]
    end

    subgraph Application Tier
        B[API Gateway - FastAPI]
        C[Data Ingestion Service]
        D[Signal Generation Service]
        F[Portfolio Service]
    end

    subgraph Data Tier
        G[PostgreSQL Database]
        H[Redis Cache]
        I[External Data APIs]
    end

    A -->|Views Signals & Portfolio| B
    A -->|Manages Positions (CRUD)| B

    B -->|/signals| D
    B -->|/portfolio| F

    C -->|Fetches Data| I
    C -->|Stores Data| G

    D -->|Reads Data| G
    D -->|Writes Signal Recommendations| G
    D -->|Caches Signals| H

    F -->|Reads & Writes User Positions| G
```

### 4.1. Data Ingestion Service

-   **Responsibility**: Fetches historical and real-time market data from external APIs.
-   **Logic**: Handles data cleaning, validation, and storage into the PostgreSQL database. Scheduled to run weekly or as needed.

### 4.2. Signal Generation Service

-   **Responsibility**: Implements the core trading logic defined in `specs_v2.md`.
-   **Logic**: Reads market data from PostgreSQL, calculates indicators, and generates buy/sell signals. These signals are stored as **recommendations** for the user to review. They do not automatically alter portfolio positions.


### 4.3. Portfolio Service

-   **Responsibility**: Manages the user's portfolio of trades based on manual input.
-   **Logic**: Provides API endpoints for the user to perform Create, Read, Update, and Delete (CRUD) operations on their trade positions. The user manually records their executed trades (instrument, entry price, size, date) via the UI. This service calculates portfolio metrics based on this user-maintained data.

---

## 5. Project Structure (Feature-Centric)

The project will be organized as follows to reflect the feature-centric approach:

```
fcm-trader/
├── app/
│   ├── main.py                 # FastAPI application entry point
│   ├── core/                   # Core configuration, settings
│   ├── features/
│   │   ├── data_ingestion/
│   │   │   ├── __init__.py
│   │   │   ├── service.py
│   │   │   └── models.py
│   │   ├── signal_generation/
│   │   │   └── ...
│   │   └── ...
│   ├── models/                 # Shared SQLAlchemy/SQLModel base models
│   └── services/               # Shared utility services
├── scripts/                    # Standalone scripts
├── tests/                      # Tests, mirroring the app structure
│   └── features/
│       └── ...
├── .env                        # Environment variables
├── docker-compose.yml          # Docker orchestration
└── pyproject.toml              # Project dependencies
