# LinkedIn Profile Scraper

# This notebook scrapes user details from a LinkedIn profile HTML file and extracts all available information into a structured JSON format.

# Import required libraries
import json
import re
import inspect
from datetime import datetime
from bs4 import BeautifulSoup
from pathlib import Path
from typing import Dict, List, Optional, Any
from urllib.parse import urlparse, parse_qs

def clean_text(text: str) -> str:
    """Clean and normalize text content."""
    if not text:
        return ""
    if not isinstance(text, str):
        text = str(text)
    # Remove extra whitespace and newlines
    text = re.sub(r'\s+', ' ', text.strip())
    # Remove zero-width characters
    text = re.sub(r'[\u200b-\u200f\u202a-\u202e]', '', text)
    # Remove leading/trailing punctuation that might be artifacts
    text = text.strip('.,;:!?')
    return text

def safe_extract(func, *args, **kwargs):
    """Safely execute an extraction function with error handling."""
    try:
        return func(*args, **kwargs)
    except Exception as e:
        # Return empty/default value based on return type
        if isinstance(func(), list):
            return []
        elif isinstance(func(), dict):
            return {}
        else:
            return None

def validate_extracted_data(data: Any, data_type: str = 'string') -> Any:
    """Validate extracted data based on expected type."""
    if data is None:
        return None
    
    if data_type == 'string':
        if isinstance(data, str):
            cleaned = clean_text(data)
            return cleaned if cleaned else None
        return str(data) if data else None
    elif data_type == 'int':
        try:
            if isinstance(data, str):
                # Remove non-numeric characters except K, M, B
                data = re.sub(r'[^\dKMBkmb.]', '', data)
                if 'K' in data.upper() or 'k' in data:
                    return int(float(data.replace('K', '').replace('k', '')) * 1000)
                elif 'M' in data.upper() or 'm' in data:
                    return int(float(data.replace('M', '').replace('m', '')) * 1000000)
                elif 'B' in data.upper() or 'b' in data:
                    return int(float(data.replace('B', '').replace('b', '')) * 1000000000)
                return int(float(data))
            return int(data)
        except (ValueError, TypeError):
            return None
    elif data_type == 'url':
        if isinstance(data, str) and (data.startswith('http') or data.startswith('/')):
            return data.strip()
        return None
    elif data_type == 'list':
        if isinstance(data, list):
            return data
        return []
    elif data_type == 'dict':
        if isinstance(data, dict):
            return data
        return {}
    
    return data

def detect_html_format(soup: BeautifulSoup) -> str:
    """
    Detect the format of LinkedIn HTML (public profile vs logged-in profile).
    
    Returns:
        'public' for public profile format (has JSON-LD, older structure)
        'logged_in' for logged-in profile format (obfuscated classes, newer structure)
    """
    # Check for JSON-LD script tag (indicates public profile)
    json_ld_script = soup.find('script', type='application/ld+json')
    if json_ld_script:
        return 'public'
    
    # Check for obfuscated class names (indicates logged-in format)
    # Look for patterns like data-sdui-screen, componentkey, data-view-name
    if soup.find(attrs={'data-sdui-screen': True}) or \
       soup.find(attrs={'componentkey': True}) or \
       soup.find(attrs={'data-view-name': True}):
        return 'logged_in'
    
    # Check for page key meta tag
    page_key_meta = soup.find('meta', {'name': 'pageKey'})
    if page_key_meta:
        page_key = page_key_meta.get('content', '').strip()
        if 'public_profile' in page_key:
            return 'public'
    
    # Default to logged_in if we can't determine
    return 'logged_in'

def extract_dates_from_range(date_range_elem) -> Dict[str, Optional[str]]:
    """Extract start and end dates from a date-range element."""
    dates = {
        'start_date': None,
        'end_date': None,
        'duration': None,
        'current': False
    }
    
    if not date_range_elem:
        return dates
    
    # Find all time elements
    time_elements = date_range_elem.find_all('time')
    if len(time_elements) >= 1:
        dates['start_date'] = clean_text(time_elements[0].get_text())
    if len(time_elements) >= 2:
        dates['end_date'] = clean_text(time_elements[1].get_text())
    
    # Check for "Present" or "Current"
    date_text = clean_text(date_range_elem.get_text())
    if 'present' in date_text.lower() or 'current' in date_text.lower():
        dates['current'] = True
        dates['end_date'] = None
    
    # Extract duration if available
    duration_match = re.search(r'(\d+)\s*(?:years?|months?|days?)', date_text, re.I)
    if duration_match:
        dates['duration'] = clean_text(duration_match.group(0))
    
    return dates

def extract_expanded_text(container_elem) -> str:
    """Extract expanded text from show-more-less sections."""
    if not container_elem:
        return ""
    
    # Try to get the expanded text first
    expanded_elem = container_elem.find('p', class_=re.compile(r'show-more-less-text__text--more', re.I))
    if expanded_elem:
        return clean_text(expanded_elem.get_text())
    
    # Fall back to less text
    less_elem = container_elem.find('p', class_=re.compile(r'show-more-less-text__text--less', re.I))
    if less_elem:
        return clean_text(less_elem.get_text())
    
    # Fall back to any text in the container
    return clean_text(container_elem.get_text())

def extract_logo_url(card_elem) -> Optional[str]:
    """Extract logo/image URL from a profile section card."""
    if not card_elem:
        return None
    
    # Try to find image with data-delayed-url
    img = card_elem.find('img', attrs={'data-delayed-url': True})
    if img:
        return img.get('data-delayed-url', '').strip()
    
    # Try regular src
    img = card_elem.find('img')
    if img:
        return img.get('src', '').strip()
    
    return None

def extract_json_ld(soup: BeautifulSoup) -> Optional[Dict]:
    """Extract structured data from JSON-LD script tag."""
    json_ld_script = soup.find('script', type='application/ld+json')
    if json_ld_script:
        try:
            json_data = json.loads(json_ld_script.string)
            # Find the Person object in the graph
            if isinstance(json_data, dict) and '@graph' in json_data:
                for item in json_data['@graph']:
                    if item.get('@type') == 'Person':
                        return item
            elif isinstance(json_data, dict) and json_data.get('@type') == 'Person':
                return json_data
        except (json.JSONDecodeError, KeyError):
            pass
    return None

def extract_comprehensive_json_ld(soup: BeautifulSoup) -> Dict[str, Any]:
    """Extract all available data from JSON-LD comprehensively."""
    json_ld_data = {
        'person_data': None,
        'webpage_data': None,
        'all_interaction_statistics': [],
        'all_works_for': [],
        'all_alumni_of': [],
        'all_awards': [],
        'all_languages': [],
        'all_member_of': []
    }
    
    json_ld_script = soup.find('script', type='application/ld+json')
    if json_ld_script:
        try:
            json_data = json.loads(json_ld_script.string)
            
            # Handle @graph structure
            items_to_process = []
            if isinstance(json_data, dict) and '@graph' in json_data:
                items_to_process = json_data['@graph']
            elif isinstance(json_data, dict):
                items_to_process = [json_data]
            elif isinstance(json_data, list):
                items_to_process = json_data
            
            for item in items_to_process:
                if not isinstance(item, dict):
                    continue
                
                item_type = item.get('@type', '')
                
                if item_type == 'Person':
                    json_ld_data['person_data'] = item
                    
                    # Extract all interaction statistics
                    if 'interactionStatistic' in item:
                        stats = item['interactionStatistic']
                        if isinstance(stats, list):
                            json_ld_data['all_interaction_statistics'].extend(stats)
                        else:
                            json_ld_data['all_interaction_statistics'].append(stats)
                    
                    # Extract all worksFor
                    if 'worksFor' in item:
                        works = item['worksFor']
                        if isinstance(works, list):
                            json_ld_data['all_works_for'].extend(works)
                        else:
                            json_ld_data['all_works_for'].append(works)
                    
                    # Extract all alumniOf
                    if 'alumniOf' in item:
                        alumni = item['alumniOf']
                        if isinstance(alumni, list):
                            json_ld_data['all_alumni_of'].extend(alumni)
                        else:
                            json_ld_data['all_alumni_of'].append(alumni)
                    
                    # Extract all awards
                    if 'awards' in item:
                        awards = item['awards']
                        if isinstance(awards, list):
                            json_ld_data['all_awards'].extend(awards)
                        else:
                            json_ld_data['all_awards'].append(awards)
                    
                    # Extract all languages
                    if 'knowsLanguage' in item:
                        langs = item['knowsLanguage']
                        if isinstance(langs, list):
                            json_ld_data['all_languages'].extend(langs)
                        else:
                            json_ld_data['all_languages'].append(langs)
                    
                    # Extract all memberOf
                    if 'memberOf' in item:
                        members = item['memberOf']
                        if isinstance(members, list):
                            json_ld_data['all_member_of'].extend(members)
                        else:
                            json_ld_data['all_member_of'].append(members)
                
                elif item_type == 'WebPage':
                    json_ld_data['webpage_data'] = item
        
        except (json.JSONDecodeError, KeyError, TypeError) as e:
            pass
    
    return json_ld_data

def extract_profile_metadata(soup: BeautifulSoup) -> Dict[str, Any]:
    """Extract profile metadata like view count, last updated, completeness, premium status."""
    metadata = {
        'profile_view_count': None,
        'last_updated': None,
        'profile_completeness': None,
        'is_premium_member': False,
        'premium_type': None,
        'is_verified': False,
        'verification_badge': None
    }
    
    # Extract premium membership indicators (enhanced)
    premium_indicators = soup.find_all(class_=re.compile(r'premium|gold|business|sales.*navigator', re.I))
    for indicator in premium_indicators:
        indicator_text = clean_text(indicator.get_text()).lower()
        if 'premium' in indicator_text or 'gold' in indicator_text:
            metadata['is_premium_member'] = True
            if 'business' in indicator_text:
                metadata['premium_type'] = 'business'
            elif 'sales navigator' in indicator_text or 'sales.*nav' in indicator_text:
                metadata['premium_type'] = 'sales_navigator'
            elif 'gold' in indicator_text:
                metadata['premium_type'] = 'gold'
            else:
                metadata['premium_type'] = 'premium'
            break
    
    # Also check for premium indicators in data attributes
    if not metadata['is_premium_member']:
        premium_attrs = soup.find_all(attrs={'data-premium': True}) or \
                       soup.find_all(attrs={'data-view-name': re.compile(r'premium', re.I)})
        if premium_attrs:
            metadata['is_premium_member'] = True
    
    # Extract profile view count if available (enhanced)
    view_count_elem = soup.find(string=re.compile(r'profile.*view', re.I))
    if view_count_elem:
        view_match = re.search(r'(\d+[KMB]?)\s*profile.*view', str(view_count_elem), re.I)
        if view_match:
            metadata['profile_view_count'] = view_match.group(1)
    
    # Also try extracting from aria-label or data attributes
    if not metadata['profile_view_count']:
        view_elements = soup.find_all(attrs={'aria-label': re.compile(r'profile.*view', re.I)})
        for elem in view_elements:
            aria_text = elem.get('aria-label', '')
            view_match = re.search(r'(\d+[KMB]?)\s*profile.*view', aria_text, re.I)
            if view_match:
                metadata['profile_view_count'] = view_match.group(1)
                break
    
    # Extract last updated timestamp (enhanced)
    last_updated_elem = soup.find('time', attrs={'datetime': True})
    if last_updated_elem:
        metadata['last_updated'] = last_updated_elem.get('datetime', '').strip()
    else:
        # Try finding from data attributes
        updated_elem = soup.find(attrs={'data-last-updated': True}) or \
                      soup.find(attrs={'data-updated': True})
        if updated_elem:
            metadata['last_updated'] = (updated_elem.get('data-last-updated', '') or
                                        updated_elem.get('data-updated', '')).strip()
    
    # Extract profile completeness if mentioned (enhanced)
    completeness_elem = soup.find(string=re.compile(r'profile.*complete|completeness', re.I))
    if completeness_elem:
        completeness_match = re.search(r'(\d+)%', str(completeness_elem))
        if completeness_match:
            metadata['profile_completeness'] = int(completeness_match.group(1))
    
    # Extract verification status
    verification_indicators = soup.find_all(class_=re.compile(r'verified|verification|badge', re.I))
    for indicator in verification_indicators:
        indicator_text = clean_text(indicator.get_text()).lower()
        if 'verified' in indicator_text or 'checkmark' in indicator_text:
            metadata['is_verified'] = True
            metadata['verification_badge'] = clean_text(indicator.get_text())
            break
    
    # Also check for verification in aria-label
    if not metadata['is_verified']:
        verified_aria = soup.find(attrs={'aria-label': re.compile(r'verified', re.I)})
        if verified_aria:
            metadata['is_verified'] = True
            metadata['verification_badge'] = verified_aria.get('aria-label', '')
    
    return metadata

def extract_page_metadata(soup: BeautifulSoup) -> Dict[str, Any]:
    """Extract page-level metadata from meta tags and data attributes."""
    metadata = {
        'open_to_provider': None,
        'locale': None,
        'page_key': None,
        'app_deep_links': {
            'android_url': None,
            'android_package': None,
            'android_app_name': None,
            'ios_url': None,
            'ios_app_store_id': None,
            'ios_app_name': None
        },
        'page_instance_id': None,
        'member_id': None,
        'app_version': None
    }
    
    # Extract openToProvider status
    page_tag_meta = soup.find('meta', {'name': 'linkedin:pageTag'})
    if page_tag_meta:
        content = page_tag_meta.get('content', '').strip()
        if content:
            metadata['open_to_provider'] = content == 'openToProvider'
    
    # Extract locale
    locale_meta = soup.find('meta', {'name': 'locale'})
    if locale_meta:
        metadata['locale'] = locale_meta.get('content', '').strip()
    
    # Extract page key
    page_key_meta = soup.find('meta', {'name': 'pageKey'})
    if page_key_meta:
        metadata['page_key'] = page_key_meta.get('content', '').strip()
    
    # Extract app deep links
    android_url_meta = soup.find('meta', {'property': 'al:android:url'})
    if android_url_meta:
        metadata['app_deep_links']['android_url'] = android_url_meta.get('content', '').strip()
    
    android_package_meta = soup.find('meta', {'property': 'al:android:package'})
    if android_package_meta:
        metadata['app_deep_links']['android_package'] = android_package_meta.get('content', '').strip()
    
    android_app_name_meta = soup.find('meta', {'property': 'al:android:app_name'})
    if android_app_name_meta:
        metadata['app_deep_links']['android_app_name'] = android_app_name_meta.get('content', '').strip()
    
    ios_url_meta = soup.find('meta', {'property': 'al:ios:url'})
    if ios_url_meta:
        metadata['app_deep_links']['ios_url'] = ios_url_meta.get('content', '').strip()
    
    ios_app_store_meta = soup.find('meta', {'property': 'al:ios:app_store_id'})
    if ios_app_store_meta:
        metadata['app_deep_links']['ios_app_store_id'] = ios_app_store_meta.get('content', '').strip()
    
    ios_app_name_meta = soup.find('meta', {'property': 'al:ios:app_name'})
    if ios_app_name_meta:
        metadata['app_deep_links']['ios_app_name'] = ios_app_name_meta.get('content', '').strip()
    
    # Extract page instance ID and member ID from config meta tag
    config_meta = soup.find('meta', {'id': 'config'})
    if config_meta:
        page_instance = config_meta.get('data-page-instance', '')
        if page_instance:
            metadata['page_instance_id'] = page_instance
        
        member_id = config_meta.get('data-member-id', '')
        if member_id and member_id != '0':
            metadata['member_id'] = member_id
        
        app_version = config_meta.get('data-app-version', '')
        if app_version:
            metadata['app_version'] = app_version
    
    return metadata

