#!/usr/bin/env python3
"""
One-click setup script for Playwright UI test suite
Run this once to set up everything needed for testing
"""

import os
import sys
import subprocess
import platform


def run_command(command, description):
    """Run a command and handle errors"""
    print(f"\n{description}...")
    print(f"Running: {command}")
    
    try:
        if platform.system() == "Windows":
            result = subprocess.run(command, shell=True, check=True, capture_output=True, text=True)
        else:
            result = subprocess.run(command.split(), check=True, capture_output=True, text=True)
        
        print(f"✓ {description} completed successfully")
        return True
    except subprocess.CalledProcessError as e:
        print(f"✗ {description} failed: {e}")
        if e.stdout:
            print(f"Output: {e.stdout}")
        if e.stderr:
            print(f"Error: {e.stderr}")
        return False


def check_python():
    """Check Python version"""
    version = sys.version_info
    if version.major >= 3 and version.minor >= 8:
        print(f"✓ Python {version.major}.{version.minor}.{version.micro} is suitable")
        return True
    else:
        print(f"✗ Python {version.major}.{version.minor}.{version.micro} is too old. Need Python 3.8+")
        return False


def setup_environment():
    """Set up the complete test environment"""
    print("="*60)
    print("PLAYWRIGHT UI TEST SUITE SETUP")
    print("="*60)
    
    # Check Python version
    if not check_python():
        return False
    
    # Get current directory and project paths
    current_dir = os.getcwd()
    if current_dir.endswith('tests/playwright_tst'):
        project_root = os.path.join(current_dir, '../..')
    else:
        project_root = current_dir
    
    print(f"Project root: {os.path.abspath(project_root)}")
    
    # Create virtual environment
    venv_path = os.path.join(project_root, 'venv')
    if not os.path.exists(venv_path):
        if not run_command(f"python -m venv {venv_path}", "Creating virtual environment"):
            return False
    else:
        print("✓ Virtual environment already exists")
    
    # Determine activation command
    if platform.system() == "Windows":
        pip_cmd = os.path.join(venv_path, 'Scripts', 'pip')
        activate_cmd = os.path.join(venv_path, 'Scripts', 'activate')
    else:
        pip_cmd = os.path.join(venv_path, 'bin', 'pip')
        activate_cmd = f"source {os.path.join(venv_path, 'bin', 'activate')}"
    
    # Install requirements
    requirements_path = os.path.join(project_root, 'requirements.txt')
    if os.path.exists(requirements_path):
        if not run_command(f"{pip_cmd} install -r {requirements_path}", "Installing Python packages"):
            return False
    else:
        print(f"⚠ requirements.txt not found at {requirements_path}")
        print("Installing packages individually...")
        packages = ["playwright==1.55.0", "pytest-playwright==0.7.1", "pytest==8.4.2", "pytest-html==4.1.1", "requests==2.31.0"]
        for package in packages:
            if not run_command(f"{pip_cmd} install {package}", f"Installing {package}"):
                return False
    
    # Install Playwright browsers
    if platform.system() == "Windows":
        playwright_cmd = os.path.join(venv_path, 'Scripts', 'playwright')
    else:
        playwright_cmd = os.path.join(venv_path, 'bin', 'playwright')
    
    if not run_command(f"{playwright_cmd} install firefox", "Installing Firefox for Playwright"):
        return False
    
    # Test Playwright installation
    test_dir = os.path.join(project_root, 'tests', 'playwright_tst')
    if os.path.exists(test_dir):
        os.chdir(test_dir)
        if platform.system() == "Windows":
            python_cmd = os.path.join(venv_path, 'Scripts', 'python')
        else:
            python_cmd = os.path.join(venv_path, 'bin', 'python')
        
        test_command = f'{python_cmd} -c "from playwright.sync_api import sync_playwright; print(\'Playwright ready!\')"'
        if not run_command(test_command, "Testing Playwright installation"):
            return False
    
    print("\n" + "="*60)
    print("SETUP COMPLETE!")
    print("="*60)
    print(f"To activate virtual environment:")
    if platform.system() == "Windows":
        print(f"  {os.path.join(venv_path, 'Scripts', 'activate.bat')}")
    else:
        print(f"  source {os.path.join(venv_path, 'bin', 'activate')}")
    
    print(f"\nTo run tests:")
    print(f"  cd {test_dir}")
    print(f"  python iv_run_all_tests.py")
    print("="*60)
    
    return True


if __name__ == "__main__":
    success = setup_environment()
    if not success:
        print("\n✗ Setup failed. Please check errors above.")
        sys.exit(1)
    else:
        print("\n✓ Setup completed successfully!")