import logging
import os
import time
from collections.abc import Callable
from typing import Awaitable

import logging_loki  # pyright: ignore[reportMissingImports]
from fastapi import Request, Response


def build_loki_logger() -> logging.Logger:
    logger = logging.getLogger("api.requests")
    if logger.handlers:
        return logger

    loki_url = os.getenv("LOKI_URL", "http://89.111.155.230:3100/loki/api/v1/push")
    app_name = os.getenv("LOKI_APP_NAME", "fastapi-time-backend")

    handler = logging_loki.LokiHandler(
        url=loki_url,
        tags={"application": app_name},
        version="1",
    )
    logger.setLevel(logging.INFO)
    logger.addHandler(handler)
    return logger


request_logger = build_loki_logger()


async def log_endpoint_calls(
    request: Request, call_next: Callable[[Request], Awaitable[Response]]
) -> Response:
    started_at = time.perf_counter()
    response = await call_next(request)
    elapsed_ms = int((time.perf_counter() - started_at) * 1000)
    request_logger.info(
        "endpoint_called",
        extra={
            "tags": {
                "method": request.method,
                "path": request.url.path,
                "status_code": str(response.status_code),
            },
            "request_id": request.headers.get("X-Request-ID", ""),
            "duration_ms": elapsed_ms,
            "query_params": str(request.query_params),
            "client_ip": request.client.host if request.client else "",
        },
    )
    return response
