from prometheus_client import Counter, Histogram, Gauge

# API Metrics

REQUEST_COUNT = Counter(
    "api_requests_total",
    "Total API requests",
    ["method", "endpoint", "status"]
)

REQUEST_LATENCY = Histogram(
    "api_request_latency_seconds",
    "API request latency",
    ["endpoint"]
)

# DB Metrics
DB_QUERY_LATENCY = Histogram(
    "db_query_latency_seconds",
    "Database query latency",
    ["query_type"]
)

DB_ACTIVE_CONNECTIONS = Gauge(
    "db_active_connections",
    "Active database connections"
)

DB_CONCURRENT_REQUESTS = Gauge(
    "db_concurrent_requests",
    "Concurrent database requests"
)
