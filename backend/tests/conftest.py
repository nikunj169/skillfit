import os
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[2]
if str(ROOT) not in sys.path:
    sys.path.insert(0, str(ROOT))

test_db_path = ROOT / "test_skillfit.db"
if test_db_path.exists():
    test_db_path.unlink()

os.environ["SKILLFIT_DATABASE_URL"] = "sqlite:///./test_skillfit.db"

import pytest
from fastapi.testclient import TestClient

from backend.main import app


@pytest.fixture
def client():
    with TestClient(app) as test_client:
        yield test_client
