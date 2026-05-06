import requests
from bs4 import BeautifulSoup
import random
import pandas as pd 
import time
import urllib3
from datetime import datetime, timedelta
import re
import json
from openai import OpenAI
from concurrent.futures import ThreadPoolExecutor, as_completed
import threading

# Thread-safe lock for shared variables
lock = threading.Lock()


openai_key = "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"

# Suppress insecure request warnings when using verify=False
urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)

# TODO: Add your OpenAI API key here
OPENAI_API_KEY = openai_key

# Initialize OpenAI client (will be None if key not set)
openai_client = None
if OPENAI_API_KEY and OPENAI_API_KEY != "YOUR_OPENAI_API_KEY_HERE":
    openai_client = OpenAI(api_key=OPENAI_API_KEY)

# Read system prompt
SYSTEM_PROMPT = ""
try:
    with open("prompt.txt", "r") as f:
        SYSTEM_PROMPT = f.read()
except FileNotFoundError:
    print("Warning: prompt.txt not found. OpenAI enrichment will be skipped.")

def parse_relative_time(time_text):
    """Convert relative time strings like '2 days ago' to exact date"""
    if not time_text:
        return None
    
    time_text = time_text.lower().strip()
    now = datetime.now()
    
    # Handle "just now" or " moments ago"
    if "just now" in time_text or "moment" in time_text:
        return now.strftime("%Y-%m-%d")
    
    # Extract number and unit using regex
    match = re.search(r'(\d+)\s+(minute|hour|day|week|month|year)s?\s*ago', time_text)
    if match:
        num = int(match.group(1))
        unit = match.group(2)
        
        if unit == "minute":
            delta = timedelta(minutes=num)
        elif unit == "hour":
            delta = timedelta(hours=num)
        elif unit == "day":
            delta = timedelta(days=num)
        elif unit == "week":
            delta = timedelta(weeks=num)
        elif unit == "month":
            delta = timedelta(days=num * 30)  # Approximate
        elif unit == "year":
            delta = timedelta(days=num * 365)  # Approximate
        else:
            return None
            
        exact_date = now - delta
        return exact_date.strftime("%Y-%m-%d")
    
    # Handle "today"
    if "today" in time_text:
        return now.strftime("%Y-%m-%d")
    
    # Handle "yesterday"
    if "yesterday" in time_text:
        return (now - timedelta(days=1)).strftime("%Y-%m-%d")
    
    return None

title = "golang developer"
location = "United States"

# SmartProxy configuration
PROXY_ADDR = "http://smart-xbevuxpgad73:9ozTxFRupD7S2xru@proxy.smartproxy.net:3121"
PROXIES = {
    "http": PROXY_ADDR,
    "https": PROXY_ADDR,
}

def fetch_with_retry(url, proxies, max_retries=3):
    for attempt in range(max_retries):
        try:
            # Set verify=False to ignore SSL certificate verification errors often caused by proxies
            response = requests.get(url, proxies=proxies, timeout=15, verify=False)
            if response.status_code == 200:
                return response
            print(f"Attempt {attempt + 1} failed: Status {response.status_code}")
        except Exception as e:
            print(f"Attempt {attempt + 1} failed: {e}")
        
        if attempt < max_retries - 1:
            time.sleep(random.uniform(2, 5))
    return None

def normalize_linkedin_url(url):
    """Convert country-specific LinkedIn URLs to standard linkedin.com format"""
    if not url:
        return url
    # Pattern: https://xx.linkedin.com/company/... → https://linkedin.com/company/...
    import re
    return re.sub(r'https?://[^/]+\.linkedin\.com/', 'https://linkedin.com/', url)

