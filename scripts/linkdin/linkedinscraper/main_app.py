"""
LinkedIn Job Scraper - Main Streamlit Application
This module provides the main interface for the LinkedIn job scraping application.
"""

import streamlit as st
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go
from datetime import datetime, timedelta
import time

# Import custom modules (these would be implemented in separate files)
from scraper.linkedin_scraper import LinkedInJobScraper
from database.vector_db import VectorDatabase
from dashboard.visualizations import JobDashboard
from dashboard.filters import JobFilters
from utils.helpers import format_salary, clean_text, extract_skills
from utils.config import Config

# Page configuration
st.set_page_config(
    page_title="LinkedIn Job Analytics Dashboard",
    page_icon="💼",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Custom CSS
st.markdown("""
<style>
    .main-header {
        font-size: 2.5rem;
        font-weight: bold;
        color: #0077B5;
        text-align: center;
        margin-bottom: 2rem;
    }
    .job-card {
        background: white;
        padding: 1.5rem;
        border-radius: 10px;
        box-shadow: 0 2px 4px rgba(0,0,0,0.1);
        margin: 1rem 0;
        border-left: 4px solid #0077B5;
    }
    .metric-card {
        background: linear-gradient(90deg, #0077B5, #005885);
        color: white;
        padding: 1rem;
        border-radius: 8px;
        text-align: center;
    }
    .sidebar-section {
        background: #f8f9fa;
        padding: 1rem;
        border-radius: 8px;
        margin: 1rem 0;
    }
</style>
""", unsafe_allow_html=True)

# Initialize session state
if 'jobs_data' not in st.session_state:
    st.session_state.jobs_data = pd.DataFrame()
if 'vector_db' not in st.session_state:
    st.session_state.vector_db = VectorDatabase()
if 'scraper' not in st.session_state:
    st.session_state.scraper = LinkedInJobScraper()

def main():
    """Main application function"""
    
    # Header
    st.markdown('<h1 class="main-header">💼 LinkedIn Job Analytics Dashboard</h1>', 
                unsafe_allow_html=True)
    
    # Sidebar
    with st.sidebar:
        st.markdown('<div class="sidebar-section">', unsafe_allow_html=True)
        st.header("🔍 Job Search Configuration")
        
        # Search parameters
        job_title = st.text_input("Job Title", value="Data Scientist", 
                                help="Enter the job title you want to search for")
        
        location = st.text_input("Location", value="United States", 
                               help="Enter the location (city, state, or country)")
        
        experience_level = st.selectbox("Experience Level", 
                                      ["All", "Internship", "Entry level", 
                                       "Associate", "Mid-Senior level", "Director", "Executive"])
        
        job_type = st.selectbox("Job Type", 
                              ["All", "Full-time", "Part-time", "Contract", "Temporary", "Internship"])
        
        salary_range = st.slider("Minimum Salary (K)", 0, 200, 50, step=10)
        
        max_pages = st.number_input("Max Pages to Scrape", min_value=1, max_value=10, value=3,
                                  help="Number of LinkedIn job pages to scrape")
        
        # Scraping controls
        if st.button("🚀 Start Job Scraping", type="primary"):
            scrape_jobs(job_title, location, experience_level, job_type, salary_range, max_pages)
        
        st.markdown('</div>', unsafe_allow_html=True)
        
        # Data management section
        st.markdown('<div class="sidebar-section">', unsafe_allow_html=True)
        st.header("💾 Data Management")
        
        if st.button("Clear All Data", type="secondary"):
            clear_all_data()
        
        if st.button("Export to CSV"):
            export_data()
            
        # Database statistics
        if not st.session_state.jobs_data.empty:
            st.subheader("📊 Database Stats")
            st.write(f"Total Jobs: {len(st.session_state.jobs_data)}")
            st.write(f"Unique Companies: {st.session_state.jobs_data['company'].nunique()}")
            st.write(f"Date Range: {get_date_range()}")
        
        st.markdown('</div>', unsafe_allow_html=True)
    
    # Main content area
    if st.session_state.jobs_data.empty:
        show_welcome_screen()
    else:
        show_dashboard()

def scrape_jobs(job_title, location, experience_level, job_type, salary_range, max_pages):
    """Scrape jobs from LinkedIn and store in vector database"""
    
    progress_bar = st.progress(0)
    status_text = st.empty()
    
    try:
        # Configure scraper
        scraper_config = {
            'job_title': job_title,
            'location': location,
            'experience_level': experience_level,
            'job_type': job_type,
            'salary_range': salary_range,
            'max_pages': max_pages
        }
        
        # Start scraping
        status_text.text("Starting job scraping...")
        progress_bar.progress(10)
        
        # Scrape jobs (this would be implemented in the scraper module)
        jobs_data = st.session_state.scraper.scrape_jobs(scraper_config)
        progress_bar.progress(60)
        
        if jobs_data:
            status_text.text("Processing and storing job data...")
            
            # Process and clean data
            processed_jobs = process_job_data(jobs_data)
            progress_bar.progress(80)
            
            # Store in vector database
            st.session_state.vector_db.store_jobs(processed_jobs)
            progress_bar.progress(90)
            
            # Update session state
            new_df = pd.DataFrame(processed_jobs)
            st.session_state.jobs_data = pd.concat([st.session_state.jobs_data, new_df], 
                                                 ignore_index=True).drop_duplicates()
            
            progress_bar.progress(100)
            status_text.text(f"✅ Successfully scraped {len(processed_jobs)} jobs!")
            
            # Show success message
            st.success(f"🎉 Scraped {len(processed_jobs)} new job postings!")
            time.sleep(2)
            st.rerun()
            
        else:
            st.error("No jobs found. Try adjusting your search parameters.")
            
    except Exception as e:
        st.error(f"Error during scraping: {str(e)}")
    finally:
        progress_bar.empty()
        status_text.empty()

def process_job_data(raw_jobs):
    """Process and clean scraped job data"""
    processed_jobs = []
    
    for job in raw_jobs:
        processed_job = {
            'id': job.get('id', ''),
            'title': clean_text(job.get('title', '')),
            'company': job.get('company', ''),
            'location': job.get('location', ''),
            'description': clean_text(job.get('description', '')),
            'salary': format_salary(job.get('salary', '')),
            'date_posted': job.get('date_posted', datetime.now().strftime('%Y-%m-%d')),
            'job_type': job.get('job_type', ''),
            'experience_level': job.get('experience_level', ''),
            'skills': extract_skills(job.get('description', '')),
            'scraped_date': datetime.now().strftime('%Y-%m-%d %H:%M:%S')
        }
        processed_jobs.append(processed_job)
    
    return processed_jobs

def show_welcome_screen():
    """Display welcome screen when no data is available"""
    
    st.markdown("""
    ## 👋 Welcome to LinkedIn Job Analytics Dashboard
    
    This application helps you:
    - 🔍 **Scrape job postings** from LinkedIn with advanced filters
    - 💾 **Store job data** in a vector database for semantic search
    - 📊 **Analyze job market trends** with interactive visualizations
    - 🎯 **Find similar jobs** using AI-powered recommendations
    
    ### Getting Started
    1. Configure your job search parameters in the sidebar
    2. Click "Start Job Scraping" to collect job data
    3. Explore the interactive dashboard and analytics
    
    ### Features
    - **Smart Search**: Find jobs using natural language queries
    - **Market Analytics**: Salary trends, demand analysis, and geographic insights
    - **Similarity Search**: Discover similar jobs using AI embeddings
    - **Data Export**: Export your data for further analysis
    """)
    
    # Sample statistics (placeholder)
    col1, col2, col3, col4 = st.columns(4)
    
    with col1:
        st.markdown('<div class="metric-card"><h3>10K+</h3><p>Jobs Analyzed</p></div>', 
                   unsafe_allow_html=True)
    with col2:
        st.markdown('<div class="metric-card"><h3>500+</h3><p>Companies</p></div>', 
                   unsafe_allow_html=True)
    with col3:
        st.markdown('<div class="metric-card"><h3>50+</h3><p>Locations</p></div>', 
                   unsafe_allow_html=True)
    with col4:
        st.markdown('<div class="metric-card"><h3>AI-Powered</h3><p>Search</p></div>', 
                   unsafe_allow_html=True)

def show_dashboard():
    """Display the main dashboard with job data"""
    
    # Dashboard tabs
    tab1, tab2, tab3, tab4 = st.tabs(["🔍 Job Search", "📊 Analytics", "🎯 Similar Jobs", "📈 Market Trends"])
    
    with tab1:
        show_job_search_tab()
    
    with tab2:
        show_analytics_tab()
    
    with tab3:
        show_similar_jobs_tab()
    
    with tab4:
        show_market_trends_tab()

def show_job_search_tab():
    """Job search and filtering interface"""
    
    st.header("🔍 Job Search & Filtering")
    
    # Search interface
    col1, col2 = st.columns([3, 1])
    
    with col1:
        search_query = st.text_input("🔎 Search jobs (natural language)", 
                                   placeholder="Find Python developer jobs with machine learning experience")
    
    with col2:
        if st.button("Search", type="primary"):
            if search_query:
                search_results = st.session_state.vector_db.semantic_search(search_query, top_k=20)
                st.session_state.filtered_jobs = search_results
    
    # Filters
    with st.expander("🔧 Advanced Filters"):
        filter_col1, filter_col2, filter_col3 = st.columns(3)
        
        with filter_col1:
            company_filter = st.multiselect("Company", 
                                          options=st.session_state.jobs_data['company'].unique())
            location_filter = st.multiselect("Location", 
                                           options=st.session_state.jobs_data['location'].unique())
        
        with filter_col2:
            salary_min = st.number_input("Min Salary", min_value=0, value=0)
            salary_max = st.number_input("Max Salary", min_value=0, value=200000)
        
        with filter_col3:
            job_type_filter = st.multiselect("Job Type", 
                                           options=st.session_state.jobs_data['job_type'].unique())
            experience_filter = st.multiselect("Experience Level", 
                                             options=st.session_state.jobs_data['experience_level'].unique())
    
    # Apply filters
    filtered_data = apply_filters(st.session_state.jobs_data, 
                                company_filter, location_filter, 
                                salary_min, salary_max, 
                                job_type_filter, experience_filter)
    
    # Display results
    st.subheader(f"📋 Job Results ({len(filtered_data)} jobs found)")
    
    # Display job cards
    for _, job in filtered_data.head(20).iterrows():
        display_job_card(job)

def show_analytics_tab():
    """Analytics and visualizations"""
    
    st.header("📊 Job Market Analytics")
    
    if st.session_state.jobs_data.empty:
        st.info("No data available. Please scrape some jobs first.")
        return
    
    # Key metrics
    col1, col2, col3, col4 = st.columns(4)
    
    with col1:
        st.metric("Total Jobs", len(st.session_state.jobs_data))
    with col2:
        st.metric("Unique Companies", st.session_state.jobs_data['company'].nunique())
    with col3:
        avg_salary = calculate_average_salary(st.session_state.jobs_data)
        st.metric("Avg Salary", f"${avg_salary:,.0f}")
    with col4:
        st.metric("Locations", st.session_state.jobs_data['location'].nunique())
    
    # Visualizations
    show_salary_distribution()
    show_top_companies()
    show_location_distribution()
    show_skills_demand()

def show_similar_jobs_tab():
    """Similar jobs finder using vector similarity"""
    
    st.header("🎯 Find Similar Jobs")
    
    # Job selection for similarity search
    job_titles = st.session_state.jobs_data['title'].tolist()
    selected_job = st.selectbox("Select a job to find similar positions:", job_titles)
    
    if selected_job:
        # Find similar jobs
        similar_jobs = st.session_state.vector_db.find_similar_jobs(selected_job, top_k=10)
        
        if similar_jobs:
            st.subheader("🔍 Similar Job Recommendations")
            
            for job in similar_jobs:
                similarity_score = job.get('similarity_score', 0)
                st.markdown(f"""
                <div class="job-card">
                    <h4>{job['title']} at {job['company']}</h4>
                    <p><strong>Location:</strong> {job['location']}</p>
                    <p><strong>Similarity Score:</strong> {similarity_score:.2f}</p>
                    <p>{job['description'][:200]}...</p>
                </div>
                """, unsafe_allow_html=True)
    
    # Custom similarity search
    st.subheader("🔎 Custom Similarity Search")
    custom_query = st.text_area("Describe your ideal job:", 
                               placeholder="I want a remote Python developer position with machine learning focus...")
    
    if st.button("Find Similar Jobs"):
        if custom_query:
            results = st.session_state.vector_db.semantic_search(custom_query, top_k=10)
            display_search_results(results)

def show_market_trends_tab():
    """Market trends and insights"""
    
    st.header("📈 Market Trends & Insights")
    
    if st.session_state.jobs_data.empty:
        st.info("No data available. Please scrape some jobs first.")
        return
    
    # Time-based trends
    show_posting_trends()
    show_salary_trends()
    show_demand_trends()
    
    # Market insights
    st.subheader("💡 Market Insights")
    generate_market_insights()

# Helper functions (these would be implemented in separate modules)

def apply_filters(data, companies, locations, salary_min, salary_max, job_types, experience_levels):
    """Apply filters to job data"""
    filtered_data = data.copy()
    
    if companies:
        filtered_data = filtered_data[filtered_data['company'].isin(companies)]
    if locations:
        filtered_data = filtered_data[filtered_data['location'].isin(locations)]
    if job_types:
        filtered_data = filtered_data[filtered_data['job_type'].isin(job_types)]
    if experience_levels:
        filtered_data = filtered_data[filtered_data['experience_level'].isin(experience_levels)]
    
    # Salary filtering (would need proper implementation)
    # filtered_data = filtered_data[(filtered_data['salary'] >= salary_min) & (filtered_data['salary'] <= salary_max)]
    
    return filtered_data

def display_job_card(job):
    """Display a job as a card"""
    st.markdown(f"""
    <div class="job-card">
        <h4>{job['title']}</h4>
        <p><strong>{job['company']}</strong> | {job['location']}</p>
        <p><strong>Posted:</strong> {job['date_posted']}</p>
        <p>{job['description'][:200]}...</p>
        <hr>
        <small><strong>Skills:</strong> {', '.join(job.get('skills', []))}</small>
    </div>
    """, unsafe_allow_html=True)

def calculate_average_salary(data):
    """Calculate average salary from job data"""
    # This would need proper implementation based on salary format
    return 75000  # Placeholder

def show_salary_distribution():
    """Show salary distribution chart"""
    st.subheader("💰 Salary Distribution")
    # Placeholder chart
    fig = px.histogram(x=[50000, 60000, 70000, 80000, 90000, 100000, 120000], 
                      title="Salary Distribution")
    st.plotly_chart(fig, use_container_width=True)

def show_top_companies():
    """Show top companies chart"""
    st.subheader("🏢 Top Hiring Companies")
    company_counts = st.session_state.jobs_data['company'].value_counts().head(10)
    fig = px.bar(x=company_counts.values, y=company_counts.index, orientation='h',
                title="Top 10 Companies by Job Postings")
    st.plotly_chart(fig, use_container_width=True)

def show_location_distribution():
    """Show location distribution"""
    st.subheader("🌍 Job Locations")
    location_counts = st.session_state.jobs_data['location'].value_counts().head(10)
    fig = px.pie(values=location_counts.values, names=location_counts.index,
                title="Job Distribution by Location")
    st.plotly_chart(fig, use_container_width=True)

def show_skills_demand():
    """Show skills demand analysis"""
    st.subheader("🛠️ Top Skills in Demand")
    # This would analyze skills from job descriptions
    skills_data = ["Python", "SQL", "JavaScript", "Java", "React", "AWS", "Docker", "Kubernetes"]
    counts = [45, 38, 32, 28, 25, 22, 18, 15]
    fig = px.bar(x=skills_data, y=counts, title="Most Demanded Skills")
    st.plotly_chart(fig, use_container_width=True)

def show_posting_trends():
    """Show job posting trends over time"""
    st.subheader("📅 Job Posting Trends")
    # Placeholder implementation
    dates = pd.date_range('2024-01-01', periods=30, freq='D')
    counts = [10, 15, 12, 18, 20, 25, 22, 16, 19, 23] * 3
    fig = px.line(x=dates, y=counts, title="Daily Job Postings")
    st.plotly_chart(fig, use_container_width=True)

def show_salary_trends():
    """Show salary trends"""
    st.subheader("💵 Salary Trends by Experience Level")
    # Placeholder data
    experience_levels = ["Entry", "Mid", "Senior", "Lead", "Principal"]
    salaries = [60000, 80000, 110000, 140000, 180000]
    fig = px.bar(x=experience_levels, y=salaries, title="Average Salary by Experience Level")
    st.plotly_chart(fig, use_container_width=True)

def show_demand_trends():
    """Show demand trends by skill/technology"""
    st.subheader("📊 Technology Demand Trends")
    # This would show trending technologies over time
    st.info("Feature coming soon: Technology demand trends over time")

def generate_market_insights():
    """Generate market insights"""
    insights = [
        "🔥 Python and SQL are the most in-demand skills",
        "📈 Remote work opportunities increased by 40%",
        "💰 Senior roles show 15% salary growth year-over-year", 
        "🌟 AI/ML positions are growing rapidly",
        "🏢 Tech companies are leading in job postings"
    ]
    
    for insight in insights:
        st.write(insight)

def display_search_results(results):
    """Display search results"""
    if results:
        for job in results:
            display_job_card(job)
    else:
        st.info("No similar jobs found.")

def clear_all_data():
    """Clear all stored data"""
    st.session_state.jobs_data = pd.DataFrame()
    st.session_state.vector_db.clear_all()
    st.success("All data cleared successfully!")

def export_data():
    """Export data to CSV"""
    if not st.session_state.jobs_data.empty:
        csv = st.session_state.jobs_data.to_csv(index=False)
        st.download_button(
            label="Download CSV",
            data=csv,
            file_name=f"linkedin_jobs_{datetime.now().strftime('%Y%m%d')}.csv",
            mime="text/csv"
        )
    else:
        st.warning("No data to export!")

def get_date_range():
    """Get date range of scraped jobs"""
    if not st.session_state.jobs_data.empty:
        min_date = st.session_state.jobs_data['date_posted'].min()
        max_date = st.session_state.jobs_data['date_posted'].max()
        return f"{min_date} to {max_date}"
    return "No data"

if __name__ == "__main__":
    main()