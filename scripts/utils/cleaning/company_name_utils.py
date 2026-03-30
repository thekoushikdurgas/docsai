"""
Company Name Cleaning and Validation Utilities

This module provides functions to clean, validate, and normalize company names.
It handles encoding issues, removes invalid patterns, and preserves legitimate
company name formats including international characters.
"""

import re
import unicodedata
from typing import Optional

# Try to import emoji library, fallback if not available
try:
    import emoji
    HAS_EMOJI = True
except ImportError:
    HAS_EMOJI = False


# Configuration constants
MIN_COMPANY_NAME_LENGTH = 2
ALLOW_SINGLE_LETTER = False
ALLOW_NUMBERS_ONLY = False
REMOVE_EMOJIS = True
FIX_ENCODING = True

# Placeholder patterns that indicate invalid names
PLACEHOLDER_PATTERNS = [
    r'^_+$',  # Only underscores
    r'^\.+$',  # Only dots
    r'^,+$',  # Only commas
    r'^\-+$',  # Only hyphens
    r'^=+$',  # Only equals
    r'^\*+$',  # Only asterisks
    r'^#+$',  # Only hash
    r'^/+$',  # Only slashes
    r'^\\+$',  # Only backslashes
    r'^\?+$',  # Only question marks
    r'^!+$',  # Only exclamation marks
    r'^~+$',  # Only tildes
]

# Patterns that indicate encoding corruption
ENCODING_CORRUPTION_PATTERNS = [
    r'^\?+$',  # Only question marks (common encoding replacement)
    r'^\uFFFD+$',  # Replacement character (U+FFFD)
    r'^\?+\s+\?+$',  # Question marks with spaces
]

# Legitimate special characters to preserve
LEGITIMATE_SPECIAL_CHARS = set([
    '&', "'", '(', ')', '-', '.', ',', '/', ':', ';', 
    '[', ']', '{', '}', '|', '\\', '`', '~', '!', '@',
    '#', '$', '%', '^', '*', '+', '=', '_', '<', '>',
    '?', '"', ' '
])


