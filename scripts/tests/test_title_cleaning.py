"""
Test script for title cleaning functionality.

Tests the clean_title function with various problematic and valid titles.
"""

from ..utils.cleaning import clean_title, is_valid_title


def test_title_cleaning():
    """Test title cleaning with various examples."""
    
    # Test cases: (input, expected_output, description)
    test_cases = [
        # Invalid titles (should return None)
        ("0", None, "Single zero"),
        ("00", None, "Double zero"),
        ("000", None, "Triple zero"),
        ("0000", None, "Many zeros"),
        ("¯\\_(ツ)_/¯", None, "ASCII art pattern"),
        ("\\_(ツ)_/", None, "ASCII art pattern"),
        ("ᕕ( ᐛ )ᕗ", None, "ASCII art pattern"),
        ("∈(ﾟ◎ﾟ)∋✨🌏🔗", None, "ASCII art with emojis"),
        ("ㅡ", None, "Single Korean character (placeholder)"),
        ("", None, "Empty string"),
        ("   ", None, "Only whitespace"),
        
        # Valid international titles (should be preserved)
        ("과장", "과장", "Korean title"),
        ("대표", "대표", "Korean title"),
        ("부장", "부장", "Korean title"),
        ("팀장", "팀장", "Korean title"),
        ("エンジニア", "エンジニア", "Japanese title"),
        ("マネージャー", "マネージャー", "Japanese title"),
        ("ディレクター", "ディレクター", "Japanese title"),
        ("(주) 동성케미컬 공동대표이사", "(주) 동성케미컬 공동대표이사", "Korean with company prefix"),
        
        # Valid titles with special characters (should be preserved)
        ("부장 : 빅데이터사업팀)광고사업", "부장 : 빅데이터사업팀)광고사업", "Korean with colon and paren"),
        ("부장 (팀장)", "부장 (팀장)", "Korean with parentheses"),
        ("팀장 (이사)", "팀장 (이사)", "Korean with parentheses"),
        ("CEO & Founder", "CEO & Founder", "English with ampersand"),
        ("VP of Sales - Northeast", "VP of Sales - Northeast", "English with dash"),
        
        # Titles needing cleaning (Unicode formatting)
        ("𝙸𝚃 𝚁𝚎𝚌𝚛𝚞𝚒𝚝𝚎𝚛", "IT Recruiter", "Mathematical monospace Unicode"),
        ("𝗜𝗻-𝗛𝗼𝘂𝘀𝗲 𝗟𝗶𝘁𝗶𝗴𝗮𝘁𝗶𝗼𝗻 𝗣𝗮𝗿𝗮𝗹𝗲𝗴𝗮𝗹", "In-House Litigation Paralegal", "Mathematical sans-serif bold"),
        ("𝗦𝗿. 𝗩𝗣 𝗼𝗳 𝗚𝗹𝗼𝗯𝗮𝗹 𝗮𝗻𝗱 𝗗𝗼𝗺𝗲𝘀𝘁𝗶𝗰 𝗦𝗮𝗹𝗲𝘀 𝗢𝗽𝗲𝗿𝗮𝘁𝗶𝗼𝗻𝘀", "Sr. VP of Global and Domestic Sales Operations", "Mathematical sans-serif bold"),
        ("🔹𝑪𝑬𝑶", "CEO", "Emoji with mathematical italic"),
        ("𝐘𝐨𝐮𝐫 𝐃𝐚𝐥𝐥𝐚𝐬,𝐓𝐞𝐱𝐚𝐬 𝐑𝐞𝐚𝐥𝐭𝐨𝐫®", "Your Dallas,Texas Realtor®", "Mathematical italic"),
        ("𝕀𝔹𝕄 𝕋𝕖𝕔𝕙𝕏𝕔𝕙𝕒𝕟𝕘𝕖 ℂ𝕠𝕞𝕞𝕦𝕟𝕚𝕥𝕪 𝕃𝕖𝕒𝕕", "IBM TechXchange Community Lead", "Mathematical bold"),
        
        # Titles needing cleaning (wrapping quotes)
        ('"Software Engineer"', "Software Engineer", "Wrapping double quotes"),
        ("'Project Manager'", "Project Manager", "Wrapping single quotes"),
        
        # Valid titles (should be preserved)
        ("Software Engineer", "Software Engineer", "Simple English title"),
        ("Project Manager", "Project Manager", "Simple English title"),
        ("백엔드 개발자", "백엔드 개발자", "Korean title"),
        ("소프트웨어 엔지니어", "소프트웨어 엔지니어", "Korean title"),
        ("프로젝트 매니저", "프로젝트 매니저", "Korean title"),
        ("ソフトウェアエンジニア", "ソフトウェアエンジニア", "Japanese title"),
        
        # Edge cases
        ("a", "a", "Single letter (if MIN_TITLE_LENGTH=1)"),
        ("123", None, "Only numbers (if ALLOW_NUMBERS_ONLY=False)"),
        ("A1", "A1", "Letter and number"),
        ("1A", "1A", "Number and letter"),
    ]
    
    print("=" * 80)
    print("Title Cleaning Test Suite")
    print("=" * 80)
    print()
    
    passed = 0
    failed = 0
    
    for input_title, expected, description in test_cases:
        result = clean_title(input_title)
        
        # Compare results
        if result == expected:
            status = "✓ PASS"
            passed += 1
        else:
            status = "✗ FAIL"
            failed += 1
        
        print(f"{status} | {description}")
        print(f"      Input:    {repr(input_title)}")
        print(f"      Expected: {repr(expected)}")
        print(f"      Got:      {repr(result)}")
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
    print("Title Validation Test")
    print("=" * 80)
    print()
    
    validation_tests = [
        ("Software Engineer", True, "Normal title"),
        ("0", False, "Single character"),
        ("000", False, "Placeholder pattern"),
        ("과장", True, "Valid Korean title"),
        ("", False, "Empty string"),
        ("   ", False, "Only whitespace"),
        ("123", False, "Only numbers"),
        ("A1", True, "Letter and number"),
    ]
    
    for title, expected_valid, description in validation_tests:
        result = is_valid_title(title)
        status = "✓" if result == expected_valid else "✗"
        print(f"{status} {description}: {repr(title)} -> {result} (expected {expected_valid})")
    
    print()


if __name__ == "__main__":
    print("Running title cleaning tests...\n")
    
    test_passed = test_title_cleaning()
    test_validation()
    
    if test_passed:
        print("\n✅ All tests passed!")
        exit(0)
    else:
        print("\n❌ Some tests failed. Please review the output above.")
        exit(1)