def extract_basic_info(soup: BeautifulSoup, json_ld: Optional[Dict]) -> Dict[str, Any]:
    """Extract basic profile information."""
    info = {
        'name': None,
        'first_name': None,
        'last_name': None,
        'headline': None,
        'location': None,
        'profile_url': None,
        'profile_image_url': None,
        'cover_image_url': None,
        'connections_count': None,
        'followers_count': None,
        'description': None,
        'company_from_title': None,
        'profile_image_variants': []
    }
    
    # Detect HTML format
    html_format = detect_html_format(soup)
    
    # Extract from meta tags
    first_name_meta = soup.find('meta', property='profile:first_name')
    last_name_meta = soup.find('meta', property='profile:last_name')
    if first_name_meta:
        info['first_name'] = first_name_meta.get('content', '').strip()
    if last_name_meta:
        info['last_name'] = last_name_meta.get('content', '').strip()
    
    # Extract full name and company from title tag (format: "Name - Company | LinkedIn")
    title_tag = soup.find('title')
    if title_tag:
        title_text = title_tag.get_text()
        # Extract name from title
        name_match = re.match(r'^([^-|]+)', title_text)
        if name_match:
            info['name'] = clean_text(name_match.group(1))
        
        # Extract company from title (between "-" and "|")
        company_match = re.search(r'-\s*([^|]+)\s*\|', title_text)
        if company_match:
            info['company_from_title'] = clean_text(company_match.group(1))
    
    # Try to get name from h1 tag (old format)
    h1_tag = soup.find('h1', class_='top-card-layout__title')
    if h1_tag:
        info['name'] = clean_text(h1_tag.get_text())
    
    # Try alternative name extraction methods (new format with obfuscated classes)
    if not info['name']:
        # Try finding h1 with any class
        h1_tags = soup.find_all('h1')
        for h1 in h1_tags:
            text = clean_text(h1.get_text())
            # Skip if it's just "LinkedIn" or empty
            if text and text.lower() != 'linkedin' and len(text) > 2:
                # Check if it looks like a name (has at least 2 words or contains Chinese characters)
                if ' ' in text or any('\u4e00' <= char <= '\u9fff' for char in text):
                    info['name'] = text
                    break
    
    # Extract name from aria-label attributes (new format)
    if not info['name']:
        aria_labels = soup.find_all(attrs={'aria-label': True})
        for elem in aria_labels:
            aria_label = elem.get('aria-label', '').strip()
            # Check if aria-label looks like a name
            if aria_label and len(aria_label) > 2 and len(aria_label) < 100:
                # Filter out common non-name aria-labels
                skip_labels = ['linkedin', 'close', 'menu', 'search', 'notification', 'message', 'home', 'profile', 'settings']
                if not any(skip in aria_label.lower() for skip in skip_labels):
                    # Check if it looks like a name
                    if ' ' in aria_label or any('\u4e00' <= char <= '\u9fff' for char in aria_label):
                        info['name'] = clean_text(aria_label)
                        break
    
    # Extract name from data-view-name="profile" or similar attributes
    if not info['name']:
        profile_elements = soup.find_all(attrs={'data-view-name': re.compile(r'profile', re.I)})
        for elem in profile_elements:
            # Look for name in nearby text
            parent = elem.find_parent(['div', 'section', 'header'])
            if parent:
                # Look for text that might be a name
                text_elements = parent.find_all(['p', 'span', 'div'], string=re.compile(r'^[A-Z][a-z]+ [A-Z]', re.M))
                for text_elem in text_elements:
                    text = clean_text(text_elem.get_text())
                    if text and len(text) > 2 and len(text) < 100:
                        if ' ' in text or any('\u4e00' <= char <= '\u9fff' for char in text):
                            info['name'] = text
                            break
                if info['name']:
                    break
    
    # Extract profile URL from canonical link
    canonical = soup.find('link', rel='canonical')
    if canonical:
        info['profile_url'] = canonical.get('href', '').strip()
    
    # Try alternative URL extraction from meta tags or og:url
    if not info['profile_url']:
        og_url = soup.find('meta', property='og:url')
        if og_url:
            info['profile_url'] = og_url.get('content', '').strip()
    
    # Try extracting from any LinkedIn profile links in the page
    if not info['profile_url']:
        profile_links = soup.find_all('a', href=re.compile(r'linkedin\.com/in/[^/]+', re.I))
        for link in profile_links:
            href = link.get('href', '').strip()
            if href and '/in/' in href:
                # Clean up the URL (remove query parameters, fragments)
                url_parts = href.split('?')[0].split('#')[0]
                if url_parts.startswith('http'):
                    info['profile_url'] = url_parts
                    break
                elif url_parts.startswith('/in/'):
                    info['profile_url'] = 'https://www.linkedin.com' + url_parts
                    break
    
    # Extract profile image from og:image
    og_image = soup.find('meta', property='og:image')
    if og_image:
        info['profile_image_url'] = og_image.get('content', '').strip()
        info['profile_image_variants'].append({
            'size': 'og',
            'url': og_image.get('content', '').strip()
        })
    
    # Extract profile images with different sizes (multiple sources)
    # Method 1: From class names
    profile_images = soup.find_all('img', class_=re.compile(r'profile.*image|profile.*photo|top-card.*image|entity.*image', re.I))
    for img in profile_images:
        # Try multiple attributes for image URL
        img_url = (img.get('data-delayed-url', '') or 
                  img.get('src', '') or 
                  img.get('data-ghost-url', '') or
                  img.get('data-src', ''))
        if img_url and img_url not in [v.get('url', '') for v in info['profile_image_variants']]:
            size_match = re.search(r'shrink_(\d+)_(\d+)', img_url)
            size = 'custom'
            if size_match:
                size = f"{size_match.group(1)}x{size_match.group(2)}"
            info['profile_image_variants'].append({
                'size': size,
                'url': img_url.strip()
            })
            if not info['profile_image_url']:
                info['profile_image_url'] = img_url.strip()
    
    # Method 2: From data-view-name="image" or data-view-name="profile" (new format)
    if not info['profile_image_url']:
        image_elements = soup.find_all(attrs={'data-view-name': re.compile(r'image|profile', re.I)})
        for elem in image_elements:
            img = elem.find('img')
            if img:
                img_url = (img.get('data-delayed-url', '') or 
                          img.get('src', '') or 
                          img.get('data-ghost-url', ''))
                if img_url and img_url not in [v.get('url', '') for v in info['profile_image_variants']]:
                    info['profile_image_variants'].append({
                        'size': 'custom',
                        'url': img_url.strip()
                    })
                    if not info['profile_image_url']:
                        info['profile_image_url'] = img_url.strip()
    
    # Method 3: From componentkey references (new format)
    if not info['profile_image_url']:
        profile_cards = soup.find_all(attrs={'componentkey': re.compile(r'Topcard|profile', re.I)})
        for card in profile_cards:
            img = card.find('img')
            if img:
                img_url = (img.get('data-delayed-url', '') or 
                          img.get('src', '') or 
                          img.get('data-ghost-url', ''))
                if img_url and img_url not in [v.get('url', '') for v in info['profile_image_variants']]:
                    info['profile_image_variants'].append({
                        'size': 'custom',
                        'url': img_url.strip()
                    })
                    if not info['profile_image_url']:
                        info['profile_image_url'] = img_url.strip()
    
    # Extract cover image from multiple sources
    # Method 1: From class name
    cover_img = soup.find('img', class_='cover-img__image')
    if cover_img:
        info['cover_image_url'] = (cover_img.get('src', '').strip() or 
                                  cover_img.get('data-delayed-url', '').strip() or
                                  cover_img.get('data-ghost-url', '').strip())
    
    # Method 2: From background images (CSS background-image)
    if not info['cover_image_url']:
        # Look for elements with background-image style
        elements_with_bg = soup.find_all(attrs={'style': re.compile(r'background.*image', re.I)})
        for elem in elements_with_bg:
            style = elem.get('style', '')
            bg_match = re.search(r'background.*image.*url\(["\']?([^"\']+)["\']?\)', style, re.I)
            if bg_match:
                bg_url = bg_match.group(1).strip()
                if 'cover' in bg_url.lower() or 'background' in bg_url.lower():
                    info['cover_image_url'] = bg_url
                    break
    
    # Method 3: From cover-img class or similar
    if not info['cover_image_url']:
        cover_elements = soup.find_all(class_=re.compile(r'cover.*img|background.*image', re.I))
        for elem in cover_elements:
            img = elem.find('img')
            if img:
                img_url = (img.get('src', '') or 
                          img.get('data-delayed-url', '') or
                          img.get('data-ghost-url', ''))
                if img_url:
                    info['cover_image_url'] = img_url.strip()
                    break
    
    # Extract location from profile-info-subheader (old format)
    location_span = soup.find('div', class_='profile-info-subheader')
    if location_span:
        location_text = location_span.find('span')
        if location_text:
            info['location'] = clean_text(location_text.get_text())
    
    # Try alternative location extraction (new format with obfuscated classes)
    if not info['location']:
        # Method 1: From aria-label attributes
        location_aria = soup.find(attrs={'aria-label': re.compile(r'location|based in|lives in', re.I)})
        if location_aria:
            aria_text = location_aria.get('aria-label', '')
            location_match = re.search(r'(?:location|based in|lives in)[:\s]+(.+)', aria_text, re.I)
            if location_match:
                info['location'] = clean_text(location_match.group(1))
        
        # Method 2: From data attributes
        if not info['location']:
            location_elements = soup.find_all(attrs={'data-view-name': re.compile(r'location', re.I)})
            for elem in location_elements:
                location_text = clean_text(elem.get_text())
                if location_text and len(location_text) > 3 and len(location_text) < 100:
                    info['location'] = location_text
                    break
        
        # Method 3: From text patterns in the page
        if not info['location']:
            all_text = soup.get_text()
            # Look for patterns like "Location: ..." or "Based in ..." or "Lives in ..."
            location_patterns = [
                r'(?:location|based in|lives in|located in)[:\s]+([A-Z][^·\n|]{3,50}?)(?:\s+·|\s*\n|\s*\|)',
                r'([A-Z][a-z]+(?:\s+[A-Z][a-z]+)*,\s*[A-Z][a-z]+(?:\s+[A-Z][a-z]+)*,\s*[A-Z][a-z]+)',
                r'([A-Z][a-z]+(?:\s+[A-Z][a-z]+)*,\s*[A-Z][a-z]+)',
            ]
            for pattern in location_patterns:
                match = re.search(pattern, all_text, re.I)
                if match:
                    potential_location = clean_text(match.group(1))
                    # Filter out false positives (university names, etc.)
                    false_positive_keywords = ['university', 'college', 'school', 'institute', 'academy']
                    if (len(potential_location) > 3 and 
                        len(potential_location) < 100 and
                        not any(keyword in potential_location.lower() for keyword in false_positive_keywords)):
                        info['location'] = potential_location
                        break
    
    # Extract connections count and followers (multiple methods)
    # Method 1: From span with text
    connections_span = soup.find('span', string=re.compile(r'\d+\+?\s*connections', re.I))
    if connections_span:
        connections_text = connections_span.get_text()
        match = re.search(r'(\d+)\+?\s*connections', connections_text, re.I)
        if match:
            info['connections_count'] = match.group(1)
    
    # Method 2: From any text containing connections pattern
    if not info['connections_count']:
        all_text = soup.get_text()
        connections_match = re.search(r'(\d+)\+?\s*connections?', all_text, re.I)
        if connections_match:
            info['connections_count'] = connections_match.group(1)
    
    # Extract followers count (multiple methods)
    # Method 1: From span with text
    followers_span = soup.find('span', string=re.compile(r'\d+[KMB]?\s*followers', re.I))
    if followers_span:
        followers_text = followers_span.get_text()
        # Handle K, M, B suffixes
        match = re.search(r'(\d+(?:\.\d+)?)\s*([KMB]?)\s*followers', followers_text, re.I)
        if match:
            count = match.group(1)
            suffix = match.group(2).upper()
            if suffix == 'K':
                info['followers_count'] = int(float(count) * 1000)
            elif suffix == 'M':
                info['followers_count'] = int(float(count) * 1000000)
            elif suffix == 'B':
                info['followers_count'] = int(float(count) * 1000000000)
            else:
                info['followers_count'] = int(count)
    
    # Method 2: From any text containing followers pattern
    if not info['followers_count']:
        all_text = soup.get_text()
        followers_match = re.search(r'(\d+(?:\.\d+)?)\s*([KMB]?)\s*followers?', all_text, re.I)
        if followers_match:
            count = followers_match.group(1)
            suffix = followers_match.group(2).upper() if len(followers_match.groups()) > 1 else ''
            try:
                if suffix == 'K':
                    info['followers_count'] = int(float(count) * 1000)
                elif suffix == 'M':
                    info['followers_count'] = int(float(count) * 1000000)
                elif suffix == 'B':
                    info['followers_count'] = int(float(count) * 1000000000)
                else:
                    info['followers_count'] = int(count)
            except (ValueError, TypeError):
                pass
    
    # Extract description from meta tags
    description_meta = soup.find('meta', property='og:description')
    if description_meta:
        info['description'] = description_meta.get('content', '').strip()
    
    # Extract headline from description or JSON-LD
    if info['description']:
        # Headline is usually the first part before "·"
        parts = info['description'].split('·')
        if parts:
            info['headline'] = clean_text(parts[0])
    
    # Try alternative headline extraction (new format with obfuscated classes)
    if not info['headline']:
        # Method 1: From aria-label attributes
        headline_aria = soup.find(attrs={'aria-label': re.compile(r'headline|title|position', re.I)})
        if headline_aria:
            aria_text = headline_aria.get('aria-label', '')
            headline_match = re.search(r'(?:headline|title|position)[:\s]+(.+)', aria_text, re.I)
            if headline_match:
                potential_headline = clean_text(headline_match.group(1))
                if len(potential_headline) > 5 and len(potential_headline) < 200:
                    info['headline'] = potential_headline
        
        # Method 2: From data-view-name attributes
        if not info['headline']:
            headline_elements = soup.find_all(attrs={'data-view-name': re.compile(r'headline|title', re.I)})
            for elem in headline_elements:
                headline_text = clean_text(elem.get_text())
                if headline_text and len(headline_text) > 5 and len(headline_text) < 200:
                    info['headline'] = headline_text
                    break
        
        # Method 3: Look for headline near the name
        if not info['headline']:
            name_elem = soup.find(string=re.compile(re.escape(info['name'] if info['name'] else ''), re.I))
            if name_elem:
                # Look for text near the name that might be a headline
                parent = name_elem.find_parent(['div', 'section', 'header'])
                if parent:
                    # Look for text that comes after the name
                    parent_text = parent.get_text()
                    # Try to extract text between name and first separator
                    if info['name']:
                        name_escaped = re.escape(info['name'])
                        headline_match = re.search(name_escaped + r'\s*[·|]\s*([^·|]+)', parent_text)
                        if headline_match:
                            potential_headline = clean_text(headline_match.group(1))
                            if len(potential_headline) > 5 and len(potential_headline) < 200:
                                info['headline'] = potential_headline
        
        # Method 4: From componentkey references (new format)
        if not info['headline']:
            profile_cards = soup.find_all(attrs={'componentkey': re.compile(r'Topcard|profile', re.I)})
            for card in profile_cards:
                # Look for text that might be a headline (usually in p tags after name)
                text_elements = card.find_all(['p', 'span', 'div'])
                for text_elem in text_elements:
                    text = clean_text(text_elem.get_text())
                    # Headlines are usually medium length and contain professional terms
                    if (text and len(text) > 10 and len(text) < 200 and
                        not any(word in text.lower() for word in ['linkedin', 'profile', 'view', 'connect', 'message'])):
                        # Check if it looks like a headline (contains professional keywords)
                        headline_keywords = ['at', 'manager', 'director', 'engineer', 'developer', 'specialist', 'expert', 'founder', 'ceo', 'cto']
                        if any(keyword in text.lower() for keyword in headline_keywords):
                            info['headline'] = text
                            break
                if info['headline']:
                    break
        
        # Method 5: General text patterns
        if not info['headline']:
            all_text = soup.get_text()
            headline_patterns = [
                r'(?:title|headline|position|role)[:\s]+([^·\n|]{10,150})',
                r'([A-Z][^·\n|]{10,150}?)\s+at\s+[A-Z]',  # "Title at Company"
            ]
            for pattern in headline_patterns:
                match = re.search(pattern, all_text, re.I)
                if match:
                    potential_headline = clean_text(match.group(1))
                    # Filter out false positives
                    if (len(potential_headline) > 10 and 
                        len(potential_headline) < 200 and
                        not any(word in potential_headline.lower() for word in ['linkedin', 'profile', 'view', 'connect'])):
                        info['headline'] = potential_headline
                        break
    
    # Extract from JSON-LD if available
    if json_ld:
        if not info['name'] and json_ld.get('name'):
            info['name'] = json_ld['name']
        if not info['description'] and json_ld.get('description'):
            info['description'] = json_ld['description']
        if json_ld.get('image') and isinstance(json_ld['image'], dict):
            if not info['profile_image_url']:
                info['profile_image_url'] = json_ld['image'].get('contentUrl', '')
        if json_ld.get('address') and isinstance(json_ld['address'], dict):
            if not info['location']:
                addr = json_ld['address']
                location_parts = []
                if addr.get('addressLocality'):
                    location_parts.append(addr['addressLocality'])
                if addr.get('addressRegion'):
                    location_parts.append(addr['addressRegion'])
                if addr.get('addressCountry'):
                    location_parts.append(addr['addressCountry'])
                if location_parts:
                    info['location'] = ', '.join(location_parts)
        if json_ld.get('interactionStatistic'):
            stat = json_ld['interactionStatistic']
            if stat.get('name') == 'Follows':
                info['followers_count'] = stat.get('userInteractionCount')
        # Extract job titles from JSON-LD (may be redacted)
        if json_ld.get('jobTitle'):
            job_titles = json_ld['jobTitle']
            if isinstance(job_titles, list) and job_titles:
                # Try to find non-redacted titles
                for title in job_titles:
                    if title and not re.match(r'^\*+$', str(title)):
                        if not info['headline']:
                            info['headline'] = str(title)
                        break
    
    return info

