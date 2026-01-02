"""
YouTube API integration service.

Handles OAuth flow and earnings data fetching from YouTube.
"""
from google.oauth2.credentials import Credentials
from google_auth_oauthlib.flow import Flow
from googleapiclient.discovery import build
from datetime import datetime, timedelta
from typing import Optional, Dict, Any
from decimal import Decimal

from app.core.config import settings


class YouTubeService:
    """Service for YouTube platform integration."""

    SCOPES = [
        "https://www.googleapis.com/auth/youtube.readonly",
        "https://www.googleapis.com/auth/yt-analytics.readonly",
        "https://www.googleapis.com/auth/yt-analytics-monetary.readonly",
    ]

    @staticmethod
    def create_oauth_flow() -> Flow:
        """
        Create OAuth flow for YouTube authentication.

        Returns:
            Google OAuth Flow object
        """
        flow = Flow.from_client_config(
            {
                "web": {
                    "client_id": settings.YOUTUBE_CLIENT_ID,
                    "client_secret": settings.YOUTUBE_CLIENT_SECRET,
                    "auth_uri": "https://accounts.google.com/o/oauth2/auth",
                    "token_uri": "https://oauth2.googleapis.com/token",
                    "redirect_uris": [settings.YOUTUBE_REDIRECT_URI],
                }
            },
            scopes=YouTubeService.SCOPES,
        )
        flow.redirect_uri = settings.YOUTUBE_REDIRECT_URI
        return flow

    @staticmethod
    def get_authorization_url() -> tuple[str, str]:
        """
        Get YouTube OAuth authorization URL.

        Returns:
            Tuple of (authorization_url, state)
        """
        flow = YouTubeService.create_oauth_flow()
        authorization_url, state = flow.authorization_url(
            access_type="offline",
            include_granted_scopes="true",
            prompt="consent",
        )
        return authorization_url, state

    @staticmethod
    def exchange_code_for_token(code: str) -> Dict[str, Any]:
        """
        Exchange authorization code for access token.

        Args:
            code: Authorization code from OAuth callback

        Returns:
            Token information dictionary
        """
        flow = YouTubeService.create_oauth_flow()
        flow.fetch_token(code=code)

        credentials = flow.credentials

        return {
            "access_token": credentials.token,
            "refresh_token": credentials.refresh_token,
            "token_uri": credentials.token_uri,
            "client_id": credentials.client_id,
            "client_secret": credentials.client_secret,
            "scopes": credentials.scopes,
            "expiry": credentials.expiry,
        }

    @staticmethod
    async def get_channel_info(access_token: str) -> Dict[str, Any]:
        """
        Get YouTube channel information.

        Args:
            access_token: OAuth access token

        Returns:
            Channel information
        """
        credentials = Credentials(token=access_token)
        youtube = build("youtube", "v3", credentials=credentials)

        request = youtube.channels().list(
            part="snippet,contentDetails,statistics",
            mine=True
        )
        response = request.execute()

        if not response.get("items"):
            raise ValueError("No channel found")

        channel = response["items"][0]

        return {
            "channel_id": channel["id"],
            "title": channel["snippet"]["title"],
            "description": channel["snippet"]["description"],
            "subscriber_count": int(channel["statistics"].get("subscriberCount", 0)),
            "view_count": int(channel["statistics"].get("viewCount", 0)),
            "video_count": int(channel["statistics"].get("videoCount", 0)),
        }

    @staticmethod
    async def fetch_analytics_revenue(
        access_token: str,
        channel_id: str,
        start_date: datetime,
        end_date: datetime,
    ) -> list[Dict[str, Any]]:
        """
        Fetch revenue analytics from YouTube.

        Args:
            access_token: OAuth access token
            channel_id: YouTube channel ID
            start_date: Start date for analytics
            end_date: End date for analytics

        Returns:
            List of revenue data by day
        """
        credentials = Credentials(token=access_token)
        youtube_analytics = build("youtubeAnalytics", "v2", credentials=credentials)

        # Query for estimated revenue
        request = youtube_analytics.reports().query(
            ids=f"channel=={channel_id}",
            startDate=start_date.strftime("%Y-%m-%d"),
            endDate=end_date.strftime("%Y-%m-%d"),
            metrics="estimatedRevenue,estimatedAdRevenue,estimatedRedPartnerRevenue",
            dimensions="day",
            sort="day",
        )

        try:
            response = request.execute()
        except Exception as e:
            # Handle API errors (e.g., channel not monetized)
            print(f"YouTube Analytics API error: {e}")
            return []

        rows = response.get("rows", [])

        earnings_data = []
        for row in rows:
            day = datetime.strptime(row[0], "%Y-%m-%d")
            estimated_revenue = Decimal(str(row[1])) if len(row) > 1 else Decimal(0)
            ad_revenue = Decimal(str(row[2])) if len(row) > 2 else Decimal(0)
            red_revenue = Decimal(str(row[3])) if len(row) > 3 else Decimal(0)

            earnings_data.append({
                "date": day,
                "total_revenue": float(estimated_revenue),
                "ad_revenue": float(ad_revenue),
                "red_revenue": float(red_revenue),
            })

        return earnings_data

    @staticmethod
    async def fetch_recent_earnings(
        access_token: str,
        channel_id: str,
        days: int = 90,
    ) -> list[Dict[str, Any]]:
        """
        Fetch recent earnings (last N days).

        Args:
            access_token: OAuth access token
            channel_id: YouTube channel ID
            days: Number of days to fetch

        Returns:
            List of earnings data
        """
        end_date = datetime.utcnow()
        start_date = end_date - timedelta(days=days)

        return await YouTubeService.fetch_analytics_revenue(
            access_token,
            channel_id,
            start_date,
            end_date,
        )