def normalize_unicode(text: str) -> str:
    """
    Normalize Unicode characters to their standard forms.
    Converts special Unicode variants (like mathematical bold, sans-serif, etc.)
    to standard ASCII/Latin characters where possible.
    
    Args:
        text: Input text with potentially special Unicode characters
        
    Returns:
        Normalized text
    """
    # First, try to decompose and recompose
    text = unicodedata.normalize('NFKC', text)
    
    # Replace common Unicode variants with ASCII equivalents
    replacements = {
        # Mathematical bold
        '𝔸': 'A', '𝔹': 'B', 'ℂ': 'C', '𝔻': 'D', '𝔼': 'E', '𝔽': 'F',
        '𝔾': 'G', 'ℍ': 'H', '𝕀': 'I', '𝕁': 'J', '𝕂': 'K', '𝕃': 'L',
        '𝕄': 'M', 'ℕ': 'N', '𝕆': 'O', 'ℙ': 'P', 'ℚ': 'Q', 'ℝ': 'R',
        '𝕊': 'S', '𝕋': 'T', '𝕌': 'U', '𝕍': 'V', '𝕎': 'W', '𝕏': 'X',
        '𝕐': 'Y', 'ℤ': 'Z',
        # Mathematical bold lowercase
        '𝕒': 'a', '𝕓': 'b', '𝕔': 'c', '𝕕': 'd', '𝕖': 'e', '𝕗': 'f',
        '𝕘': 'g', '𝕙': 'h', '𝕚': 'i', '𝕛': 'j', '𝕜': 'k', '𝕝': 'l',
        '𝕞': 'm', '𝕟': 'n', '𝕠': 'o', '𝕡': 'p', '𝕢': 'q', '𝕣': 'r',
        '𝕤': 's', '𝕥': 't', '𝕦': 'u', '𝕧': 'v', '𝕨': 'w', '𝕩': 'x',
        '𝕪': 'y', '𝕫': 'z',
        # Mathematical sans-serif bold
        '𝗔': 'A', '𝗕': 'B', '𝗖': 'C', '𝗗': 'D', '𝗘': 'E', '𝗙': 'F',
        '𝗚': 'G', '𝗛': 'H', '𝗜': 'I', '𝗝': 'J', '𝗞': 'K', '𝗟': 'L',
        '𝗠': 'M', '𝗡': 'N', '𝗢': 'O', '𝗣': 'P', '𝗤': 'Q', '𝗥': 'R',
        '𝗦': 'S', '𝗧': 'T', '𝗨': 'U', '𝗩': 'V', '𝗪': 'W', '𝗫': 'X',
        '𝗬': 'Y', '𝗭': 'Z',
        # Mathematical sans-serif bold lowercase
        '𝗮': 'a', '𝗯': 'b', '𝗰': 'c', '𝗱': 'd', '𝗲': 'e', '𝗳': 'f',
        '𝗴': 'g', '𝗵': 'h', '𝗶': 'i', '𝗷': 'j', '𝗸': 'k', '𝗹': 'l',
        '𝗺': 'm', '𝗻': 'n', '𝗼': 'o', '𝗽': 'p', '𝗾': 'q', '𝗿': 'r',
        '𝘀': 's', '𝘁': 't', '𝘂': 'u', '𝘃': 'v', '𝘄': 'w', '𝘅': 'x',
        '𝘆': 'y', '𝘇': 'z',
        # Mathematical italic
        '𝐴': 'A', '𝐵': 'B', '𝐶': 'C', '𝐷': 'D', '𝐸': 'E', '𝐹': 'F',
        '𝐺': 'G', '𝐻': 'H', '𝐼': 'I', '𝐽': 'J', '𝐾': 'K', '𝐿': 'L',
        '𝑀': 'M', '𝑁': 'N', '𝑂': 'O', '𝑃': 'P', '𝑄': 'Q', '𝑅': 'R',
        '𝑆': 'S', '𝑇': 'T', '𝑈': 'U', '𝑉': 'V', '𝑊': 'W', '𝑋': 'X',
        '𝑌': 'Y', '𝑍': 'Z',
        # Mathematical italic lowercase
        '𝑎': 'a', '𝑏': 'b', '𝑐': 'c', '𝑑': 'd', '𝑒': 'e', '𝑓': 'f',
        '𝑔': 'g', 'ℎ': 'h', '𝑖': 'i', '𝑗': 'j', '𝑘': 'k', '𝑙': 'l',
        '𝑚': 'm', '𝑛': 'n', '𝑜': 'o', '𝑝': 'p', '𝑞': 'q', '𝑟': 'r',
        '𝑠': 't', '𝑡': 't', '𝑢': 'u', '𝑣': 'v', '𝑤': 'w', '𝑥': 'x',
        '𝑦': 'y', '𝑧': 'z',
        # Fullwidth characters
        'Ａ': 'A', 'Ｂ': 'B', 'Ｃ': 'C', 'Ｄ': 'D', 'Ｅ': 'E', 'Ｆ': 'F',
        'Ｇ': 'G', 'Ｈ': 'H', 'Ｉ': 'I', 'Ｊ': 'J', 'Ｋ': 'K', 'Ｌ': 'L',
        'Ｍ': 'M', 'Ｎ': 'N', 'Ｏ': 'O', 'Ｐ': 'P', 'Ｑ': 'Q', 'Ｒ': 'R',
        'Ｓ': 'S', 'Ｔ': 'T', 'Ｕ': 'U', 'Ｖ': 'V', 'Ｗ': 'W', 'Ｘ': 'X',
        'Ｙ': 'Y', 'Ｚ': 'Z',
        'ａ': 'a', 'ｂ': 'b', 'ｃ': 'c', 'ｄ': 'd', 'ｅ': 'e', 'ｆ': 'f',
        'ｇ': 'g', 'ｈ': 'h', 'ｉ': 'i', 'ｊ': 'j', 'ｋ': 'k', 'ｌ': 'l',
        'ｍ': 'm', 'ｎ': 'n', 'ｏ': 'o', 'ｐ': 'p', 'ｑ': 'q', 'ｒ': 'r',
        'ｓ': 's', 'ｔ': 't', 'ｕ': 'u', 'ｖ': 'v', 'ｗ': 'w', 'ｘ': 'x',
        'ｙ': 'y', 'ｚ': 'z',
        # Replacement character
        '': '',  # Remove replacement characters
    }
    
    for old, new in replacements.items():
        text = text.replace(old, new)
    
    return text


