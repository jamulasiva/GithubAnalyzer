"""
Test runner script for GitHub Audit Platform webhook testing.
"""

import subprocess
import sys
from pathlib import Path

def run_tests():
    """Run the comprehensive test suite."""
    backend_path = Path(__file__).parent
    
    print("🧪 GitHub Audit Platform - Test Suite")
    print("=" * 50)
    
    # Install test dependencies if needed
    print("\n📦 Installing test dependencies...")
    subprocess.run([
        sys.executable, "-m", "pip", "install", 
        "pytest", "pytest-asyncio", "httpx"
    ], cwd=backend_path)
    
    # Run basic API tests
    print("\n🔍 Running API endpoint tests...")
    result1 = subprocess.run([
        sys.executable, "-m", "pytest", 
        "tests/api/test_endpoints.py", "-v"
    ], cwd=backend_path)
    
    # Run webhook processing tests
    print("\n🔗 Running webhook processing tests...")
    result2 = subprocess.run([
        sys.executable, "-m", "pytest", 
        "tests/api/test_webhooks.py", "-v"
    ], cwd=backend_path)
    
    # Run payload integration tests
    print("\n📋 Running payload integration tests...")
    result3 = subprocess.run([
        sys.executable, "-m", "pytest", 
        "tests/api/test_payload_integration.py", "-v"
    ], cwd=backend_path)
    
    # Summary
    print("\n" + "=" * 50)
    print("📊 Test Results Summary:")
    print(f"   API Endpoints: {'✅ PASSED' if result1.returncode == 0 else '❌ FAILED'}")
    print(f"   Webhook Processing: {'✅ PASSED' if result2.returncode == 0 else '❌ FAILED'}")
    print(f"   Payload Integration: {'✅ PASSED' if result3.returncode == 0 else '❌ FAILED'}")
    
    # Overall result
    overall_success = all(r.returncode == 0 for r in [result1, result2, result3])
    print(f"\n🎯 Overall Result: {'✅ ALL TESTS PASSED' if overall_success else '❌ SOME TESTS FAILED'}")
    
    return overall_success

def run_specific_payload_test(payload_name):
    """Run test for a specific payload."""
    backend_path = Path(__file__).parent
    
    print(f"🧪 Testing specific payload: {payload_name}")
    print("=" * 50)
    
    result = subprocess.run([
        sys.executable, "-m", "pytest", 
        "tests/api/test_payload_integration.py", 
        "-k", f"test_webhook_with_specific_payload and {payload_name.replace('.json', '')}",
        "-v"
    ], cwd=backend_path)
    
    print(f"\n🎯 Result: {'✅ PASSED' if result.returncode == 0 else '❌ FAILED'}")
    return result.returncode == 0

if __name__ == "__main__":
    if len(sys.argv) > 1:
        # Test specific payload
        payload_name = sys.argv[1]
        success = run_specific_payload_test(payload_name)
    else:
        # Run all tests
        success = run_tests()
    
    sys.exit(0 if success else 1)