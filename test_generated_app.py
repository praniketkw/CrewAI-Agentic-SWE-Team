#!/usr/bin/env python3
"""
Test Script for Generated CrewAI Application
Validates that the generated app works correctly
"""

import os
import sys
import time
import requests
import subprocess
from pathlib import Path
import json

def print_test(test_name):
    """Print a formatted test name"""
    print(f"\n🧪 {test_name}")
    print("-" * 50)

def test_file_structure():
    """Test that all expected files were generated"""
    print_test("Testing File Structure")
    
    expected_files = [
        "backend/main.py",
        "backend/models.py", 
        "backend/database.py",
        "backend/security.py",
        "backend/requirements.txt",
        "frontend/index.html",
        "frontend/styles/main.css",
        "frontend/js/app.js",
        "docs/requirements.md",
        "docs/architecture.md"
    ]
    
    missing_files = []
    present_files = []
    
    for file_path in expected_files:
        if Path(file_path).exists():
            present_files.append(file_path)
            print(f"✅ {file_path}")
        else:
            missing_files.append(file_path)
            print(f"❌ {file_path}")
    
    print(f"\n📊 Results: {len(present_files)}/{len(expected_files)} files present")
    
    if missing_files:
        print("⚠️  Missing files:")
        for file in missing_files:
            print(f"   • {file}")
        return False
    
    return True

def test_backend_syntax():
    """Test that backend Python files have valid syntax"""
    print_test("Testing Backend Python Syntax")
    
    python_files = [
        "backend/main.py",
        "backend/models.py",
        "backend/database.py", 
        "backend/security.py"
    ]
    
    syntax_errors = []
    
    for file_path in python_files:
        if not Path(file_path).exists():
            print(f"⚠️  {file_path} not found, skipping")
            continue
            
        try:
            with open(file_path, 'r') as f:
                code = f.read()
            
            # Try to compile the code
            compile(code, file_path, 'exec')
            print(f"✅ {file_path} - syntax OK")
            
        except SyntaxError as e:
            syntax_errors.append((file_path, str(e)))
            print(f"❌ {file_path} - syntax error: {e}")
        except Exception as e:
            syntax_errors.append((file_path, str(e)))
            print(f"❌ {file_path} - error: {e}")
    
    if syntax_errors:
        print(f"\n❌ Found {len(syntax_errors)} syntax errors")
        return False
    else:
        print("\n✅ All Python files have valid syntax")
        return True

def test_backend_imports():
    """Test that backend imports work"""
    print_test("Testing Backend Imports")
    
    # Change to backend directory for imports
    original_cwd = os.getcwd()
    backend_path = Path("backend")
    
    if not backend_path.exists():
        print("❌ Backend directory not found")
        return False
    
    os.chdir(backend_path)
    sys.path.insert(0, str(backend_path.absolute()))
    
    import_tests = [
        ("models", "User, Task"),
        ("database", "get_db"),
        ("security", "create_access_token")
    ]
    
    import_errors = []
    
    for module, items in import_tests:
        try:
            exec(f"from {module} import {items}")
            print(f"✅ Successfully imported {items} from {module}")
        except ImportError as e:
            import_errors.append((module, str(e)))
            print(f"❌ Failed to import from {module}: {e}")
        except Exception as e:
            import_errors.append((module, str(e)))
            print(f"❌ Error importing from {module}: {e}")
    
    # Restore original directory and path
    os.chdir(original_cwd)
    sys.path.remove(str(backend_path.absolute()))
    
    if import_errors:
        print(f"\n❌ Found {len(import_errors)} import errors")
        return False
    else:
        print("\n✅ All imports work correctly")
        return True

