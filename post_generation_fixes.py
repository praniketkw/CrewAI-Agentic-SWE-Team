#!/usr/bin/env python3
"""
Post-Generation Fixes for CrewAI Generated Code
Automatically applies common fixes needed after CrewAI generation
"""

import os
import re
import subprocess
import sys
from pathlib import Path

def print_step(step_name):
    """Print a formatted step name"""
    print(f"\n🔧 {step_name}")
    print("-" * 50)

def fix_backend_requirements():
    """Fix backend requirements.txt"""
    print_step("Fixing Backend Requirements")
    
    requirements_path = Path("backend/requirements.txt")
    if not requirements_path.exists():
        print("❌ backend/requirements.txt not found")
        return False
    
    # Read current requirements
    with open(requirements_path, 'r') as f:
        content = f.read()
    
    # Remove sqlite3 if present (it's built into Python)
    content = re.sub(r'\nsqlite3\s*', '\n', content)
    content = re.sub(r'^sqlite3\s*\n', '', content, flags=re.MULTILINE)
    
    # Ensure we have the essential packages with compatible versions
    essential_packages = [
        "fastapi>=0.100.0",
        "uvicorn>=0.23.0", 
        "sqlalchemy>=2.0.0",
        "pydantic>=2.0.0",
        "python-jose>=3.3.0",
        "passlib>=1.7.4",
        "bcrypt>=4.0.0",
        "python-multipart>=0.0.6",
        "email-validator>=2.0.0"
    ]
    
    # Write updated requirements
    with open(requirements_path, 'w') as f:
        f.write("# Backend dependencies for Task Management App\n")
        for package in essential_packages:
            f.write(f"{package}\n")
    
    print("✅ Fixed backend/requirements.txt")
    return True

def fix_backend_imports():
    """Fix import statements in backend files"""
    print_step("Fixing Backend Import Statements")
    
    backend_files = [
        "backend/main.py",
        "backend/security.py", 
        "backend/models.py",
        "backend/database.py"
    ]
    
    fixes_applied = 0
    
    for file_path in backend_files:
        if not Path(file_path).exists():
            print(f"⚠️  {file_path} not found, skipping")
            continue
            
        with open(file_path, 'r') as f:
            content = f.read()
        
        original_content = content
        
        # Fix relative imports to absolute imports
        content = re.sub(r'from \.(\w+) import', r'from \1 import', content)
        content = re.sub(r'from \.(\w+)\.(\w+) import', r'from \1.\2 import', content)
        
        # Fix specific common import issues
        content = content.replace('from .database import', 'from database import')
        content = content.replace('from .models import', 'from models import')
        content = content.replace('from .security import', 'from security import')
        
        if content != original_content:
            with open(file_path, 'w') as f:
                f.write(content)
            print(f"✅ Fixed imports in {file_path}")
            fixes_applied += 1
        else:
            print(f"ℹ️  No import fixes needed in {file_path}")
    
    return fixes_applied > 0

def fix_pydantic_syntax():
    """Fix Pydantic v2 compatibility issues"""
    print_step("Fixing Pydantic v2 Compatibility")
    
    models_path = Path("backend/models.py")
    if not models_path.exists():
        print("❌ backend/models.py not found")
        return False
    
    with open(models_path, 'r') as f:
        content = f.read()
    
    original_content = content
    
    # Fix regex -> pattern
    content = re.sub(r'regex=', 'pattern=', content)
    
    # Fix Config class for Pydantic v2
    content = re.sub(r'class Config:\s*\n\s*orm_mode = True', 
                    'class Config:\n        from_attributes = True', content)
    
    # Fix Field imports if needed
    if 'from pydantic import' in content and 'Field' not in content:
        content = re.sub(r'from pydantic import ([^\\n]+)', 
                        r'from pydantic import \1, Field', content)
    
    if content != original_content:
        with open(models_path, 'w') as f:
            f.write(content)
        print("✅ Fixed Pydantic v2 syntax in models.py")
        return True
    else:
        print("ℹ️  No Pydantic fixes needed")
        return False

def add_cors_middleware():
    """Add CORS middleware to FastAPI app"""
    print_step("Adding CORS Middleware")
    
    main_path = Path("backend/main.py")
    if not main_path.exists():
        print("❌ backend/main.py not found")
        return False
    
    with open(main_path, 'r') as f:
        content = f.read()
    
    # Check if CORS is already added
    if 'CORSMiddleware' in content:
        print("ℹ️  CORS middleware already present")
        return True
    
    # Add CORS import
    if 'from fastapi import' in content:
        content = re.sub(r'from fastapi import ([^\\n]+)', 
                        r'from fastapi import \1\nfrom fastapi.middleware.cors import CORSMiddleware', 
                        content)
    
    # Add CORS middleware after app creation
    if 'app = FastAPI(' in content:
        cors_config = '''
# Add CORS middleware
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # In production, specify your frontend domain
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)
'''
        content = re.sub(r'(app = FastAPI\([^)]*\))', 
                        r'\1\n' + cors_config, content)
        
        with open(main_path, 'w') as f:
            f.write(content)
        print("✅ Added CORS middleware to main.py")
        return True
    
    print("⚠️  Could not add CORS middleware automatically")
    return False

