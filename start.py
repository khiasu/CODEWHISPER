#!/usr/bin/env python3
"""
Startup script for Code Whisper Backend
Includes pre-flight checks and helpful messages
"""

import sys
import subprocess
import requests
import time
from config import Config

def check_python_version():
    """Check if Python version is compatible"""
    if sys.version_info < (3, 8):
        print("❌ Python 3.8+ is required")
        return False
    print(f"✅ Python {sys.version.split()[0]} detected")
    return True

def check_dependencies():
    """Check if required packages are installed"""
    try:
        import flask
        import flask_cors
        import requests
        print("✅ All dependencies are installed")
        return True
    except ImportError as e:
        print(f"❌ Missing dependency: {e}")
        print("   Run: pip install -r requirements.txt")
        return False

def check_ollama():
    """Check if Ollama is running and has CodeLLaMA"""
    print("🔍 Checking Ollama service...")
    
    try:
        # Check if Ollama is running
        response = requests.get(f"http://{Config.OLLAMA_HOST}:{Config.OLLAMA_PORT}/api/tags", timeout=5)
        if response.status_code != 200:
            print("❌ Ollama is not responding")
            return False
        
        # Check if CodeLLaMA model is available
        models = response.json().get('models', [])
        model_names = [model.get('name', '') for model in models]
        
        if any('codellama' in name.lower() for name in model_names):
            print("✅ Ollama is running with CodeLLaMA model")
            return True
        else:
            print("⚠️  Ollama is running but CodeLLaMA model not found")
            print("   Run: ollama pull codellama")
            return False
            
    except requests.exceptions.ConnectionError:
        print("❌ Cannot connect to Ollama")
        print("   Make sure Ollama is running: ollama serve")
        return False
    except Exception as e:
        print(f"❌ Error checking Ollama: {e}")
        return False

def start_server():
    """Start the Flask server"""
    print("\n🚀 Starting Code Whisper Backend...")
    print(f"🔗 Server will be available at http://{Config.HOST}:{Config.PORT}")
    print("📡 Press Ctrl+C to stop the server")
    print("-" * 50)
    
    try:
        from app import app
        app.run(debug=Config.DEBUG, host=Config.HOST, port=Config.PORT)
    except KeyboardInterrupt:
        print("\n👋 Server stopped by user")
    except Exception as e:
        print(f"\n❌ Server error: {e}")

def main():
    """Main startup function"""
    print("🎯 Code Whisper Backend Startup")
    print("=" * 40)
    
    # Pre-flight checks
    checks_passed = True
    
    if not check_python_version():
        checks_passed = False
    
    if not check_dependencies():
        checks_passed = False
    
    ollama_available = check_ollama()
    if not ollama_available:
        print("\n⚠️  Warning: Ollama issues detected")
        print("   The server will start but AI features may not work")
        response = input("   Continue anyway? (y/N): ").lower()
        if response != 'y':
            print("👋 Startup cancelled")
            return
    
    if not checks_passed:
        print("\n❌ Pre-flight checks failed")
        print("   Please fix the issues above before starting")
        return
    
    # Start the server
    start_server()

if __name__ == "__main__":
    main()
