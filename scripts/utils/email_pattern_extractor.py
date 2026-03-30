"""
Utility functions for extracting email patterns from contact data.

This module provides pattern extraction logic that matches the backend service.
"""


def _get_name_variations(first_name: str, last_name: str) -> dict:
    """
    Extract various name variations for email pattern matching.
    
    Args:
        first_name: Contact first name (will be lowercased)
        last_name: Contact last name (will be lowercased)
        
    Returns:
        Dictionary with name variations:
        - fn: full first name (lowercase)
        - ln: full last name (lowercase)
        - f_initial: first initial
        - l_initial: last initial
        - fi: first 2 chars of first name
        - kau: first 3 chars of first name
        - las: last 3 chars of last name
        - sahaa: last 4 chars of last name
    """
    fn = first_name.lower().strip() if first_name else ""
    ln = last_name.lower().strip() if last_name else ""
    
    f_initial = fn[0] if fn else ""
    l_initial = ln[0] if ln else ""
    
    # First name truncations (2-3 chars)
    fi = fn[:2] if len(fn) >= 2 else fn
    kau = fn[:3] if len(fn) >= 3 else fn
    
    # Last name truncations (3-4 chars)
    las = ln[:3] if len(ln) >= 3 else ln
    sahaa = ln[:4] if len(ln) >= 4 else ln
    
    variations = {
        "fn": fn,
        "ln": ln,
        "f_initial": f_initial,
        "l_initial": l_initial,
        "fi": fi,
        "ka": fi,  # Same as fi for 2 chars
        "kau": kau,
        "first_truncated": fi,
        "las": las,
        "sah": las,
        "sahaa": sahaa,
        "last_truncated": las,
    }
    return variations


def extract_pattern_from_email(
    email: str,
    first_name: str,
    last_name: str,
) -> tuple[str, str] | None:
    """
    Extract pattern format and pattern string from an email address.
    
    Args:
        email: Email address (e.g., "john.doe@example.com")
        first_name: Contact first name
        last_name: Contact last name
        
    Returns:
        Tuple of (pattern_format, pattern_string) or None if pattern cannot be determined
    """
    if not email or "@" not in email:
        return None

    local_part = email.split("@")[0].lower()

    if not first_name or not last_name:
        # If we don't have names, we can't determine the pattern
        return None

    # Get name variations
    name_vars = _get_name_variations(first_name, last_name)

    # Try to match against known patterns
    # Check Tier 1 patterns first (most common)
    patterns_to_check = [
        # first.last
        (f"{name_vars['fn']}.{name_vars['ln']}", "first.last"),
        # firstlast
        (f"{name_vars['fn']}{name_vars['ln']}", "firstlast"),
        # first
        (name_vars["fn"], "first"),
        # f.last
        (f"{name_vars['f_initial']}.{name_vars['ln']}", "f.last"),
        # flast
        (f"{name_vars['f_initial']}{name_vars['ln']}", "flast"),
        # first.l
        (f"{name_vars['fn']}.{name_vars['l_initial']}", "first.l"),
        # first_last
        (f"{name_vars['fn']}_{name_vars['ln']}", "first_last"),
        # first_l
        (f"{name_vars['fn']}_{name_vars['l_initial']}", "first_l"),
        # first-last
        (f"{name_vars['fn']}-{name_vars['ln']}", "first-last"),
        # first-l
        (f"{name_vars['fn']}-{name_vars['l_initial']}", "first-l"),
    ]

    # Check Tier 2 patterns
    patterns_to_check.extend([
        # f.l
        (f"{name_vars['f_initial']}.{name_vars['l_initial']}", "f.l"),
        # fl
        (f"{name_vars['f_initial']}{name_vars['l_initial']}", "fl"),
        # last.first
        (f"{name_vars['ln']}.{name_vars['fn']}", "last.first"),
        # lastfirst
        (f"{name_vars['ln']}{name_vars['fn']}", "lastfirst"),
        # last.f
        (f"{name_vars['ln']}.{name_vars['f_initial']}", "last.f"),
        # l.first
        (f"{name_vars['l_initial']}.{name_vars['fn']}", "l.first"),
        # l.f
        (f"{name_vars['l_initial']}.{name_vars['f_initial']}", "l.f"),
        # first.las
        (f"{name_vars['fn']}.{name_vars['las']}", "first.las"),
        # fi.last
        (f"{name_vars['fi']}.{name_vars['ln']}", "fi.last"),
        # fi.las
        (f"{name_vars['fi']}.{name_vars['las']}", "fi.las"),
    ])

    # Check if local part matches any pattern
    for pattern_string, pattern_format in patterns_to_check:
        if local_part == pattern_string:
            return (pattern_format, pattern_string)

    # If no exact match, return None
    return None