def test_frontend_files():
    """Test that frontend files are complete"""
    print_test("Testing Frontend Files")
    
    frontend_files = {
        "frontend/index.html": ["<html", "<body", "<script"],
        "frontend/styles/main.css": ["body", "{", "}"],
        "frontend/js/app.js": ["function", "document", "addEventListener"]
    }
    
    incomplete_files = []
    
    for file_path, required_content in frontend_files.items():
        if not Path(file_path).exists():
            print(f"❌ {file_path} not found")
            incomplete_files.append(file_path)
            continue
        
        with open(file_path, 'r') as f:
            content = f.read()
        
        missing_content = []
        for required in required_content:
            if required not in content:
                missing_content.append(required)
        
        if missing_content:
            print(f"❌ {file_path} missing: {', '.join(missing_content)}")
            incomplete_files.append(file_path)
        else:
            print(f"✅ {file_path} appears complete")
    
    if incomplete_files:
        print(f"\n❌ Found {len(incomplete_files)} incomplete frontend files")
        return False
    else:
        print("\n✅ All frontend files appear complete")
        return True

def test_backend_startup():
    """Test that the backend can start up"""
    print_test("Testing Backend Startup")
    
    if not Path("backend/main.py").exists():
        print("❌ backend/main.py not found")
        return False
    
    # Try to start the backend in a subprocess
    try:
        print("🚀 Starting backend server...")
        
        # Start the server
        process = subprocess.Popen([
            sys.executable, "-c", 
            "import sys; sys.path.append('backend'); from main import app; import uvicorn; uvicorn.run(app, host='127.0.0.1', port=8001)"
        ], stdout=subprocess.PIPE, stderr=subprocess.PIPE)
        
        # Wait a bit for startup
        time.sleep(3)
        
        # Check if it's running
        try:
            response = requests.get("http://127.0.0.1:8001/docs", timeout=5)
            if response.status_code == 200:
                print("✅ Backend started successfully")
                print("✅ API documentation accessible")
                success = True
            else:
                print(f"❌ Backend responded with status {response.status_code}")
                success = False
        except requests.exceptions.RequestException as e:
            print(f"❌ Could not connect to backend: {e}")
            success = False
        
        # Stop the server
        process.terminate()
        process.wait(timeout=5)
        
        return success
        
    except Exception as e:
        print(f"❌ Error starting backend: {e}")
        return False

def generate_test_report():
    """Generate a comprehensive test report"""
    print_test("Generating Test Report")
    
    tests = [
        ("File Structure", test_file_structure),
        ("Python Syntax", test_backend_syntax), 
        ("Backend Imports", test_backend_imports),
        ("Frontend Files", test_frontend_files),
        ("Backend Startup", test_backend_startup)
    ]
    
    results = {}
    
    for test_name, test_func in tests:
        try:
            results[test_name] = test_func()
        except Exception as e:
            print(f"❌ Test '{test_name}' failed with error: {e}")
            results[test_name] = False
    
    # Generate report
    print("\n" + "=" * 60)
    print("📊 TEST REPORT")
    print("=" * 60)
    
    passed = sum(1 for result in results.values() if result)
    total = len(results)
    
    for test_name, result in results.items():
        status = "✅ PASS" if result else "❌ FAIL"
        print(f"{status} {test_name}")
    
    print(f"\n📈 Overall: {passed}/{total} tests passed ({passed/total*100:.1f}%)")
    
    if passed == total:
        print("🎉 All tests passed! The generated app is ready to use.")
        return True
    else:
        print("⚠️  Some tests failed. Check the output above for details.")
        print("💡 Run post_generation_fixes.py to automatically fix common issues.")
        return False

def main():
    """Main test function"""
    print("🧪 CrewAI Generated App Test Suite")
    print("=" * 60)
    print("Testing the generated application for completeness and functionality...")
    
    # Check if we're in the right directory
    if not Path("run_crewai.py").exists():
        print("❌ Please run this script from the project root directory")
        sys.exit(1)
    
    # Run comprehensive tests
    success = generate_test_report()
    
    if success:
        print("\n🚀 Next Steps:")
        print("1. Run the backend: cd backend && python run.py")
        print("2. Open frontend/index.html in your browser")
        print("3. Test the application functionality")
    else:
        print("\n🔧 Recommended Actions:")
        print("1. Run: python post_generation_fixes.py")
        print("2. Manually review failed components")
        print("3. Check DEVELOPMENT_NOTES.md for known issues")
    
    return success

if __name__ == "__main__":
    success = main()
    sys.exit(0 if success else 1)