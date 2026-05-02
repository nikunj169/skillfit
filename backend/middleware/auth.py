from fastapi import Header, HTTPException, status

from backend.config import get_settings


def verify_admin_token(x_admin_token: str | None = Header(default=None)) -> str:
    settings = get_settings()
    if x_admin_token != settings.admin_token:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalid or missing admin token.",
        )
    return x_admin_token
