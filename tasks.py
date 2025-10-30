"""
CrewAI Tasks - Software Engineering Workflow
Defines the tasks that each agent will perform in the development process
"""

from crewai import Task
from agents import (
    product_manager_agent,
    system_architect_agent,
    backend_developer_agent,
    frontend_developer_agent,
    qa_engineer_agent,
    devops_engineer_agent
)

# Task 1: Requirements Analysis
requirements_analysis_task = Task(
    description="""Create docs/requirements.md with:
    - User can register/login with email/password
    - User can create tasks with title, description, priority (LOW/MEDIUM/HIGH), due date
    - User can view, edit, delete, mark tasks complete
    - Tasks have status: TODO, IN_PROGRESS, DONE
    - Responsive web interface
    - Tech stack: FastAPI backend, SQLite database, vanilla JavaScript frontend
    
    NOTE: This will guide the System Architect, Backend Developer, and Frontend Developer.""",
    agent=product_manager_agent,
    expected_output="Comprehensive requirements documentation with user stories and technical specifications"
)

# Task 2: System Architecture Design
architecture_design_task = Task(
    description="""Based on the requirements, create docs/architecture.md with:
    - Database: User table (id, username, email, password_hash), Task table (id, user_id, title, description, status, priority, due_date)
    - API endpoints: POST /auth/register, POST /auth/login, GET/POST/PUT/DELETE /tasks
    - Frontend: Single-page app with login form, task list, create/edit modals
    - Authentication: JWT tokens, password hashing
    - Tech: FastAPI + SQLAlchemy + SQLite + HTML/CSS/JS
    
    NOTE: Backend and Frontend developers will implement this exact architecture.""",
    agent=system_architect_agent,
    expected_output="Architecture document created at docs/architecture.md with complete system design",
    context=[requirements_analysis_task]
)

# Task 3: Backend Development
backend_development_task = Task(
    description="""Following the architecture design, create backend files:
    - main.py: FastAPI app with CORS, endpoints for /auth/register, /auth/login, /tasks CRUD
    - models.py: SQLAlchemy User model (id, username, email, password_hash) and Task model (id, user_id, title, description, status enum, priority enum, due_date)
    - database.py: SQLite database setup, session management
    - security.py: JWT token creation/validation, password hashing with bcrypt
    - requirements.txt: fastapi, uvicorn, sqlalchemy, python-jose, passlib, python-multipart
    
    NOTE: Frontend will connect to these exact API endpoints. QA will test these endpoints.""",
    agent=backend_developer_agent,
    expected_output="Complete FastAPI backend with authentication, database models, and API endpoints",
    context=[requirements_analysis_task, architecture_design_task]
)

# Task 4: Frontend Development
frontend_development_task = Task(
    description="""Create a COMPLETE frontend/index.html file that starts with <!DOCTYPE html> and ends with </html>.
    
    The file MUST be a complete, valid HTML document with:
    - Full HTML structure: <!DOCTYPE html>, <html>, <head>, <body>
    - Embedded CSS in <style> tags with responsive design and modern UI
    - Complete JavaScript in <script> tags with all functions for:
      * User registration and login
      * JWT token management
      * Task CRUD operations (create, read, update, delete)
      * Task status management (TODO, IN_PROGRESS, DONE)
      * Priority handling (LOW, MEDIUM, HIGH)
    - Login/register forms and complete task management interface
    - API integration with backend endpoints (/auth/register, /auth/login, /tasks)
    - Error handling and user feedback
    
    CRITICAL: The file must be complete and valid HTML that can run in a browser immediately.""",
    agent=frontend_developer_agent,
    expected_output="Complete, functional single-page application at frontend/index.html with embedded CSS and JavaScript",
    context=[requirements_analysis_task, architecture_design_task, backend_development_task]
)

# Task 5: Testing
testing_task = Task(
    description="""Create tests/test_backend.py with basic pytest tests for user registration, login, and task operations. Keep it simple and focused.""",
    agent=qa_engineer_agent,
    expected_output="Complete test file created at tests/test_backend.py with comprehensive API tests",
    context=[requirements_analysis_task, architecture_design_task, backend_development_task]
)

# Task 6: Deployment Configuration
deployment_task = Task(
    description="""Package the complete application for deployment:
    - docker-compose.yml: Backend service (FastAPI on port 8000), frontend service (nginx on port 80), volume mounts for development
    - deploy/README.md: Setup instructions - how to install dependencies, run backend, open frontend, test the app
    
    NOTE: Must containerize both backend and frontend components built by other agents.""",
    agent=devops_engineer_agent,
    expected_output="Docker-compose.yml file created in root directory and deploy/README.md with deployment instructions",
    context=[requirements_analysis_task, architecture_design_task, backend_development_task, frontend_development_task]
)