def enrich_batch_with_websites(job_list, model="gpt-4-turbo"):
    """
    Send batch of jobs to OpenAI to get company websites.
    Returns job_list with official_website and website_confidence populated.
    """
    if not openai_client or not SYSTEM_PROMPT:
        return job_list
    
    # Get unique companies from this batch (deduplicate by company_name)
    unique_companies = {}
    for job in job_list:
        company_name = job.get("company_name")
        linkedin_url = job.get("company_linkedin_url")
        if company_name and company_name not in unique_companies:
            unique_companies[company_name] = linkedin_url
    
    if not unique_companies:
        return job_list
    
    # Prepare input for OpenAI
    companies_json = [
        {"company_name": name, "linkedin_url": url}
        for name, url in unique_companies.items()
    ]
    
    print(f"    Sending {len(companies_json)} unique companies to OpenAI...")
    
    try:
        response = openai_client.chat.completions.create(
            model=model,
            messages=[
                {"role": "system", "content": SYSTEM_PROMPT},
                {"role": "user", "content": json.dumps(companies_json)}
            ],
            temperature=0.1,
            max_tokens=2000
        )
        
        # Parse response
        result_text = response.choices[0].message.content.strip()
        
        # Clean up any markdown code blocks
        if result_text.startswith("```json"):
            result_text = result_text[7:]
        if result_text.endswith("```"):
            result_text = result_text[:-3]
        results = json.loads(result_text)
        
        # Create lookup dicts by company name (normalized) and LinkedIn URL
        website_lookup_by_name = {}
        website_lookup_by_url = {}
        for r in results:
            name = r.get("company_name", "").strip()
            linkedin_url = normalize_linkedin_url(r.get("linkedin_url", "").strip())
            data = {
                "official_website": r.get("official_website"),
                "confidence": r.get("confidence")
            }
            if name:
                website_lookup_by_name[name.lower()] = data
            if linkedin_url:
                website_lookup_by_url[linkedin_url.lower()] = data
        
        # Map results back to all jobs in batch
        enriched_count = 0
        unmatched_companies = []
        for job in job_list:
            company_name = job.get("company_name", "").strip()
            linkedin_url = job.get("company_linkedin_url", "").strip()
            data = None
            
            # Try matching by name first (case-insensitive)
            if company_name and company_name.lower() in website_lookup_by_name:
                data = website_lookup_by_name[company_name.lower()]
            # Fallback: match by LinkedIn URL (case-insensitive)
            elif linkedin_url and linkedin_url.lower() in website_lookup_by_url:
                data = website_lookup_by_url[linkedin_url.lower()]
            else:
                # Track unmatched for debugging
                if company_name:
                    unmatched_companies.append(f"'{company_name}' (URL: {linkedin_url})")
            
            if data:
                job["official_website"] = data.get("official_website")
                job["website_confidence"] = data.get("confidence")
                if data.get("official_website"):
                    enriched_count += 1
        
        print(f"    ✓ Enriched {enriched_count}/{len(job_list)} jobs with websites")
        if unmatched_companies:
            print(f"    ⚠ Unmatched ({len(unmatched_companies)}): {', '.join(unmatched_companies[:5])}")
        
        # Rate limiting
        time.sleep(0.5)
        
    except Exception as e:
        print(f"    ✗ OpenAI API error: {e}")
    
    return job_list

id_list = []
start = 0
CSV_FILE = "test9.csv"
MAX_JOBS = None  # Scrape all available jobs (no limit)
jobs_collected = 0
geo_id = 105080838
BATCH_SIZE = 25  # Process OpenAI enrichment in batches of 25

# Job buffer to accumulate jobs before batch processing
job_buffer = []

