#!/usr/bin/env python3
"""
Test runner script for the island counter assignment.
Runs all tests and generates a comprehensive report.
"""

import pytest
import sys
import os
import subprocess
import time

# Get the root directory of the project
PROJECT_ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
TESTS_DIR = os.path.join(PROJECT_ROOT, 'tests')
TEST_DATA_DIR = os.path.join(TESTS_DIR, 'data')
MAIN_MODULE_PATH = os.path.join(PROJECT_ROOT, 'island_counter', 'main.py')


def run_unit_tests():
    """Run unit tests with pytest."""
    print("="*60)
    print("RUNNING UNIT TESTS")
    print("="*60)

    test_file_path = os.path.join(TESTS_DIR, "test_comprehensive.py")
    result = pytest.main([
        test_file_path,
        "-v",
        "--tb=short",
        "--color=yes"
    ])

    return result == 0


def run_integration_tests():
    """Run integration tests with actual files."""
    print("\n" + "="*60)
    print("RUNNING INTEGRATION TESTS")
    print("="*60)

    test_files = [
        ('test_small.txt', 1),  # This file contains one island.
        ('test_medium.txt', 11),
        ('test_no_islands.txt', 0),
        ('test_checkerboard.txt', 13)
    ]

    passed = 0
    total = len(test_files)

    for filename, expected_count in test_files:
        full_path = os.path.join(TEST_DATA_DIR, filename)
        if os.path.exists(full_path):
            try:
                result = subprocess.run([
                    sys.executable, MAIN_MODULE_PATH, full_path
                ], capture_output=True, text=True, timeout=30)

                if result.returncode == 0:
                    actual_count = int(result.stdout.strip())
                    if actual_count == expected_count:
                        print(f"✅ {filename}: PASSED ({actual_count} islands)")
                        passed += 1
                    else:
                        print(
                            f"❌ {filename}: FAILED (Expected: {expected_count}, Got: {actual_count})")
                else:
                    print(f"❌ {filename}: ERROR - {result.stderr.strip()}")
            except Exception as e:
                print(f"❌ {filename}: EXCEPTION - {str(e)}")
        else:
            print(f"⚠️  {filename}: FILE NOT FOUND at {full_path}")

    print(f"\nIntegration Tests: {passed}/{total} passed")
    return passed == total


def run_error_handling_tests():
    """Test error handling scenarios."""
    print("\n" + "="*60)
    print("RUNNING ERROR HANDLING TESTS")
    print("="*60)

    error_tests = [
        ('test_invalid_chars.txt', 'Invalid character'),
        ('test_non_rectangular.txt', 'not rectangular'),
        ('nonexistent_file.txt', 'not found')
    ]

    passed = 0
    total = len(error_tests)

    for filename, expected_error in error_tests:
        full_path = os.path.join(
            TEST_DATA_DIR, filename) if 'nonexistent' not in filename else filename
        try:
            result = subprocess.run([
                sys.executable, MAIN_MODULE_PATH, full_path
            ], capture_output=True, text=True, timeout=30)

            if result.returncode != 0 and expected_error.lower() in result.stderr.lower():
                print(f"✅ {filename}: PASSED (Correctly handled error)")
                passed += 1
            else:
                print(
                    f"❌ {filename}: FAILED (Should have failed with '{expected_error}')")
        except Exception as e:
            print(f"❌ {filename}: EXCEPTION - {str(e)}")

    print(f"\nError Handling Tests: {passed}/{total} passed")
    return passed == total


def run_performance_tests():
    """Run basic performance tests."""
    print("\n" + "="*60)
    print("RUNNING PERFORMANCE TESTS")
    print("="*60)

    large_test_file = os.path.join(TEST_DATA_DIR, 'test_large.txt')
    if not os.path.exists(large_test_file):
        print(
            f"⚠️ Large grid test: SKIPPED (File not found at {large_test_file})")
        return True

    try:
        start_time = time.time()
        result = subprocess.run([
            sys.executable, MAIN_MODULE_PATH, large_test_file
        ], capture_output=True, text=True, timeout=60)
        end_time = time.time()

        if result.returncode == 0:
            execution_time = end_time - start_time
            island_count = int(result.stdout.strip())
            print(f"✅ Large grid test: PASSED")
            print(f"   Islands found: {island_count}")
            print(f"   Execution time: {execution_time:.3f}s")
            return True
        else:
            print(f"❌ Large grid test: FAILED - {result.stderr.strip()}")
            return False
    except subprocess.TimeoutExpired:
        print("❌ Large grid test: TIMEOUT (>60 seconds)")
        return False
    except Exception as e:
        print(f"❌ Large grid test: EXCEPTION - {str(e)}")
        return False


def main():
    """Run all tests and generate final report."""
    print("ISLAND COUNTER - COMPREHENSIVE TEST SUITE")
    print("="*60)

    start_time = time.time()

    unit_passed = run_unit_tests()
    integration_passed = run_integration_tests()
    error_handling_passed = run_error_handling_tests()
    performance_passed = run_performance_tests()

    end_time = time.time()
    total_time = end_time - start_time

    print("\n" + "="*60)
    print("FINAL TEST REPORT")
    print("="*60)

    results = [
        ("Unit Tests", unit_passed),
        ("Integration Tests", integration_passed),
        ("Error Handling Tests", error_handling_passed),
        ("Performance Tests", performance_passed)
    ]

    passed_suites = sum(1 for _, passed in results if passed)
    total_suites = len(results)

    for test_type, passed in results:
        status = "✅ PASSED" if passed else "❌ FAILED"
        print(f"{test_type}: {status}")

    print(f"\nOverall: {passed_suites}/{total_suites} test suites passed")
    print(f"Total execution time: {total_time:.2f}s")

    if passed_suites == total_suites:
        print("\n🎉 ALL TESTS PASSED! Your assignment is working correctly.")
        return 0
    else:
        print(f"\n⚠️  Some tests failed. Please review the output above.")
        return 1


if __name__ == "__main__":
    exit_code = main()
    sys.exit(exit_code)