def extract_experience_from_text(soup: BeautifulSoup) -> List[Dict[str, Any]]:
    """Fallback method to extract experience from text patterns when structured HTML fails."""
    experience_list = []
    experience_dict = {}
    
    # Look for structured experience sections first using data attributes
    experience_sections = soup.find_all('div', attrs={'data-view-name': re.compile(r'experience', re.I)}) or \
                         soup.find_all('div', attrs={'componentkey': re.compile(r'experience', re.I)})
    
    for section in experience_sections:
        # Look for company names in links
        company_links = section.find_all('a', href=re.compile(r'/company/'))
        for link in company_links:
            company_name = clean_text(link.get_text())
            if company_name and company_name not in experience_dict and len(company_name) > 2 and len(company_name) < 100:
                # Try to find the parent container for this experience
                card = link.find_parent('div', class_=re.compile(r'card|item|section', re.I))
                if not card:
                    card = link.find_parent(['div', 'li', 'article'])
                
                exp = {
                    'company': company_name,
                    'company_url': link.get('href', '').strip(),
                    'location': None,
                    'title': None,
                    'description': None,
                    'start_date': None,
                    'end_date': None,
                    'duration': None,
                    'current': False,
                    'logo_url': None,
                    'employment_type': None,
                    'industry': None,
                    'company_size': None,
                    'team_size': None
                }
                
                if card:
                    # Try to extract title (look for text that might be a job title)
                    # Job titles are usually near company names
                    card_text = card.get_text()
                    # Look for patterns like "Title at Company" or "Title, Company"
                    title_patterns = [
                        r'([A-Z][^·\n|]+?)\s+at\s+' + re.escape(company_name),
                        r'([A-Z][^·\n|]+?),\s*' + re.escape(company_name),
                    ]
                    for pattern in title_patterns:
                        match = re.search(pattern, card_text, re.I)
                        if match:
                            exp['title'] = clean_text(match.group(1))
                            break
                    
                    # Extract dates
                    date_match = re.search(r'(\d{4}|\w+\s+\d{4})\s*[-–—]\s*(\d{4}|\w+\s+\d{4}|present|current)', card_text, re.I)
                    if date_match:
                        exp['start_date'] = clean_text(date_match.group(1))
                        end_date = clean_text(date_match.group(2))
                        if end_date.lower() in ['present', 'current']:
                            exp['current'] = True
                        else:
                            exp['end_date'] = end_date
                
                experience_dict[company_name] = exp
    
    # If still no experience found, try very conservative text patterns
    if not experience_dict:
        all_text = soup.get_text()
        # Very specific pattern: "at Company Name" where Company Name looks legitimate
        company_pattern = r'at\s+([A-Z][A-Za-z\s&]+(?:Technologies|Inc|LLC|Corp|Ltd|Company|Group|Systems|Solutions|Technologies 美國新港科技))'
        matches = re.finditer(company_pattern, all_text)
        for match in matches:
            company_name = clean_text(match.group(1))
            # Filter out obvious false positives
            if (company_name and 
                company_name not in experience_dict and 
                len(company_name) > 3 and 
                len(company_name) < 80 and
                not any(word in company_name.lower() for word in ['discussing', 'referring', 'message', 'follow'])):
                experience_dict[company_name] = {
                    'company': company_name,
                    'company_url': None,
                    'location': None,
                    'title': None,
                    'description': None,
                    'start_date': None,
                    'end_date': None,
                    'duration': None,
                    'current': False,
                    'logo_url': None,
                    'employment_type': None,
                    'industry': None,
                    'company_size': None,
                    'team_size': None
                }
    
    experience_list = list(experience_dict.values())
    return experience_list

def extract_experience(json_ld: Optional[Dict], soup: BeautifulSoup) -> List[Dict[str, Any]]:
    """Extract work experience information."""
    experience_list = []
    experience_dict = {}
    
    # Extract from JSON-LD first
    if json_ld and 'worksFor' in json_ld:
        for work in json_ld['worksFor']:
            if isinstance(work, dict):
                company_name = work.get('name', '')
                if company_name and not re.match(r'^\*+$', company_name):
                    exp = {
                        'company': company_name,
                        'company_url': work.get('url', ''),
                        'location': work.get('location', ''),
                        'title': None,
                        'description': None,
                        'start_date': None,
                        'end_date': None,
                        'duration': None,
                        'current': False,
                        'logo_url': None,
                        'employment_type': None,
                        'industry': None,
                        'company_size': None,
                        'team_size': None
                    }
                    
                    # Extract role description
                    if 'member' in work and isinstance(work['member'], dict):
                        exp['description'] = work['member'].get('description', '')
                    
                    experience_dict[company_name] = exp
    
    # Extract from HTML (even if blurred, we can get company names and dates)
    experience_section = soup.find('section', class_=re.compile(r'experience', re.I))
    if not experience_section:
        experience_section = soup.find('div', class_=re.compile(r'experience-education', re.I))
    
    # Try alternative selectors for new format (data attributes, component keys, etc.)
    if not experience_section:
        # Look for sections with data attributes
        experience_section = (soup.find('section', {'data-section': 'experience'}) or 
                           soup.find('div', {'data-section': 'experience'}) or 
                           soup.find('div', attrs={'data-view-name': re.compile(r'experience', re.I)}) or 
                           soup.find('div', attrs={'componentkey': re.compile(r'experience', re.I)}) or
                           soup.find('div', attrs={'data-sdui-component': re.compile(r'experience', re.I)}))
    
    # Also try finding experience cards by componentkey pattern
    if not experience_section:
        experience_cards = soup.find_all(attrs={'componentkey': re.compile(r'experience|position|work', re.I)})
        if experience_cards:
            # Create a virtual section from these cards
            experience_section = soup.new_tag('div')
            for card in experience_cards:
                experience_section.append(card)
    
    if experience_section:
        # Try visible list first
        visible_list = experience_section.find('ul', class_='visible-list')
        if visible_list:
            profile_cards = visible_list.find_all('li', class_='profile-section-card')
        else:
            profile_cards = experience_section.find_all('li', class_='profile-section-card')
        
        # Also check blurred list for additional data
        blurred_list = experience_section.find('ul', class_='blurred-list')
        if blurred_list:
            blurred_cards = blurred_list.find_all('li', class_='profile-section-card')
            profile_cards.extend(blurred_cards)
        
        for card in profile_cards:
            company_elem = card.find('h3')
            company_name = None
            
            if company_elem:
                company_name = clean_text(company_elem.get_text())
            
            # Try alternative company name extraction (new format)
            if not company_name or re.match(r'^\*+$', company_name):
                # Check for company name in links or other attributes
                company_link = card.find('a', href=re.compile(r'/company/'))
                if company_link:
                    company_name = clean_text(company_link.get_text())
            
            # Try finding company name in any text that looks like a company
            if not company_name or re.match(r'^\*+$', company_name):
                # Look for text patterns that might indicate a company name
                card_text = card.get_text()
                # Try to find company names in various formats
                # Look for patterns like "Company Name" or "at Company Name"
                company_patterns = [
                    r'at\s+([A-Z][^·\n|]+?)(?:\s+·|\s*\n|\s*\|)',
                    r'([A-Z][A-Za-z\s&]+(?:Technologies|Technologies|Inc|LLC|Corp|Ltd|Company))',
                ]
                for pattern in company_patterns:
                    match = re.search(pattern, card_text)
                    if match:
                        potential_company = clean_text(match.group(1))
                        if len(potential_company) > 2 and len(potential_company) < 100:
                            company_name = potential_company
                            break
            
            if not company_name or re.match(r'^\*+$', company_name):
                continue
                
                # Get or create experience entry
                if company_name not in experience_dict:
                    experience_dict[company_name] = {
                        'company': company_name,
                        'company_url': None,
                        'location': None,
                        'title': None,
                        'description': None,
                        'start_date': None,
                        'end_date': None,
                        'duration': None,
                        'current': False,
                        'logo_url': None,
                        'employment_type': None,
                        'industry': None,
                        'company_size': None,
                        'team_size': None
                    }
                
                exp = experience_dict[company_name]
                
                # Extract title (h4) - try to get visible parts even if blurred
                title_elem = card.find('h4')
                if title_elem:
                    # Check for non-blurred text first
                    title_p = title_elem.find('p', class_=re.compile(r'blur', re.I))
                    if not title_p:
                        title_text = clean_text(title_elem.get_text())
                        # Skip if it's all asterisks
                        if title_text and not re.match(r'^\*+$', title_text):
                            exp['title'] = title_text
                
                # Extract logo
                if not exp['logo_url']:
                    exp['logo_url'] = extract_logo_url(card)
                
                # Extract dates with better parsing
                date_range = card.find('span', class_='date-range')
                if date_range:
                    dates = extract_dates_from_range(date_range)
                    if dates['start_date']:
                        exp['start_date'] = dates['start_date']
                    if dates['end_date']:
                        exp['end_date'] = dates['end_date']
                    if dates['duration']:
                        exp['duration'] = dates['duration']
                    exp['current'] = dates['current']
                else:
                    # Try alternative date formats
                    date_text_elem = card.find(string=re.compile(r'\d{4}|\w+\s+\d{4}|present|current', re.I))
                    if date_text_elem:
                        date_text = clean_text(date_text_elem)
                        # Try to parse date ranges
                        date_match = re.search(r'(\w+\s+\d{4}|\d{4})\s*[-–—]\s*(\w+\s+\d{4}|\d{4}|present|current)', date_text, re.I)
                        if date_match:
                            exp['start_date'] = clean_text(date_match.group(1))
                            end_date = clean_text(date_match.group(2))
                            if end_date.lower() in ['present', 'current']:
                                exp['current'] = True
                            else:
                                exp['end_date'] = end_date
                
                # Extract location
                location_elem = card.find('div', class_=re.compile(r'text-color-text-low-emphasis', re.I))
                if location_elem:
                    location_text = clean_text(location_elem.get_text())
                    # Check if it looks like a location (not a date or description)
                    if location_text and 'time' not in location_text.lower() and len(location_text) < 200:
                        if not exp['location']:
                            exp['location'] = location_text
                
                # Extract description
                show_more_container = card.find('div', class_='show-more-less-text')
                if show_more_container:
                    exp['description'] = extract_expanded_text(show_more_container)
                
                # Extract company URL from link
                company_link = card.find('a', href=re.compile(r'/company/'))
                if company_link:
                    href = company_link.get('href', '').strip()
                    if href:
                        exp['company_url'] = href
                
                # Extract employment type (full-time, part-time, contract, etc.)
                card_text = clean_text(card.get_text())
                employment_types = ['full-time', 'part-time', 'contract', 'freelance', 'internship', 'temporary', 'self-employed']
                for emp_type in employment_types:
                    if emp_type.lower() in card_text.lower():
                        exp['employment_type'] = emp_type
                        break
                
                # Also check for employment type in aria-labels or data attributes
                if not exp['employment_type']:
                    emp_type_elem = card.find(attrs={'aria-label': re.compile(r'full.time|part.time|contract|freelance', re.I)})
                    if emp_type_elem:
                        aria_text = emp_type_elem.get('aria-label', '').lower()
                        for emp_type in employment_types:
                            if emp_type.replace('-', ' ') in aria_text:
                                exp['employment_type'] = emp_type
                                break
                
                # Extract industry/sector if mentioned
                industry_keywords = ['industry', 'sector', 'field']
                for keyword in industry_keywords:
                    if keyword in card_text.lower():
                        # Try to extract industry name
                        industry_match = re.search(rf'{keyword}[:\s]+([^,\n]+)', card_text, re.I)
                        if industry_match:
                            exp['industry'] = clean_text(industry_match.group(1))
                            break
                
                # Extract company/team size if mentioned
                size_match = re.search(r'(?:company|team|organization).*?size[:\s]+([^,\n]+)', card_text, re.I)
                if size_match:
                    size_text = clean_text(size_match.group(1))
                    if 'team' in card_text.lower():
                        exp['team_size'] = size_text
                    else:
                        exp['company_size'] = size_text
                
                # Extract team size from patterns like "Team of X" or "Managed team of X"
                if not exp['team_size']:
                    team_size_match = re.search(r'(?:team|managed|leading).*?(?:of|size)[:\s]+(\d+)', card_text, re.I)
                    if team_size_match:
                        exp['team_size'] = team_size_match.group(1)
                
                # Extract company size from patterns
                if not exp['company_size']:
                    company_size_patterns = [
                        r'company.*?size[:\s]+([^,\n]+)',
                        r'organization.*?size[:\s]+([^,\n]+)',
                        r'(\d+[KMB]?)\s*(?:employees?|staff|people)',
                    ]
                    for pattern in company_size_patterns:
                        size_match = re.search(pattern, card_text, re.I)
                        if size_match:
                            exp['company_size'] = clean_text(size_match.group(1))
                            break
    
    experience_list = list(experience_dict.values())
    
    # If no experience found with structured methods, try text-based extraction
    if not experience_list:
        experience_list = extract_experience_from_text(soup)
    
    return experience_list

