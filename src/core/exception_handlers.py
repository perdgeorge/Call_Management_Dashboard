import logging
import traceback
from fastapi import Request
from fastapi.responses import JSONResponse
from .exceptions import CallBaseException

logger = logging.getLogger(__name__)


def register_exception_handlers(app):
    @app.exception_handler(CallBaseException)
    async def app_exc_handler(
        request: Request,
        exc: CallBaseException,
    ):
        return JSONResponse(
            status_code=exc.status_code,
            content={
                "error": exc.error_code,
                "message": exc.message,
            },
        )

    @app.exception_handler(Exception)
    async def catch_all_handler(request: Request, exc: Exception):
        logger.error(
            "UnhandledException:\n%s",
            "".join(
                traceback.format_exception(
                    type(exc),
                    exc,
                    exc.__traceback__,
                )
            ),
        )
        return JSONResponse(
            status_code=500,
            content={
                "error": "Internal_Server_Error",
                "message": "Something went wrong. Please try again later.",
            },
        )
