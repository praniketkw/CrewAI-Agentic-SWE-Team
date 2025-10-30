#!/usr/bin/env python3
"""
Quick Start Script for CrewAI Task Management App Generator
Sets up the environment and guides users through the process
"""

import os
import sys
import subprocess
from pathlib import Path

def print_banner():
    print("🤖 CrewAI Task Management App Generator")
    print("=" * 50)
    print("Welcome! This script will help you set up and run")
    print("the CrewAI demonstration project.")
    print("=" * 50)

def check_python_version():
    """Check if Python version is compatible"""
    if sys.version_info < (3, 8):
        print("❌ Python 3.8+ is required. You have:", sys.version)
        return False
    print(f"✅ Python version: {sys.version.split()[0]}")
    return True

def setup_virtual_environment():
    """Set up virtual environment"""
    venv_path = Path("crewai_env")
    
    if venv_path.exists():
        print("✅ Virtual environment already exists")
        return True
    
    print("📦 Creating virtual environment...")
    try:
        subprocess.run([sys.executable, "-m", "venv", "crewai_env"], check=True)
        print("✅ Virtual environment created")
        return True
    except subprocess.CalledProcessError:
        print("❌ Failed to create virtual environment")
        return False

def install_dependencies():
    """Install required dependencies"""
    print("📦 Installing CrewAI dependencies...")
    
    # Determine the correct pip path
    if os.name == 'nt':  # Windows
        pip_path = Path("crewai_env/Scripts/pip")
    else:  # Unix/Linux/macOS
        pip_path = Path("crewai_env/bin/pip")
    
    try:
        subprocess.run([str(pip_path), "install", "-r", "requirements.txt"], check=True)
        print("✅ Dependencies installed successfully")
        return True
    except subprocess.CalledProcessError:
        print("❌ Failed to install dependencies")
        return False

def setup_environment_file():
    """Set up .env file"""
    env_file = Path(".env")
    env_example = Path(".env.example")
    
    if env_file.exists():
        print("✅ .env file already exists")
        return True
    
    if env_example.exists():
        # Copy example file
        with open(env_example, 'r') as f:
            content = f.read()
        with open(env_file, 'w') as f:
            f.write(content)
        print("📝 Created .env file from template")
    else:
        # Create basic .env file
        with open(env_file, 'w') as f:
            f.write("# Anthropic API Key for Claude\n")
            f.write("ANTHROPIC_API_KEY=your_api_key_here\n")
        print("📝 Created basic .env file")
    
    print("\n🔑 IMPORTANT: You need to add your Anthropic API key to .env")
    print("   1. Get your API key from: https://console.anthropic.com")
    print("   2. Edit .env file and replace 'your_api_key_here' with your key")
    
    return True

def check_api_key():
    """Check if API key is configured"""
    env_file = Path(".env")
    if not env_file.exists():
        return False
    
    with open(env_file, 'r') as f:
        content = f.read()
    
    if "your_api_key_here" in content:
        print("⚠️  Please update your API key in .env file before running CrewAI")
        return False
    
    if "ANTHROPIC_API_KEY=" in content:
        print("✅ API key appears to be configured")
        return True
    
    return False

def show_next_steps():
    """Show next steps to user"""
    print("\n🚀 Setup Complete! Next Steps:")
    print("=" * 40)
    
    if os.name == 'nt':  # Windows
        print("1. Activate virtual environment:")
        print("   crewai_env\\Scripts\\activate")
    else:  # Unix/Linux/macOS
        print("1. Activate virtual environment:")
        print("   source crewai_env/bin/activate")
    
    print("\n2. Run the CrewAI generation:")
    print("   python run_crewai.py")
    
    print("\n3. After generation, run the app:")
    print("   cd backend")
    print("   pip install -r requirements.txt")
    print("   python main.py")
    
    print("\n4. Open frontend/index.html in your browser")
    
    print("\n📚 For more details, check README.md")

def main():
    """Main setup function"""
    print_banner()
    
    # Check Python version
    if not check_python_version():
        sys.exit(1)
    
    # Set up virtual environment
    if not setup_virtual_environment():
        sys.exit(1)
    
    # Install dependencies
    if not install_dependencies():
        sys.exit(1)
    
    # Set up environment file
    if not setup_environment_file():
        sys.exit(1)
    
    # Check API key
    api_key_ready = check_api_key()
    
    # Show next steps
    show_next_steps()
    
    if not api_key_ready:
        print("\n⚠️  Remember to update your API key in .env before running!")
    
    print("\n🎉 Setup complete! You're ready to use CrewAI!")

if __name__ == "__main__":
    main()