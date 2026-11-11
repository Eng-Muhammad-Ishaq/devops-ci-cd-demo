import os
import time

from flask import Flask, Response, g, jsonify, request
from prometheus_client import CONTENT_TYPE_LATEST, Counter, Histogram, generate_latest

app = Flask(__name__)
SERVICE_NAME = os.getenv("SERVICE_NAME", "devops-platform-api")
VERSION = os.getenv("APP_VERSION", "development")
REQUEST_COUNT = Counter(
    "http_requests_total",
    "Total HTTP requests",
    ["method", "endpoint", "status"],
)
REQUEST_LATENCY = Histogram(
    "http_request_duration_seconds",
    "HTTP request latency in seconds",
    ["method", "endpoint"],
)


@app.after_request
def record_request_metrics(response):
    endpoint = getattr(response, "endpoint", request_path())
    REQUEST_COUNT.labels(request.method, endpoint, response.status_code).inc()
    return response


def request_method():
    return request.method


def request_path():
    return request.path


@app.get("/")
def home():
    return jsonify({"service": SERVICE_NAME, "version": VERSION, "status": "healthy"})


@app.get("/health")
def health():
    return jsonify({"status": "ok", "service": SERVICE_NAME})


@app.get("/ready")
def ready():
    return jsonify({"status": "ready", "service": SERVICE_NAME})


@app.get("/metrics")
def metrics():
    return Response(generate_latest(), mimetype=CONTENT_TYPE_LATEST)


@app.before_request
def start_timer():
    g.request_start_time = time.perf_counter()


@app.after_request
def record_latency(response):
    elapsed = time.perf_counter() - getattr(g, "request_start_time", time.perf_counter())
    REQUEST_LATENCY.labels(request_method(), request_path()).observe(elapsed)
    return response


if __name__ == "__main__":
    app.run(host="0.0.0.0", port=int(os.getenv("PORT", "5000")))
