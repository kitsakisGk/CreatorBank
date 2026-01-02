"""
Platform connection endpoints.

Handles OAuth flows for connecting creator platforms.
"""
from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select
from typing import List

from app.db.base import get_db
from app.models.user import User
from app.models.platform import ConnectedPlatform, PlatformType
from app.schemas.platform import ConnectedPlatformResponse, PlatformOAuthInitiate
from app.api.v1.endpoints.auth import get_current_user

router = APIRouter()


@router.get("/connected", response_model=List[ConnectedPlatformResponse])
async def get_connected_platforms(
    current_user: User = Depends(get_current_user),
    db: AsyncSession = Depends(get_db),
):
    """
    Get all connected platforms for the current user.
    """
    result = await db.execute(
        select(ConnectedPlatform)
        .where(ConnectedPlatform.user_id == current_user.id)
        .where(ConnectedPlatform.is_active == True)
    )
    platforms = result.scalars().all()

    return platforms


@router.post("/connect/youtube")
async def initiate_youtube_oauth(
    current_user: User = Depends(get_current_user),
):
    """
    Initiate YouTube OAuth flow.

    Returns the authorization URL for the user to visit.
    """
    # TODO: Implement YouTube OAuth flow
    # This will be implemented in the YouTube service
    return {
        "authorization_url": "https://accounts.google.com/o/oauth2/v2/auth?...",
        "state": "random_state_token",
    }


@router.get("/connect/youtube/callback")
async def youtube_oauth_callback(
    code: str,
    state: str = None,
    current_user: User = Depends(get_current_user),
    db: AsyncSession = Depends(get_db),
):
    """
    Handle YouTube OAuth callback.

    Exchanges authorization code for access token and stores credentials.
    """
    # TODO: Implement YouTube OAuth callback
    # 1. Exchange code for access token
    # 2. Fetch YouTube channel info
    # 3. Store credentials in database
    # 4. Fetch initial earnings data

    return {
        "status": "success",
        "message": "YouTube account connected successfully",
    }


@router.delete("/disconnect/{platform_id}")
async def disconnect_platform(
    platform_id: int,
    current_user: User = Depends(get_current_user),
    db: AsyncSession = Depends(get_db),
):
    """
    Disconnect a platform.
    """
    result = await db.execute(
        select(ConnectedPlatform)
        .where(ConnectedPlatform.id == platform_id)
        .where(ConnectedPlatform.user_id == current_user.id)
    )
    platform = result.scalar_one_or_none()

    if not platform:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Platform not found",
        )

    platform.is_active = False
    await db.commit()

    return {"status": "success", "message": "Platform disconnected"}


@router.post("/sync/{platform_id}")
async def sync_platform_earnings(
    platform_id: int,
    current_user: User = Depends(get_current_user),
    db: AsyncSession = Depends(get_db),
):
    """
    Manually trigger earnings sync for a platform.
    """
    result = await db.execute(
        select(ConnectedPlatform)
        .where(ConnectedPlatform.id == platform_id)
        .where(ConnectedPlatform.user_id == current_user.id)
    )
    platform = result.scalar_one_or_none()

    if not platform:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Platform not found",
        )

    # TODO: Trigger background job to sync earnings
    return {
        "status": "success",
        "message": "Sync initiated",
    }
