from fastapi import FastAPI, Depends, HTTPException, status
from fastapi.security import OAuth2PasswordRequestForm
from fastapi.middleware.cors import CORSMiddleware
from sqlalchemy.orm import Session
from datetime import timedelta

from database import engine, get_db
from models import Base, User, Task, TaskStatus, TaskPriority
from security import create_access_token, hash_password, verify_password, get_current_user, ACCESS_TOKEN_EXPIRE_MINUTES

# Create database tables
Base.metadata.create_all(bind=engine)

# FastAPI application
app = FastAPI(title='Task Management API', version='1.0.0')

# CORS Configuration
app.add_middleware(
    CORSMiddleware,
    allow_origins=['*'],  # Allows all origins
    allow_credentials=True,
    allow_methods=['*'],  # Allows all methods
    allow_headers=['*'],  # Allows all headers
)

# Authentication Routes
@app.post('/auth/register')
def register_user(username: str, email: str, password: str, db: Session = Depends(get_db)):
    # Check if user already exists
    existing_user = db.query(User).filter((User.username == username) | (User.email == email)).first()
    if existing_user:
        raise HTTPException(status_code=400, detail='Username or email already registered')
    
    # Create new user
    new_user = User(
        username=username,
        email=email,
        password_hash=hash_password(password)
    )
    db.add(new_user)
    db.commit()
    db.refresh(new_user)
    return {'message': 'User registered successfully'}

@app.post('/auth/login')
def login_user(form_data: OAuth2PasswordRequestForm = Depends(), db: Session = Depends(get_db)):
    # Find user by username
    user = db.query(User).filter(User.username == form_data.username).first()
    if not user or not verify_password(form_data.password, user.password_hash):
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail='Incorrect username or password',
            headers={'WWW-Authenticate': 'Bearer'}
        )
    
    # Create access token
    access_token_expires = timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)
    access_token = create_access_token(
        data={'sub': user.username}, expires_delta=access_token_expires
    )
    return {'access_token': access_token, 'token_type': 'bearer'}

# Task Routes
@app.post('/tasks')
def create_task(title: str, description: str = None, status: TaskStatus = TaskStatus.TODO, 
               priority: TaskPriority = TaskPriority.MEDIUM, due_date: str = None, 
               current_user: User = Depends(get_current_user), db: Session = Depends(get_db)):
    new_task = Task(
        user_id=current_user.id,
        title=title,
        description=description,
        status=status,
        priority=priority,
        due_date=due_date
    )
    db.add(new_task)
    db.commit()
    db.refresh(new_task)
    return new_task

@app.get('/tasks')
def list_tasks(current_user: User = Depends(get_current_user), db: Session = Depends(get_db)):
    tasks = db.query(Task).filter(Task.user_id == current_user.id).all()
    return tasks

@app.get('/tasks/{task_id}')
def get_task(task_id: int, current_user: User = Depends(get_current_user), db: Session = Depends(get_db)):
    task = db.query(Task).filter(Task.id == task_id, Task.user_id == current_user.id).first()
    if not task:
        raise HTTPException(status_code=404, detail='Task not found')
    return task

@app.put('/tasks/{task_id}')
def update_task(task_id: int, title: str = None, description: str = None, 
               status: TaskStatus = None, priority: TaskPriority = None, due_date: str = None,
               current_user: User = Depends(get_current_user), db: Session = Depends(get_db)):
    task = db.query(Task).filter(Task.id == task_id, Task.user_id == current_user.id).first()
    if not task:
        raise HTTPException(status_code=404, detail='Task not found')
    
    if title is not None:
        task.title = title
    if description is not None:
        task.description = description
    if status is not None:
        task.status = status
    if priority is not None:
        task.priority = priority
    if due_date is not None:
        task.due_date = due_date
    
    db.commit()
    db.refresh(task)
    return task

@app.delete('/tasks/{task_id}')
def delete_task(task_id: int, current_user: User = Depends(get_current_user), db: Session = Depends(get_db)):
    task = db.query(Task).filter(Task.id == task_id, Task.user_id == current_user.id).first()
    if not task:
        raise HTTPException(status_code=404, detail='Task not found')
    
    db.delete(task)
    db.commit()
    return {'message': 'Task deleted successfully'}