def save_batch_to_csv(batch_list):
    """Save a batch of jobs to CSV with enrichment, sorted by confidence (low to high)"""
    if not batch_list:
        return
    
    # Enrich with OpenAI if available
    if openai_client and SYSTEM_PROMPT:
        print(f"\n  Enriching batch of {len(batch_list)} jobs with OpenAI...")
        batch_list = enrich_batch_with_websites(batch_list)
    
    # Sort by confidence: low -> medium -> high -> None
    confidence_order = {"low": 0, "medium": 1, "high": 2}
    batch_list.sort(key=lambda x: confidence_order.get(x.get("website_confidence"), 3))
    
    # Save to CSV
    columns = [
        "company_name", "company_linkedin_url", "linkedin_job_url", "official_website", "website_confidence",
        "job_title", "job_location", "time_posted", "num_applicants", "salary_range",
        "seniority_level", "employment_type", "job_function", "industry", "job_description"
    ]
    pd.DataFrame(batch_list, columns=columns).to_csv(CSV_FILE, mode='a', header=False, index=False)
    print(f"  ✓ Saved {len(batch_list)} jobs to {CSV_FILE} (sorted: low → high confidence)")

# Clear or create the file with headers
pd.DataFrame(columns=[
    "company_name", 
    "company_linkedin_url",
    "linkedin_job_url",
    "official_website",
    "website_confidence",
    "job_title", 
    "job_location",
    "time_posted", 
    "num_applicants",
    "salary_range",
    "seniority_level",
    "employment_type",
    "job_function",
    "industry",
    "job_description"
]).to_csv(CSV_FILE, index=False)

