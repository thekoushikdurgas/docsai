"""
Test script for company name cleaning functionality.

Tests the clean_company_name function with various problematic and valid company names.
"""

from ..utils.cleaning import clean_company_name, is_valid_company_name


def test_company_name_cleaning():
    """Test company name cleaning with various examples."""
    
    # Test cases: (input, expected_output, description)
    test_cases = [
        # Invalid names (should return None)
        ("~", None, "Single tilde"),
        ("_", None, "Single underscore"),
        ("__", None, "Double underscore"),
        ("!", None, "Single exclamation"),
        ("?", None, "Single question mark"),
        ("//", None, "Double slash"),
        ("...", None, "Three dots"),
        ("*****", None, "Multiple asterisks"),
        ("0", None, "Single zero"),
        ("000", None, "Multiple zeros"),
        ("___________________________________", None, "Many underscores"),
        (".,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,", None, "Many commas and dots"),
        ("", None, "Empty string"),
        ("   ", None, "Only whitespace"),
        
        # Encoding issues (should return None or cleaned)
        ("??", None, "Encoding corruption - question marks"),
        ("???", None, "Encoding corruption - multiple question marks"),
        ("", None, "Replacement character"),
        
        # Emojis (should be removed or return None)
        ("👋", None, "Single emoji"),
        ("☘️", None, "Single emoji with variation"),
        ("Company 👋 Name", "Company Name", "Emoji in middle"),
        
        # Special Unicode formatting (should be normalized)
        ("𝕄𝕋ℂ 𝔾𝕃𝕆𝔹𝔸𝕃", "MTC GLOBAL", "Mathematical bold Unicode"),
        ("𝗧𝗵𝗲 𝗙𝘂𝘀𝗶𝗼𝗻 𝗠𝗮𝗿𝗸𝗲𝘁𝗶𝗻𝗴", "The Fusion Marketing", "Mathematical sans-serif bold"),
        ("𝐒𝐎𝐎𝐍", "SOON", "Mathematical italic"),
        
        # Wrapping quotes (should be removed)
        ('"Company Name"', "Company Name", "Double quotes"),
        ("'Company Name'", "Company Name", "Single quotes"),
        ('""Company Name""', "Company Name", "Nested quotes"),
        ("'\"Company Name\"'", "Company Name", "Mixed nested quotes"),
        
        # Valid names with special characters (should be preserved)
        ("O'Reilly & Associates", "O'Reilly & Associates", "Apostrophe and ampersand"),
        ("Smith & Co.", "Smith & Co.", "Ampersand and period"),
        ("ABC (Inc.)", "ABC (Inc.)", "Parentheses"),
        ("Company-Co", "Company-Co", "Hyphen"),
        ("St. John's", "St. John's", "Period and apostrophe"),
        ("A/B Testing Co", "A/B Testing Co", "Slash"),
        
        # Whitespace normalization
        ("  Company  Name  ", "Company Name", "Extra whitespace"),
        ("Company\t\tName", "Company Name", "Tabs"),
        ("Company\n\nName", "Company Name", "Newlines"),
        
        # International names (should be preserved)
        ("휴넷", "휴넷", "Korean company name"),
        ("설탕(오누이)", "설탕(오누이)", "Korean with parentheses"),
        ("ゼヒトモ", "ゼヒトモ", "Japanese company name"),
        ("ソーシャス", "ソーシャス", "Japanese katakana"),
        ("บริษัท ทีโอที จำกัด(มหาชน)", "บริษัท ทีโอที จำกัด(มหาชน)", "Thai company name"),
        
        # Numbers with letters (potentially valid)
        ("001 Limited", "001 Limited", "Number prefix with suffix"),
        ("0101 Labs", "0101 Labs", "Number prefix"),
        ("Company 123", "Company 123", "Number suffix"),
        
        # Edge cases
        ("A", None, "Single letter (if ALLOW_SINGLE_LETTER=False)"),
        ("123", None, "Only numbers (if ALLOW_NUMBERS_ONLY=False)"),
        ("A1", "A1", "Letter and number"),
        ("1A", "1A", "Number and letter"),
    ]
    
    print("=" * 80)
    print("Company Name Cleaning Test Suite")
    print("=" * 80)
    print()
    
    passed = 0
    failed = 0
    
    for input_name, expected, description in test_cases:
        result = clean_company_name(input_name)
        
        # Compare results
        if result == expected:
            status = "✓ PASS"
            passed += 1
        else:
            status = "✗ FAIL"
            failed += 1
        
        print(f"{status} | {description}")
        print(f"      Input:    {repr(input_name)}")
        print(f"      Expected:  {repr(expected)}")
        print(f"      Got:       {repr(result)}")
        if result != expected:
            print(f"      ⚠️  MISMATCH!")
        print()
    
    print("=" * 80)
    print(f"Results: {passed} passed, {failed} failed out of {len(test_cases)} tests")
    print("=" * 80)
    
    return failed == 0


def test_validation():
    """Test the validation function separately."""
    print("\n" + "=" * 80)
    print("Company Name Validation Test")
    print("=" * 80)
    print()
    
    validation_tests = [
        ("Valid Company", True, "Normal company name"),
        ("~", False, "Single character"),
        ("__", False, "Placeholder pattern"),
        ("O'Reilly", True, "Valid with apostrophe"),
        ("", False, "Empty string"),
        ("   ", False, "Only whitespace"),
        ("123", False, "Only numbers"),
        ("A1", True, "Letter and number"),
    ]
    
    for name, expected_valid, description in validation_tests:
        result = is_valid_company_name(name)
        status = "✓" if result == expected_valid else "✗"
        print(f"{status} {description}: {repr(name)} -> {result} (expected {expected_valid})")
    
    print()


if __name__ == "__main__":
    print("Running company name cleaning tests...\n")
    
    test_passed = test_company_name_cleaning()
    test_validation()
    
    if test_passed:
        print("\n✅ All tests passed!")
        exit(0)
    else:
        print("\n❌ Some tests failed. Please review the output above.")
        exit(1)

