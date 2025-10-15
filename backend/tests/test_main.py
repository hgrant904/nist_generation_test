"""Smoke tests for main application."""

import pytest
from httpx import AsyncClient


@pytest.mark.asyncio
async def test_app_creates_successfully(client: AsyncClient) -> None:
    """Test that the application can be created and responds."""
    response = await client.get("/api/v1/health")
    assert response.status_code == 200
