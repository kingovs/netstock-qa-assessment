# RUNNING ALL TESTS

import pytest
import sys
from datetime import datetime


def run_all_tests():
    """Run all simplified UI automation tests"""
    
    print("="*60)
    print("BOOKING AUTOMATION TEST SUITE")
    print("="*60)
    print(f"Started: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
    print()
    
    # Test files to run
    test_files = [
        "i_test_missing_email.py",
        "ii_test_complete_booking.py", 
        "iii_test_booking_deletion.py"
    ]
    
    # Run the tests
    pytest_args = [
        *test_files,
        "-v",           # Verbose output
        "-s",           # Show print statements
        "--tb=short",   # Short traceback format
        "--html=test_report.html",
        "--self-contained-html"
    ]
    
    print("Running tests...")
    print("-" * 60)
    
    exit_code = pytest.main(pytest_args)
    
    print("-" * 60)
    print(f"Completed: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
    
    if exit_code == 0:
        print("All tests passed!")
    else:
        print("Some tests failed or had issues")
    
    print("Report: test_report.html")
    print("="*60)
    
    return exit_code


if __name__ == "__main__":
    exit_code = run_all_tests()
    sys.exit(exit_code)