def fix_database_models():
    """Ensure database models are properly structured"""
    print_step("Fixing Database Models")
    
    models_path = Path("backend/models.py")
    database_path = Path("backend/database.py")
    
    if not models_path.exists():
        print("❌ backend/models.py not found")
        return False
    
    with open(models_path, 'r') as f:
        models_content = f.read()
    
    # Check if SQLAlchemy models are in models.py
    if 'class User(Base):' not in models_content:
        print("⚠️  SQLAlchemy models not found in models.py")
        # Could add model creation logic here
        return False
    
    # Ensure database.py has proper Base import
    if database_path.exists():
        with open(database_path, 'r') as f:
            db_content = f.read()
        
        if 'Base = declarative_base()' not in db_content:
            print("⚠️  Base not properly defined in database.py")
            return False
    
    print("✅ Database models structure looks good")
    return True

def complete_incomplete_files():
    """Check for and complete obviously incomplete files"""
    print_step("Checking for Incomplete Files")
    
    files_to_check = [
        "frontend/index.html",
        "backend/main.py",
        "backend/models.py"
    ]
    
    incomplete_files = []
    
    for file_path in files_to_check:
        if Path(file_path).exists():
            with open(file_path, 'r') as f:
                content = f.read().strip()
            
            # Check for obviously incomplete files
            if len(content) < 100 or content.count('\n') < 5:
                incomplete_files.append(file_path)
                print(f"⚠️  {file_path} appears incomplete ({len(content)} chars)")
    
    if incomplete_files:
        print(f"❌ Found {len(incomplete_files)} incomplete files")
        print("💡 You may need to manually complete these files")
        return False
    else:
        print("✅ All files appear complete")
        return True

def install_backend_dependencies():
    """Install backend dependencies"""
    print_step("Installing Backend Dependencies")
    
    if not Path("backend/requirements.txt").exists():
        print("❌ backend/requirements.txt not found")
        return False
    
    try:
        # Check if we're in a virtual environment
        if not os.environ.get('VIRTUAL_ENV'):
            print("⚠️  Not in virtual environment. Activating crewai_env...")
            # We can't activate venv from Python, so just warn the user
            print("💡 Please run: source crewai_env/bin/activate")
            return False
        
        print("📦 Installing backend dependencies...")
        result = subprocess.run([
            sys.executable, "-m", "pip", "install", "-r", "backend/requirements.txt"
        ], capture_output=True, text=True, cwd=".")
        
        if result.returncode == 0:
            print("✅ Backend dependencies installed successfully")
            return True
        else:
            print(f"❌ Failed to install dependencies: {result.stderr}")
            return False
            
    except Exception as e:
        print(f"❌ Error installing dependencies: {e}")
        return False

def create_run_script():
    """Create a simple run script for the backend"""
    print_step("Creating Backend Run Script")
    
    run_script = '''#!/usr/bin/env python3
"""
Simple script to run the Task Management backend
"""

import uvicorn
import os

if __name__ == "__main__":
    # Ensure we're in the backend directory
    os.chdir(os.path.dirname(os.path.abspath(__file__)))
    
    print("🚀 Starting Task Management API...")
    print("📍 API will be available at: http://localhost:8000")
    print("📚 API docs will be available at: http://localhost:8000/docs")
    print("🛑 Press Ctrl+C to stop")
    
    uvicorn.run(
        "main:app",
        host="0.0.0.0",
        port=8000,
        reload=True
    )
'''
    
    with open("backend/run.py", 'w') as f:
        f.write(run_script)
    
    # Make it executable
    os.chmod("backend/run.py", 0o755)
    
    print("✅ Created backend/run.py")
    return True

def main():
    """Main function to run all fixes"""
    print("🤖 CrewAI Post-Generation Fixes")
    print("=" * 60)
    print("Automatically applying common fixes to generated code...")
    
    fixes_applied = []
    
    # Run all fixes
    if fix_backend_requirements():
        fixes_applied.append("Backend requirements")
    
    if fix_backend_imports():
        fixes_applied.append("Import statements")
    
    if fix_pydantic_syntax():
        fixes_applied.append("Pydantic v2 syntax")
    
    if add_cors_middleware():
        fixes_applied.append("CORS middleware")
    
    if fix_database_models():
        fixes_applied.append("Database models")
    
    if complete_incomplete_files():
        fixes_applied.append("File completeness check")
    
    if create_run_script():
        fixes_applied.append("Backend run script")
    
    # Try to install dependencies (optional)
    install_backend_dependencies()
    
    # Summary
    print("\n" + "=" * 60)
    print("🎉 Post-Generation Fixes Complete!")
    print("=" * 60)
    
    if fixes_applied:
        print("✅ Applied fixes:")
        for fix in fixes_applied:
            print(f"   • {fix}")
    else:
        print("ℹ️  No fixes were needed or applied")
    
    print("\n🚀 Next Steps:")
    print("1. Activate virtual environment: source crewai_env/bin/activate")
    print("2. Run backend: cd backend && python run.py")
    print("3. Open frontend/index.html in your browser")
    print("4. Check API docs at: http://localhost:8000/docs")
    
    print("\n💡 If you encounter issues:")
    print("   • Check the generated files manually")
    print("   • Review DEVELOPMENT_NOTES.md for known issues")
    print("   • The working backup is in *_working_backup/ directories")

if __name__ == "__main__":
    main()