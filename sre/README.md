# SRE Observability Project

## Overview
This project scaffolds a modern Site Reliability Engineering (SRE) observability stack. It integrates application metrics, health checks, and chaos testing capabilities, visualized through Prometheus and Grafana.

## Architecture Decisions
The architecture follows the standard "three pillars of observability":
1. **Metrics:** Collected via Prometheus, scraping endpoints exposed by the application.
2. **Visualization:** Grafana provides dashboards to visualize metrics and system health.
3. **Tracing/Logging:** (Future Scope) While this scaffold focuses on metrics, logging and tracing integration points are planned for future expansion.

## Services
* **App:** The core Python application service, responsible for generating metrics and health checks.
* **Prometheus:** Time-series database and monitoring system, responsible for scraping metrics from the `app` service.
* **Grafana:** Visualization layer, used to query and display metrics collected by Prometheus.

## How To Run
1. **Setup Environment:** Ensure Docker and Docker Compose are installed.
2. **Configure Environment:** Create a `.env` file based on `.env.example` and fill in the necessary credentials (e.g., `GRAFANA_ADMIN_USER`).
3. **Build and Run:** Execute `docker-compose up --build`.
4. **Access:**
    * Grafana: http://localhost:3000 (Login with configured credentials)
    * Prometheus: http://localhost:9090
    * Application Metrics: http://localhost:${APP_PORT}/metrics

## Chaos Testing
The `sre/app/chaos.py` module is designed to house logic for controlled failure injection (Chaos Engineering). This allows us to test system resilience by simulating failures (e.g., network latency, service downtime) in a controlled environment.

## Observability
The application exposes dedicated endpoints (`/metrics`, `/health`) that Prometheus will scrape. These endpoints provide granular data points on application performance, resource utilization, and service health, enabling proactive monitoring and alerting.
