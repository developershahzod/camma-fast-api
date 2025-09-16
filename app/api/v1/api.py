from fastapi import APIRouter
from .endpoints import auth, fighters, users, dashboard, contracts, events, tasks

api_router = APIRouter()
api_router.include_router(auth.router, prefix="/auth", tags=["authentication"])
api_router.include_router(users.router, prefix="/users", tags=["users"])
api_router.include_router(fighters.router, prefix="/fighters", tags=["fighters"])
api_router.include_router(dashboard.router, prefix="/dashboard", tags=["dashboard"])
api_router.include_router(contracts.router, prefix="/contracts", tags=["contracts"])
api_router.include_router(events.router, prefix="/events", tags=["events"])
api_router.include_router(tasks.router, prefix="/tasks", tags=["tasks"])