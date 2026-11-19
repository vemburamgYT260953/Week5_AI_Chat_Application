
import os
import secrets

from fastapi import Security, HTTPException, status
from fastapi.security import APIKeyHeader
from dotenv import load_dotenv

load_dotenv()

API_KEY = os.getenv("API_KEY", "")

api_key_header = APIKeyHeader(
    name="X-API-Key",
    auto_error=False
)


async def verify_api_key(
    api_key: str = Security(api_key_header)
):
    if not API_KEY:
        raise HTTPException(
            status_code=500,
            detail="API key is not configured"
        )

    if not api_key or not secrets.compare_digest(
        api_key, API_KEY
    ):
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalid or missing API key"
        )

    return api_key