def extract_education(json_ld: Optional[Dict], soup: BeautifulSoup) -> List[Dict[str, Any]]:
    """Extract education information."""
    education_list = []
    education_dict = {}
    
    # Extract from JSON-LD first
    if json_ld:
        # Check for alumniOf
        if 'alumniOf' in json_ld:
            for edu in json_ld['alumniOf']:
                if isinstance(edu, dict):
                    school_name = edu.get('name', '')
                    if school_name and not re.match(r'^\*+$', school_name):
                        edu_info = {
                            'school': school_name,
                            'school_url': edu.get('url', ''),
                            'degree': None,
                            'field_of_study': None,
                            'start_date': None,
                            'end_date': None,
                            'duration': None,
                            'description': None,
                            'logo_url': None,
                            'gpa': None,
                            'activities': [],
                            'honors': []
                        }
                        education_dict[school_name] = edu_info
    
    # Try to extract from HTML
    experience_education_section = soup.find('section', class_=re.compile(r'experience-education', re.I))
    
    # Try alternative selectors for new format
    if not experience_education_section:
        experience_education_section = (soup.find('section', {'data-section': 'education'}) or
                                      soup.find('div', {'data-section': 'education'}) or
                                      soup.find('div', attrs={'data-view-name': re.compile(r'education', re.I)}) or
                                      soup.find('div', attrs={'componentkey': re.compile(r'education', re.I)}))
    
    if experience_education_section:
        # Look for education items in the experience-education section
        profile_cards = experience_education_section.find_all('li', class_='profile-section-card')
        
        # Also try finding cards with obfuscated classes
        if not profile_cards:
            profile_cards = experience_education_section.find_all('li', class_=re.compile(r'card|item', re.I))
        
        # Also try finding by componentkey
        if not profile_cards:
            profile_cards = experience_education_section.find_all(attrs={'componentkey': re.compile(r'education|school|university', re.I)})
        
        for card in profile_cards:
            school_elem = card.find('h3')
            if school_elem:
                school_name = clean_text(school_elem.get_text())
                # Skip redacted names
                if not school_name or re.match(r'^\*+$', school_name):
                    continue
                
                # Get or create education entry
                if school_name not in education_dict:
                    education_dict[school_name] = {
                        'school': school_name,
                        'school_url': None,
                        'degree': None,
                        'field_of_study': None,
                        'start_date': None,
                        'end_date': None,
                        'duration': None,
                        'description': None,
                        'logo_url': None,
                        'gpa': None,
                        'activities': [],
                        'honors': []
                    }
                
                edu = education_dict[school_name]
                
                # Extract degree/field (h4) with better parsing
                degree_elem = card.find('h4')
                if degree_elem:
                    degree_text = clean_text(degree_elem.get_text())
                    # Skip if it's all asterisks
                    if degree_text and not re.match(r'^\*+$', degree_text):
                        # Try to parse degree and field of study
                        # Format might be "Degree, Field of Study" or "Degree in Field" or just "Degree"
                        if ',' in degree_text:
                            parts = [p.strip() for p in degree_text.split(',')]
                            edu['degree'] = parts[0]
                            if len(parts) > 1:
                                edu['field_of_study'] = parts[1]
                        elif ' in ' in degree_text.lower():
                            parts = degree_text.lower().split(' in ', 1)
                            edu['degree'] = clean_text(parts[0])
                            if len(parts) > 1:
                                edu['field_of_study'] = clean_text(parts[1])
                        else:
                            edu['degree'] = degree_text
                
                # Extract logo
                if not edu['logo_url']:
                    edu['logo_url'] = extract_logo_url(card)
                
                # Extract dates
                date_range = card.find('span', class_='date-range')
                if date_range:
                    dates = extract_dates_from_range(date_range)
                    if dates['start_date']:
                        edu['start_date'] = dates['start_date']
                    if dates['end_date']:
                        edu['end_date'] = dates['end_date']
                    if dates['duration']:
                        edu['duration'] = dates['duration']
                
                # Extract description
                show_more_container = card.find('div', class_='show-more-less-text')
                if show_more_container:
                    edu['description'] = extract_expanded_text(show_more_container)
                
                # Extract school URL from link
                school_link = card.find('a', href=re.compile(r'/school/'))
                if school_link:
                    edu['school_url'] = school_link.get('href', '').strip()
                
                # Extract GPA if mentioned (multiple patterns)
                card_text = clean_text(card.get_text())
                gpa_patterns = [
                    r'GPA[:\s]+([0-9.]+(?:\s*/\s*[0-9.]+)?)',
                    r'Grade[:\s]+Point[:\s]+Average[:\s]+([0-9.]+)',
                    r'([0-9.]+)\s*GPA',
                    r'GPA[:\s]*([0-9.]+)\s*(?:out of|/)\s*([0-9.]+)',
                ]
                for pattern in gpa_patterns:
                    gpa_match = re.search(pattern, card_text, re.I)
                    if gpa_match:
                        if len(gpa_match.groups()) > 1:
                            edu['gpa'] = f"{gpa_match.group(1)}/{gpa_match.group(2)}"
                        else:
                            edu['gpa'] = clean_text(gpa_match.group(1))
                        break
                
                # Extract activities and societies (enhanced)
                activities = []
                activities_keywords = ['activities', 'societies', 'clubs', 'organizations', 'extracurricular']
                for keyword in activities_keywords:
                    if keyword in card_text.lower():
                        # Try to extract activity names (multiple formats)
                        activity_patterns = [
                            rf'{keyword}[:\s]+([^,\n.]+)',
                            rf'{keyword}[:\s]+([^,\n.]+?)(?:\s+and\s+([^,\n.]+))?',
                        ]
                        for pattern in activity_patterns:
                            activity_matches = re.findall(pattern, card_text, re.I)
                            for match in activity_matches:
                                if isinstance(match, tuple):
                                    activities.extend([clean_text(a) for a in match if a])
                                else:
                                    activities.append(clean_text(match))
                
                # Also extract from structured lists
                activity_list = card.find_all('li', class_=re.compile(r'activity|society|club', re.I))
                for activity_item in activity_list:
                    activity_text = clean_text(activity_item.get_text())
                    if activity_text and activity_text not in activities:
                        activities.append(activity_text)
                
                if activities:
                    edu['activities'] = list(set(activities))  # Remove duplicates
                
                # Extract honors/achievements (enhanced)
                honors = []
                honors_keywords = ['honors', 'honor', 'achievement', 'award', 'dean\'s list', 'summa cum laude', 'magna cum laude', 'cum laude', 'distinction', 'merit']
                for keyword in honors_keywords:
                    if keyword in card_text.lower():
                        # Try to extract honor names (multiple formats)
                        honor_patterns = [
                            rf'{keyword}[:\s]+([^,\n.]+)',
                            rf'{keyword}[:\s]+([^,\n.]+?)(?:\s+and\s+([^,\n.]+))?',
                        ]
                        for pattern in honor_patterns:
                            honor_matches = re.findall(pattern, card_text, re.I)
                            for match in honor_matches:
                                if isinstance(match, tuple):
                                    honors.extend([clean_text(h) for h in match if h])
                                else:
                                    honors.append(clean_text(match))
                
                # Also extract from structured lists
                honor_list = card.find_all('li', class_=re.compile(r'honor|award|achievement', re.I))
                for honor_item in honor_list:
                    honor_text = clean_text(honor_item.get_text())
                    if honor_text and honor_text not in honors:
                        honors.append(honor_text)
                
                if honors:
                    edu['honors'] = list(set(honors))  # Remove duplicates
    
    # Extract from meta description (basic info) as fallback
    description_meta = soup.find('meta', property='og:description')
    if description_meta:
        desc = description_meta.get('content', '')
        # Look for "Education: School Name" pattern
        edu_match = re.search(r'Education:\s*([^·]+)', desc)
        if edu_match:
            school_name = clean_text(edu_match.group(1))
            if school_name and school_name not in education_dict:
                education_dict[school_name] = {
                    'school': school_name,
                    'school_url': None,
                    'degree': None,
                    'field_of_study': None,
                    'start_date': None,
                    'end_date': None,
                    'duration': None,
                    'description': None,
                    'logo_url': None,
                    'gpa': None,
                    'activities': [],
                    'honors': []
                }
    
    education_list = list(education_dict.values())
    return education_list

def extract_volunteer_experience(soup: BeautifulSoup) -> List[Dict[str, Any]]:
    """Extract volunteer experience information."""
    volunteer_list = []
    volunteer_section = soup.find('section', {'data-section': 'volunteering'})
    
    if volunteer_section:
        volunteer_items = volunteer_section.find_all('li', class_='profile-section-card')
        for item in volunteer_items:
            volunteer = {
                'organization': None,
                'organization_url': None,
                'role': None,
                'start_date': None,
                'end_date': None,
                'duration': None,
                'current': False,
                'cause': None,
                'description': None,
                'logo_url': None
            }
            
            # Extract role (h3)
            role_elem = item.find('h3')
            if role_elem:
                volunteer['role'] = clean_text(role_elem.get_text())
            
            # Extract organization (h4 with link)
            org_elem = item.find('h4')
            if org_elem:
                org_link = org_elem.find('a')
                if org_link:
                    volunteer['organization'] = clean_text(org_link.get_text())
                    volunteer['organization_url'] = org_link.get('href', '').strip()
                else:
                    volunteer['organization'] = clean_text(org_elem.get_text())
            
            # Extract logo
            volunteer['logo_url'] = extract_logo_url(item)
            
            # Extract dates
            date_range = item.find('span', class_='date-range')
            if date_range:
                dates = extract_dates_from_range(date_range)
                volunteer['start_date'] = dates['start_date']
                volunteer['end_date'] = dates['end_date']
                volunteer['duration'] = dates['duration']
                volunteer['current'] = dates['current']
            
            # Extract cause/category
            cause_elem = item.find('p', class_=re.compile(r'line-height', re.I))
            if cause_elem and 'text-md' in cause_elem.get('class', []):
                volunteer['cause'] = clean_text(cause_elem.get_text())
            
            # Extract description
            show_more_container = item.find('div', class_='show-more-less-text')
            if show_more_container:
                volunteer['description'] = extract_expanded_text(show_more_container)
            
            if volunteer['organization'] or volunteer['role']:
                volunteer_list.append(volunteer)
    
    return volunteer_list

def extract_awards(json_ld: Optional[Dict], soup: BeautifulSoup) -> List[Dict[str, Any]]:
    """Extract awards and honors from both JSON-LD and HTML."""
    awards = []
    awards_dict = {}
    
    # Extract from JSON-LD first
    if json_ld and 'awards' in json_ld:
        for award in json_ld['awards']:
            if award:
                award_str = str(award)
                awards_dict[award_str] = {
                    'name': award_str,
                    'issuer': None,
                    'date': None,
                    'description': None
                }
    
    # Extract from HTML
    awards_section = soup.find('section', {'data-section': 'honors-and-awards'})
    if awards_section:
        award_items = awards_section.find_all('li', class_='profile-section-card')
        for item in award_items:
            award = {
                'name': None,
                'issuer': None,
                'date': None,
                'description': None
            }
            
            # Extract award name (h3)
            name_elem = item.find('h3')
            if name_elem:
                award['name'] = clean_text(name_elem.get_text())
            
            # Extract issuer (h4)
            issuer_elem = item.find('h4')
            if issuer_elem:
                issuer_text = clean_text(issuer_elem.get_text())
                if issuer_text and issuer_text != '-':
                    award['issuer'] = issuer_text
            
            # Extract date
            date_range = item.find('span', class_='date-range')
            if date_range:
                time_elem = date_range.find('time')
                if time_elem:
                    award['date'] = clean_text(time_elem.get_text())
            
            if award['name']:
                # Merge with JSON-LD data if exists
                if award['name'] in awards_dict:
                    awards_dict[award['name']].update(award)
                else:
                    awards_dict[award['name']] = award
    
    # Convert dict to list
    awards = list(awards_dict.values())
    
    # If we only have simple strings from JSON-LD, convert them
    if not awards and json_ld and 'awards' in json_ld:
        awards = [{'name': str(a), 'issuer': None, 'date': None, 'description': None} 
                  for a in json_ld['awards'] if a]
    
    return awards

def extract_skills(soup: BeautifulSoup) -> List[Dict[str, Any]]:
    """Extract skills information."""
    skills = []
    skills_section = soup.find('section', {'data-section': 'skills'}) or \
                    soup.find('section', {'id': 'skills-section'}) or \
                    soup.find('div', class_=re.compile(r'skill', re.I))
    
    # Try alternative selectors for new format
    if not skills_section:
        skills_section = (soup.find('div', attrs={'data-view-name': re.compile(r'skill', re.I)}) or
                         soup.find('div', attrs={'componentkey': re.compile(r'skill', re.I)}) or
                         soup.find('div', attrs={'data-sdui-component': re.compile(r'skill', re.I)}))
    
    if skills_section:
        skill_items = skills_section.find_all('li', class_='profile-section-card') or \
                      skills_section.find_all('span', class_=re.compile(r'skill', re.I))
        
        # Also try finding skills with obfuscated classes
        if not skill_items:
            skill_items = skills_section.find_all('li', class_=re.compile(r'card|item', re.I))
        
        # Also try finding by componentkey
        if not skill_items:
            skill_items = skills_section.find_all(attrs={'componentkey': re.compile(r'skill', re.I)})
        
        for item in skill_items:
            skill = {
                'name': None,
                'endorsement_count': None,
                'category': None,
                'endorsers': [],
                'skill_url': None
            }
            
            # Try to extract skill name
            name_elem = item.find('span') or item.find('a')
            if name_elem:
                skill['name'] = clean_text(name_elem.get_text())
                # Extract skill URL if it's a link
                if name_elem.name == 'a':
                    skill['skill_url'] = name_elem.get('href', '').strip()
            
            # If no name found, try getting text directly
            if not skill['name']:
                skill['name'] = clean_text(item.get_text())
            
            # Extract endorsement count if available (multiple methods)
            # Method 1: From span with endorsement class
            endorsement_elem = item.find('span', class_=re.compile(r'endorsement', re.I))
            if endorsement_elem:
                endorsement_text = clean_text(endorsement_elem.get_text())
                count_match = re.search(r'(\d+)', endorsement_text)
                if count_match:
                    skill['endorsement_count'] = int(count_match.group(1))
            
            # Method 2: From aria-label
            if not skill['endorsement_count']:
                endorsement_aria = item.find(attrs={'aria-label': re.compile(r'endorsement|endorsed', re.I)})
                if endorsement_aria:
                    aria_text = endorsement_aria.get('aria-label', '')
                    count_match = re.search(r'(\d+)', aria_text)
                    if count_match:
                        skill['endorsement_count'] = int(count_match.group(1))
            
            # Method 3: From text patterns
            if not skill['endorsement_count']:
                item_text = clean_text(item.get_text())
                endorsement_patterns = [
                    r'(\d+)\s*endorsements?',
                    r'endorsed\s+by\s+(\d+)',
                    r'(\d+)\s*people',
                ]
                for pattern in endorsement_patterns:
                    count_match = re.search(pattern, item_text, re.I)
                    if count_match:
                        skill['endorsement_count'] = int(count_match.group(1))
                        break
            
            # Extract endorsers if available (usually in tooltips or hidden elements)
            endorser_links = item.find_all('a', href=re.compile(r'/in/'))
            for endorser_link in endorser_links:
                endorser_name = clean_text(endorser_link.get_text())
                if endorser_name and endorser_name not in skill['endorsers']:
                    skill['endorsers'].append(endorser_name)
            
            # Extract category if mentioned (enhanced)
            item_text = clean_text(item.get_text())
            category_keywords = {
                'technical': ['technical', 'programming', 'coding', 'development', 'engineering'],
                'soft': ['soft skill', 'communication', 'leadership', 'management', 'teamwork'],
                'language': ['language', 'speaking', 'bilingual', 'multilingual'],
                'certification': ['certification', 'certified', 'certificate'],
                'tool': ['tool', 'software', 'platform', 'framework', 'library'],
                'domain': ['domain', 'industry', 'sector', 'field'],
            }
            for category, keywords in category_keywords.items():
                if any(keyword in item_text.lower() for keyword in keywords):
                    skill['category'] = category
                    break
            
            # Also check aria-label for category
            if not skill['category']:
                category_aria = item.find(attrs={'aria-label': re.compile(r'technical|soft|language', re.I)})
                if category_aria:
                    aria_text = category_aria.get('aria-label', '').lower()
                    for category, keywords in category_keywords.items():
                        if any(keyword in aria_text for keyword in keywords):
                            skill['category'] = category
                            break
            
            if skill['name'] and skill['name'] not in [s.get('name') for s in skills]:
                skills.append(skill)
    
    return skills

def extract_skills_enhanced(soup: BeautifulSoup, about_text: str = '') -> List[Dict[str, Any]]:
    """Extract skills with fallback to about section text."""
    skills = extract_skills(soup)
    
    # If no skills found, try extracting from about section
    if not skills and about_text:
        # Look for skills mentioned in the about section
        # Common patterns: "expertise in X", "specialist in X", "experience with X", "X specialist"
        skill_patterns = [
            r'expertise in\s+([^·\n,]+)',
            r'specialist in\s+([^·\n,]+)',
            r'experience with\s+([^·\n,]+)',
            r'([A-Z][^·\n,]+?)\s+specialist',
            r'([A-Z][^·\n,]+?)\s+expert',
        ]
        
        seen_skills = set()
        for pattern in skill_patterns:
            matches = re.finditer(pattern, about_text, re.I)
            for match in matches:
                skill_name = clean_text(match.group(1))
                if (skill_name and 
                    skill_name.lower() not in seen_skills and 
                    len(skill_name) > 3 and 
                    len(skill_name) < 100):
                    seen_skills.add(skill_name.lower())
                    skills.append({
                        'name': skill_name,
                        'endorsement_count': None,
                        'category': None,
                        'endorsers': [],
                        'skill_url': None
                    })
        
        # Also extract from "Specialties:" section if present
        specialties_match = re.search(r'Specialties?[:\s]+([^·\n]+)', about_text, re.I)
        if specialties_match:
            specialties_text = specialties_match.group(1)
            # Split by common separators
            specialty_list = re.split(r'[,\s]+and\s+|[,\s]+', specialties_text)
            for specialty in specialty_list:
                specialty = clean_text(specialty)
                if (specialty and 
                    specialty.lower() not in seen_skills and 
                    len(specialty) > 3 and 
                    len(specialty) < 100):
                    seen_skills.add(specialty.lower())
                    skills.append({
                        'name': specialty,
                        'endorsement_count': None,
                        'category': None,
                        'endorsers': [],
                        'skill_url': None
                    })
    
    return skills

