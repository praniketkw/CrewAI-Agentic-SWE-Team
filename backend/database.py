from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker, declarative_base
from sqlalchemy.pool import StaticPool

# SQLite database configuration
DATABASE_URL = 'sqlite:///./task_management.db'

# Create engine with StaticPool for thread safety
engine = create_engine(
    DATABASE_URL, 
    connect_args={'check_same_thread': False},
    poolclass=StaticPool
)

# Create SessionLocal for database interactions
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

# Base class for declarative models
Base = declarative_base()

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()
