"""
Title Cleaning and Validation Utilities

This module provides functions to clean, validate, and normalize contact titles.
Titles have different validation rules than company names - they can be shorter
and more varied, but should still filter out invalid patterns.
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
MIN_TITLE_LENGTH = 1  # Titles can be very short (even single word)
ALLOW_NUMBERS_ONLY = False  # Titles that are only numbers are usually invalid
REMOVE_EMOJIS = True
FIX_ENCODING = True
NORMALIZE_UNICODE = True

# Placeholder patterns that indicate invalid titles
TITLE_PLACEHOLDER_PATTERNS = [
    r'^_+$',  # Only underscores
    r'^\.+$',  # Only dots
    r'^,+$',  # Only commas
    r'^\-+$',  # Only hyphens
    r'^=+$',  # Only equals
    r'^\*+$',  # Only asterisks
    r'^#+$',  # Only hash
    r'^/+$',  # Only slashes
    r'^\\+$',  # Only backslashes
    r'^!+$',  # Only exclamation marks
    r'^~+$',  # Only tildes
    r'^0+$',  # Only zeros
    r'^00+$',  # Multiple zeros
    r'^000+$',  # Many zeros
]

# Patterns that indicate encoding corruption
TITLE_ENCODING_CORRUPTION_PATTERNS = [
    r'^\?+$',  # Only question marks (common encoding replacement)
    r'^\uFFFD+$',  # Replacement character (U+FFFD)
    r'^\?+\s+\?+$',  # Question marks with spaces
    r'^\\_\(.+\)_/',  # Escaped ASCII art patterns like "\\_(ツ)_/"
    r'^¯\\_\(.+\)_/¯',  # ASCII art patterns like "¯\\_(ツ)_/¯"
]

# ASCII art patterns that should be removed
ASCII_ART_PATTERNS = [
    r'^¯\\_\(.+\)_/¯',  # "¯\\_(ツ)_/¯"
    r'^\\_\(.+\)_/',  # "\\_(ツ)_/"
    r'^ᕕ\(.+\)ᕗ',  # "ᕕ( ᐛ )ᕗ"
    r'^∈\(.+\)∋',  # "∈(ﾟ◎ﾟ)∋✨🌏🔗"
]


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
    # (Same replacements as in company_name_utils.py)
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


def remove_ascii_art(text: str) -> str:
    """
    Remove ASCII art patterns from text.
    
    Args:
        text: Input text potentially containing ASCII art
        
    Returns:
        Text with ASCII art removed
    """
    # Check if entire text matches ASCII art patterns
    for pattern in ASCII_ART_PATTERNS:
        if re.match(pattern, text):
            return ''  # Entire text is ASCII art, remove it
    
    # If text contains ASCII art but also has other content, be more careful
    # Only remove if it's clearly just ASCII art
    if re.match(r'^[¯_\\/()ツᕕᕗ∈∋\s]+$', text):
        return ''  # Only ASCII art characters and whitespace
    
    return text


def remove_wrapping_quotes(text: str) -> str:
    """
    Remove wrapping quotes (single or double) from text.
    
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


def is_title_placeholder_pattern(text: str) -> bool:
    """
    Check if text matches placeholder patterns (like "___", "...", "000", etc.).
    
    Args:
        text: Text to check
        
    Returns:
        True if text matches a placeholder pattern
    """
    for pattern in TITLE_PLACEHOLDER_PATTERNS:
        if re.match(pattern, text):
            return True
    return False


def has_title_encoding_corruption(text: str) -> bool:
    """
    Check if text shows signs of encoding corruption.
    
    Args:
        text: Text to check
        
    Returns:
        True if text appears to have encoding corruption
    """
    if not FIX_ENCODING:
        return False
    
    for pattern in TITLE_ENCODING_CORRUPTION_PATTERNS:
        if re.match(pattern, text):
            return True
    
    # Check for replacement characters
    if '' in text:
        return True
    
    return False


def contains_letters(text: str) -> bool:
    """
    Check if text contains at least one letter (any language).
    
    Args:
        text: Text to check
        
    Returns:
        True if text contains at least one letter
    """
    # Match letters from all Unicode scripts
    return bool(re.search(r'[a-zA-Z\u0080-\uFFFF]', text))


def is_valid_title(title: Optional[str]) -> bool:
    """
    Validate if a title is valid.
    
    Validation rules:
    - Must not be None or empty
    - Must meet minimum length requirement
    - Must contain at least one letter (unless ALLOW_NUMBERS_ONLY is True)
    - Cannot be only special characters
    - Cannot be a placeholder pattern
    - Cannot show encoding corruption
    
    Args:
        title: Title to validate
        
    Returns:
        True if title is valid, False otherwise
    """
    if title is None:
        return False
    
    # Convert to string if not already
    if not isinstance(title, str):
        title = str(title)
    
    # Strip whitespace for validation
    title = title.strip()
    
    # Empty after stripping
    if not title:
        return False
    
    # Check minimum length
    if len(title) < MIN_TITLE_LENGTH:
        return False
    
    # Check for placeholder patterns
    if is_title_placeholder_pattern(title):
        return False
    
    # Check for encoding corruption
    if has_title_encoding_corruption(title):
        return False
    
    # Must contain at least one letter (unless numbers only is allowed)
    if not ALLOW_NUMBERS_ONLY:
        if not contains_letters(title):
            return False
    
    # Check if it's only special characters (after removing spaces)
    title_no_spaces = title.replace(' ', '')
    if title_no_spaces:
        # Count alphanumeric characters (including international characters)
        alnum_count = len(re.findall(r'[a-zA-Z0-9\u0080-\uFFFF]', title_no_spaces))
        if alnum_count == 0:
            return False
    
    return True


def clean_title(title: Optional[str]) -> Optional[str]:
    """
    Clean and validate a contact title.
    
    Cleaning steps:
    1. Handle None/empty input
    2. Convert to string
    3. Strip whitespace
    4. Remove wrapping quotes
    5. Remove ASCII art patterns
    6. Normalize whitespace
    7. Fix encoding issues
    8. Remove emojis
    9. Normalize Unicode
    10. Validate result
    
    Args:
        title: Title to clean
        
    Returns:
        Cleaned title, or None if invalid
    """
    # Handle None input
    if title is None:
        return None
    
    # Convert to string if not already
    if not isinstance(title, str):
        title = str(title)
    
    # Strip whitespace
    title = title.strip()
    
    # Empty after stripping
    if not title:
        return None
    
    # Remove wrapping quotes
    title = remove_wrapping_quotes(title)
    
    # Remove ASCII art patterns
    title = remove_ascii_art(title)
    title = normalize_whitespace(title)  # Re-normalize after ASCII art removal
    
    # Empty after cleaning
    if not title:
        return None
    
    # Normalize whitespace
    title = normalize_whitespace(title)
    
    # Empty after cleaning
    if not title:
        return None
    
    # Fix encoding issues - remove replacement characters
    if FIX_ENCODING:
        title = title.replace('', '')
        if not title:
            return None
    
    # Remove emojis
    if REMOVE_EMOJIS:
        title = remove_emojis(title)
        title = normalize_whitespace(title)  # Re-normalize after emoji removal
        if not title:
            return None
    
    # Normalize Unicode
    if NORMALIZE_UNICODE:
        title = normalize_unicode(title)
        title = normalize_whitespace(title)  # Re-normalize after Unicode normalization
        if not title:
            return None
    
    # Validate the cleaned title
    if not is_valid_title(title):
        return None
    
    return title

