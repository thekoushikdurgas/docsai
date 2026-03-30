"""
Test script for keyword cleaning functionality.

Tests the clean_keyword function with various problematic and valid keywords.
"""

from ..utils.cleaning import clean_keyword, clean_keyword_array, is_valid_keyword


def test_keyword_cleaning():
    """Test keyword cleaning with various examples."""
    
    # Test cases: (input, expected_output, description)
    test_cases = [
        # Invalid keywords (should return None)
        ("??", None, "Encoding corruption - question marks"),
        ("???", None, "Encoding corruption - multiple question marks"),
        ("????", None, "Encoding corruption - many question marks"),
        ("0", None, "Single zero"),
        ("00", None, "Double zero"),
        ("000", None, "Triple zero"),
        ("000)", None, "Zero with closing paren"),
        ("000#", None, "Zero with hash"),
        ("000%", None, "Zero with percent"),
        ("000+", None, "Zero with plus"),
        ("_", None, "Single underscore"),
        ("__", None, "Double underscore"),
        ("", None, "Empty string"),
        ("   ", None, "Only whitespace"),
        
        # Valid keywords (should be preserved)
        ("000 employees", "000 employees", "Number with descriptive text"),
        ("000 products", "000 products", "Number with descriptive text"),
        ("1000 sq ft", "1000 sq ft", "Number with unit"),
        ("0-10v dimming", "0-10v dimming", "Range with descriptive text"),
        ("000 psi", "000 psi", "Number with unit"),
        ("technology", "technology", "Simple word"),
        ("manufacturing", "manufacturing", "Simple word"),
        ("software development", "software development", "Two words"),
        ("AI & Machine Learning", "AI & Machine Learning", "With ampersand"),
        ("cloud-based", "cloud-based", "With hyphen"),
        
        # Keywords needing cleaning
        ('"keyword"', "keyword", "Wrapping quotes"),
        ("'keyword'", "keyword", "Wrapping single quotes"),
        ("  keyword  ", "keyword", "Extra whitespace"),
        ("keyword\n\nkeyword", "keyword keyword", "Newlines"),
        
        # Edge cases
        ("a", "a", "Single letter (if MIN_KEYWORD_LENGTH=1)"),
        ("123", None, "Only numbers (if ALLOW_NUMBERS_ONLY=False)"),
        ("a1", "a1", "Letter and number"),
        ("1a", "1a", "Number and letter"),
    ]
    
    print("=" * 80)
    print("Keyword Cleaning Test Suite")
    print("=" * 80)
    print()
    
    passed = 0
    failed = 0
    
    for input_keyword, expected, description in test_cases:
        result = clean_keyword(input_keyword)
        
        # Compare results
        if result == expected:
            status = "✓ PASS"
            passed += 1
        else:
            status = "✗ FAIL"
            failed += 1
        
        print(f"{status} | {description}")
        print(f"      Input:    {repr(input_keyword)}")
        print(f"      Expected: {repr(expected)}")
        print(f"      Got:      {repr(result)}")
        if result != expected:
            print(f"      ⚠️  MISMATCH!")
        print()
    
    print("=" * 80)
    print(f"Results: {passed} passed, {failed} failed out of {len(test_cases)} tests")
    print("=" * 80)
    
    return failed == 0


def test_keyword_array_cleaning():
    """Test keyword array cleaning."""
    print("\n" + "=" * 80)
    print("Keyword Array Cleaning Test")
    print("=" * 80)
    print()
    
    test_cases = [
        (["??", "000", "valid keyword"], ["valid keyword"], "Mix of invalid and valid"),
        (["000 employees", "technology", "??"], ["000 employees", "technology"], "Valid keywords with one invalid"),
        (["??", "???", "000"], None, "All invalid"),
        (["keyword1", "keyword2", "keyword3"], ["keyword1", "keyword2", "keyword3"], "All valid"),
        (None, None, "None input"),
        ([], None, "Empty array"),
    ]
    
    passed = 0
    failed = 0
    
    for input_array, expected, description in test_cases:
        result = clean_keyword_array(input_array)
        
        if result == expected:
            status = "✓ PASS"
            passed += 1
        else:
            status = "✗ FAIL"
            failed += 1
        
        print(f"{status} | {description}")
        print(f"      Input:    {input_array}")
        print(f"      Expected: {expected}")
        print(f"      Got:      {result}")
        if result != expected:
            print(f"      ⚠️  MISMATCH!")
        print()
    
    print("=" * 80)
    print(f"Results: {passed} passed, {failed} failed out of {len(test_cases)} tests")
    print("=" * 80)
    
    return failed == 0


if __name__ == "__main__":
    print("Running keyword cleaning tests...\n")
    
    test1_passed = test_keyword_cleaning()
    test2_passed = test_keyword_array_cleaning()
    
    if test1_passed and test2_passed:
        print("\n✅ All tests passed!")
        exit(0)
    else:
        print("\n❌ Some tests failed. Please review the output above.")
        exit(1)