def remove_emojis(text: str) -> str:
    """
    Remove emojis and emoji-like symbols from text.
    
    Args:
        text: Input text potentially containing emojis
        
    Returns:
        Text with emojis removed
    """
    # Remove emojis using the emoji library if available
    if HAS_EMOJI:
        text = emoji.replace_emoji(text, replace='')
    
    # Remove other common symbols that might be used as emojis
    symbol_patterns = [
        r'[\U0001F300-\U0001F9FF]',  # Emoticons
        r'[\U00002600-\U000027BF]',  # Miscellaneous symbols
        r'[\U0001F600-\U0001F64F]',  # Emoticons
        r'[\U0001F680-\U0001F6FF]',  # Transport and map symbols
    ]
    
    for pattern in symbol_patterns:
        text = re.sub(pattern, '', text)
    
    return text


def fix_encoding_issues(text: str) -> str:
    """
    Attempt to fix common encoding issues.
    
    Args:
        text: Input text with potential encoding issues
        
    Returns:
        Text with encoding issues fixed where possible
    """
    # Remove replacement characters
    text = text.replace('', '')
    
    # Try to decode and re-encode to fix common issues
    try:
        # If text contains only question marks (common encoding replacement)
        if re.match(r'^\?+\s*\?*$', text.strip()):
            return ''  # Likely encoding corruption, return empty
    except Exception:
        pass
    
    return text


def remove_wrapping_quotes(text: str) -> str:
    """
    Remove wrapping quotes (single or double) from text.
    Handles cases like: "Company Name", 'Company Name', "'Company Name'"
    
    Args:
        text: Input text potentially wrapped in quotes
        
    Returns:
        Text with wrapping quotes removed
    """
    text = text.strip()
    
    # Remove wrapping quotes (can be nested)
    while len(text) >= 2:
        if (text[0] == '"' and text[-1] == '"') or (text[0] == "'" and text[-1] == "'"):
            text = text[1:-1].strip()
        else:
            break
    
    return text


def normalize_whitespace(text: str) -> str:
    """
    Normalize whitespace: remove leading/trailing, collapse multiple spaces.
    
    Args:
        text: Input text with potentially irregular whitespace
        
    Returns:
        Text with normalized whitespace
    """
    # Collapse multiple spaces to single space
    text = re.sub(r'\s+', ' ', text)
    # Strip leading and trailing whitespace
    text = text.strip()
    return text


def is_placeholder_pattern(text: str) -> bool:
    """
    Check if text matches placeholder patterns (like "___", "...", etc.).
    
    Args:
        text: Text to check
        
    Returns:
        True if text matches a placeholder pattern
    """
    for pattern in PLACEHOLDER_PATTERNS:
        if re.match(pattern, text):
            return True
    return False


def has_encoding_corruption(text: str) -> bool:
    """
    Check if text shows signs of encoding corruption.
    
    Args:
        text: Text to check
        
    Returns:
        True if text appears to have encoding corruption
    """
    for pattern in ENCODING_CORRUPTION_PATTERNS:
        if re.match(pattern, text):
            return True
    
    # Check for replacement characters
    if '' in text:
        return True
    
    return False


def contains_letters(text: str) -> bool:
    """
    Check if text contains at least one letter (any language).
    
    Supports:
    - ASCII letters (a-z, A-Z)
    - Unicode letters from all scripts (Chinese, Japanese, Arabic, Hebrew, Cyrillic, etc.)
    - Treats any Unicode letter (non-control) via regex, covering major scripts.
    
    Args:
        text: Text to check
        
    Returns:
        True if text contains at least one letter from any language
    """
    # Match letters from all Unicode scripts
    # This includes: Latin, Cyrillic, Arabic, Hebrew, Chinese, Japanese, Korean, etc.
    # Pattern matches any Unicode character in the range \u0080-\uFFFF (non-ASCII)
    # plus ASCII letters a-z, A-Z
    return bool(re.search(r'[a-zA-Z\u0080-\uFFFF]', text))


