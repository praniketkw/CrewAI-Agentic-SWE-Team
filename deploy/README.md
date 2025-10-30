# Task Management Application Deployment Guide

## Prerequisites
- Docker
- Docker Compose
- Git

## Setup Instructions

1. Clone the Repository
```bash
git clone <repository-url>
cd task-management-app
```

2. Environment Configuration
- Ensure Docker and Docker Compose are installed
- No additional environment variables needed for basic setup

3. Build and Run the Application
```bash
docker-compose up --build
```

4. Access the Application
- Frontend: http://localhost
- Backend API: http://localhost:8000
- API Documentation: http://localhost:8000/docs

## Development Notes
- Backend runs on FastAPI (port 8000)
- Frontend served via Nginx (port 80)
- SQLite database persisted in volume

## Stopping the Application
```bash
docker-compose down
```

## Troubleshooting
- Ensure no other services are running on ports 80 and 8000
- Check Docker logs for any startup issues
- Verify Docker and Docker Compose versions are up to date