def extract_languages_from_about(languages: List[Dict[str, Any]], about_text: str) -> List[Dict[str, Any]]:
    """Extract languages from about section text if not already found."""
    if languages:
        return languages
    
    if not about_text:
        return languages
    
    # Look for language mentions
    language_patterns = [
        r'([A-Z][a-z]+(?: Chinese| English| Spanish| French| German| Japanese| Korean| Arabic| Hindi| Portuguese))',
        r'(Mandarin|Hokkien|Cantonese|English|Spanish|French|German|Japanese|Korean|Arabic|Hindi|Portuguese)',
        r'Bilingual\s+([A-Z][a-z]+)/?([A-Z][a-z]+)',
    ]
    seen_languages = set()
    for pattern in language_patterns:
        matches = re.finditer(pattern, about_text, re.I)
        for match in matches:
            if match.groups():
                for group in match.groups():
                    if group:
                        lang_name = clean_text(group)
                        if lang_name and lang_name.lower() not in seen_languages:
                            seen_languages.add(lang_name.lower())
                            languages.append({
                                'name': lang_name,
                                'proficiency': None
                            })
            else:
                lang_name = clean_text(match.group(0))
                if lang_name and lang_name.lower() not in seen_languages:
                    seen_languages.add(lang_name.lower())
                    languages.append({
                        'name': lang_name,
                        'proficiency': None
                    })
    
    return languages

def extract_certifications(soup: BeautifulSoup) -> List[Dict[str, Any]]:
    """Extract certifications information."""
    certifications = []
    cert_section = soup.find('section', {'data-section': 'certifications'}) or \
                   soup.find('section', class_=re.compile(r'certification', re.I))
    
    if cert_section:
        cert_items = cert_section.find_all('li', class_='profile-section-card')
        for item in cert_items:
            cert = {
                'name': None,
                'issuing_organization': None,
                'issue_date': None,
                'expiration_date': None,
                'credential_id': None,
                'credential_url': None
            }
            
            # Extract certification name (h3)
            name_elem = item.find('h3')
            if name_elem:
                cert['name'] = clean_text(name_elem.get_text())
            
            # Extract issuing organization (h4)
            org_elem = item.find('h4')
            if org_elem:
                cert['issuing_organization'] = clean_text(org_elem.get_text())
            
            # Extract dates
            date_range = item.find('span', class_='date-range')
            if date_range:
                time_elements = date_range.find_all('time')
                if len(time_elements) >= 1:
                    cert['issue_date'] = clean_text(time_elements[0].get_text())
                if len(time_elements) >= 2:
                    cert['expiration_date'] = clean_text(time_elements[1].get_text())
            
            # Extract credential ID and URL
            link = item.find('a', href=re.compile(r'certification', re.I))
            if link:
                cert['credential_url'] = link.get('href', '').strip()
            
            if cert['name']:
                certifications.append(cert)
    
    return certifications

def extract_licenses(soup: BeautifulSoup) -> List[Dict[str, Any]]:
    """Extract licenses information."""
    licenses = []
    license_section = soup.find('section', {'data-section': 'licenses'}) or \
                     soup.find('section', class_=re.compile(r'license', re.I))
    
    if license_section:
        license_items = license_section.find_all('li', class_='profile-section-card')
        for item in license_items:
            license_info = {
                'name': None,
                'issuing_organization': None,
                'issue_date': None,
                'expiration_date': None
            }
            
            # Extract license name (h3)
            name_elem = item.find('h3')
            if name_elem:
                license_info['name'] = clean_text(name_elem.get_text())
            
            # Extract issuing organization (h4)
            org_elem = item.find('h4')
            if org_elem:
                license_info['issuing_organization'] = clean_text(org_elem.get_text())
            
            # Extract dates
            date_range = item.find('span', class_='date-range')
            if date_range:
                time_elements = date_range.find_all('time')
                if len(time_elements) >= 1:
                    license_info['issue_date'] = clean_text(time_elements[0].get_text())
                if len(time_elements) >= 2:
                    license_info['expiration_date'] = clean_text(time_elements[1].get_text())
            
            if license_info['name']:
                licenses.append(license_info)
    
    return licenses

def extract_projects(soup: BeautifulSoup) -> List[Dict[str, Any]]:
    """Extract projects information."""
    projects = []
    project_section = soup.find('section', {'data-section': 'projects'}) or \
                     soup.find('section', class_=re.compile(r'project', re.I))
    
    if project_section:
        project_items = project_section.find_all('li', class_='profile-section-card')
        for item in project_items:
            project = {
                'name': None,
                'description': None,
                'start_date': None,
                'end_date': None,
                'url': None,
                'team_members': []
            }
            
            # Extract project name (h3)
            name_elem = item.find('h3')
            if name_elem:
                project['name'] = clean_text(name_elem.get_text())
            
            # Extract dates
            date_range = item.find('span', class_='date-range')
            if date_range:
                dates = extract_dates_from_range(date_range)
                project['start_date'] = dates['start_date']
                project['end_date'] = dates['end_date']
            
            # Extract description
            show_more_container = item.find('div', class_='show-more-less-text')
            if show_more_container:
                project['description'] = extract_expanded_text(show_more_container)
            
            # Extract URL
            link = item.find('a', href=re.compile(r'^https?://', re.I))
            if link:
                project['url'] = link.get('href', '').strip()
            
            if project['name']:
                projects.append(project)
    
    return projects

def extract_publications(soup: BeautifulSoup) -> List[Dict[str, Any]]:
    """Extract publications information."""
    publications = []
    pub_section = soup.find('section', {'data-section': 'publications'}) or \
                  soup.find('section', class_=re.compile(r'publication', re.I))
    
    if pub_section:
        pub_items = pub_section.find_all('li', class_='profile-section-card')
        for item in pub_items:
            pub = {
                'title': None,
                'publisher': None,
                'publication_date': None,
                'description': None,
                'url': None
            }
            
            # Extract title (h3)
            title_elem = item.find('h3')
            if title_elem:
                pub['title'] = clean_text(title_elem.get_text())
            
            # Extract publisher (h4)
            publisher_elem = item.find('h4')
            if publisher_elem:
                pub['publisher'] = clean_text(publisher_elem.get_text())
            
            # Extract date
            date_range = item.find('span', class_='date-range')
            if date_range:
                time_elem = date_range.find('time')
                if time_elem:
                    pub['publication_date'] = clean_text(time_elem.get_text())
            
            # Extract description
            show_more_container = item.find('div', class_='show-more-less-text')
            if show_more_container:
                pub['description'] = extract_expanded_text(show_more_container)
            
            # Extract URL
            link = item.find('a', href=re.compile(r'^https?://', re.I))
            if link:
                pub['url'] = link.get('href', '').strip()
            
            if pub['title']:
                publications.append(pub)
    
    return publications

def extract_recommendations(soup: BeautifulSoup) -> List[Dict[str, Any]]:
    """Extract recommendations information."""
    recommendations = []
    rec_section = soup.find('section', {'data-section': 'recommendations'}) or \
                  soup.find('section', class_=re.compile(r'recommendation', re.I))
    
    # Try alternative selectors for new format
    if not rec_section:
        rec_section = (soup.find('div', attrs={'data-view-name': re.compile(r'recommendation', re.I)}) or
                      soup.find('div', attrs={'componentkey': re.compile(r'recommendation', re.I)}))
    
    if rec_section:
        rec_items = rec_section.find_all('li', class_='profile-section-card')
        
        # Also try finding with obfuscated classes
        if not rec_items:
            rec_items = rec_section.find_all('li', class_=re.compile(r'card|item', re.I))
        
        for item in rec_items:
            rec = {
                'text': None,
                'recommender_name': None,
                'recommender_title': None,
                'recommender_company': None,
                'recommender_profile_url': None,
                'date': None,
                'relationship_context': None,
                'visibility': None
            }
            
            # Extract recommendation text (enhanced)
            text_elem = item.find('p', class_=re.compile(r'recommendation', re.I))
            if not text_elem:
                text_elem = item.find('p') or item.find('div', class_=re.compile(r'text|content', re.I))
            if text_elem:
                rec['text'] = extract_expanded_text(text_elem)
            
            # Extract recommender name and profile URL (enhanced)
            name_elem = item.find('h3') or item.find('a', href=re.compile(r'/in/'))
            if not name_elem:
                # Try finding name in aria-label
                name_aria = item.find(attrs={'aria-label': re.compile(r'^[A-Z][a-z]+ [A-Z]', re.M)})
                if name_aria:
                    name_elem = name_aria
            
            if name_elem:
                rec['recommender_name'] = clean_text(name_elem.get_text())
                if name_elem.name == 'a':
                    rec['recommender_profile_url'] = name_elem.get('href', '').strip()
                else:
                    link = item.find('a', href=re.compile(r'/in/'))
                    if link:
                        rec['recommender_profile_url'] = link.get('href', '').strip()
            
            # Extract recommender title and company (enhanced)
            subtitle_elem = item.find('h4')
            if not subtitle_elem:
                subtitle_elem = item.find('div', class_=re.compile(r'subtitle|title', re.I))
            
            if subtitle_elem:
                subtitle_text = clean_text(subtitle_elem.get_text())
                # Try to parse "Title at Company"
                if ' at ' in subtitle_text:
                    parts = subtitle_text.split(' at ', 1)
                    rec['recommender_title'] = parts[0].strip()
                    rec['recommender_company'] = parts[1].strip() if len(parts) > 1 else None
                elif ', ' in subtitle_text:
                    # Format might be "Title, Company"
                    parts = subtitle_text.split(', ', 1)
                    rec['recommender_title'] = parts[0].strip()
                    rec['recommender_company'] = parts[1].strip() if len(parts) > 1 else None
                else:
                    rec['recommender_title'] = subtitle_text
            
            # Extract date with better parsing (enhanced)
            date_range = item.find('span', class_='date-range')
            if date_range:
                time_elem = date_range.find('time')
                if time_elem:
                    rec['date'] = time_elem.get('datetime', '') or clean_text(time_elem.get_text())
            else:
                # Try alternative date formats
                time_elem = item.find('time')
                if not time_elem:
                    time_elem = item.find('span', class_=re.compile(r'time|date', re.I))
                if time_elem:
                    rec['date'] = (time_elem.get('datetime', '') or 
                                  time_elem.get('data-time', '') or
                                  clean_text(time_elem.get_text()))
            
            # Extract relationship context (e.g., "worked together", "reported to", etc.) - enhanced
            item_text = clean_text(item.get_text())
            relationship_keywords = {
                'worked together': ['worked together', 'colleague', 'teammate'],
                'reported to': ['reported to', 'manager', 'supervisor'],
                'managed': ['managed', 'supervised', 'led'],
                'client': ['client', 'customer'],
                'student': ['student', 'learner'],
                'mentor': ['mentor', 'mentored'],
                'partner': ['partner', 'collaborated'],
            }
            for relationship, keywords in relationship_keywords.items():
                if any(keyword in item_text.lower() for keyword in keywords):
                    rec['relationship_context'] = relationship
                    break
            
            # Extract visibility (public/private) if available
            visibility_elem = item.find(string=re.compile(r'public|private', re.I))
            if visibility_elem:
                rec['visibility'] = clean_text(visibility_elem).lower()
            
            # Extract recommender image if available
            recommender_img = item.find('img')
            if recommender_img:
                rec['recommender_image_url'] = (recommender_img.get('data-delayed-url', '') or
                                              recommender_img.get('src', '') or
                                              recommender_img.get('data-ghost-url', ''))
            
            if rec['text'] or rec['recommender_name']:
                recommendations.append(rec)
    
    return recommendations

def extract_websites(soup: BeautifulSoup) -> List[Dict[str, Any]]:
    """Extract website URLs and descriptions."""
    websites = []
    websites_section = soup.find('div', {'data-section': 'websites'})
    
    if websites_section:
        # Look for links in the websites section
        links = websites_section.find_all('a', class_='top-card-link')
        for link in links:
            website = {
                'url': None,
                'description': None,
                'title': None
            }
            
            website['url'] = link.get('href', '').strip()
            
            # Extract description
            desc_elem = link.find('span', class_='top-card-link__description')
            if desc_elem:
                website['description'] = clean_text(desc_elem.get_text())
            
            # Extract title from link text
            link_text = clean_text(link.get_text())
            if link_text:
                website['title'] = link_text
            
            if website['url']:
                websites.append(website)
    
    return websites

def extract_contact_info(soup: BeautifulSoup) -> Dict[str, Any]:
    """Extract contact information."""
    contact_info = {
        'email': None,
        'phone': None,
        'websites': [],
        'twitter': None,
        'birthday': None,
        'im_accounts': [],
        'social_media': {}
    }
    
    # Try to find contact info modal
    contact_modal = soup.find('div', id=re.compile(r'contact-info', re.I))
    if not contact_modal:
        # Try alternative selectors
        contact_modal = soup.find('div', class_=re.compile(r'contact-info', re.I))
    
    # Try finding from data attributes
    if not contact_modal:
        contact_modal = soup.find('div', attrs={'data-view-name': re.compile(r'contact', re.I)})
    
    # Extract email from multiple sources
    if contact_modal:
        # Extract email
        email_elem = contact_modal.find('a', href=re.compile(r'^mailto:', re.I))
        if email_elem:
            contact_info['email'] = email_elem.get('href', '').replace('mailto:', '').strip()
    
    # Also try extracting email from text patterns (if not in modal)
    if not contact_info['email']:
        all_text = soup.get_text()
        email_patterns = [
            r'([a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,})',
            r'mailto:([a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,})',
        ]
        for pattern in email_patterns:
            email_match = re.search(pattern, all_text, re.I)
            if email_match:
                contact_info['email'] = email_match.group(1).strip()
                break
    
    # Extract phone from multiple sources
    if contact_modal:
        # Extract phone
        phone_elem = contact_modal.find('a', href=re.compile(r'^tel:', re.I))
        if phone_elem:
            contact_info['phone'] = phone_elem.get('href', '').replace('tel:', '').strip()
    
    # Also try extracting phone from text patterns
    if not contact_info['phone']:
        all_text = soup.get_text()
        phone_patterns = [
            r'tel:([+\d\s\-()]+)',
            r'phone[:\s]+([+\d\s\-()]+)',
            r'(\+?\d{1,3}[\s\-]?\(?\d{3}\)?[\s\-]?\d{3}[\s\-]?\d{4})',
        ]
        for pattern in phone_patterns:
            phone_match = re.search(pattern, all_text, re.I)
            if phone_match:
                contact_info['phone'] = clean_text(phone_match.group(1))
                break
        
        # Extract websites and social media
        website_links = contact_modal.find_all('a', href=re.compile(r'^https?://', re.I))
        for link in website_links:
            url = link.get('href', '').strip()
            link_text = clean_text(link.get_text()).lower()
            
            if url and 'linkedin.com' not in url:
                # Check for social media platforms
                if 'twitter.com' in url or 'x.com' in url:
                    contact_info['twitter'] = url
                    contact_info['social_media']['twitter'] = url
                elif 'facebook.com' in url:
                    contact_info['social_media']['facebook'] = url
                elif 'instagram.com' in url:
                    contact_info['social_media']['instagram'] = url
                elif 'github.com' in url:
                    contact_info['social_media']['github'] = url
                elif 'youtube.com' in url or 'youtu.be' in url:
                    contact_info['social_media']['youtube'] = url
                elif 'medium.com' in url:
                    contact_info['social_media']['medium'] = url
                elif 'behance.net' in url:
                    contact_info['social_media']['behance'] = url
                elif 'dribbble.com' in url:
                    contact_info['social_media']['dribbble'] = url
                elif 'tiktok.com' in url:
                    contact_info['social_media']['tiktok'] = url
                elif 'snapchat.com' in url:
                    contact_info['social_media']['snapchat'] = url
                elif 'pinterest.com' in url:
                    contact_info['social_media']['pinterest'] = url
                elif 'linkedin.com' not in url:
                    contact_info['websites'].append({
                        'url': url,
                        'label': clean_text(link.get_text())
                    })
    
    # Also extract social media from about section and other text
    all_text = soup.get_text()
    social_patterns = {
        'twitter': r'(?:twitter|@)(?:\.com/)?([a-zA-Z0-9_]+)',
        'github': r'github\.com/([a-zA-Z0-9_-]+)',
        'youtube': r'(?:youtube\.com|youtu\.be)/(?:channel/|user/|@)?([a-zA-Z0-9_-]+)',
    }
    for platform, pattern in social_patterns.items():
        if platform not in contact_info['social_media']:
            match = re.search(pattern, all_text, re.I)
            if match:
                username = match.group(1)
                if platform == 'twitter':
                    contact_info['social_media'][platform] = f"https://twitter.com/{username}"
                elif platform == 'github':
                    contact_info['social_media'][platform] = f"https://github.com/{username}"
                elif platform == 'youtube':
                    contact_info['social_media'][platform] = f"https://youtube.com/@{username}"
        
        # Extract IM accounts (Skype, etc.)
        im_links = contact_modal.find_all('a', href=re.compile(r'^(skype:|im:|xmpp:)', re.I))
        for link in im_links:
            href = link.get('href', '').strip()
            im_type = None
            if href.startswith('skype:'):
                im_type = 'skype'
                account = href.replace('skype:', '').strip()
            elif href.startswith('im:'):
                im_type = 'im'
                account = href.replace('im:', '').strip()
            elif href.startswith('xmpp:'):
                im_type = 'xmpp'
                account = href.replace('xmpp:', '').strip()
            
            if im_type and account:
                contact_info['im_accounts'].append({
                    'type': im_type,
                    'account': account
                })
        
        # Extract birthday
        birthday_elem = contact_modal.find(string=re.compile(r'birthday|date of birth', re.I))
        if birthday_elem:
            birthday_match = re.search(r'(\d{1,2}[/-]\d{1,2}[/-]\d{2,4})', str(birthday_elem), re.I)
            if birthday_match:
                contact_info['birthday'] = birthday_match.group(1)
    
    # Also try extracting birthday from text patterns
    if not contact_info['birthday']:
        all_text = soup.get_text()
        birthday_patterns = [
            r'birthday[:\s]+(\d{1,2}[/-]\d{1,2}[/-]\d{2,4})',
            r'date\s+of\s+birth[:\s]+(\d{1,2}[/-]\d{1,2}[/-]\d{2,4})',
            r'born[:\s]+(\d{1,2}[/-]\d{1,2}[/-]\d{2,4})',
        ]
        for pattern in birthday_patterns:
            birthday_match = re.search(pattern, all_text, re.I)
            if birthday_match:
                contact_info['birthday'] = birthday_match.group(1)
                break
    
    return contact_info

