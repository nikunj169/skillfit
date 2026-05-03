"""
Verify and print the effective admin credentials for this SkillFit deployment.

Credentials are read from environment variables (SKILLFIT_ prefix) or a .env
file in the backend directory.  Run this after `alembic upgrade head` to confirm
your admin setup before starting the server.

Usage:
    cd backend
    python ../scripts/seed_admin.py
"""

import os
import sys

# Allow running from either the repo root or the backend directory.
_here = os.path.dirname(os.path.abspath(__file__))
_repo_root = os.path.dirname(_here)
sys.path.insert(0, _repo_root)

from backend.config import get_settings  # noqa: E402

settings = get_settings()

print("SkillFit admin credentials")
print("-" * 40)
print(f"  Username : {settings.admin_username}")
print(f"  Password : {settings.admin_password}")
print(f"  Token    : {settings.admin_token}")
print("-" * 40)

_using_defaults = (
    settings.admin_username == "admin@skillfit.in"
    and settings.admin_password == "skillfit2024"
    and settings.admin_token == "skillfit-admin"
)

if _using_defaults:
    print(
        "WARNING: All values are at their default (dev-only) settings.\n"
        "For production, set SKILLFIT_ADMIN_USERNAME, SKILLFIT_ADMIN_PASSWORD,\n"
        "and SKILLFIT_ADMIN_TOKEN in your environment or .env file."
    )
else:
    print("Custom credentials detected — defaults have been overridden.")

print("\nAdmin setup verified. Start the server and log in at /api/v1/admin/login.")
