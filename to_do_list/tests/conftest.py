import pytest
from fastapi.testclient import TestClient

from to_do_list.app import app


@pytest.fixture
def client():
    return TestClient(app)
