import pandas as pd
import json
import time
from openai import OpenAI

# TODO: Add your OpenAI API key here
OPENAI_API_KEY = "YOUR_OPENAI_API_KEY_HERE"

# Initialize OpenAI client
client = OpenAI(api_key=OPENAI_API_KEY)

# Read prompt from file
with open("prompt.txt", "r") as f:
    SYSTEM_PROMPT = f.read()


def read_prompt():
    """Read the system prompt from prompt.txt"""
    with open("prompt.txt", "r") as f:
        return f.read()


def enrich_companies_with_websites(csv_file, batch_size=25, model="gpt-4o-mini"):
    """
    Read CSV, batch companies, call OpenAI to get websites, update CSV.
    
    Args:
        csv_file: Path to the CSV file
        batch_size: Number of companies to send per API call (default 25)
        model: OpenAI model to use
    """
    # Read CSV
    df = pd.read_csv(csv_file)
    
    # Check if website column exists, if not create it
    if "official_website" not in df.columns:
        df["official_website"] = None
    if "website_confidence" not in df.columns:
        df["website_confidence"] = None
    
    # Get rows without website data
    missing_websites = df[df["official_website"].isna()].copy()
    
    if missing_websites.empty:
        print("All companies already have website data.")
        return
    
    print(f"Found {len(missing_websites)} companies needing website enrichment")
    
    # Process in batches
    total_processed = 0
    for i in range(0, len(missing_websites), batch_size):
        batch = missing_websites.iloc[i:i+batch_size]
        batch_num = (i // batch_size) + 1
        total_batches = (len(missing_websites) + batch_size - 1) // batch_size
        
        print(f"\nProcessing batch {batch_num}/{total_batches} ({len(batch)} companies)...")
        
        # Prepare JSON input for OpenAI
        companies_json = []
        for idx, row in batch.iterrows():
            companies_json.append({
                "company_name": row["company_name"],
                "linkedin_url": row["company_linkedin_url"]
            })
        
        # Call OpenAI API
        try:
            response = client.chat.completions.create(
                model=model,
                messages=[
                    {"role": "system", "content": SYSTEM_PROMPT},
                    {"role": "user", "content": json.dumps(companies_json)}
                ],
                temperature=0.1,  # Low temperature for consistent results
                max_tokens=2000
            )
            
            # Parse response
            result_text = response.choices[0].message.content.strip()
            
            # Clean up any markdown code blocks if present
            if result_text.startswith("```json"):
                result_text = result_text[7:]
            if result_text.endswith("```"):
                result_text = result_text[:-3]
            result_text = result_text.strip()
            
            # Parse JSON
            try:
                results = json.loads(result_text)
            except json.JSONDecodeError as e:
                print(f"  Error parsing JSON: {e}")
                print(f"  Raw response: {result_text[:200]}...")
                continue
            
            # Validate response length matches batch
            if len(results) != len(batch):
                print(f"  Warning: Response count ({len(results)}) doesn't match batch size ({len(batch)})")
            
            # Map results back to DataFrame
            for idx, (df_idx, row) in enumerate(batch.iterrows()):
                if idx < len(results):
                    result = results[idx]
                    df.at[df_idx, "official_website"] = result.get("official_website")
                    df.at[df_idx, "website_confidence"] = result.get("confidence")
                    
                    website = result.get("official_website", "N/A")
                    confidence = result.get("confidence", "unknown")
                    print(f"  ✓ {row['company_name']}: {website} ({confidence})")
                else:
                    print(f"  ✗ {row['company_name']}: No result returned")
            
            total_processed += len(batch)
            
            # Save progress after each batch
            df.to_csv(csv_file, index=False)
            print(f"  Saved progress: {total_processed} companies processed")
            
            # Rate limiting - be nice to the API
            if i + batch_size < len(missing_websites):
                time.sleep(1)
                
        except Exception as e:
            print(f"  Error calling OpenAI API: {e}")
            continue
    
    print(f"\n✅ Done! Enriched {total_processed} companies with website data.")
    print(f"Updated file: {csv_file}")


def get_website_for_single_company(company_name, linkedin_url, model="gpt-4o-mini"):
    """
    Get website for a single company (utility function).
    
    Returns:
        dict with official_website and confidence, or None on error
    """
    companies_json = [{
        "company_name": company_name,
        "linkedin_url": linkedin_url
    }]
    
    try:
        response = client.chat.completions.create(
            model=model,
            messages=[
                {"role": "system", "content": SYSTEM_PROMPT},
                {"role": "user", "content": json.dumps(companies_json)}
            ],
            temperature=0.1,
            max_tokens=500
        )
        
        result_text = response.choices[0].message.content.strip()
        
        # Clean up markdown
        if result_text.startswith("```json"):
            result_text = result_text[7:]
        if result_text.endswith("```"):
            result_text = result_text[:-3]
        result_text = result_text.strip()
        
        results = json.loads(result_text)
        
        if results and len(results) > 0:
            return {
                "official_website": results[0].get("official_website"),
                "confidence": results[0].get("confidence")
            }
        return None
        
    except Exception as e:
        print(f"Error: {e}")
        return None


if __name__ == "__main__":
    # Example usage
    CSV_FILE = "test2.csv"  # Change to your CSV file
    
    # Check if API key is set
    if OPENAI_API_KEY == "YOUR_OPENAI_API_KEY_HERE" or not OPENAI_API_KEY:
        print("⚠️  Please set your OpenAI API key in OPENAI_API_KEY variable")
        print("   Edit this file and replace 'YOUR_OPENAI_API_KEY_HERE' with your actual key")
        exit(1)
    
    # Run enrichment
    enrich_companies_with_websites(CSV_FILE, batch_size=25)
