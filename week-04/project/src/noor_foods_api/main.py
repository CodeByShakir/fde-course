import logging
import time
from collections.abc import Awaitable, Callable

from fastapi import FastAPI, Request, Response, status
from fastapi.responses import JSONResponse
from sqlalchemy.exc import IntegrityError

from .config import configure_logging, get_settings
from .routers import categories, orders, products

configure_logging(debug=get_settings().debug)
logger = logging.getLogger(__name__)

app = FastAPI(
    title="Noor Foods API",
    description="Products, orders and stock for Noor Foods.",
)

app.include_router(categories.router)
app.include_router(products.router)
app.include_router(orders.router)


@app.middleware("http")
async def log_requests(
    request: Request, call_next: Callable[[Request], Awaitable[Response]]
) -> Response:
    start_time = time.perf_counter()
    response = await call_next(request)
    process_time = (time.perf_counter() - start_time) * 1000

    logger.info(
        "%s %s completed in %.2fms with status code %s",
        request.method,
        request.url.path,
        process_time,
        response.status_code,
    )
    return response


@app.exception_handler(IntegrityError)
def handle_integrity_error(
    request: Request, exc: IntegrityError
) -> JSONResponse:
    logger.warning("Integrity error on %s: %s", request.url.path, exc.orig)
    return JSONResponse(
        status_code=status.HTTP_409_CONFLICT,
        content={
            "detail": "This conflicts with existing data, such as a "
            "duplicate value or a row that is still in use."
        },
    )


@app.get("/")
def read_root() -> dict[str, str]:
    return {"app": "Noor Foods API", "docs": "/docs"}