while MAX_JOBS is None or jobs_collected < MAX_JOBS:
    print(f"Fetching jobs starting from {start}...")
    jobs_url = f"https://www.linkedin.com/jobs/search/?&f_TPR=r3600&geoId={geo_id}&keywords=developer%20OR%20engineer%20OR%20software&origin=JOB_SEARCH_PAGE_JOB_FILTER&refresh=true&sortBy=R&spellCorrectionEnabled=true&start={start}"
    # jobs_url = f"https://www.linkedin.com/jobs-guest/jobs/api/seeMoreJobPostings/search?keywords=Golang%2BDeveloper&location=United%2BStates&start={start}"
    response = fetch_with_retry(jobs_url, PROXIES)
    if not response:
        print(f"Failed to fetch jobs starting from {start} after retries.")
        break
    list_data = response.text
    list_soup = BeautifulSoup(list_data, "html.parser")
    page_jobs = list_soup.find_all("li")
    page_id_list = []
    
    if not page_jobs:
        print("No more jobs found.")
        break
    
    found_valid_job = False
    for job in page_jobs:
        base_card_div = job.find("div", {"class": "base-card"})
        if base_card_div is None:
            continue
        
        entity_urn = base_card_div.get("data-entity-urn")
        if not entity_urn or not isinstance(entity_urn, str):
            continue
        
        job_id = entity_urn.split(":")[3]
        page_id_list.append(job_id)
        found_valid_job = True

    if not found_valid_job:
        print("No valid jobs found on this page.")
        break
    
    print(f"Found {len(page_id_list)} jobs on this page.")
    
    def fetch_job_details(job_id):
        """Fetch details for a single job - runs in parallel"""
        job_post = {
            "company_name": None,
            "company_linkedin_url": None,
            "linkedin_job_url": None,
            "official_website": None,
            "website_confidence": None,
            "job_title": None,
            "job_location": None,
            "time_posted": None,
            "num_applicants": None,
            "salary_range": None,
            "seniority_level": None,
            "employment_type": None,
            "job_function": None,
            "industry": None,
            "job_description": None
        }
        job_url = f"https://www.linkedin.com/jobs-guest/jobs/api/jobPosting/{job_id}"
        job_response = fetch_with_retry(job_url, PROXIES)
        
        if not job_response:
            return None
            
        job_soup = BeautifulSoup(job_response.text, "html.parser")
        
        # LinkedIn Job URL
        try:
            job_link_tag = job_soup.find("a", {"class": "topcard__link"})
            if job_link_tag:
                job_post["linkedin_job_url"] = job_link_tag.get("href", "").split("?")[0]
        except:
            pass
        
        # Company Name & LinkedIn URL
        company_tag = job_soup.find("a", {"class": "topcard__org-name-link topcard__flavor--black-link"})
        if company_tag:
            job_post["company_name"] = company_tag.text.strip()
            raw_url = company_tag.get("href", "").split("?")[0]
            job_post["company_linkedin_url"] = normalize_linkedin_url(raw_url)

        # Job Description
        try:
            desc_div = job_soup.find("div", {"class": "description__text description__text--rich"})
            if desc_div:
                job_post["job_description"] = desc_div.get_text(separator=' ', strip=True)
        except:
            pass

        # Job Title
        try:
            job_post["job_title"] = job_soup.find("h2", {"class":"top-card-layout__title font-sans text-lg papabear:text-xl font-bold leading-open text-color-text mb-0 topcard__title"}).text.strip()
        except:
            pass

        # Job Location
        try:
            location_span = job_soup.find("span", {"class": "topcard__flavor topcard__flavor--bullet"})
            job_post["job_location"] = location_span.text.strip() if location_span else None
        except:
            pass

        # Time Posted - convert to exact date
        try:
            time_text = job_soup.find("span", {"class": "posted-time-ago__text topcard__flavor--metadata"}).text.strip()
            job_post["time_posted"] = parse_relative_time(time_text)
        except:
            pass

        # Number of Applicants
        try:
            job_post["num_applicants"] = job_soup.find("span", {"class": "num-applicants__caption topcard__flavor--metadata topcard__flavor--bullet"}).text.strip()
        except:
            job_post["num_applicants"] = 0

        # Salary Range
        try:
            salary_div = job_soup.find("div", {"class": "salary compensation__salary"})
            job_post["salary_range"] = salary_div.text.strip() if salary_div else None
        except:
            pass

        # Job Criteria (Seniority, Employment Type, Job Function, Industry)
        try:
            criteria_items = job_soup.find_all("li", {"class": "description__job-criteria-item"})
            for item in criteria_items:
                header = item.find("h3", {"class": "description__job-criteria-subheader"})
                value = item.find("span", {"class": "description__job-criteria-text--criteria"})
                if header and value:
                    header_text = header.text.strip().lower()
                    value_text = value.text.strip()
                    if "seniority" in header_text:
                        job_post["seniority_level"] = value_text
                    elif "employment" in header_text:
                        job_post["employment_type"] = value_text
                    elif "job function" in header_text:
                        job_post["job_function"] = value_text
                    elif "industries" in header_text:
                        job_post["industry"] = value_text
        except:
            pass
        
        return job_post
    
    # Fetch all jobs from this page (no limit)
    
    print(f"  Fetching {len(page_id_list)} jobs concurrently with 10 workers...")
    
    # Fetch jobs concurrently
    with ThreadPoolExecutor(max_workers=10) as executor:
        future_to_job = {executor.submit(fetch_job_details, job_id): job_id for job_id in page_id_list}
        
        for future in as_completed(future_to_job):
            job_id = future_to_job[future]
            try:
                job_post = future.result()
                if job_post:
                    with lock:
                        job_buffer.append(job_post)
                        jobs_collected += 1
                        current_buffer = len(job_buffer)
                        current_total = jobs_collected
                    print(f"  ✓ Job {job_id} fetched ({current_total} total, buffer: {current_buffer}/{BATCH_SIZE})")
                    
                    # Process batch when we reach BATCH_SIZE
                    if current_buffer >= BATCH_SIZE:
                        with lock:
                            batch_to_save = job_buffer.copy()
                            job_buffer = []
                        save_batch_to_csv(batch_to_save)
                else:
                    print(f"  ✗ Job {job_id} failed")
            except Exception as e:
                print(f"  ✗ Job {job_id} error: {e}")

    # Advance start by actual number of jobs found (not fixed 10)
    start += len(page_id_list)
    time.sleep(random.uniform(1, 3)) # Respectful delay

# Process any remaining jobs in buffer after loop ends
if job_buffer:
    print(f"\nProcessing final batch of {len(job_buffer)} jobs...")
    save_batch_to_csv(job_buffer)
