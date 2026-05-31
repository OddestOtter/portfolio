from prometheus_client import Counter, Gauge, Histogram, CollectorRegistry

# Global registry to ensure metrics are isolated
REGISTRY = CollectorRegistry()

# Define metrics
REQUEST_COUNT = Counter(
    'http_requests_total', 
    'Total number of HTTP requests', 
    ['method', 'endpoint', 'status'], 
    registry=REGISTRY
)

REQUEST_LATENCY = Histogram(
    'http_request_duration_seconds', 
    'Histogram of request latencies', 
    ['method', 'endpoint'], 
    buckets=[0.005, 0.01, 0.05, 0.1, 0.5, 1.0], # Buckets in seconds
    registry=REGISTRY
)

# Example Gauge metric (e.g., current queue size)
QUEUE_SIZE = Gauge(
    'app_queue_size', 
    'Current size of the processing queue', 
    registry=REGISTRY
)

def setup_metrics(app):
    """
    Initializes and registers all application metrics with the Flask app.
    """
    print("Metrics setup complete. Metrics exposed at /metrics.")
    # In a real application, middleware would capture request details and increment these counters/histograms.
    pass
