import time

from fastapi import FastAPI, Request, Response
from prometheus_client import generate_latest

from .database import engine
from . import models
from .routers import post, user
from .metrics import (
    REQUEST_COUNT,
    REQUEST_LATENCY,
    DB_CONCURRENT_REQUESTS,
    DB_ACTIVE_CONNECTIONS,
    DB_QUERY_LATENCY
)


models.Base.metadata.create_all(bind=engine)

app = FastAPI()
app.include_router(post.router)
app.include_router(user.router)


@app.middleware("http")
async def metrics_middleware(request: Request, call_next):
    start_time = time.time()
    response = await call_next(request)
    duration = time.time() - start_time

    REQUEST_COUNT.labels(
        method=request.method,
        endpoint=request.url.path,
        status=response.status_code
    ).inc()

    REQUEST_LATENCY.labels(
        endpoint=request.url.path
    ).observe(duration)

    return response


@app.get("/metrics")
def metrics():
    return Response(generate_latest(), media_type="text/plain")