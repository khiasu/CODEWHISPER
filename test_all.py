#!/usr/bin/env python3
"""
Simple test runner for Code Whisper
Tests the reorganized backend without depending on Ollama
"""

import sys
import os

# Add the project root to Python path
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

def test_imports():
    """Test that all modules can be imported correctly"""
    print("🧪 Testing imports...")
    
    try:
        from backend.config import Config, MODE_PROMPTS
        print("✅ Config import successful")
        
        from backend.services.ollama_service import OllamaService
        print("✅ OllamaService import successful")
        
        import app
        print("✅ App import successful")
        
        return True
    except Exception as e:
        print(f"❌ Import failed: {e}")
        return False

def test_config():
    """Test configuration values"""
    print("\n🔧 Testing configuration...")
    
    try:
        from backend.config import Config, MODE_PROMPTS
        
        print(f"   Model: {Config.MODEL_NAME}")
        print(f"   Max tokens: {Config.MAX_TOKENS}")
        print(f"   Available modes: {list(MODE_PROMPTS.keys())}")
        
        # Test that we have all expected modes
        expected_modes = ["friend", "professor", "babysitter", "review"]
        for mode in expected_modes:
            if mode not in MODE_PROMPTS:
                print(f"❌ Missing mode: {mode}")
                return False
        
        print("✅ Configuration looks good")
        return True
    except Exception as e:
        print(f"❌ Config test failed: {e}")
        return False

def test_folder_structure():
    """Test the new folder structure"""
    print("\n📁 Testing folder structure...")
    
    expected_files = [
        "backend/__init__.py",
        "backend/config.py", 
        "backend/services/__init__.py",
        "backend/services/ollama_service.py",
        "frontend/index.html",
        "frontend/styles.css",
        "frontend/script.js",
        "tests/test_backend.py",
        "app.py",
        "requirements.txt",
        ".env"
    ]
    
    missing_files = []
    for file_path in expected_files:
        if not os.path.exists(file_path):
            missing_files.append(file_path)
    
    if missing_files:
        print(f"❌ Missing files: {missing_files}")
        return False
    else:
        print("✅ Folder structure is correct")
        return True

def main():
    """Run all tests"""
    print("🚀 Code Whisper - Post-Reorganization Tests")
    print("=" * 50)
    
    tests = [
        test_folder_structure,
        test_imports,
        test_config
    ]
    
    passed = 0
    failed = 0
    
    for test_func in tests:
        try:
            if test_func():
                passed += 1
            else:
                failed += 1
        except Exception as e:
            print(f"❌ Test {test_func.__name__} crashed: {e}")
            failed += 1
    
    print("\n" + "=" * 50)
    print(f"🏁 Test Results: {passed} passed, {failed} failed")
    
    if failed == 0:
        print("🎉 All tests passed! The reorganization was successful.")
        print("\n💡 Next steps:")
        print("   1. Run: py app.py")
        print("   2. Open: http://localhost:5000")
        print("   3. Test the AI features")
    else:
        print("❌ Some tests failed. Check the output above.")
    
    return failed == 0

if __name__ == "__main__":
    success = main()
    sys.exit(0 if success else 1)
