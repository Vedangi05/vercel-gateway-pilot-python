# vercel-gateway-pilot-python

A very small in-memory notes API built with Flask.

Notes are stored **in memory only** — they are lost when the server stops.
There is no database, authentication, or deployment configuration.

## Endpoints

| Method | Path     | Description        |
| ------ | -------- | ------------------ |
| GET    | `/notes` | Return all notes   |
| POST   | `/notes` | Create a note      |

### Create a note

`POST /notes` accepts a JSON body:

```json
{ "title": "Groceries", "content": "Milk, eggs, bread" }
```

- `title` — required, non-empty string (max 200 chars).
- `content` — optional string (max 10,000 chars), defaults to `""`.

On success it returns `201 Created` with the created note:

```json
{ "id": 1, "title": "Groceries", "content": "Milk, eggs, bread" }
```

Invalid input returns `400 Bad Request` with an `{ "error": "..." }` body.

## Setup

```bash
python3 -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt
```

## Run the app

```bash
flask --app app run
# or:
python app.py
```

The API is served at http://127.0.0.1:5000.

Example requests:

```bash
curl http://127.0.0.1:5000/notes

curl -X POST http://127.0.0.1:5000/notes \
  -H 'Content-Type: application/json' \
  -d '{"title": "Groceries", "content": "Milk"}'
```

## Run the tests

```bash
pytest
```