def extract_about(soup: BeautifulSoup) -> Optional[str]:
    """Extract about/summary section including expanded content."""
    about = None
    about_section = soup.find('section', {'data-section': 'summary'})
    
    if not about_section:
        about_section = soup.find('section', {'id': 'about-section'}) or \
                        soup.find('div', class_=re.compile(r'about', re.I))
    
    # Try alternative selectors for new format
    if not about_section:
        about_section = soup.find('div', attrs={'data-view-name': re.compile(r'about|summary', re.I)}) or \
                        soup.find('div', attrs={'componentkey': re.compile(r'about|summary', re.I)})
    
    if about_section:
        # Try to get the full text including expanded content
        content_div = about_section.find('div', class_='core-section-container__content')
        if content_div:
            # Look for show-more-less text
            show_more_container = content_div.find('div', class_='show-more-less-text')
            if show_more_container:
                about = extract_expanded_text(show_more_container)
            else:
                # Get all text from content div
                about = clean_text(content_div.get_text())
        
        # Fallback to any text in the section
        if not about:
            about_text = about_section.find('div', class_=re.compile(r'text', re.I))
            if about_text:
                about = clean_text(about_text.get_text())
            else:
                about = clean_text(about_section.get_text())
    
    # If still no about found, try finding paragraphs that look like an about section
    if not about:
        # Look for long paragraphs that might be the about section
        all_paragraphs = soup.find_all('p')
        for p in all_paragraphs:
            text = clean_text(p.get_text())
            # About sections are usually longer and contain personal/professional info
            if len(text) > 100 and len(text) < 2000:
                # Check if it contains common about section keywords
                about_keywords = ['experience', 'specialist', 'expert', 'focus', 'specialties', 'background', 'professional']
                if any(keyword in text.lower() for keyword in about_keywords):
                    about = text
                    break
    
    return about

def extract_activities(soup: BeautifulSoup) -> List[Dict[str, Any]]:
    """Extract activities/posts that the user has interacted with."""
    activities = []
    activities_list = soup.find('ul', {'data-test-id': 'activities__list'})
    
    # Try alternative selectors for new format
    if not activities_list:
        activities_list = (soup.find('ul', class_=re.compile(r'activity', re.I)) or
                         soup.find('div', attrs={'data-view-name': re.compile(r'activity', re.I)}) or
                         soup.find('div', attrs={'componentkey': re.compile(r'activity', re.I)}))
    
    if activities_list:
        activity_items = activities_list.find_all('li')
        
        # Also try finding with obfuscated classes
        if not activity_items:
            activity_items = activities_list.find_all('li', class_=re.compile(r'card|item|post', re.I))
        
        # Also try finding articles or divs
        if not activity_items:
            activity_items = activities_list.find_all(['article', 'div'], class_=re.compile(r'activity|post', re.I))
        
        for item in activity_items:
            activity = {
                'post_url': None,
                'post_title': None,
                'post_text': None,
                'post_image_url': None,
                'post_type': None,  # 'liked', 'shared', 'commented', etc.
                'post_author': None,
                'post_timestamp': None,
                'engagement_metrics': {
                    'likes': None,
                    'comments': None,
                    'shares': None
                },
                'media': {
                    'images': [],
                    'videos': []
                }
            }
            
            # Extract post URL (multiple methods)
            link = item.find('a', class_='base-card__full-link')
            if not link:
                # Try alternative link patterns
                link = item.find('a', href=re.compile(r'/posts/|/activity-|/feed/', re.I))
            if not link:
                # Try any link with post-like URL
                all_links = item.find_all('a', href=True)
                for l in all_links:
                    href = l.get('href', '')
                    if '/posts/' in href or '/activity-' in href or '/feed/' in href:
                        link = l
                        break
            
            if link:
                activity['post_url'] = link.get('href', '').strip()
            
            # Extract post title (multiple methods)
            title_elem = item.find('h3', class_='base-main-card__title')
            if not title_elem:
                title_elem = item.find('h3') or item.find('h2') or item.find('h4')
            if title_elem:
                activity['post_title'] = clean_text(title_elem.get_text())
            
            # Extract post text from sr-only span (full text) or other sources
            sr_only = item.find('span', class_='sr-only')
            if sr_only:
                activity['post_text'] = clean_text(sr_only.get_text())
            else:
                # Try to find post text in paragraphs
                text_elem = item.find('p', class_=re.compile(r'text|content|post', re.I))
                if text_elem:
                    activity['post_text'] = clean_text(text_elem.get_text())
                else:
                    # Try any paragraph
                    paragraphs = item.find_all('p')
                    for p in paragraphs:
                        text = clean_text(p.get_text())
                        if text and len(text) > 20:  # Likely post text if longer
                            activity['post_text'] = text
                            break
            
            # Extract post image (multiple methods)
            img = item.find('img', class_='main-activity-card__img')
            if not img:
                img = item.find('img', class_=re.compile(r'activity|post|image', re.I))
            if not img:
                img = item.find('img')
            
            if img:
                img_url = (img.get('data-delayed-url', '').strip() or 
                          img.get('src', '').strip() or
                          img.get('data-ghost-url', '').strip() or
                          img.get('data-src', '').strip())
                activity['post_image_url'] = img_url
                if img_url:
                    activity['media']['images'].append(img_url)
            
            # Extract all images
            all_images = item.find_all('img')
            for img_elem in all_images:
                img_url = (img_elem.get('data-delayed-url', '').strip() or 
                          img_elem.get('src', '').strip() or
                          img_elem.get('data-ghost-url', '').strip())
                if img_url and img_url not in activity['media']['images']:
                    activity['media']['images'].append(img_url)
            
            # Extract videos (enhanced)
            video_elem = item.find('video')
            if not video_elem:
                video_elem = item.find('iframe', src=re.compile(r'youtube|vimeo|video', re.I))
            if not video_elem:
                video_elem = item.find('div', class_=re.compile(r'video', re.I))
            
            if video_elem:
                video_url = (video_elem.get('src', '') or 
                            video_elem.get('data-src', '') or
                            video_elem.get('data-video-url', ''))
                if video_url:
                    activity['media']['videos'].append(video_url)
            
            # Extract post type and author from subtitle (enhanced)
            subtitle = item.find('h4', class_='base-main-card__subtitle')
            if not subtitle:
                subtitle = item.find('h4') or item.find('div', class_=re.compile(r'subtitle|author', re.I))
            
            if subtitle:
                subtitle_text = clean_text(subtitle.get_text())
                # Check for "Liked by", "Shared by", etc.
                if 'liked by' in subtitle_text.lower() or 'liked' in subtitle_text.lower():
                    activity['post_type'] = 'liked'
                elif 'shared' in subtitle_text.lower():
                    activity['post_type'] = 'shared'
                elif 'commented' in subtitle_text.lower():
                    activity['post_type'] = 'commented'
                elif 'posted' in subtitle_text.lower():
                    activity['post_type'] = 'posted'
                
                # Extract author name
                author_link = subtitle.find('a')
                if not author_link:
                    author_link = item.find('a', href=re.compile(r'/in/'))
                if author_link:
                    activity['post_author'] = clean_text(author_link.get_text())
            
            # Extract timestamp (enhanced)
            time_elem = item.find('time')
            if not time_elem:
                time_elem = item.find('span', class_=re.compile(r'time|date|timestamp', re.I))
            if time_elem:
                activity['post_timestamp'] = (time_elem.get('datetime', '') or 
                                             time_elem.get('data-time', '') or
                                             clean_text(time_elem.get_text()))
            
            # Extract engagement metrics (enhanced)
            item_text = clean_text(item.get_text())
            
            # Extract likes (multiple patterns)
            likes_patterns = [
                r'(\d+[KMB]?)\s*(?:like|👍)',
                r'(\d+[KMB]?)\s*people\s*(?:like|liked)',
                r'liked\s+by\s+(\d+[KMB]?)',
            ]
            for pattern in likes_patterns:
                likes_match = re.search(pattern, item_text, re.I)
                if likes_match:
                    activity['engagement_metrics']['likes'] = likes_match.group(1)
                    break
            
            # Extract comments (multiple patterns)
            comments_patterns = [
                r'(\d+[KMB]?)\s*comment',
                r'(\d+[KMB]?)\s*replies?',
            ]
            for pattern in comments_patterns:
                comments_match = re.search(pattern, item_text, re.I)
                if comments_match:
                    activity['engagement_metrics']['comments'] = comments_match.group(1)
                    break
            
            # Extract shares (multiple patterns)
            shares_patterns = [
                r'(\d+[KMB]?)\s*share',
                r'shared\s+(\d+[KMB]?)\s*times?',
            ]
            for pattern in shares_patterns:
                shares_match = re.search(pattern, item_text, re.I)
                if shares_match:
                    activity['engagement_metrics']['shares'] = shares_match.group(1)
                    break
            
            if activity['post_url'] or activity['post_title']:
                activities.append(activity)
    
    return activities

def extract_same_name_profiles(soup: BeautifulSoup) -> List[Dict[str, Any]]:
    """Extract profiles of people with the same name."""
    profiles = []
    same_name_section = soup.find('section', class_=re.compile(r'samename', re.I))
    
    if same_name_section:
        profile_links = same_name_section.find_all('a', href=re.compile(r'/in/'))
        for link in profile_links:
            profile = {
                'profile_url': None,
                'name': None,
                'location': None,
                'profile_image_url': None
            }
            
            profile['profile_url'] = link.get('href', '').strip()
            
            # Extract name
            name_elem = link.find('h3', class_='base-aside-card__title')
            if name_elem:
                profile['name'] = clean_text(name_elem.get_text())
            
            # Extract location
            location_elem = link.find('div', class_='base-aside-card__metadata')
            if location_elem:
                profile['location'] = clean_text(location_elem.get_text())
            
            # Extract profile image
            img_div = link.find('div', attrs={'data-delayed-url': True})
            if img_div:
                profile['profile_image_url'] = img_div.get('data-delayed-url', '').strip()
            
            if profile['profile_url']:
                profiles.append(profile)
    
    return profiles

def extract_course_recommendations(soup: BeautifulSoup) -> List[Dict[str, Any]]:
    """Extract LinkedIn Learning course recommendations."""
    courses = []
    course_section = soup.find('section', class_='course-recommendations')
    
    if course_section:
        course_items = course_section.find_all('li', class_='course-recommendations__course')
        for item in course_items:
            course = {
                'course_url': None,
                'course_title': None,
                'course_image_url': None,
                'course_duration': None
            }
            
            # Extract course URL
            link = item.find('a')
            if link:
                course['course_url'] = link.get('href', '').strip()
            
            # Extract course title
            title_elem = item.find('h3', class_='base-aside-card__title')
            if title_elem:
                course['course_title'] = clean_text(title_elem.get_text())
            
            # Extract course image
            img = item.find('img', class_='base-aside-card__media-element')
            if img:
                course['course_image_url'] = img.get('data-delayed-url', '').strip() or \
                                          img.get('src', '').strip()
            
            # Extract duration
            duration_elem = item.find('div', class_='duration')
            if duration_elem:
                course['course_duration'] = clean_text(duration_elem.get_text())
            
            if course['course_url'] or course['course_title']:
                courses.append(course)
    
    return courses

def extract_mutual_connections(soup: BeautifulSoup) -> List[Dict[str, Any]]:
    """Extract mutual connections information."""
    mutual_conns = []
    face_pile = soup.find('div', class_='face-pile')
    
    if face_pile:
        images = face_pile.find_all('img', class_='face-pile__image')
        for img in images:
            conn = {
                'image_url': img.get('data-delayed-url', '').strip() or \
                           img.get('src', '').strip(),
                'name': None  # Names are usually not available in public profiles
            }
            if conn['image_url']:
                mutual_conns.append(conn)
    
    return mutual_conns

def extract_interests(soup: BeautifulSoup) -> List[str]:
    """Extract interests from profile."""
    interests = []
    interests_section = soup.find('section', {'data-section': 'interests'}) or \
                        soup.find('section', class_=re.compile(r'interest', re.I))
    
    # Try alternative selectors for new format
    if not interests_section:
        interests_section = (soup.find('div', attrs={'data-view-name': re.compile(r'interest', re.I)}) or
                           soup.find('div', attrs={'componentkey': re.compile(r'interest', re.I)}))
    
    if interests_section:
        interest_items = interests_section.find_all('li', class_='profile-section-card') or \
                         interests_section.find_all('a', class_=re.compile(r'interest', re.I))
        
        # Also try finding with obfuscated classes
        if not interest_items:
            interest_items = interests_section.find_all('li', class_=re.compile(r'card|item', re.I))
        
        # Also try finding by componentkey
        if not interest_items:
            interest_items = interests_section.find_all(attrs={'componentkey': re.compile(r'interest', re.I)})
        
        for item in interest_items:
            interest_text = clean_text(item.get_text())
            if interest_text and interest_text not in interests:
                interests.append(interest_text)
    
    return interests

