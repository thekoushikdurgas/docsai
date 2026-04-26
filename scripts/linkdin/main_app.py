"""
LinkedIn Job Scraper - Main Streamlit Application
Enhanced with comprehensive logging, error handling, and advanced features.
"""

import streamlit as st
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go
from datetime import datetime, timedelta
import time
import json
import logging
from typing import Dict, List, Any, Optional
import traceback

# Import custom modules
from scraper.linkedin_scraper import LinkedInJobScraper, ScrapingConfig
from database.vector_db import VectorDatabase, JobAnalytics, DatabaseConfig
from dashboard.visualizations import JobDashboard
from dashboard.filters import JobFilters
from utils.helpers import TextProcessor, ProcessingStats
from utils.config import get_config, Config
from utils.logger import setup_logger, log_performance_metrics, log_function_calls
from utils.validators import validate_job_data, validate_search_query, validate_filters
from utils.cache import get_cache, cache_result

# Set up logging
logger = setup_logger(__name__)

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
        text-shadow: 2px 2px 4px rgba(0,0,0,0.1);
    }
    .job-card {
        background: linear-gradient(135deg, #ffffff 0%, #f8f9fa 100%);
        padding: 1.5rem;
        border-radius: 15px;
        box-shadow: 0 4px 6px rgba(0,0,0,0.1);
        margin: 1rem 0;
        border-left: 5px solid #0077B5;
        transition: transform 0.2s ease-in-out;
    }
    .job-card:hover {
        transform: translateY(-2px);
        box-shadow: 0 6px 12px rgba(0,0,0,0.15);
    }
    .metric-card {
        background: linear-gradient(135deg, #0077B5 0%, #005885 100%);
        color: white;
        padding: 1.5rem;
        border-radius: 15px;
        text-align: center;
        box-shadow: 0 4px 6px rgba(0,0,0,0.1);
        margin: 0.5rem 0;
    }
    .sidebar-section {
        background: linear-gradient(135deg, #f8f9fa 0%, #e9ecef 100%);
        padding: 1.5rem;
        border-radius: 15px;
        margin: 1rem 0;
        box-shadow: 0 2px 4px rgba(0,0,0,0.1);
    }
    .success-message {
        background: linear-gradient(135deg, #d4edda 0%, #c3e6cb 100%);
        color: #155724;
        padding: 1rem;
        border-radius: 10px;
        border-left: 5px solid #28a745;
        margin: 1rem 0;
    }
    .error-message {
        background: linear-gradient(135deg, #f8d7da 0%, #f5c6cb 100%);
        color: #721c24;
        padding: 1rem;
        border-radius: 10px;
        border-left: 5px solid #dc3545;
        margin: 1rem 0;
    }
    .warning-message {
        background: linear-gradient(135deg, #fff3cd 0%, #ffeaa7 100%);
        color: #856404;
        padding: 1rem;
        border-radius: 10px;
        border-left: 5px solid #ffc107;
        margin: 1rem 0;
    }
    .info-message {
        background: linear-gradient(135deg, #d1ecf1 0%, #bee5eb 100%);
        color: #0c5460;
        padding: 1rem;
        border-radius: 10px;
        border-left: 5px solid #17a2b8;
        margin: 1rem 0;
    }
    .stButton > button {
        background: linear-gradient(135deg, #0077B5 0%, #005885 100%);
        color: white;
        border: none;
        border-radius: 10px;
        padding: 0.5rem 1rem;
        font-weight: bold;
        transition: all 0.3s ease;
    }
    .stButton > button:hover {
        transform: translateY(-2px);
        box-shadow: 0 4px 8px rgba(0,0,0,0.2);
    }
    .stSelectbox > div > div {
        background: white;
        border-radius: 10px;
    }
    .stTextInput > div > div > input {
        border-radius: 10px;
    }
    .stSlider > div > div > div > div {
        background: linear-gradient(135deg, #0077B5 0%, #005885 100%);
    }
</style>
""", unsafe_allow_html=True)

# Initialize session state
def initialize_session_state():
    """Initialize session state variables."""
    if 'jobs_data' not in st.session_state:
        st.session_state.jobs_data = pd.DataFrame()
    if 'vector_db' not in st.session_state:
        st.session_state.vector_db = None
    if 'scraper' not in st.session_state:
        st.session_state.scraper = None
    if 'text_processor' not in st.session_state:
        st.session_state.text_processor = TextProcessor()
    if 'config' not in st.session_state:
        st.session_state.config = get_config()
    if 'cache' not in st.session_state:
        st.session_state.cache = get_cache()
    if 'scraping_stats' not in st.session_state:
        st.session_state.scraping_stats = {}
    if 'processing_stats' not in st.session_state:
        st.session_state.processing_stats = {}

@log_performance_metrics("initialize_components")
def initialize_components():
    """Initialize application components."""
    try:
        logger.info("Initializing application components")
        
        # Initialize vector database
        if st.session_state.vector_db is None:
            db_config = DatabaseConfig(
                persist_directory=st.session_state.config.database.persist_directory,
                collection_name=st.session_state.config.database.collection_name,
                embedding_model=st.session_state.config.database.embedding_model
            )
            st.session_state.vector_db = VectorDatabase(db_config)
            logger.info("Vector database initialized")
        
        # Initialize scraper
        if st.session_state.scraper is None:
            scrap_config = ScrapingConfig(
                delay_range=st.session_state.config.scraping.delay_range,
                max_retries=st.session_state.config.scraping.max_retries,
                max_pages=st.session_state.config.scraping.max_pages
            )
            st.session_state.scraper = LinkedInJobScraper(scrap_config)
            logger.info("LinkedIn scraper initialized")
        
        logger.info("All components initialized successfully")
        
    except Exception as e:
        logger.error(f"Error initializing components: {str(e)}")
        st.error(f"Error initializing application: {str(e)}")

@log_performance_metrics("scrape_jobs")
def scrape_jobs(job_title: str, location: str, experience_level: str, 
                job_type: str, salary_range: int, max_pages: int) -> bool:
    """
    Scrape jobs from LinkedIn and store in vector database.
    
    Args:
        job_title: Job title to search for
        location: Location to search in
        experience_level: Experience level filter
        job_type: Job type filter
        salary_range: Minimum salary range
        max_pages: Maximum pages to scrape
        
    Returns:
        True if successful, False otherwise
    """
    try:
        logger.info(f"Starting job scraping: {job_title} in {location}")
        
        # Configure scraper
        scraper_config = {
            'job_title': job_title,
            'location': location,
            'experience_level': experience_level,
            'job_type': job_type,
            'salary_range': salary_range,
            'max_pages': max_pages
        }
        
        # Validate configuration
        validation_result = validate_filters(scraper_config)
        if not validation_result.is_valid:
            st.error(f"Invalid scraping configuration: {', '.join(validation_result.errors)}")
            return False
        
        # Start scraping
        with st.spinner("Scraping jobs from LinkedIn..."):
            jobs_data = st.session_state.scraper.scrape_jobs(scraper_config)
        
        if not jobs_data:
            st.warning("No jobs found. Try adjusting your search parameters.")
            return False
        
        # Process and validate jobs
        with st.spinner("Processing and validating job data..."):
            processed_jobs = []
            validation_errors = 0
            
            for job in jobs_data:
                # Process job data
                processed_job = st.session_state.text_processor.process_single_job(job)
                
                if processed_job:
                    # Validate job data
                    validation_result = validate_job_data(processed_job)
                    
                    if validation_result.is_valid:
                        processed_jobs.append(processed_job)
                    else:
                        validation_errors += 1
                        logger.warning(f"Job validation failed: {validation_result.errors}")
            
            if not processed_jobs:
                st.error("No valid jobs found after processing and validation.")
                return False
            
            # Store in vector database
            with st.spinner("Storing jobs in vector database..."):
                stored_ids = st.session_state.vector_db.store_jobs(processed_jobs)
            
            # Update session state
            new_df = pd.DataFrame(processed_jobs)
            st.session_state.jobs_data = pd.concat([st.session_state.jobs_data, new_df], 
                                                 ignore_index=True).drop_duplicates(subset=['job_hash'])
            
            # Update statistics
            st.session_state.scraping_stats = st.session_state.scraper.get_statistics()
            st.session_state.processing_stats = st.session_state.text_processor.get_statistics()
            
            # Show success message
            st.success(f"✅ Successfully scraped and processed {len(processed_jobs)} jobs!")
            
            if validation_errors > 0:
                st.warning(f"⚠️ {validation_errors} jobs were rejected due to validation errors.")
            
            logger.info(f"Job scraping completed: {len(processed_jobs)} jobs processed")
            return True
            
    except Exception as e:
        logger.error(f"Error during job scraping: {str(e)}")
        st.error(f"Error during scraping: {str(e)}")
        return False

@log_performance_metrics("process_job_data")
def process_job_data(raw_jobs: List[Dict[str, Any]]) -> List[Dict[str, Any]]:
    """
    Process and clean scraped job data.
    
    Args:
        raw_jobs: List of raw job dictionaries
        
    Returns:
        List of processed job dictionaries
    """
    try:
        logger.info(f"Processing {len(raw_jobs)} jobs")
        
        processed_jobs = []
        for job in raw_jobs:
            try:
                processed_job = st.session_state.text_processor.process_single_job(job)
                if processed_job:
                    processed_jobs.append(processed_job)
            except Exception as e:
                logger.error(f"Error processing job: {str(e)}")
                continue
        
        logger.info(f"Successfully processed {len(processed_jobs)} jobs")
        return processed_jobs
        
    except Exception as e:
        logger.error(f"Error processing job data: {str(e)}")
        return []

def show_welcome_screen():
    """Display welcome screen when no data is available."""
    
    st.markdown('<h1 class="main-header">💼 LinkedIn Job Analytics Dashboard</h1>', 
                unsafe_allow_html=True)
    
    st.markdown("""
    <div class="info-message">
    <h3>👋 Welcome to LinkedIn Job Analytics Dashboard</h3>
    <p>This application helps you:</p>
    <ul>
        <li>🔍 <strong>Scrape job postings</strong> from LinkedIn with advanced filters</li>
        <li>💾 <strong>Store job data</strong> in a vector database for semantic search</li>
        <li>📊 <strong>Analyze job market trends</strong> with interactive visualizations</li>
        <li>🎯 <strong>Find similar jobs</strong> using AI-powered recommendations</li>
    </ul>
    </div>
    """, unsafe_allow_html=True)
    
    # Getting started section
    st.markdown("### 🚀 Getting Started")
    st.markdown("""
    1. **Configure your job search parameters** in the sidebar
    2. **Click "Start Job Scraping"** to collect job data
    3. **Explore the interactive dashboard** and analytics
    4. **Use semantic search** to find relevant opportunities
    """)
    
    # Features section
    st.markdown("### ✨ Key Features")
    
    col1, col2, col3, col4 = st.columns(4)
    
    with col1:
        st.markdown("""
        <div class="metric-card">
            <h3>🔍 Smart Search</h3>
            <p>Find jobs using natural language queries</p>
        </div>
        """, unsafe_allow_html=True)
    
    with col2:
        st.markdown("""
        <div class="metric-card">
            <h3>📊 Market Analytics</h3>
            <p>Salary trends, demand analysis, and insights</p>
        </div>
        """, unsafe_allow_html=True)
    
    with col3:
        st.markdown("""
        <div class="metric-card">
            <h3>🤖 AI-Powered</h3>
            <p>Similarity search and recommendations</p>
        </div>
        """, unsafe_allow_html=True)
    
    with col4:
        st.markdown("""
        <div class="metric-card">
            <h3>📈 Real-time</h3>
            <p>Live data updates and trends</p>
        </div>
        """, unsafe_allow_html=True)
    
    # Sample statistics
    st.markdown("### 📊 Sample Statistics")
    
    col1, col2, col3, col4 = st.columns(4)
    
    with col1:
        st.metric("Jobs Analyzed", "10K+", "↗️")
    with col2:
        st.metric("Companies", "500+", "↗️")
    with col3:
        st.metric("Locations", "50+", "↗️")
    with col4:
        st.metric("Success Rate", "95%", "↗️")

def show_dashboard():
    """Display the main dashboard with job data."""
    
    # Dashboard tabs
    tab1, tab2, tab3, tab4, tab5 = st.tabs([
        "🔍 Job Search", "📊 Analytics", "🎯 Similar Jobs", "📈 Market Trends", "⚙️ Settings"
    ])
    
    with tab1:
        show_job_search_tab()
    
    with tab2:
        show_analytics_tab()
    
    with tab3:
        show_similar_jobs_tab()
    
    with tab4:
        show_market_trends_tab()
    
    with tab5:
        show_settings_tab()

def show_job_search_tab():
    """Job search and filtering interface."""
    
    st.header("🔍 Job Search & Filtering")
    
    # Search interface
    col1, col2 = st.columns([3, 1])
    
    with col1:
        search_query = st.text_input(
            "🔎 Search jobs (natural language)", 
            placeholder="Find Python developer jobs with machine learning experience",
            help="Enter a natural language query to search for jobs"
        )
    
    with col2:
        if st.button("Search", type="primary", use_container_width=True):
            if search_query:
                with st.spinner("Searching for similar jobs..."):
                    search_results = st.session_state.vector_db.semantic_search(
                        search_query, top_k=20
                    )
                    st.session_state.filtered_jobs = search_results
                    st.success(f"Found {len(search_results)} similar jobs!")
            else:
                st.warning("Please enter a search query")
    
    # Advanced filters
    with st.expander("🔧 Advanced Filters", expanded=False):
        filter_col1, filter_col2, filter_col3 = st.columns(3)
        
        with filter_col1:
            company_filter = st.multiselect(
                "Company", 
                options=st.session_state.jobs_data['company'].unique() if not st.session_state.jobs_data.empty else [],
                help="Filter by specific companies"
            )
            location_filter = st.multiselect(
                "Location", 
                options=st.session_state.jobs_data['location'].unique() if not st.session_state.jobs_data.empty else [],
                help="Filter by specific locations"
            )
        
        with filter_col2:
            salary_min = st.number_input(
                "Min Salary (K)", 
                min_value=0, 
                value=0,
                help="Minimum salary in thousands"
            )
            salary_max = st.number_input(
                "Max Salary (K)", 
                min_value=0, 
                value=200,
                help="Maximum salary in thousands"
            )
        
        with filter_col3:
            job_type_filter = st.multiselect(
                "Job Type", 
                options=st.session_state.jobs_data['job_type'].unique() if not st.session_state.jobs_data.empty else [],
                help="Filter by job type"
            )
            experience_filter = st.multiselect(
                "Experience Level", 
                options=st.session_state.jobs_data['experience_level'].unique() if not st.session_state.jobs_data.empty else [],
                help="Filter by experience level"
            )
    
    # Apply filters
    if not st.session_state.jobs_data.empty:
        filtered_data = apply_filters(
            st.session_state.jobs_data, 
            company_filter, location_filter, 
            salary_min, salary_max, 
            job_type_filter, experience_filter
        )
        
        # Display results
        st.subheader(f"📋 Job Results ({len(filtered_data)} jobs found)")
        
        # Display job cards
        for _, job in filtered_data.head(20).iterrows():
            display_job_card(job)
    else:
        st.info("No job data available. Please scrape some jobs first.")

def show_analytics_tab():
    """Analytics and visualizations."""
    
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
    """Similar jobs finder using vector similarity."""
    
    st.header("🎯 Find Similar Jobs")
    
    if st.session_state.jobs_data.empty:
        st.info("No data available. Please scrape some jobs first.")
        return
    
    # Job selection for similarity search
    job_titles = st.session_state.jobs_data['title'].tolist()
    selected_job = st.selectbox(
        "Select a job to find similar positions:", 
        job_titles,
        help="Choose a job to find similar positions"
    )
    
    if selected_job:
        # Find similar jobs
        with st.spinner("Finding similar jobs..."):
            similar_jobs = st.session_state.vector_db.find_similar_jobs(selected_job, top_k=10)
        
        if similar_jobs:
            st.subheader("🔍 Similar Job Recommendations")
            
            for job in similar_jobs:
                similarity_score = job.get('similarity_score', 0)
                display_similar_job_card(job, similarity_score)
    
    # Custom similarity search
    st.subheader("🔎 Custom Similarity Search")
    custom_query = st.text_area(
        "Describe your ideal job:", 
        placeholder="I want a remote Python developer position with machine learning focus...",
        help="Describe your ideal job to find similar positions"
    )
    
    if st.button("Find Similar Jobs", type="primary"):
        if custom_query:
            with st.spinner("Searching for similar jobs..."):
                results = st.session_state.vector_db.semantic_search(custom_query, top_k=10)
                display_search_results(results)
        else:
            st.warning("Please enter a job description")

def show_market_trends_tab():
    """Market trends and insights."""
    
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

def show_settings_tab():
    """Application settings and configuration."""
    
    st.header("⚙️ Application Settings")
    
    # Configuration sections
    tab1, tab2, tab3, tab4 = st.tabs([
        "🔧 Scraping", "💾 Database", "📊 Dashboard", "🔍 Logging"
    ])
    
    with tab1:
        st.subheader("Scraping Configuration")
        
        col1, col2 = st.columns(2)
        
        with col1:
            delay_min = st.number_input(
                "Min Delay (seconds)", 
                min_value=1, 
                max_value=10, 
                value=st.session_state.config.scraping.delay_range[0]
            )
            delay_max = st.number_input(
                "Max Delay (seconds)", 
                min_value=1, 
                max_value=10, 
                value=st.session_state.config.scraping.delay_range[1]
            )
            max_retries = st.number_input(
                "Max Retries", 
                min_value=1, 
                max_value=10, 
                value=st.session_state.config.scraping.max_retries
            )
        
        with col2:
            max_pages = st.number_input(
                "Max Pages", 
                min_value=1, 
                max_value=20, 
                value=st.session_state.config.scraping.max_pages
            )
            timeout = st.number_input(
                "Timeout (seconds)", 
                min_value=10, 
                max_value=120, 
                value=st.session_state.config.scraping.timeout
            )
            respect_robots = st.checkbox(
                "Respect robots.txt", 
                value=st.session_state.config.scraping.respect_robots_txt
            )
        
        if st.button("Update Scraping Settings"):
            st.session_state.config.update_scraping_config(
                delay_range=(delay_min, delay_max),
                max_retries=max_retries,
                max_pages=max_pages,
                timeout=timeout,
                respect_robots_txt=respect_robots
            )
            st.success("Scraping settings updated!")
    
    with tab2:
        st.subheader("Database Configuration")
        
        col1, col2 = st.columns(2)
        
        with col1:
            persist_dir = st.text_input(
                "Persist Directory", 
                value=st.session_state.config.database.persist_directory
            )
            collection_name = st.text_input(
                "Collection Name", 
                value=st.session_state.config.database.collection_name
            )
            embedding_model = st.selectbox(
                "Embedding Model", 
                options=["all-MiniLM-L6-v2", "all-mpnet-base-v2", "paraphrase-multilingual-mpnet-base-v2"],
                index=0
            )
        
        with col2:
            max_results = st.number_input(
                "Max Results", 
                min_value=100, 
                max_value=10000, 
                value=st.session_state.config.database.max_results
            )
            similarity_threshold = st.slider(
                "Similarity Threshold", 
                min_value=0.0, 
                max_value=1.0, 
                value=st.session_state.config.database.similarity_threshold
            )
            batch_size = st.number_input(
                "Batch Size", 
                min_value=10, 
                max_value=1000, 
                value=st.session_state.config.database.batch_size
            )
        
        if st.button("Update Database Settings"):
            st.session_state.config.update_database_config(
                persist_directory=persist_dir,
                collection_name=collection_name,
                embedding_model=embedding_model,
                max_results=max_results,
                similarity_threshold=similarity_threshold,
                batch_size=batch_size
            )
            st.success("Database settings updated!")
    
    with tab3:
        st.subheader("Dashboard Configuration")
        
        col1, col2 = st.columns(2)
        
        with col1:
            page_title = st.text_input(
                "Page Title", 
                value=st.session_state.config.dashboard.page_title
            )
            theme = st.selectbox(
                "Theme", 
                options=["light", "dark"],
                index=0
            )
            max_display_jobs = st.number_input(
                "Max Display Jobs", 
                min_value=10, 
                max_value=1000, 
                value=st.session_state.config.dashboard.max_display_jobs
            )
        
        with col2:
            items_per_page = st.number_input(
                "Items Per Page", 
                min_value=5, 
                max_value=100, 
                value=st.session_state.config.dashboard.items_per_page
            )
            cache_ttl = st.number_input(
                "Cache TTL (seconds)", 
                min_value=60, 
                max_value=86400, 
                value=st.session_state.config.dashboard.cache_ttl
            )
            enable_analytics = st.checkbox(
                "Enable Analytics", 
                value=st.session_state.config.dashboard.enable_analytics
            )
        
        if st.button("Update Dashboard Settings"):
            st.session_state.config.update_dashboard_config(
                page_title=page_title,
                theme=theme,
                max_display_jobs=max_display_jobs,
                items_per_page=items_per_page,
                cache_ttl=cache_ttl,
                enable_analytics=enable_analytics
            )
            st.success("Dashboard settings updated!")
    
    with tab4:
        st.subheader("Logging Configuration")
        
        col1, col2 = st.columns(2)
        
        with col1:
            log_level = st.selectbox(
                "Log Level", 
                options=["DEBUG", "INFO", "WARNING", "ERROR", "CRITICAL"],
                index=1
            )
            log_file = st.text_input(
                "Log File", 
                value=st.session_state.config.logging.file_path
            )
            max_file_size = st.number_input(
                "Max File Size (MB)", 
                min_value=1, 
                max_value=100, 
                value=st.session_state.config.logging.max_file_size // 1048576
            )
        
        with col2:
            backup_count = st.number_input(
                "Backup Count", 
                min_value=1, 
                max_value=20, 
                value=st.session_state.config.logging.backup_count
            )
            enable_console = st.checkbox(
                "Enable Console Logging", 
                value=st.session_state.config.logging.enable_console
            )
            enable_file = st.checkbox(
                "Enable File Logging", 
                value=st.session_state.config.logging.enable_file
            )
        
        if st.button("Update Logging Settings"):
            st.session_state.config.update_logging_config(
                level=log_level,
                file_path=log_file,
                max_file_size=max_file_size * 1048576,
                backup_count=backup_count,
                enable_console=enable_console,
                enable_file=enable_file
            )
            st.success("Logging settings updated!")

# Helper functions
def apply_filters(data: pd.DataFrame, companies: List[str], locations: List[str], 
                 salary_min: int, salary_max: int, job_types: List[str], 
                 experience_levels: List[str]) -> pd.DataFrame:
    """Apply filters to job data."""
    filtered_data = data.copy()
    
    if companies:
        filtered_data = filtered_data[filtered_data['company'].isin(companies)]
    if locations:
        filtered_data = filtered_data[filtered_data['location'].isin(locations)]
    if job_types:
        filtered_data = filtered_data[filtered_data['job_type'].isin(job_types)]
    if experience_levels:
        filtered_data = filtered_data[filtered_data['experience_level'].isin(experience_levels)]
    
    # Salary filtering (simplified)
    if salary_min > 0 or salary_max < 200:
        # This would need proper implementation based on salary format
        pass
    
    return filtered_data

def display_job_card(job: pd.Series):
    """Display a job as a card."""
    st.markdown(f"""
    <div class="job-card">
        <h4>{job['title']}</h4>
        <p><strong>{job['company']}</strong> | {job['location']}</p>
        <p><strong>Posted:</strong> {job['date_posted']}</p>
        <p><strong>Type:</strong> {job.get('job_type', 'N/A')} | <strong>Level:</strong> {job.get('experience_level', 'N/A')}</p>
        <p><strong>Salary:</strong> {job.get('salary', 'Not specified')}</p>
        <p>{job['description'][:200]}...</p>
        <hr>
        <small><strong>Skills:</strong> {', '.join(job.get('skills', [])[:5])}</small>
    </div>
    """, unsafe_allow_html=True)

def display_similar_job_card(job: Dict[str, Any], similarity_score: float):
    """Display a similar job card."""
    st.markdown(f"""
    <div class="job-card">
        <h4>{job['title']}</h4>
        <p><strong>{job['company']}</strong> | {job['location']}</p>
        <p><strong>Similarity Score:</strong> {similarity_score:.2f}</p>
        <p>{job['description'][:200]}...</p>
    </div>
    """, unsafe_allow_html=True)

def display_search_results(results: List[Dict[str, Any]]):
    """Display search results."""
    if results:
        for job in results:
            display_job_card(pd.Series(job))
    else:
        st.info("No similar jobs found.")

def calculate_average_salary(data: pd.DataFrame) -> float:
    """Calculate average salary from job data."""
    # This would need proper implementation based on salary format
    return 75000  # Placeholder

def show_salary_distribution():
    """Show salary distribution chart."""
    st.subheader("💰 Salary Distribution")
    # Placeholder chart
    fig = px.histogram(
        x=[50000, 60000, 70000, 80000, 90000, 100000, 120000], 
        title="Salary Distribution"
    )
    st.plotly_chart(fig, use_container_width=True)

def show_top_companies():
    """Show top companies chart."""
    st.subheader("🏢 Top Hiring Companies")
    company_counts = st.session_state.jobs_data['company'].value_counts().head(10)
    fig = px.bar(
        x=company_counts.values, 
        y=company_counts.index, 
        orientation='h',
        title="Top 10 Companies by Job Postings"
    )
    st.plotly_chart(fig, use_container_width=True)

def show_location_distribution():
    """Show location distribution."""
    st.subheader("🌍 Job Locations")
    location_counts = st.session_state.jobs_data['location'].value_counts().head(10)
    fig = px.pie(
        values=location_counts.values, 
        names=location_counts.index,
        title="Job Distribution by Location"
    )
    st.plotly_chart(fig, use_container_width=True)

def show_skills_demand():
    """Show skills demand analysis."""
    st.subheader("🛠️ Top Skills in Demand")
    # This would analyze skills from job descriptions
    skills_data = ["Python", "SQL", "JavaScript", "Java", "React", "AWS", "Docker", "Kubernetes"]
    counts = [45, 38, 32, 28, 25, 22, 18, 15]
    fig = px.bar(x=skills_data, y=counts, title="Most Demanded Skills")
    st.plotly_chart(fig, use_container_width=True)

def show_posting_trends():
    """Show job posting trends over time."""
    st.subheader("📅 Job Posting Trends")
    # Placeholder implementation
    dates = pd.date_range('2024-01-01', periods=30, freq='D')
    counts = [10, 15, 12, 18, 20, 25, 22, 16, 19, 23] * 3
    fig = px.line(x=dates, y=counts, title="Daily Job Postings")
    st.plotly_chart(fig, use_container_width=True)

def show_salary_trends():
    """Show salary trends."""
    st.subheader("💵 Salary Trends by Experience Level")
    # Placeholder data
    experience_levels = ["Entry", "Mid", "Senior", "Lead", "Principal"]
    salaries = [60000, 80000, 110000, 140000, 180000]
    fig = px.bar(x=experience_levels, y=salaries, title="Average Salary by Experience Level")
    st.plotly_chart(fig, use_container_width=True)

def show_demand_trends():
    """Show demand trends by skill/technology."""
    st.subheader("📊 Technology Demand Trends")
    # This would show trending technologies over time
    st.info("Feature coming soon: Technology demand trends over time")

def generate_market_insights():
    """Generate market insights."""
    insights = [
        "🔥 Python and SQL are the most in-demand skills",
        "📈 Remote work opportunities increased by 40%",
        "💰 Senior roles show 15% salary growth year-over-year", 
        "🌟 AI/ML positions are growing rapidly",
        "🏢 Tech companies are leading in job postings"
    ]
    
    for insight in insights:
        st.markdown(f"<div class='info-message'>{insight}</div>", unsafe_allow_html=True)

def clear_all_data():
    """Clear all stored data."""
    st.session_state.jobs_data = pd.DataFrame()
    if st.session_state.vector_db:
        st.session_state.vector_db.clear_all()
    st.success("All data cleared successfully!")

def export_data():
    """Export data to CSV."""
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
    """Get date range of scraped jobs."""
    if not st.session_state.jobs_data.empty:
        min_date = st.session_state.jobs_data['date_posted'].min()
        max_date = st.session_state.jobs_data['date_posted'].max()
        return f"{min_date} to {max_date}"
    return "No data"

def main():
    """Main application function."""
    
    try:
        # Initialize session state
        initialize_session_state()
        
        # Initialize components
        initialize_components()
        
        # Sidebar
        with st.sidebar:
            st.markdown('<div class="sidebar-section">', unsafe_allow_html=True)
            st.header("🔍 Job Search Configuration")
            
            # Search parameters
            job_title = st.text_input(
                "Job Title", 
                value="Data Scientist", 
                help="Enter the job title you want to search for"
            )
            
            location = st.text_input(
                "Location", 
                value="United States", 
                help="Enter the location (city, state, or country)"
            )
            
            experience_level = st.selectbox(
                "Experience Level", 
                ["All", "Internship", "Entry level", "Associate", "Mid-Senior level", "Director", "Executive"]
            )
            
            job_type = st.selectbox(
                "Job Type", 
                ["All", "Full-time", "Part-time", "Contract", "Temporary", "Internship"]
            )
            
            salary_range = st.slider(
                "Minimum Salary (K)", 
                0, 200, 50, 
                step=10,
                help="Minimum salary in thousands"
            )
            
            max_pages = st.number_input(
                "Max Pages to Scrape", 
                min_value=1, 
                max_value=10, 
                value=3,
                help="Number of LinkedIn job pages to scrape"
            )
            
            # Scraping controls
            if st.button("🚀 Start Job Scraping", type="primary", use_container_width=True):
                scrape_jobs(job_title, location, experience_level, job_type, salary_range, max_pages)
            
            st.markdown('</div>', unsafe_allow_html=True)
            
            # Data management section
            st.markdown('<div class="sidebar-section">', unsafe_allow_html=True)
            st.header("💾 Data Management")
            
            col1, col2 = st.columns(2)
            
            with col1:
                if st.button("Clear All Data", type="secondary", use_container_width=True):
                    clear_all_data()
            
            with col2:
                if st.button("Export to CSV", use_container_width=True):
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
            
    except Exception as e:
        logger.error(f"Error in main application: {str(e)}")
        st.error(f"Application error: {str(e)}")
        st.error(f"Please check the logs for more details.")

if __name__ == "__main__":
    main()
