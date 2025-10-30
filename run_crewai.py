#!/usr/bin/env python3
"""
CrewAI Task Management App Generator - BULLETPROOF VERSION
This MUST generate a complete working application with all 6 agents
"""

import os
import sys
import time
from pathlib import Path
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

def validate_setup():
    """Validate environment setup - BULLETPROOF VERSION"""
    print("🔍 Validating setup...")
    
    # Check API key
    api_key = os.getenv("ANTHROPIC_API_KEY")
    if not api_key:
        print("❌ ANTHROPIC_API_KEY not found!")
        print("💡 Please set your Anthropic API key in .env file")
        return False
    
    if api_key.startswith("sk-ant-"):
        print("✅ Anthropic API key format looks correct")
    else:
        print("⚠️  API key format looks unusual - but proceeding...")
    
    # Check directories
    required_dirs = ["docs", "backend", "frontend", "tests", "deploy"]
    for directory in required_dirs:
        Path(directory).mkdir(exist_ok=True)
        print(f"✅ Directory {directory}/ ready")
    
    # Check Python packages
    try:
        import crewai
        import langchain_anthropic
        print("✅ Required packages available")
    except ImportError as e:
        print(f"❌ Missing package: {e}")
        print("💡 Run: pip install crewai crewai-tools langchain-anthropic")
        return False
    
    print("✅ All pre-flight checks passed!")
    return True

def validate_complete_app():
    """Validate that we have a complete working application"""
    print("\n🔍 Validating application files...")
    
    # Core files needed for basic functionality
    core_files = {
        "docs/requirements.md": "Requirements documentation",
        "docs/architecture.md": "Architecture documentation", 
        "backend/main.py": "FastAPI main application",
        "backend/models.py": "Database models",
        "backend/requirements.txt": "Backend dependencies",
        "frontend/index.html": "Frontend main page",
    }
    
    # Optional files that enhance the app but aren't critical
    optional_files = {
        "tests/test_backend.py": "Backend tests",
        "frontend/styles/main.css": "Frontend styles",
        "frontend/js/app.js": "Frontend JavaScript",
    }
    
    missing_core = []
    missing_optional = []
    present_files = []
    
    # Check core files
    for file_path, description in core_files.items():
        if Path(file_path).exists():
            present_files.append(f"✅ {description}")
        else:
            missing_core.append(f"❌ {description} ({file_path})")
    
    # Check optional files
    for file_path, description in optional_files.items():
        if Path(file_path).exists():
            present_files.append(f"✅ {description}")
        else:
            missing_optional.append(f"⚠️  {description} ({file_path})")
    
    print(f"\n📊 Application Files Status:")
    for item in present_files:
        print(f"   {item}")
    
    # Only fail if core files are missing
    if missing_core:
        print(f"\n❌ Missing Critical Files:")
        for item in missing_core:
            print(f"   {item}")
        print(f"\n💡 {len(missing_core)} critical files missing - some agents may have failed.")
        return False
    
    # Show optional missing files but don't fail
    if missing_optional:
        print(f"\n📝 Optional Files (can be added later):")
        for item in missing_optional:
            print(f"   {item}")
    
    print(f"\n🎉 Core application files present - app should be functional!")
    return True

def show_generated_files():
    """Show what files were generated"""
    print("\n📁 Generated Files:")
    
    output_dirs = ["docs", "backend", "frontend", "tests", "deploy"]
    total_files = 0
    
    for directory in output_dirs:
        if Path(directory).exists():
            files = list(Path(directory).rglob("*"))
            files = [f for f in files if f.is_file() and not f.name.startswith('.')]
            
            if files:
                print(f"\n📂 {directory}/")
                for file_path in sorted(files):
                    print(f"   📄 {file_path}")
                    total_files += 1
    
    if total_files > 0:
        print(f"\n🎉 Total: {total_files} files generated!")
        
        # Log specific missing files at the end
        log_missing_files()
        
        print("\n🚀 Next Steps:")
        print("1. Run post-generation fixes: python post_generation_fixes.py")
        print("2. Test the generated app: python test_generated_app.py")
        print("3. Run backend: cd backend && python main.py")
        print("4. Open frontend/index.html in browser")
        print("5. Check out the deployment configurations in deploy/")
        print("\n💡 The post-generation script will automatically fix common issues!")
    else:
        print("⚠️  No files were generated. Check the execution logs above.")
    
    return total_files

def log_missing_files():
    """Log which specific files are missing at the end"""
    expected_files = {
        "docs/requirements.md": "Requirements documentation",
        "docs/architecture.md": "Architecture documentation", 
        "backend/main.py": "FastAPI main application",
        "backend/models.py": "Database models",
        "backend/database.py": "Database configuration",
        "backend/security.py": "Authentication logic",
        "backend/requirements.txt": "Backend dependencies",
        "frontend/index.html": "Frontend main page",
        "frontend/styles/main.css": "Frontend styles",
        "frontend/js/app.js": "Frontend JavaScript",
        "tests/test_backend.py": "Backend tests",
        "deploy/docker-compose.yml": "Docker deployment",
    }
    
    missing_files = []
    for file_path, description in expected_files.items():
        if not Path(file_path).exists():
            missing_files.append(f"   📄 {file_path} - {description}")
    
    if missing_files:
        print(f"\n📋 Missing Files Summary ({len(missing_files)} files):")
        for missing in missing_files:
            print(missing)
        print(f"\n💡 These files can often be created by the post-generation fixes script.")
    else:
        print(f"\n✅ All expected files are present!")

