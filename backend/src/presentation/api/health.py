from typing import Annotated

from fastapi import APIRouter, Depends
from fastapi.responses import JSONResponse

from application.health.check_readiness import CheckReadiness
from presentation.dependencies import get_readiness_check

router = APIRouter(tags=["health"])


@router.get("/health/live")
async def live() -> dict[str, str]:
    return {"status": "ok"}


@router.get("/health/ready")
async def ready(
    check: Annotated[CheckReadiness, Depends(get_readiness_check)],
) -> JSONResponse:
    result = await check()
    if result.healthy:
        return JSONResponse({"status": "ok", "database": "ok"})
    return JSONResponse({"status": "unavailable", "database": "down"}, status_code=503)
