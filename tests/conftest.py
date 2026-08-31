import os
import sys
import hashlib
from pathlib import Path

import pytest

from fastapi.testclient import TestClient


def _set_test_env_defaults() -> None:
    # Ensure required settings exist before app import.
    os.environ.setdefault("ADMIN_TOKEN_HASH", hashlib.sha256(b"test-admin-token").hexdigest())
    os.environ.setdefault("SECRET_KEY", "test-secret-key")
    os.environ.setdefault("SESSION_EXPIRE", "30")
    os.environ.setdefault("APP_ENV", "test")
    os.environ.setdefault("ISSUER", "http://testserver")
    os.environ.setdefault("PRIVATE_KEY_PATH", "app/private.pem") # Default
    os.environ.setdefault("PUBLIC_KEY_PATH", "app/public.pem")


@pytest.fixture(scope="session")
def app():
    project_root = Path(__file__).resolve().parents[1]
    if str(project_root) not in sys.path:
        sys.path.insert(0, str(project_root))

    _set_test_env_defaults()
    from app.main import create_app

    return create_app()


@pytest.fixture()
def client(app):
    with TestClient(app) as test_client:
        yield test_client
