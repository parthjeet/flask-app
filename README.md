# Flask Task API

A minimal Flask REST API. Built with Flask-RESTX for automatic Swagger documentation.

## Requirements

- Python 3.12
- UV (package manager)

## Quick Start

```bash
# Install dependencies
uv sync

# Run the development server
uv run python src/app.py
```

The server starts at `http://localhost:5000`.

## API Endpoints

| Method | Endpoint | Description |
|--------|----------|-------------|
| GET | `/` | Welcome message |
| GET | `/health` | Health check with task count |
| GET | `/docs` | Swagger UI documentation |
| GET | `/api/tasks` | List all tasks |
| GET | `/api/tasks?done=true` | Filter tasks by status |
| GET | `/api/tasks/<id>` | Get a task by ID |
| POST | `/api/tasks` | Create a new task |
| PUT | `/api/tasks/<id>` | Update a task |
| DELETE | `/api/tasks/<id>` | Delete a task |

## Example Usage

```bash
# Get welcome message
curl http://localhost:5000/

# Health check
curl http://localhost:5000/health

# Create a task
curl -X POST http://localhost:5000/api/tasks \
  -H "Content-Type: application/json" \
  -d '{"title": "Learn Kubernetes"}'

# List all tasks
curl http://localhost:5000/api/tasks

# Update a task
curl -X PUT http://localhost:5000/api/tasks/1 \
  -H "Content-Type: application/json" \
  -d '{"done": true}'

# Delete a task
curl -X DELETE http://localhost:5000/api/tasks/1
```

## Project Structure

```
flask-app/
├── src/
│   └── app.py          # Flask application
├── pyproject.toml      # Project configuration
├── uv.lock             # Dependency lockfile
├── .python-version     # Python version (3.12)
└── README.md
```

## Dependencies

- Flask - Web framework
- Flask-RESTX - REST API extension with Swagger UI
