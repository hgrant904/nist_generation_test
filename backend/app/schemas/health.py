"""Schemas for health and status endpoints."""

from pydantic import BaseModel


class HealthResponse(BaseModel):
    """Health check response model."""

    status: str
    version: str


class DatabaseHealthResponse(BaseModel):
    """Database health check response model."""

    database: str
    status: str