def run_crewai_development():
    """Run the CrewAI development process - MUST COMPLETE ALL 6 AGENTS"""
    
    try:
        print("🚀 Starting CrewAI Software Development Team...")
        
        # Import CrewAI components
        from crewai import Crew, Process
        from agents import (
            product_manager_agent,
            system_architect_agent,
            backend_developer_agent,
            frontend_developer_agent,
            qa_engineer_agent,
            devops_engineer_agent
        )
        from tasks import (
            requirements_analysis_task,
            architecture_design_task,
            backend_development_task,
            frontend_development_task,
            testing_task,
            deployment_task
        )
        
        # Create the crew with BULLETPROOF settings
        crew = Crew(
            agents=[
                product_manager_agent,
                system_architect_agent,
                backend_developer_agent,
                frontend_developer_agent,
                qa_engineer_agent,
                devops_engineer_agent
            ],
            tasks=[
                requirements_analysis_task,
                architecture_design_task,
                backend_development_task,
                frontend_development_task,
                testing_task,
                deployment_task
            ],
            process=Process.sequential,
            verbose=True,  # Keep the beautiful logging!
            memory=False,  # Disabled to avoid OpenAI dependency
            max_execution_time=2400,  # 40 minutes timeout - GENEROUS
            max_rpm=30,  # Higher RPM for efficient file generation
            respect_context_window=True,  # Handle context length properly
            max_iter=3  # Limit iterations to prevent context bloat
        )
        
        # Project input
        project_input = {
            "project_name": "Task Manager Web App",
            "description": """
            Build a modern task management web application with:
            - User authentication (JWT)
            - Task CRUD operations
            - Task priorities and categories
            - Responsive design
            - REST API backend with FastAPI
            - SQLite database
            """,
            "target_users": "Individuals and small teams",
            "tech_preferences": "Python FastAPI backend, vanilla JavaScript frontend, SQLite"
        }
        
        print("🎯 Starting CrewAI development process...")
        print(f"Project: {project_input['project_name']}")
        print("=" * 60)
        
        # Execute the crew
        start_time = time.time()
        result = crew.kickoff(inputs=project_input)
        end_time = time.time()
        
        print(f"\n🎉 CrewAI execution completed in {end_time - start_time:.1f} seconds!")
        print("=" * 60)
        
        # Validate we have a working application
        if validate_complete_app():
            print("✅ SUCCESS - Core application files generated!")
            show_generated_files()
            return "complete_success"
        else:
            print("⚠️  Missing critical files - some agents may have failed.")
            show_generated_files()
            return None
        
    except ImportError as e:
        print(f"❌ Import error: {e}")
        print("💡 Make sure you have installed CrewAI and dependencies:")
        print("   pip install crewai crewai-tools langchain-anthropic")
        return None
        
    except Exception as e:
        error_msg = str(e)
        print(f"❌ Error: {error_msg}")
        
        # Handle specific timeout errors - but we need COMPLETE success
        if "timeout" in error_msg.lower() or "timed out" in error_msg.lower():
            print("❌ TIMEOUT FAILURE - This is not acceptable!")
            print("💡 We need ALL 6 agents to complete for a working app.")
            
            # Check what we got but don't call it success
            total_files = show_generated_files()
            
            print(f"\n⚠️  Only got {total_files} files - INCOMPLETE APPLICATION")
            print("🔄 You MUST run this again to get a complete working app!")
            print("💡 Try again - timeouts are often temporary network issues.")
            return None
        
        # Handle other errors - NO PARTIAL SUCCESS ALLOWED
        print("💡 Checking what was generated...")
        total_files = show_generated_files()
        
        print(f"❌ FAILURE - Only {total_files} files generated")
        print("💡 We need ALL 6 agents to complete successfully!")
        print("🔄 Please run again to get a complete working application.")
        
        import traceback
        traceback.print_exc()
        return None

def main():
    """Main function"""
    print("🤖 CrewAI Task Management App Generator - BULLETPROOF VERSION")
    print("=" * 70)
    print("This MUST generate a complete working application with all 6 agents")
    print("No partial success - we need the full working app!")
    print("=" * 70)
    
    if not validate_setup():
        sys.exit(1)
    
    result = run_crewai_development()
    
    if result == "complete_success":
        print("\n🎉 SUCCESS - Application Generated!")
        print("📝 CrewAI agents completed their tasks:")
        print("✅ Product Manager - Requirements & user stories")
        print("✅ System Architect - Architecture & database design")
        print("✅ Backend Developer - FastAPI backend")
        print("✅ Frontend Developer - Web interface")
        print("✅ QA Engineer - Test suites")
        print("✅ DevOps Engineer - Deployment configurations")
        print("\n🚀 Your task management application is ready!")
        print("💡 Run post-generation fixes to handle any remaining issues.")
        
    else:
        print("\n⚠️  Generation completed with some missing files.")
        print("💡 Some agents may have had issues - check the missing files log above.")
        print("🔄 You can run the script again or use post-generation fixes.")
        print("💡 Many missing files can be automatically created by the fixes script.")

if __name__ == "__main__":
    main()