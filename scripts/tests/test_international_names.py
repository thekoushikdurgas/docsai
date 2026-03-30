"""
Test script for international company name cleaning.

Tests the clean_company_name function with international company names
from various languages and scripts.
"""

from ..utils.cleaning import clean_company_name, is_valid_company_name


def test_international_names():
    """Test company name cleaning with international examples."""
    
    # Sample international company names from the provided list
    test_cases = [
        # Chinese (Simplified)
        ("齐默+罗德", "齐默+罗德", "Chinese with plus sign"),
        ("黑钻运动设备(珠海保税区)有限公司", "黑钻运动设备(珠海保税区)有限公司", "Chinese with parentheses"),
        ("麦克斯塑料公司", "麦克斯塑料公司", "Chinese company name"),
        ("麒麟远创软件(中国)有限公司", "麒麟远创软件(中国)有限公司", "Chinese with parentheses"),
        ("高途Gaotu (NYSE: GOTU)", "高途Gaotu (NYSE: GOTU)", "Chinese-English mixed with stock symbol"),
        ("饿了么", "饿了么", "Chinese company"),
        ("蒙牛", "蒙牛", "Chinese company"),
        
        # Chinese (Traditional)
        ("鴻海精密工業股份有限公司", "鴻海精密工業股份有限公司", "Traditional Chinese"),
        ("電通総研_DENTSU SOKEN INC.", "電通総研_DENTSU SOKEN INC.", "Japanese-Chinese-English mixed"),
        
        # Japanese
        ("黒崎播磨（株）", "黒崎播磨（株）", "Japanese with company suffix"),
        ("高広貿易（株）", "高広貿易（株）", "Japanese with parentheses"),
        ("株式会社 YAMAZEN", "株式会社 YAMAZEN", "Japanese with English"),
        ("（株）島津製作所", "（株）島津製作所", "Japanese with parentheses"),
        ("みずほ証券（株）", "みずほ証券（株）", "Japanese hiragana"),
        ("シティグループ証券（株）", "シティグループ証券（株）", "Japanese katakana"),
        ("カシオ計算機（株）", "カシオ計算機（株）", "Japanese katakana"),
        
        # Russian/Cyrillic
        ("Яндекс Лавка", "Яндекс Лавка", "Russian company"),
        ("Тинькофф", "Тинькофф", "Russian bank"),
        ("ООО \"Спортмастер\"", "ООО \"Спортмастер\"", "Russian LLC with quotes"),
        ("МегаФон", "МегаФон", "Russian telecom"),
        ("Сбер Банк (Беларусь)", "Сбер Банк (Беларусь)", "Russian with parentheses"),
        
        # Arabic
        ("وكالة الفضاء السعودية | Saudi Space Agency", "وكالة الفضاء السعودية | Saudi Space Agency", "Arabic-English mixed"),
        ("وزارة الثقافة Ministry of Culture", "وزارة الثقافة Ministry of Culture", "Arabic-English"),
        ("بنك التعمير والإسكان HD Bank", "بنك التعمير والإسكان HD Bank", "Arabic-English"),
        ("الهيئة السعودية للمراجعين والمحاسبين SOCPA", "الهيئة السعودية للمراجعين والمحاسبين SOCPA", "Arabic-English"),
        
        # Hebrew
        ("בנק ישראל Bank of Israel", "בנק ישראל Bank of Israel", "Hebrew-English"),
        ("ארקיע Arkia Israeli airlines", "ארקיע Arkia Israeli airlines", "Hebrew-English"),
        ("האקריו - HackerU", "האקריו - HackerU", "Hebrew-English with dash"),
        
        # Greek
        ("Ωκεανός Coffee Company", "Ωκεανός Coffee Company", "Greek-English"),
        ("Πολυτεχνείο Κρήτης - Technical University of Crete", "Πολυτεχνείο Κρήτης - Technical University of Crete", "Greek-English"),
        
        # Georgian
        ("სადაზღვევო კომპანია პრაიმი • Prime Insurance", "სადაზღვევო კომპანია პრაიმი • Prime Insurance", "Georgian-English"),
        ("თიბისი ფეი - TBC Pay", "თიბისი ფეი - TBC Pay", "Georgian-English"),
        
        # Mixed languages
        ("颉羿资本 Jubilee Capital Management Pte Ltd", "颉羿资本 Jubilee Capital Management Pte Ltd", "Chinese-English"),
        ("顺为资本 Shunwei Capital", "顺为资本 Shunwei Capital", "Chinese-English"),
        ("银泰集团Yintai Group", "银泰集团Yintai Group", "Chinese-English"),
        ("钛媒体TMTPOST", "钛媒体TMTPOST", "Chinese-English"),
        
        # Names with special characters that should be preserved
        ("高途Gaotu (NYSE: GOTU)", "高途Gaotu (NYSE: GOTU)", "Parentheses and colon"),
        ("電通総研_DENTSU SOKEN INC.", "電通総研_DENTSU SOKEN INC.", "Underscore"),
        ("齐默+罗德", "齐默+罗德", "Plus sign"),
        ("達盈管顧 Darwin Venture Management", "達盈管顧 Darwin Venture Management", "Traditional Chinese-English"),
        
        # Edge cases with international characters
        ("zzzz", None, "Only ASCII letters (should be valid if length OK)"),
        ("ZZZ's Collective", "ZZZ's Collective", "Apostrophe in English"),
        ("ZZZ Corporate Accommodation", "ZZZ Corporate Accommodation", "Multiple Z's"),
    ]
    
    print("=" * 80)
    print("International Company Name Cleaning Test Suite")
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
        print(f"      Expected: {repr(expected)}")
        print(f"      Got:      {repr(result)}")
        if result != expected:
            print(f"      ⚠️  MISMATCH!")
            # Check if it's a validation issue
            is_valid = is_valid_company_name(input_name)
            print(f"      Validation: {is_valid}")
        print()
    
    print("=" * 80)
    print(f"Results: {passed} passed, {failed} failed out of {len(test_cases)} tests")
    print("=" * 80)
    
    return failed == 0


if __name__ == "__main__":
    print("Running international company name cleaning tests...\n")
    
    test_passed = test_international_names()
    
    if test_passed:
        print("\n✅ All tests passed!")
        exit(0)
    else:
        print("\n❌ Some tests failed. Please review the output above.")
        exit(1)

