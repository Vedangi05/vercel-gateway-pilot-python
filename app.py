"""A very small in-memory notes API built with Flask.

Endpoints:
    GET  /notes  -> return all notes
    POST /notes  -> create a note

Notes are stored in memory only; they are lost when the process exits.
"""

from flask import Flask, jsonify, request

MAX_TITLE_LENGTH = 200
MAX_CONTENT_LENGTH = 10_000


def create_app():
    """Application factory.

    A fresh in-memory store is created per app instance, which keeps tests
    isolated from one another.
    """
    app = Flask(__name__)

    # In-memory store. `notes` holds the created notes; `next_id` is a simple
    # auto-incrementing identifier.
    notes = []
    state = {"next_id": 1}

    @app.get("/notes")
    def list_notes():
        return jsonify({"notes": notes}), 200

    @app.post("/notes")
    def create_note():
        data = request.get_json(silent=True)

        error = _validate_note_payload(data)
        if error is not None:
            return jsonify({"error": error}), 400

        note = {
            "id": state["next_id"],
            "title": data["title"].strip(),
            "content": data.get("content", "").strip(),
        }
        state["next_id"] += 1
        notes.append(note)
        return jsonify(note), 201

    return app


def _validate_note_payload(data):
    """Return an error message string if invalid, else None."""
    if not isinstance(data, dict):
        return "Request body must be a JSON object."

    if "title" not in data:
        return "Field 'title' is required."

    title = data["title"]
    if not isinstance(title, str) or not title.strip():
        return "Field 'title' must be a non-empty string."
    if len(title) > MAX_TITLE_LENGTH:
        return f"Field 'title' must be at most {MAX_TITLE_LENGTH} characters."

    content = data.get("content", "")
    if not isinstance(content, str):
        return "Field 'content' must be a string."
    if len(content) > MAX_CONTENT_LENGTH:
        return f"Field 'content' must be at most {MAX_CONTENT_LENGTH} characters."

    return None


if __name__ == "__main__":
    create_app().run(debug=True)
