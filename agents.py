"""
CrewAI Agents - Software Engineering Team
Optimized for maximum reliability and speed
"""

from crewai import Agent
from crewai_tools import FileReadTool, FileWriterTool, DirectoryReadTool
from langchain_anthropic import ChatAnthropic

# Initialize the LLM with bulletproof settings - HANDLE API OVERLOADS
llm = ChatAnthropic(
    model="claude-3-5-haiku-20241022",  # Keep the cheaper model
    temperature=0.1,
    max_tokens=8192,  # Maximum allowed for Claude 3.5 Haiku
    timeout=300,  # 5 minutes per request - very generous
    max_retries=3,
    request_timeout=300
)

# Initialize tools
file_read_tool = FileReadTool()
file_writer_tool = FileWriterTool()
directory_read_tool = DirectoryReadTool()

# Special high-capacity LLM for Frontend Developer
frontend_llm = ChatAnthropic(
    model="claude-3-5-haiku-20241022",
    temperature=0.1,
    max_tokens=8192,  # Maximum allowed for Claude 3.5 Haiku
    timeout=300,
    max_retries=3,
    request_timeout=300
)

# Product Manager Agent
product_manager_agent = Agent(
    role="Product Manager",
    goal="Define clear requirements, user stories, and project scope for the task management application",
    backstory="""You are a Product Manager who creates clear requirements. 
    Create docs/requirements.md with user stories and technical specs for a task management app.""",
    tools=[file_writer_tool],
    llm=llm,
    verbose=True,
    allow_delegation=False,
    memory=False,
    max_iter=3  # Match successful agents
)

# System Architect Agent  
system_architect_agent = Agent(
    role="System Architect",
    goal="Design scalable system architecture, database schema, and API specifications",
    backstory="""You are a System Architect who designs app structure. 
    Create docs/architecture.md with database schema, API endpoints, and tech stack details.""",
    tools=[file_writer_tool],
    llm=llm,
    verbose=True,
    allow_delegation=False,
    memory=False,
    max_iter=3  # Match successful agents
)

# Frontend Developer Agent
frontend_developer_agent = Agent(
    role="Frontend Developer", 
    goal="Build a complete, functional frontend application",
    backstory="""You are a Frontend Developer who creates complete, functional web applications. 
    Create frontend/index.html with embedded CSS and JavaScript - a full single-page application with:
    - Beautiful, responsive design
    - Complete login/register functionality
    - Full task management interface (create, edit, delete, mark complete)
    - API integration with backend
    - Modern UI/UX
    
    You can read backend files to understand the API endpoints and integrate properly.""",
    tools=[file_writer_tool, file_read_tool],
    llm=frontend_llm,  # Special high-capacity LLM for exceptional frontend
    verbose=True,
    allow_delegation=False,
    memory=False,
    max_iter=5  # Allow multiple iterations for quality
)

# Backend Developer Agent
backend_developer_agent = Agent(
    role="Backend Developer",
    goal="Implement robust server-side logic, APIs, and database integration using Python FastAPI",
    backstory="""You are a Backend Developer who builds APIs with FastAPI. 
    Create backend/main.py, backend/models.py, backend/database.py, backend/security.py, and backend/requirements.txt.""",
    tools=[file_writer_tool], 
    llm=llm,
    verbose=True,
    allow_delegation=False,
    memory=False,
    max_iter=3  # Match successful agents
)

# QA Engineer Agent
qa_engineer_agent = Agent(
    role="QA Engineer",
    goal="Create comprehensive test suites and ensure code quality and reliability",
    backstory="""You are a QA Engineer who writes tests. 
    Create tests/test_backend.py with pytest tests for the backend API.""",
    tools=[file_writer_tool],
    llm=llm,
    verbose=True,
    allow_delegation=False,
    memory=False,
    max_iter=3  # Match successful agents
)

# DevOps Engineer Agent
devops_engineer_agent = Agent(
    role="DevOps Engineer", 
    goal="Set up deployment pipelines, containerization, and production infrastructure",
    backstory="""You are a DevOps Engineer who handles deployment. 
    Create docker-compose.yml in root directory and deploy/README.md with setup instructions.""",
    tools=[file_writer_tool],
    llm=llm,
    verbose=True,
    allow_delegation=False,
    memory=False,
    max_iter=3  # Match successful agents
)