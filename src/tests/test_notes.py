import json

from app.api import crud

NOTES_URL = "/notes/"


def note_detail_url(note_id):
    return f"{NOTES_URL}{note_id}"


def test_create_note(test_app, monkeypatch):
    test_request_payload = {
        "title": "something",
        "description": "something else"
    }
    test_response_payload = {
        "id": 1,
        "title": "something",
        "description": "something else"
    }

    async def mock_post(payload):
        return 1

    monkeypatch.setattr(crud, "post", mock_post)

    response = test_app.post(
        NOTES_URL,
        content=json.dumps(test_request_payload),
    )

    assert response.status_code == 201
    assert response.json() == test_response_payload


def test_create_note_invalid_json(test_app):
    response = test_app.post(
        NOTES_URL,
        content=json.dumps({"title": "somthing"})
    )

    assert response.status_code == 422


def test_read_note(test_app, monkeypatch):
    test_data = {"id": 1, "title": "something",
                 "description": "something else"}

    async def mock_get(id):
        return test_data

    monkeypatch.setattr(crud, "get", mock_get)

    response = test_app.get(note_detail_url(test_data["id"]))
    assert response.status_code == 200
    assert response.json() == test_data


def test_read_note_incorrect_id(test_app, monkeypatch):
    async def mock_get(id):
        return None

    monkeypatch.setattr(crud, "get", mock_get)

    response = test_app.get(note_detail_url(999))
    assert response.status_code == 404
    assert response.json()["detail"] == "Note not found"


def test_read_all_notes(test_app, monkeypatch):
    test_data = [{"id": 1, "title": "something",
                  "description": "something else"},
                 {"id": 2, "title": "someone",
                  "description": "someone else"}]

    async def mock_get_all():
        return test_data

    monkeypatch.setattr(crud, "get_all", mock_get_all)

    response = test_app.get(NOTES_URL)
    assert response.status_code == 200
    assert response.json() == test_data
