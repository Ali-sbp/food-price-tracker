#!/usr/bin/env python3
"""
Food Price Anomaly Tracker - One-Click Launcher
Builds frontend and starts backend server
"""

import os
import sys
import subprocess
import time
import webbrowser
from pathlib import Path

def main():
    # Get the app directory
    app_dir = Path(__file__).parent
    frontend_dir = app_dir / "frontend"
    backend_dir = app_dir / "backend"
    
    print("🍞 Food Price Anomaly Tracker")
    print("=" * 50)
    
    # Step 1: Build frontend
    print("\n📦 Building frontend...")
    try:
        result = subprocess.run(
            ["npm", "run", "build"],
            cwd=frontend_dir,
            capture_output=True,
            text=True,
            timeout=120
        )
        if result.returncode != 0:
            print(f"❌ Frontend build failed:\n{result.stderr}")
            sys.exit(1)
        print("✅ Frontend built successfully")
    except FileNotFoundError:
        print("❌ npm not found. Please install Node.js")
        sys.exit(1)
    except subprocess.TimeoutExpired:
        print("❌ Frontend build timed out")
        sys.exit(1)
    
    # Step 2: Start backend
    print("\n🚀 Starting backend server...")
    try:
        # Determine which Python to use - prefer venv
        venv_python = backend_dir.parent / ".venv" / "bin" / "python"
        if venv_python.exists():
            python_exe = str(venv_python)
        else:
            # Fallback to system python
            python_exe = "python3"
        
        # Check if uvicorn is available
        check_result = subprocess.run(
            [python_exe, "-m", "uvicorn", "--version"],
            cwd=backend_dir,
            capture_output=True,
            text=True,
            timeout=5
        )
        if check_result.returncode != 0:
            print(f"❌ uvicorn not found. Please install dependencies:")
            print(f"   cd backend && pip install -r requirements.txt")
            sys.exit(1)
        
        backend_process = subprocess.Popen(
            [python_exe, "-m", "uvicorn", "app.main:application", "--port", "8000"],
            cwd=backend_dir,
            stdout=subprocess.PIPE,
            stderr=subprocess.PIPE,
            text=True
        )
        print("✅ Backend server started")
    except Exception as e:
        print(f"❌ Failed to start backend: {e}")
        sys.exit(1)
    
    # Step 3: Wait for server to be ready
    print("\n⏳ Waiting for server to start...")
    for i in range(30):
        try:
            import urllib.request
            urllib.request.urlopen("http://localhost:8000", timeout=1)
            print("✅ Server is ready!")
            break
        except:
            if i == 29:
                print("❌ Server failed to start in time")
                backend_process.terminate()
                sys.exit(1)
            time.sleep(0.5)
    
    # Step 4: Open browser
    print("\n🌐 Opening browser...")
    time.sleep(1)
    webbrowser.open("http://localhost:8000")
    
    print("\n" + "=" * 50)
    print("✨ App is running at http://localhost:8000")
    print("Press Ctrl+C to stop the server")
    print("=" * 50)
    
    # Keep the process running
    try:
        backend_process.wait()
    except KeyboardInterrupt:
        print("\n\n👋 Shutting down...")
        backend_process.terminate()
        backend_process.wait()
        print("Done!")

if __name__ == "__main__":
    main()