def is_valid_company_name(name: Optional[str]) -> bool:
    """
    Validate if a company name is valid.
    
    Validation rules:
    - Must not be None or empty
    - Must meet minimum length requirement
    - Must contain at least one letter (unless ALLOW_NUMBERS_ONLY is True)
    - Cannot be only special characters
    - Cannot be a placeholder pattern
    - Cannot show encoding corruption
    
    Args:
        name: Company name to validate
        
    Returns:
        True if name is valid, False otherwise
    """
    if name is None:
        return False
    
    # Convert to string if not already
    if not isinstance(name, str):
        name = str(name)
    
    # Strip whitespace for validation
    name = name.strip()
    
    # Empty after stripping
    if not name:
        return False
    
    # Check minimum length
    if len(name) < MIN_COMPANY_NAME_LENGTH:
        if not ALLOW_SINGLE_LETTER or len(name) < 1:
            return False
    
    # Check for placeholder patterns
    if is_placeholder_pattern(name):
        return False
    
    # Check for encoding corruption
    if FIX_ENCODING and has_encoding_corruption(name):
        return False
    
    # Must contain at least one letter (unless numbers only is allowed)
    if not ALLOW_NUMBERS_ONLY:
        if not contains_letters(name):
            return False
    
    # Check if it's only special characters (after removing spaces)
    name_no_spaces = name.replace(' ', '')
    if name_no_spaces:
        # Count alphanumeric characters (including international characters)
        # Use Unicode letter and number categories
        alnum_count = len(re.findall(r'[a-zA-Z0-9\u0080-\uFFFF]', name_no_spaces))
        if alnum_count == 0:
            return False
    
    return True


def clean_company_name(name: Optional[str]) -> Optional[str]:
    """
    Clean and validate a company name.
    
    Cleaning steps:
    1. Handle None/empty input
    2. Convert to string
    3. Strip whitespace
    4. Remove wrapping quotes
    5. Normalize whitespace
    6. Fix encoding issues
    7. Remove emojis
    8. Normalize Unicode
    9. Validate result
    
    Args:
        name: Company name to clean
        
    Returns:
        Cleaned company name, or None if invalid
    """
    # Handle None input
    if name is None:
        return None
    
    # Convert to string if not already
    if not isinstance(name, str):
        name = str(name)
    
    # Strip whitespace
    name = name.strip()
    
    # Empty after stripping
    if not name:
        return None
    
    # Remove wrapping quotes
    name = remove_wrapping_quotes(name)
    
    # Normalize whitespace
    name = normalize_whitespace(name)
    
    # Empty after cleaning
    if not name:
        return None
    
    # Fix encoding issues
    if FIX_ENCODING:
        name = fix_encoding_issues(name)
        if not name:
            return None
    
    # Remove emojis
    if REMOVE_EMOJIS:
        name = remove_emojis(name)
        name = normalize_whitespace(name)  # Re-normalize after emoji removal
        if not name:
            return None
    
    # Normalize Unicode
    name = normalize_unicode(name)
    name = normalize_whitespace(name)  # Re-normalize after Unicode normalization
    if not name:
        return None
    
    # Validate the cleaned name
    if not is_valid_company_name(name):
        return None
    
    return name


def clean_company_name_preserve_invalid(name: Optional[str]) -> tuple[Optional[str], bool]:
    """
    Clean a company name but return it even if invalid (for analysis purposes).
    
    Args:
        name: Company name to clean
        
    Returns:
        Tuple of (cleaned_name, is_valid)
    """
    cleaned = clean_company_name(name)
    is_valid = cleaned is not None and is_valid_company_name(cleaned)
    
    # If cleaning resulted in None but original had content, return cleaned version
    if cleaned is None and name and name.strip():
        # Try to get a cleaned version even if invalid
        if isinstance(name, str):
            cleaned = normalize_whitespace(remove_wrapping_quotes(name.strip()))
            if not cleaned:
                cleaned = None
    
    return cleaned, is_valid

