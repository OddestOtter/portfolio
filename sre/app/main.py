from flask import Flask
from prometheus_client import make_wsgi_app
from .metrics import setup_metrics
from .health import check_health
from .chaos import run_chaos_test

app = Flask(__name__)

# Initialize metrics and health checks
setup_metrics(app)
health_app = check_health(app)

# --- Routes ---

@app.route('/metrics')
def metrics():
    """
    Exposes Prometheus metrics endpoint.
    """
    return make_wsgi_app()

@app.route('/health')
def health():
    """
    Exposes a simple health check endpoint.
    """
    return health_app

@app.route('/chaos/run')
def run_chaos():
    """
    Placeholder endpoint to trigger a chaos test run.
    """
    # In a real scenario, this would trigger the chaos module logic
    return {"status": "Chaos test triggered successfully. Check logs for results."}, 200

if __name__ == '__main__':
    # This block is primarily for local testing/debugging
    from os import environ
    app.config['APP_PORT'] = environ.get('APP_PORT', '8000')
    app.run(host='0.0.0.0', port=int(app.config['APP_PORT']))
