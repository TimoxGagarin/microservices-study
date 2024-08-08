from app.api.notifications import router as notifications
from fastapi import FastAPI

app = FastAPI(
    openapi_url="/api/v1/notifications/openapi.json",
    docs_url="/api/v1/notifications/docs",
)
app.include_router(
    notifications, prefix="/api/v1/notifications", tags=["notifications"]
)
