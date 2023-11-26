import json
import pytest

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


def test_update_note(test_app, monkeypatch):
    test_update_data = {"id": 1, "title": "something",
                        "description": "something else"}

    async def mock_get(id):
        return True

    monkeypatch.setattr(crud, "get", mock_get)

    async def mock_put(id, payload):
        return 1

    monkeypatch.setattr(crud, "put", mock_put)

    response = test_app.put(note_detail_url(test_update_data["id"]),
                            content=json.dumps(test_update_data))

    assert response.status_code == 200
    assert response.json() == test_update_data


@pytest.mark.parametrize(
    "id, payload, status_code",
    [
        [1, {}, 422],
        [1, {"description": "bar"}, 422],
        [999, {"title": "foo", "description": "bar"}, 404],
    ],
)
def test_update_note_invalid(test_app, monkeypatch, id, payload, status_code):
    async def mock_get(id):
        return None

    monkeypatch.setattr(crud, "get", mock_get)

    response = test_app.put(note_detail_url(id),
                            content=json.dumps(payload))

    assert response.status_code == status_code


def test_remove_note(test_app, monkeypatch):
    test_data = test_data = {"id": 1, "title": "something",
                             "description": "something else"}

    async def mock_get(id):
        return test_data

    monkeypatch.setattr(crud, "get", mock_get)

    async def mock_delete(id):
        return id

    monkeypatch.setattr(crud, "delete", mock_delete)

    response = test_app.delete(note_detail_url(test_data["id"]))

    assert response.status_code == 200
    assert response.json() == test_data


def test_remove_note_incorrect(test_app, monkeypatch):
    async def mock_get(id):
        return None

    monkeypatch.setattr(crud, "get", mock_get)

    response = test_app.delete(note_detail_url(999))

    assert response.status_code == 404
    assert response.json()["detail"] == "Note not found"