def extract_organizations(soup: BeautifulSoup) -> List[Dict[str, Any]]:
    """Extract organizations the person is a member of."""
    organizations = []
    org_section = soup.find('section', {'data-section': 'organizations'}) or \
                  soup.find('section', class_=re.compile(r'organization|member', re.I))
    
    # Try alternative selectors for new format
    if not org_section:
        org_section = (soup.find('div', attrs={'data-view-name': re.compile(r'organization|member', re.I)}) or
                      soup.find('div', attrs={'componentkey': re.compile(r'organization|member', re.I)}))
    
    if org_section:
        org_items = org_section.find_all('li', class_='profile-section-card')
        
        # Also try finding with obfuscated classes
        if not org_items:
            org_items = org_section.find_all('li', class_=re.compile(r'card|item', re.I))
        
        for item in org_items:
            org = {
                'name': None,
                'url': None,
                'role': None,
                'start_date': None,
                'end_date': None,
                'current': False,
                'logo_url': None
            }
            
            # Extract organization name
            name_elem = item.find('h3') or item.find('a')
            if name_elem:
                org['name'] = clean_text(name_elem.get_text())
                if name_elem.name == 'a':
                    org['url'] = name_elem.get('href', '').strip()
            
            # Extract role
            role_elem = item.find('h4') or item.find('span', class_=re.compile(r'role', re.I))
            if role_elem:
                org['role'] = clean_text(role_elem.get_text())
            
            # Extract dates
            date_range = item.find('span', class_='date-range')
            if date_range:
                dates = extract_dates_from_range(date_range)
                org['start_date'] = dates['start_date']
                org['end_date'] = dates['end_date']
                org['current'] = dates['current']
            
            # Extract logo
            org['logo_url'] = extract_logo_url(item)
            
            if org['name']:
                organizations.append(org)
    
    return organizations

def extract_featured_content(soup: BeautifulSoup) -> List[Dict[str, Any]]:
    """Extract featured content from profile."""
    featured = []
    featured_section = soup.find('section', {'data-section': 'featured'}) or \
                      soup.find('section', class_=re.compile(r'featured', re.I))
    
    # Try alternative selectors for new format
    if not featured_section:
        featured_section = (soup.find('div', attrs={'data-view-name': re.compile(r'featured', re.I)}) or
                           soup.find('div', attrs={'componentkey': re.compile(r'featured', re.I)}))
    
    if featured_section:
        featured_items = featured_section.find_all('li', class_='profile-section-card')
        
        # Also try finding with obfuscated classes
        if not featured_items:
            featured_items = featured_section.find_all('li', class_=re.compile(r'card|item', re.I))
        
        for item in featured_items:
            content = {
                'title': None,
                'description': None,
                'url': None,
                'image_url': None,
                'type': None,  # 'post', 'article', 'video', etc.
                'date': None
            }
            
            # Extract title
            title_elem = item.find('h3') or item.find('a')
            if title_elem:
                content['title'] = clean_text(title_elem.get_text())
                if title_elem.name == 'a':
                    content['url'] = title_elem.get('href', '').strip()
            
            # Extract description
            desc_elem = item.find('p') or item.find('div', class_=re.compile(r'description', re.I))
            if desc_elem:
                content['description'] = clean_text(desc_elem.get_text())
            
            # Extract image
            img = item.find('img')
            if img:
                content['image_url'] = (img.get('data-delayed-url', '') or 
                                      img.get('src', '') or 
                                      img.get('data-ghost-url', ''))
            
            # Determine type from URL or class
            if content['url']:
                if '/posts/' in content['url'] or '/activity-' in content['url']:
                    content['type'] = 'post'
                elif '/articles/' in content['url']:
                    content['type'] = 'article'
                elif '/videos/' in content['url'] or 'youtube' in content['url'] or 'vimeo' in content['url']:
                    content['type'] = 'video'
            
            # Extract date
            time_elem = item.find('time')
            if time_elem:
                content['date'] = time_elem.get('datetime', '') or clean_text(time_elem.get_text())
            
            if content['title'] or content['url']:
                featured.append(content)
    
    return featured

def extract_services(soup: BeautifulSoup) -> List[Dict[str, Any]]:
    """Extract services offered by the person."""
    services = []
    services_section = soup.find('section', {'data-section': 'services'}) or \
                      soup.find('section', class_=re.compile(r'service', re.I))
    
    # Try alternative selectors for new format
    if not services_section:
        services_section = (soup.find('div', attrs={'data-view-name': re.compile(r'service', re.I)}) or
                          soup.find('div', attrs={'componentkey': re.compile(r'service', re.I)}))
    
    if services_section:
        service_items = services_section.find_all('li', class_='profile-section-card')
        
        # Also try finding with obfuscated classes
        if not service_items:
            service_items = services_section.find_all('li', class_=re.compile(r'card|item', re.I))
        
        for item in service_items:
            service = {
                'name': None,
                'description': None,
                'price': None,
                'url': None
            }
            
            # Extract service name
            name_elem = item.find('h3') or item.find('a')
            if name_elem:
                service['name'] = clean_text(name_elem.get_text())
                if name_elem.name == 'a':
                    service['url'] = name_elem.get('href', '').strip()
            
            # Extract description
            desc_elem = item.find('p') or item.find('div', class_=re.compile(r'description', re.I))
            if desc_elem:
                service['description'] = clean_text(desc_elem.get_text())
            
            # Extract price if mentioned
            item_text = clean_text(item.get_text())
            price_match = re.search(r'\$?(\d+(?:,\d{3})*(?:\.\d{2})?)\s*(?:per|/|USD|EUR|GBP)', item_text, re.I)
            if price_match:
                service['price'] = price_match.group(1)
            
            if service['name']:
                services.append(service)
    
    return services

def extract_open_to_work(soup: BeautifulSoup) -> Dict[str, Any]:
    """Extract open to work status and details."""
    open_to_work = {
        'is_open_to_work': False,
        'open_to_work_type': None,  # 'jobs', 'freelance', 'consulting', etc.
        'job_titles': [],
        'locations': [],
        'start_date': None,
        'description': None
    }
    
    # Check for open to work indicators
    # Method 1: From meta tags
    page_tag_meta = soup.find('meta', {'name': 'linkedin:pageTag'})
    if page_tag_meta:
        content = page_tag_meta.get('content', '').strip()
        if 'openTo' in content.lower() or 'open' in content.lower():
            open_to_work['is_open_to_work'] = True
    
    # Method 2: From text patterns
    all_text = soup.get_text()
    open_patterns = [
        r'open\s+to\s+(work|jobs|opportunities|freelance|consulting)',
        r'looking\s+for\s+(work|jobs|opportunities)',
        r'available\s+for\s+(work|jobs|opportunities|freelance)',
    ]
    for pattern in open_patterns:
        match = re.search(pattern, all_text, re.I)
        if match:
            open_to_work['is_open_to_work'] = True
            open_to_work['open_to_work_type'] = match.group(1).lower()
            break
    
    # Method 3: From data attributes
    open_elements = soup.find_all(attrs={'data-view-name': re.compile(r'open.*work|available', re.I)})
    if open_elements:
        open_to_work['is_open_to_work'] = True
    
    # Extract job titles if open to work
    if open_to_work['is_open_to_work']:
        job_title_patterns = [
            r'looking\s+for[:\s]+([^,\n]+)',
            r'interested\s+in[:\s]+([^,\n]+)',
            r'seeking[:\s]+([^,\n]+)',
        ]
        for pattern in job_title_patterns:
            matches = re.findall(pattern, all_text, re.I)
            for match in matches:
                title = clean_text(match)
                if title and title not in open_to_work['job_titles']:
                    open_to_work['job_titles'].append(title)
    
    return open_to_work

def extract_groups(soup: BeautifulSoup) -> List[Dict[str, Any]]:
    """Extract LinkedIn groups the person belongs to."""
    groups = []
    groups_section = soup.find('section', {'data-section': 'groups'}) or \
                    soup.find('section', class_=re.compile(r'group', re.I))
    
    # Try alternative selectors for new format
    if not groups_section:
        groups_section = (soup.find('div', attrs={'data-view-name': re.compile(r'group', re.I)}) or
                         soup.find('div', attrs={'componentkey': re.compile(r'group', re.I)}))
    
    if groups_section:
        group_items = groups_section.find_all('li', class_='profile-section-card')
        
        # Also try finding with obfuscated classes
        if not group_items:
            group_items = groups_section.find_all('li', class_=re.compile(r'card|item', re.I))
        
        for item in group_items:
            group = {
                'name': None,
                'group_url': None,
                'member_count': None,
                'logo_url': None
            }
            
            # Extract group name
            name_elem = item.find('h3') or item.find('a')
            if name_elem:
                group['name'] = clean_text(name_elem.get_text())
                # Extract URL from link
                if name_elem.name == 'a':
                    group['group_url'] = name_elem.get('href', '').strip()
                else:
                    link = item.find('a', href=re.compile(r'/groups/'))
                    if link:
                        group['group_url'] = link.get('href', '').strip()
            
            # Extract member count
            member_count_elem = item.find(string=re.compile(r'\d+\s*members?', re.I))
            if member_count_elem:
                count_match = re.search(r'(\d+)', member_count_elem)
                if count_match:
                    group['member_count'] = int(count_match.group(1))
            
            # Extract logo
            group['logo_url'] = extract_logo_url(item)
            
            if group['name']:
                groups.append(group)
    
    return groups

def extract_patents(soup: BeautifulSoup) -> List[Dict[str, Any]]:
    """Extract patents information."""
    patents = []
    patents_section = soup.find('section', {'data-section': 'patents'}) or \
                     soup.find('section', class_=re.compile(r'patent', re.I))
    
    if patents_section:
        patent_items = patents_section.find_all('li', class_='profile-section-card')
        for item in patent_items:
            patent = {
                'title': None,
                'patent_number': None,
                'issue_date': None,
                'description': None,
                'url': None
            }
            
            # Extract patent title (h3)
            title_elem = item.find('h3')
            if title_elem:
                patent['title'] = clean_text(title_elem.get_text())
            
            # Extract patent number
            patent_num_elem = item.find(string=re.compile(r'patent\s*(?:no\.?|number)[:\s]+([A-Z0-9-]+)', re.I))
            if patent_num_elem:
                num_match = re.search(r'patent\s*(?:no\.?|number)[:\s]+([A-Z0-9-]+)', patent_num_elem, re.I)
                if num_match:
                    patent['patent_number'] = num_match.group(1)
            
            # Extract issue date
            date_range = item.find('span', class_='date-range')
            if date_range:
                time_elem = date_range.find('time')
                if time_elem:
                    patent['issue_date'] = clean_text(time_elem.get_text())
            
            # Extract description
            show_more_container = item.find('div', class_='show-more-less-text')
            if show_more_container:
                patent['description'] = extract_expanded_text(show_more_container)
            
            # Extract URL
            link = item.find('a', href=re.compile(r'^https?://', re.I))
            if link:
                patent['url'] = link.get('href', '').strip()
            
            if patent['title']:
                patents.append(patent)
    
    return patents

def extract_test_scores(soup: BeautifulSoup) -> List[Dict[str, Any]]:
    """Extract standardized test scores."""
    test_scores = []
    test_section = soup.find('section', {'data-section': 'test-scores'}) or \
                  soup.find('section', class_=re.compile(r'test.*score', re.I))
    
    if test_section:
        test_items = test_section.find_all('li', class_='profile-section-card')
        for item in test_items:
            test = {
                'test_name': None,
                'score': None,
                'date': None,
                'description': None
            }
            
            # Extract test name (h3)
            name_elem = item.find('h3')
            if name_elem:
                test['test_name'] = clean_text(name_elem.get_text())
            
            # Extract score
            score_elem = item.find(string=re.compile(r'score[:\s]+([0-9.]+)', re.I))
            if score_elem:
                score_match = re.search(r'score[:\s]+([0-9.]+)', score_elem, re.I)
                if score_match:
                    test['score'] = score_match.group(1)
            
            # Extract date
            date_range = item.find('span', class_='date-range')
            if date_range:
                time_elem = date_range.find('time')
                if time_elem:
                    test['date'] = clean_text(time_elem.get_text())
            
            # Extract description
            show_more_container = item.find('div', class_='show-more-less-text')
            if show_more_container:
                test['description'] = extract_expanded_text(show_more_container)
            
            if test['test_name']:
                test_scores.append(test)
    
    return test_scores

def extract_accomplishments(soup: BeautifulSoup) -> List[Dict[str, Any]]:
    """Extract additional accomplishments beyond awards."""
    accomplishments = []
    accomplishments_section = soup.find('section', {'data-section': 'accomplishments'}) or \
                             soup.find('section', class_=re.compile(r'accomplishment', re.I))
    
    if accomplishments_section:
        accomplishment_items = accomplishments_section.find_all('li', class_='profile-section-card')
        for item in accomplishment_items:
            accomplishment = {
                'title': None,
                'issuer': None,
                'date': None,
                'description': None
            }
            
            # Extract title (h3)
            title_elem = item.find('h3')
            if title_elem:
                accomplishment['title'] = clean_text(title_elem.get_text())
            
            # Extract issuer (h4)
            issuer_elem = item.find('h4')
            if issuer_elem:
                accomplishment['issuer'] = clean_text(issuer_elem.get_text())
            
            # Extract date
            date_range = item.find('span', class_='date-range')
            if date_range:
                time_elem = date_range.find('time')
                if time_elem:
                    accomplishment['date'] = clean_text(time_elem.get_text())
            
            # Extract description
            show_more_container = item.find('div', class_='show-more-less-text')
            if show_more_container:
                accomplishment['description'] = extract_expanded_text(show_more_container)
            
            if accomplishment['title']:
                accomplishments.append(accomplishment)
    
    return accomplishments

def extract_people_also_viewed(soup: BeautifulSoup) -> List[Dict[str, Any]]:
    """Extract 'People Also Viewed' section."""
    people = []
    people_section = soup.find('section', class_=re.compile(r'people.*viewed|browsemap', re.I))
    
    if people_section:
        people_items = people_section.find_all('li', class_='profile-section-card') or \
                       people_section.find_all('a', href=re.compile(r'/in/'))
        for item in people_items:
            person = {
                'name': None,
                'profile_url': None,
                'headline': None,
                'location': None,
                'profile_image_url': None
            }
            
            # Extract profile URL
            link = item.find('a', href=re.compile(r'/in/'))
            if link:
                person['profile_url'] = link.get('href', '').strip()
            
            # Extract name
            name_elem = item.find('h3') or (link and link.find('h3'))
            if name_elem:
                person['name'] = clean_text(name_elem.get_text())
            
            # Extract headline
            headline_elem = item.find('h4')
            if headline_elem:
                person['headline'] = clean_text(headline_elem.get_text())
            
            # Extract location
            location_elem = item.find('div', class_=re.compile(r'metadata|location', re.I))
            if location_elem:
                person['location'] = clean_text(location_elem.get_text())
            
            # Extract profile image
            img = item.find('img')
            if img:
                person['profile_image_url'] = img.get('data-delayed-url', '').strip() or \
                                             img.get('src', '').strip()
            
            if person['name'] or person['profile_url']:
                people.append(person)
    
    return people

def extract_related_posts(soup: BeautifulSoup) -> List[Dict[str, Any]]:
    """Extract related posts section."""
    posts = []
    related_posts_section = soup.find('section', class_=re.compile(r'related.*post', re.I))
    
    if related_posts_section:
        post_items = related_posts_section.find_all('li', class_='profile-section-card') or \
                    related_posts_section.find_all('article')
        for item in post_items:
            post = {
                'post_url': None,
                'post_title': None,
                'post_text': None,
                'post_author': None,
                'post_date': None,
                'post_image_url': None
            }
            
            # Extract post URL
            link = item.find('a', href=re.compile(r'/posts/|/activity-', re.I))
            if link:
                post['post_url'] = link.get('href', '').strip()
            
            # Extract post title
            title_elem = item.find('h3')
            if title_elem:
                post['post_title'] = clean_text(title_elem.get_text())
            
            # Extract post text
            text_elem = item.find('p') or item.find('div', class_=re.compile(r'text', re.I))
            if text_elem:
                post['post_text'] = clean_text(text_elem.get_text())
            
            # Extract author
            author_elem = item.find('a', href=re.compile(r'/in/'))
            if author_elem:
                post['post_author'] = clean_text(author_elem.get_text())
            
            # Extract date
            date_elem = item.find('time')
            if date_elem:
                post['post_date'] = clean_text(date_elem.get_text())
            
            # Extract image
            img = item.find('img')
            if img:
                post['post_image_url'] = img.get('data-delayed-url', '').strip() or \
                                        img.get('src', '').strip()
            
            if post['post_url'] or post['post_title']:
                posts.append(post)
    
    return posts

