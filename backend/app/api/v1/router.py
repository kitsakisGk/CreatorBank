"""
API v1 router - combines all endpoint routes.
"""
from fastapi import APIRouter
from app.api.v1.endpoints import auth, users, platforms, earnings, dashboard

api_router = APIRouter()

# Include all endpoint routers
api_router.include_router(auth.router, prefix="/auth", tags=["Authentication"])
api_router.include_router(users.router, prefix="/users", tags=["Users"])
api_router.include_router(platforms.router, prefix="/platforms", tags=["Platforms"])
api_router.include_router(earnings.router, prefix="/earnings", tags=["Earnings"])
api_router.include_router(dashboard.router, prefix="/dashboard", tags=["Dashboard"])
