"""Tests for the in-memory notes API."""

import pytest

from app import create_app


@pytest.fixture
def client():
    app = create_app()
    app.testing = True
    with app.test_client() as client:
        yield client


def test_list_notes_empty_initially(client):
    resp = client.get("/notes")
    assert resp.status_code == 200
    assert resp.get_json() == {"notes": []}


def test_create_note_returns_201_and_note(client):
    resp = client.post("/notes", json={"title": "Groceries", "content": "Milk"})
    assert resp.status_code == 201

    note = resp.get_json()
    assert note["id"] == 1
    assert note["title"] == "Groceries"
    assert note["content"] == "Milk"


def test_created_note_appears_in_list(client):
    client.post("/notes", json={"title": "First"})
    client.post("/notes", json={"title": "Second", "content": "body"})

    resp = client.get("/notes")
    assert resp.status_code == 200

    notes = resp.get_json()["notes"]
    assert [n["title"] for n in notes] == ["First", "Second"]
    assert [n["id"] for n in notes] == [1, 2]


def test_missing_title_is_rejected(client):
    resp = client.post("/notes", json={"content": "no title here"})
    assert resp.status_code == 400
    assert "title" in resp.get_json()["error"]


def test_blank_title_is_rejected(client):
    resp = client.post("/notes", json={"title": "   "})
    assert resp.status_code == 400
    assert "title" in resp.get_json()["error"]


def test_non_json_body_is_rejected(client):
    resp = client.post("/notes", data="not json", content_type="text/plain")
    assert resp.status_code == 400


def test_title_is_trimmed(client):
    resp = client.post("/notes", json={"title": "  spaced  "})
    assert resp.status_code == 201
    assert resp.get_json()["title"] == "spaced"