def extract_profile_id(profile_url: Optional[str]) -> Optional[str]:
    """Extract LinkedIn profile ID from URL."""
    if not profile_url:
        return None
    
    # Pattern: /in/username-12345678 or /in/username
    match = re.search(r'/in/[^/]+-(\d+)', profile_url)
    if match:
        return match.group(1)
    
    return None

def extract_vanity_name(profile_url: Optional[str]) -> Optional[str]:
    """Extract vanity name from profile URL."""
    if not profile_url:
        return None
    
    # Pattern: /in/vanity-name-12345678
    match = re.search(r'/in/([^/]+)', profile_url)
    if match:
        return match.group(1)
    
    return None

def extract_data_attributes(soup: BeautifulSoup) -> Dict[str, Any]:
    """Extract data from data-* attributes, URNs, tracking IDs, and embedded JavaScript data."""
    data_attributes = {
        'urns': [],
        'tracking_ids': [],
        'component_keys': [],
        'view_names': [],
        'sdui_components': [],
        'embedded_data': {}
    }
    
    # Extract URNs (urn:li:activity, urn:li:profile, etc.)
    all_text = soup.get_text()
    urn_pattern = r'urn:li:[a-z]+:[A-Za-z0-9_-]+'
    urns = re.findall(urn_pattern, all_text)
    data_attributes['urns'] = list(set(urns))
    
    # Extract from href attributes
    links = soup.find_all('a', href=True)
    for link in links:
        href = link.get('href', '')
        urn_matches = re.findall(urn_pattern, href)
        data_attributes['urns'].extend(urn_matches)
    
    # Remove duplicates
    data_attributes['urns'] = list(set(data_attributes['urns']))
    
    # Extract tracking IDs (data-tracking-control-name, data-tracking-will-navigate, etc.)
    tracking_elements = soup.find_all(attrs={'data-tracking-control-name': True})
    for elem in tracking_elements:
        tracking_id = elem.get('data-tracking-control-name', '').strip()
        if tracking_id:
            data_attributes['tracking_ids'].append(tracking_id)
    
    # Extract component keys
    component_elements = soup.find_all(attrs={'componentkey': True})
    for elem in component_elements:
        component_key = elem.get('componentkey', '').strip()
        if component_key:
            data_attributes['component_keys'].append(component_key)
    
    # Extract view names
    view_elements = soup.find_all(attrs={'data-view-name': True})
    for elem in view_elements:
        view_name = elem.get('data-view-name', '').strip()
        if view_name:
            data_attributes['view_names'].append(view_name)
    
    # Extract SDUI components
    sdui_elements = soup.find_all(attrs={'data-sdui-component': True})
    for elem in sdui_elements:
        sdui_component = elem.get('data-sdui-component', '').strip()
        if sdui_component:
            data_attributes['sdui_components'].append(sdui_component)
    
    # Extract embedded JavaScript data (if present)
    script_tags = soup.find_all('script')
    for script in script_tags:
        script_content = script.string
        if script_content:
            # Look for common data patterns in JavaScript
            # Try to find JSON data
            json_patterns = [
                r'window\.__INITIAL_STATE__\s*=\s*({.+?});',
                r'window\.linkedin\.data\s*=\s*({.+?});',
                r'profileData\s*[:=]\s*({.+?});',
            ]
            for pattern in json_patterns:
                match = re.search(pattern, script_content, re.DOTALL)
                if match:
                    try:
                        json_data = json.loads(match.group(1))
                        data_attributes['embedded_data']['initial_state'] = json_data
                    except (json.JSONDecodeError, ValueError):
                        pass
    
    return data_attributes

def scrape_linkedin_profile(html_file_path: str) -> Dict[str, Any]:
    """
    Main function to scrape LinkedIn profile from HTML file.
    
    Args:
        html_file_path: Path to the HTML file
        
    Returns:
        Dictionary containing all extracted profile information
    """
    # #region agent log
    import json as json_module
    log_path = r"d:\code\ayan\contact360\.cursor\debug.log"
    def log_debug(location, message, data, hypothesis_id="A"):
        try:
            with open(log_path, 'a', encoding='utf-8') as f:
                log_entry = {
                    "sessionId": "debug-session",
                    "runId": "run1",
                    "hypothesisId": hypothesis_id,
                    "location": location,
                    "message": message,
                    "data": data,
                    "timestamp": datetime.now().isoformat()
                }
                f.write(json_module.dumps(log_entry) + '\n')
        except:
            pass
    # #endregion
    
    # Read HTML file
    with open(html_file_path, 'r', encoding='utf-8') as f:
        html_content = f.read()
    
    # #region agent log
    log_debug("scrape_linkedin_profile:entry", "Starting profile extraction", {
        "file": html_file_path,
        "html_size": len(html_content)
    }, "A")
    # #endregion
    
    # Parse HTML
    soup = BeautifulSoup(html_content, 'html.parser')
    
    # #region agent log
    log_debug("scrape_linkedin_profile:after_parse", "HTML parsed", {
        "title": soup.find('title').get_text() if soup.find('title') else None,
        "has_json_ld_script": bool(soup.find('script', type='application/ld+json'))
    }, "A")
    # #endregion
    
    # Extract JSON-LD structured data
    json_ld = extract_json_ld(soup)
    comprehensive_json_ld = extract_comprehensive_json_ld(soup)
    
    # #region agent log
    log_debug("scrape_linkedin_profile:json_ld", "JSON-LD extraction result", {
        "has_json_ld": json_ld is not None,
        "has_comprehensive": comprehensive_json_ld.get('person_data') is not None
    }, "A")
    # #endregion
    
    # Extract page metadata
    page_metadata = extract_page_metadata(soup)
    
    # Extract basic info first
    basic_info = extract_basic_info(soup, json_ld)
    
    # #region agent log
    log_debug("scrape_linkedin_profile:basic_info", "Basic info extracted", {
        "name": basic_info.get('name'),
        "headline": basic_info.get('headline'),
        "location": basic_info.get('location'),
        "profile_url": basic_info.get('profile_url'),
        "has_name": bool(basic_info.get('name')),
        "has_headline": bool(basic_info.get('headline'))
    }, "B")
    # #endregion
    
    # Extract profile ID and vanity name from URL
    profile_url = basic_info.get('profile_url')
    if profile_url:
        basic_info['profile_id'] = extract_profile_id(profile_url)
        basic_info['vanity_name'] = extract_vanity_name(profile_url)
    
    # Extract profile metadata
    profile_metadata = extract_profile_metadata(soup)
    
    # Extract additional JSON-LD data
    languages = []
    member_of = []
    if json_ld:
        if json_ld.get('knowsLanguage'):
            for lang in json_ld['knowsLanguage']:
                if isinstance(lang, dict):
                    languages.append({
                        'name': lang.get('name', str(lang)),
                        'proficiency': None
                    })
                else:
                    languages.append({
                        'name': str(lang),
                        'proficiency': None
                    })
        if json_ld.get('memberOf'):
            for org in json_ld['memberOf']:
                if isinstance(org, dict):
                    member_of.append({
                        'name': org.get('name', ''),
                        'url': org.get('url', '')
                    })
    
    # Try to extract languages from HTML if not found in JSON-LD (enhanced)
    if not languages:
        languages_section = soup.find('section', {'data-section': 'languages'}) or \
                          soup.find('section', class_=re.compile(r'language', re.I))
        
        # Try alternative selectors for new format
        if not languages_section:
            languages_section = (soup.find('div', attrs={'data-view-name': re.compile(r'language', re.I)}) or
                               soup.find('div', attrs={'componentkey': re.compile(r'language', re.I)}))
        
        if languages_section:
            lang_items = languages_section.find_all('li', class_='profile-section-card')
            
            # Also try finding with obfuscated classes
            if not lang_items:
                lang_items = languages_section.find_all('li', class_=re.compile(r'card|item', re.I))
            
            # Also try finding by componentkey
            if not lang_items:
                lang_items = languages_section.find_all(attrs={'componentkey': re.compile(r'language', re.I)})
            
            for item in lang_items:
                lang = {
                    'name': None,
                    'proficiency': None
                }
                # Extract language name (multiple methods)
                name_elem = item.find('h3') or item.find('span') or item.find('div')
                if name_elem:
                    lang['name'] = clean_text(name_elem.get_text())
                
                # Try to extract proficiency (multiple methods)
                # Method 1: From span with proficiency class
                proficiency_elem = item.find('span', class_=re.compile(r'proficiency', re.I))
                if proficiency_elem:
                    lang['proficiency'] = clean_text(proficiency_elem.get_text())
                
                # Method 2: From aria-label
                if not lang['proficiency']:
                    proficiency_aria = item.find(attrs={'aria-label': re.compile(r'proficiency|level', re.I)})
                    if proficiency_aria:
                        aria_text = proficiency_aria.get('aria-label', '')
                        proficiency_match = re.search(r'(?:proficiency|level)[:\s]+(.+)', aria_text, re.I)
                        if proficiency_match:
                            lang['proficiency'] = clean_text(proficiency_match.group(1))
                
                # Method 3: From text patterns
                if not lang['proficiency']:
                    item_text = clean_text(item.get_text())
                    proficiency_patterns = [
                        r'(?:proficiency|level)[:\s]+(native|fluent|conversational|basic|beginner|intermediate|advanced|professional)',
                        r'(native|fluent|conversational|basic|beginner|intermediate|advanced|professional)\s+(?:proficiency|level)',
                    ]
                    for pattern in proficiency_patterns:
                        prof_match = re.search(pattern, item_text, re.I)
                        if prof_match:
                            lang['proficiency'] = clean_text(prof_match.group(1))
                            break
                
                if lang['name']:
                    languages.append(lang)
    
    # Note: Languages will be extracted from about_text later in the extraction process
    
    # Extract all information (with error handling)
    try:
        experience_data = extract_experience(json_ld, soup)
    except Exception as e:
        experience_data = []
    
    try:
        education_data = extract_education(json_ld, soup)
    except Exception as e:
        education_data = []
    
    try:
        about_text = extract_about(soup) or ''
    except Exception as e:
        about_text = ''
    
    # Extract languages from about_text if not already found
    languages = extract_languages_from_about(languages, about_text)
    
    # #region agent log
    log_debug("scrape_linkedin_profile:extractions", "Section extractions", {
        "experience_count": len(experience_data),
        "education_count": len(education_data),
        "has_experience": len(experience_data) > 0,
        "has_education": len(education_data) > 0,
        "about_length": len(about_text)
    }, "C")
    # #endregion
    
    # Extract all sections with error handling
    def safe_extract_section(extract_func, *args):
        try:
            return extract_func(*args)
        except Exception as e:
            # Return appropriate default based on return type annotation
            try:
                sig = inspect.signature(extract_func)
                return_annotation = sig.return_annotation
                annotation_str = str(return_annotation)
                
                # Check if return type is annotated as List
                if 'List' in annotation_str or (hasattr(return_annotation, '__origin__') and return_annotation.__origin__ is list):
                    return []
                
                # Check if return type is annotated as Dict
                if 'Dict' in annotation_str or (hasattr(return_annotation, '__origin__') and return_annotation.__origin__ is dict):
                    return {}
            except (ValueError, TypeError):
                # If signature inspection fails, use function name pattern
                pass
            
            # Fallback: check function name for common patterns
            func_name = extract_func.__name__
            if any(keyword in func_name for keyword in ['contact', 'open_to_work', 'metadata', 'data_attributes']):
                return {}
            
            # Default to empty list for most extract functions
            return []
    
    profile_data = {
        'basic_info': basic_info,
        'page_metadata': page_metadata,
        'profile_metadata': profile_metadata,
        'experience': experience_data,
        'education': education_data,
        'volunteer_experience': safe_extract_section(extract_volunteer_experience, soup),
        'awards': safe_extract_section(extract_awards, json_ld, soup),
        'certifications': safe_extract_section(extract_certifications, soup),
        'licenses': safe_extract_section(extract_licenses, soup),
        'projects': safe_extract_section(extract_projects, soup),
        'publications': safe_extract_section(extract_publications, soup),
        'skills': safe_extract_section(extract_skills_enhanced, soup, about_text),
        'languages': extract_languages_from_about(languages, about_text),
        'websites': safe_extract_section(extract_websites, soup),
        'contact_info': safe_extract_section(extract_contact_info, soup),
        'about': about_text,
        'activities': safe_extract_section(extract_activities, soup),
        'recommendations': safe_extract_section(extract_recommendations, soup),
        'mutual_connections': safe_extract_section(extract_mutual_connections, soup),
        'same_name_profiles': safe_extract_section(extract_same_name_profiles, soup),
        'course_recommendations': safe_extract_section(extract_course_recommendations, soup),
        'organizations': safe_extract_section(extract_organizations, soup) or member_of,
        'interests': safe_extract_section(extract_interests, soup),
        'groups': safe_extract_section(extract_groups, soup),
        'featured_content': safe_extract_section(extract_featured_content, soup),
        'services': safe_extract_section(extract_services, soup),
        'open_to_work': safe_extract_section(extract_open_to_work, soup),
        'patents': safe_extract_section(extract_patents, soup),
        'test_scores': safe_extract_section(extract_test_scores, soup),
        'accomplishments': safe_extract_section(extract_accomplishments, soup),
        'people_also_viewed': safe_extract_section(extract_people_also_viewed, soup),
        'related_posts': safe_extract_section(extract_related_posts, soup),
        'comprehensive_json_ld': comprehensive_json_ld,
        'data_attributes': safe_extract_section(extract_data_attributes, soup),
        'extraction_metadata': {
            'source_file': html_file_path,
            'has_json_ld': json_ld is not None,
            'html_format': detect_html_format(soup),
            'extraction_timestamp': datetime.now().isoformat()
        }
    }
    
    return profile_data

# Main execution
if __name__ == "__main__":
    import sys
    
    # Define HTML files to process
    html_files = ["linkdin1.html", "linkdin2.html", "linkdin3.html"]
    
    # Base directory for HTML files (input)
    base_paths = [
        Path("scripts/html/linkdin profile"),
        Path.cwd() / "scripts" / "html" / "linkdin profile",
        Path("html/linkdin profile"),
        Path.cwd() / "html" / "linkdin profile",
    ]
    
    # Find the base directory for HTML input files
    base_dir = None
    for path in base_paths:
        if path.exists():
            base_dir = path
            break
    
    if not base_dir:
        error_output = json.dumps({
            "error": f"HTML directory not found. Tried: {[str(p) for p in base_paths]}"
        }, indent=2)
        print(error_output)
        sys.exit(1)
    
    # Output directory for JSON files - use "scripts/output/linkdin profile"
    output_paths = [
        Path("scripts/output/linkdin profile"),
        Path.cwd() / "scripts" / "output" / "linkdin profile",
    ]
    
    # Find or create output directory
    output_dir = None
    for path in output_paths:
        if path.exists():
            output_dir = path
            break
    
    # If output directory doesn't exist, create it
    if not output_dir:
        output_dir = Path.cwd() / "scripts" / "output" / "linkdin profile"
        output_dir.mkdir(parents=True, exist_ok=True)
    
    # Process each HTML file
    for html_filename in html_files:
        html_file = base_dir / html_filename
        
        if not html_file.exists():
            print(f"Warning: {html_file} not found, skipping...", file=sys.stderr)
            continue
        
        try:
            # Scrape the profile
            profile_data = scrape_linkedin_profile(str(html_file))
            
            # Generate output filename
            output_filename = html_filename.replace('.html', '_profile.json')
            output_file = output_dir / output_filename
            
            # Save to JSON file
            with open(output_file, 'w', encoding='utf-8') as f:
                json.dump(profile_data, f, indent=2, ensure_ascii=False)
            
            print(f"Successfully scraped {html_filename} and saved to {output_file}", file=sys.stderr)
            
        except Exception as e:
            error_output = json.dumps({
                "error": f"Error processing {html_filename}",
                "message": str(e)
            }, indent=2)
            print(error_output, file=sys.stderr)
            continue
