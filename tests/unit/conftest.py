"""Pytest configuration for unit tests."""
import pytest

@pytest.fixture(scope="session")
def dummy():
    """Return a dummy value."""
    return "dummy"
