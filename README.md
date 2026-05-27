# Call Management Dashboard

[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](https://opensource.org/licenses/MIT)
[![Python 3.14+](https://img.shields.io/badge/python-3.14+-blue.svg)](https://www.python.org/downloads/)
[![FastAPI](https://img.shields.io/badge/FastAPI-0.104+-green.svg)](https://fastapi.tiangolo.com/)

A FastAPI-based backend for managing call records, notes, and archiving status using a PostgreSQL database.

## Overview

This project provides a simple REST API for:
- creating call records
- retrieving all calls or only non-archived calls
- filtering calls by type, direction, or archived status
- archiving/unarchiving calls
- attaching notes to calls
- deleting call records

## Tech Stack

- Python 3.14+
- FastAPI
- SQLAlchemy
- PostgreSQL
- Pydantic
- Uvicorn

## Installation

1. Clone the repository:

```bash
git clone https://github.com/<your-repo>/Call_Management_Dashboard.git
cd Call_Management_Dashboard
```

2. Create and activate a virtual environment:

```bash
python -m venv .venv
.\.venv\Scripts\Activate.ps1   # PowerShell
# or .venv\Scripts\activate.bat  # cmd
```

3. Install dependencies:

```bash
python -m pip install --upgrade pip
python -m pip install -e .
```

## Configuration

Create a `.env` file in the project root with your PostgreSQL connection URL:

```env
DATABASE_URL=postgresql://user:password@host:port/database_name
```

The app expects `DATABASE_URL` to be available when starting.

## Database Setup

This project uses SQLAlchemy with the following tables:
- `calls`
- `notes`

If the tables do not exist, create them manually or add a small initialization script to run SQLAlchemy metadata creation.

## Running the Application

Start the API server with Uvicorn:

```bash
uvicorn main:app --reload --host 0.0.0.0 --port 8000
```

Open the interactive API docs at:

- http://127.0.0.1:8000/docs
- http://127.0.0.1:8000/redoc

## API Endpoints

### Create a call

- POST `/calls`
- Request body: `CallSchema`

Example payload:

```json
{
  "direction": "inbound",
  "from_number": "+30 123 4567890",
  "to_number": "+30 098 7654321",
  "call_type": "answered",
  "duration": 120,
  "created_at": "2023-01-01T00:00:00",
  "is_archived": false,
  "notes": [
    {"content": "Follow up on invoice"}
  ]
}
```

### Get all calls

- GET `/calls`

### Get non-archived calls

- GET `/calls/non-archived`

### Get a single call by ID

- GET `/calls/{call_id}`

### Filter calls

- GET `/calls/{call_filter}/filter`

Supported filter values:
- `missed`
- `answered`
- `voicemail`
- `inbound`
- `outbound`
- `archived`
- `not_archived`

### Archive all calls

- PATCH `/calls/archive-all`

### Archive a call

- PATCH `/calls/{call_id}/archive`

### Unarchive a call

- PATCH `/calls/{call_id}/unarchive`

### Add a note to a call

- PATCH `/calls/{call_id}/notes`

Example payload:

```json
{
  "content": "Customer requested callback"
}
```

### Delete a call

- DELETE `/calls/{call_id}`

### Health check

- GET `/health`

## Validation Rules

- `direction`: `inbound` or `outbound`
- `call_type`: `missed`, `answered`, or `voicemail`
- `from_number` / `to_number`: must match `+CC AAA NNNNNNN` format, e.g. `+30 123 4567890`

## Testing

Run tests with:

```bash
python -m pytest
```

## Notes

- This repo uses SQLAlchemy ORM models in `src/models`
- Request and response validation is handled by Pydantic schemas in `src/core/schemas.py`
- Database connection is configured in `src/core/database.py`
- API routes are defined in `main.py`

## Future Improvements

Given more time, the following enhancements would be valuable additions:

- **Authentication & Authorization**: Implement JWT-based authentication with role-based access control (admin, user, read-only)
- **Call Recording Integration**: Add support for storing and retrieving call recording links/metadata
- **Advanced Filtering**: Implement date range filtering, full-text search on note content, and pagination
- **Call Analytics**: Add endpoints to generate call statistics (average duration, call counts by type/direction, trends)
- **Real-time Updates**: Integrate WebSockets for real-time call updates and notifications
- **Docker Support**: Add Dockerfile and docker-compose.yml for simplified deployment
- **CI/CD Pipeline**: Set up GitHub Actions for automated testing and deployment
- **API Documentation Enhancement**: Add OpenAPI schema examples and request/response validation documentation
- **Database Migrations**: Implement Alembic for managing schema changes across environments
- **Performance Optimization**: Add caching layer (Redis) for frequently accessed call data and implement query optimization
