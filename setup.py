#!/usr/bin/env python
"""
Setup script for Smart Expense Tracker
Run this once to initialize the project
"""

import os
import sys
import subprocess
from pathlib import Path

def main():
    print("\n" + "="*60)
    print("🚀 SMART EXPENSE TRACKER - SETUP")
    print("="*60 + "\n")
    
    # Check Python version
    if sys.version_info < (3, 8):
        print("❌ Python 3.8+ required")
        sys.exit(1)
    print(f"✅ Python {sys.version.split()[0]}")
    
    # Create virtual environment
    venv_path = ".venv"
    if not os.path.exists(venv_path):
        print("\n📦 Creating virtual environment...")
        subprocess.run([sys.executable, "-m", "venv", venv_path], check=True)
        print("✅ Virtual environment created")
    else:
        print("\n✅ Virtual environment already exists")
    
    # Determine activation command
    if sys.platform == "win32":
        activate_cmd = f"{venv_path}\\Scripts\\activate.bat"
        pip_cmd = f"{venv_path}\\Scripts\\pip"
    else:
        activate_cmd = f"source {venv_path}/bin/activate"
        pip_cmd = f"{venv_path}/bin/pip"
    
    print(f"\n   To activate: {activate_cmd}")
    
    # Install requirements
    print("\n📥 Installing dependencies...")
    req_file = Path("requirements.txt")
    if req_file.exists():
        subprocess.run([pip_cmd, "install", "-r", "requirements.txt"], check=True)
        print("✅ Dependencies installed")
    else:
        print("❌ requirements.txt not found")
        sys.exit(1)
    
    # Create necessary directories
    print("\n📁 Creating directories...")
    Path("src/expense_tracker").mkdir(parents=True, exist_ok=True)
    Path("tests").mkdir(parents=True, exist_ok=True)
    Path("reports").mkdir(parents=True, exist_ok=True)
    print("✅ Directories created")
    
    # Run tests
    print("\n🧪 Running tests...")
    result = subprocess.run([sys.executable, "tests/test_expense_tracker.py"], 
                          capture_output=True, text=True)
    if "OK" in result.stderr or "ok" in result.stdout:
        print("✅ All tests passed")
    else:
        print("⚠️  Some tests may have issues")
        print(result.stderr)
    
    # Summary
    print("\n" + "="*60)
    print("✅ SETUP COMPLETE!")
    print("="*60)
    print(f"\n📋 Next steps:")
    print(f"   1. Activate environment: {activate_cmd}")
    print(f"   2. Run demo: python demo.py")
    print(f"   3. Start app: streamlit run app.py")
    print("\n" + "="*60 + "\n")

if __name__ == "__main__":
    main()
