"""Shared pytest fixtures.

Every fixture builds a real application with its own SQLite file, so tests never
see each other's accounts or progress.
"""
from __future__ import annotations

import pathlib
import sys

import pytest

ROOT = pathlib.Path(__file__).resolve().parents[1]
if str(ROOT) not in sys.path:
    sys.path.insert(0, str(ROOT))

from helpers import make_user, signed_in  # noqa: E402
from web.app import create_app  # noqa: E402


@pytest.fixture()
def app(tmp_path):
    return create_app(db_path=tmp_path / "test.db", testing=True)


@pytest.fixture()
def client(app):
    """Signed in as an approved learner on the Python course."""
    return signed_in(app)


@pytest.fixture()
def admin_client(app):
    """Signed in as an approved admin."""
    return signed_in(app, name="Owner", email="owner@example.com", role="admin")


@pytest.fixture()
def pending_client(app):
    """A browser that signed up but has not been approved yet."""
    client = app.test_client()
    make_user(app, status="pending", email="waiting@example.com", name="Waiting")
    return client
