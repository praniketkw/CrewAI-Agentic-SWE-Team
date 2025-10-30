import pytest
from fastapi.testclient import TestClient
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from sqlalchemy.pool import StaticPool

from backend.main import app
from backend.database import Base, get_db
from backend.models import User, Task, TaskStatus, TaskPriority

# Test database setup
TEST_DATABASE_URL = 'sqlite:///./test_task_management.db'
test_engine = create_engine(
    TEST_DATABASE_URL, 
    connect_args={'check_same_thread': False},
    poolclass=StaticPool
)
TestingSessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=test_engine)

def override_get_db():
    """Override database dependency for testing"""
    try:
        db = TestingSessionLocal()
        yield db
    finally:
        db.close()

app.dependency_overrides[get_db] = override_get_db

# Test client setup
client = TestClient(app)

@pytest.fixture(scope='module')
def test_db():
    """Create and drop test database"""
    Base.metadata.create_all(bind=test_engine)
    yield TestingSessionLocal()
    Base.metadata.drop_all(bind=test_engine)

def test_user_registration():
    """Test user registration endpoint"""
    # Test successful registration
    response = client.post('/auth/register', params={
        'username': 'testuser',
        'email': 'testuser@example.com',
        'password': 'strongpassword123'
    })
    assert response.status_code == 200
    assert response.json() == {'message': 'User registered successfully'}

    # Test duplicate registration
    response = client.post('/auth/register', params={
        'username': 'testuser',
        'email': 'testuser@example.com',
        'password': 'strongpassword123'
    })
    assert response.status_code == 400
    assert 'already registered' in response.json()['detail']

def test_user_login():
    """Test user login endpoint"""
    # First, ensure user exists
    client.post('/auth/register', params={
        'username': 'loginuser',
        'email': 'loginuser@example.com',
        'password': 'loginpassword123'
    })

    # Test successful login
    response = client.post('/auth/login', data={
        'username': 'loginuser',
        'password': 'loginpassword123'
    })
    assert response.status_code == 200
    assert 'access_token' in response.json()
    assert response.json()['token_type'] == 'bearer'

    # Test failed login
    response = client.post('/auth/login', data={
        'username': 'loginuser',
        'password': 'wrongpassword'
    })
    assert response.status_code == 401

def test_task_operations():
    """Test task CRUD operations"""
    # Register and login a user to get token
    client.post('/auth/register', params={
        'username': 'taskuser',
        'email': 'taskuser@example.com',
        'password': 'taskpassword123'
    })
    login_response = client.post('/auth/login', data={
        'username': 'taskuser',
        'password': 'taskpassword123'
    })
    access_token = login_response.json()['access_token']

    # Create task
    create_response = client.post('/tasks', 
        params={
            'title': 'Test Task',
            'description': 'Test Description',
            'status': TaskStatus.TODO,
            'priority': TaskPriority.MEDIUM
        },
        headers={'Authorization': f'Bearer {access_token}'}
    )
    assert create_response.status_code == 200
    task = create_response.json()
    assert task['title'] == 'Test Task'

    # List tasks
    list_response = client.get('/tasks', 
        headers={'Authorization': f'Bearer {access_token}'}
    )
    assert list_response.status_code == 200
    assert len(list_response.json()) > 0

    # Get specific task
    get_response = client.get(f'/tasks/{task["id"]}', 
        headers={'Authorization': f'Bearer {access_token}'}
    )
    assert get_response.status_code == 200
    assert get_response.json()['id'] == task['id']

    # Update task
    update_response = client.put(f'/tasks/{task["id"]}', 
        params={'title': 'Updated Task Title'},
        headers={'Authorization': f'Bearer {access_token}'}
    )
    assert update_response.status_code == 200
    assert update_response.json()['title'] == 'Updated Task Title'

    # Delete task
    delete_response = client.delete(f'/tasks/{task["id"]}', 
        headers={'Authorization': f'Bearer {access_token}'}
    )
    assert delete_response.status_code == 200
    assert delete_response.json()['message'] == 'Task deleted successfully'