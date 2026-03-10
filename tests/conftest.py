import copy

import pytest
from fastapi.testclient import TestClient

from src.app import app, activities


@pytest.fixture
def client() -> TestClient:
    """Return a TestClient for the FastAPI app."""
    return TestClient(app)


@pytest.fixture(autouse=True)
def reset_activities() -> None:
    """Reset the in-memory activities state between tests."""
    backup = copy.deepcopy(activities)
    try:
        yield
    finally:
        activities.clear()
        activities.update(backup)
