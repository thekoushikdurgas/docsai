"""
Dashboard Layout Module
Provides layout management and page structure for the job analytics dashboard.
Enhanced with responsive design, navigation, and user experience features.
"""

import streamlit as st
import pandas as pd
from typing import Dict, List, Any, Optional, Tuple
import logging
from datetime import datetime, timedelta
import json

# Set up logging
logger = logging.getLogger(__name__)

class DashboardLayout:
    """
    Dashboard layout management class.
    Enhanced with comprehensive logging and responsive design.
    """
    
    def __init__(self):
        """Initialize dashboard layout."""
        self.logger = logging.getLogger(__name__)
        self.logger.info("DashboardLayout initialized")
        
        # Page configuration
        self.setup_page_config()
        
        # Custom CSS
        self.setup_custom_css()
        
        # Initialize session state
        self.initialize_session_state()
    
    def setup_page_config(self) -> None:
        """Set up Streamlit page configuration."""
        try:
            self.logger.info("Setting up page configuration")
            
            st.set_page_config(
                page_title="LinkedIn Job Scraper & Analytics",
                page_icon="💼",
                layout="wide",
                initial_sidebar_state="expanded",
                menu_items={
                    'Get Help': 'https://github.com/your-repo/linkedin-job-scraper',
                    'Report a bug': 'https://github.com/your-repo/linkedin-job-scraper/issues',
                    'About': 'A comprehensive LinkedIn job scraping and analytics tool with vector database integration.'
                }
            )
            
        except Exception as e:
            self.logger.error(f"Error setting up page configuration: {str(e)}")
            st.error(f"Error setting up page configuration: {str(e)}")
    
    def setup_custom_css(self) -> None:
        """Set up custom CSS for enhanced UI."""
        try:
            self.logger.info("Setting up custom CSS")
            
            custom_css = """
            <style>
            /* Main theme colors */
            :root {
                --primary-color: #0077B5;
                --secondary-color: #005885;
                --success-color: #28a745;
                --warning-color: #ffc107;
                --danger-color: #dc3545;
                --info-color: #17a2b8;
                --light-color: #f8f9fa;
                --dark-color: #343a40;
            }
            
            /* Custom header styling */
            .main-header {
                background: linear-gradient(90deg, var(--primary-color), var(--secondary-color));
                padding: 1rem;
                border-radius: 10px;
                margin-bottom: 2rem;
                color: white;
                text-align: center;
            }
            
            .main-header h1 {
                margin: 0;
                font-size: 2.5rem;
                font-weight: bold;
            }
            
            .main-header p {
                margin: 0.5rem 0 0 0;
                font-size: 1.2rem;
                opacity: 0.9;
            }
            
            /* Custom sidebar styling */
            .sidebar .sidebar-content {
                background: linear-gradient(180deg, var(--light-color), white);
            }
            
            .sidebar .sidebar-content .block-container {
                padding-top: 2rem;
            }
            
            /* Custom metric cards */
            .metric-card {
                background: white;
                padding: 1.5rem;
                border-radius: 10px;
                box-shadow: 0 2px 10px rgba(0,0,0,0.1);
                border-left: 4px solid var(--primary-color);
                margin-bottom: 1rem;
            }
            
            .metric-card h3 {
                color: var(--primary-color);
                margin: 0 0 0.5rem 0;
                font-size: 1.1rem;
            }
            
            .metric-card .metric-value {
                font-size: 2rem;
                font-weight: bold;
                color: var(--dark-color);
                margin: 0;
            }
            
            /* Custom job cards */
            .job-card {
                background: white;
                padding: 1.5rem;
                border-radius: 10px;
                box-shadow: 0 2px 10px rgba(0,0,0,0.1);
                margin-bottom: 1rem;
                border-left: 4px solid var(--success-color);
                transition: transform 0.2s ease;
            }
            
            .job-card:hover {
                transform: translateY(-2px);
                box-shadow: 0 4px 20px rgba(0,0,0,0.15);
            }
            
            .job-card h3 {
                color: var(--primary-color);
                margin: 0 0 0.5rem 0;
                font-size: 1.3rem;
            }
            
            .job-card .company {
                color: var(--secondary-color);
                font-weight: bold;
                margin-bottom: 0.5rem;
            }
            
            .job-card .location {
                color: var(--info-color);
                margin-bottom: 0.5rem;
            }
            
            .job-card .salary {
                color: var(--success-color);
                font-weight: bold;
                margin-bottom: 0.5rem;
            }
            
            .job-card .skills {
                margin-top: 1rem;
            }
            
            .job-card .skill-tag {
                background: var(--light-color);
                color: var(--dark-color);
                padding: 0.25rem 0.5rem;
                border-radius: 15px;
                font-size: 0.8rem;
                margin: 0.25rem;
                display: inline-block;
            }
            
            /* Custom buttons */
            .stButton > button {
                background: var(--primary-color);
                color: white;
                border: none;
                border-radius: 5px;
                padding: 0.5rem 1rem;
                font-weight: bold;
                transition: background 0.2s ease;
            }
            
            .stButton > button:hover {
                background: var(--secondary-color);
            }
            
            /* Custom tabs */
            .stTabs [data-baseweb="tab-list"] {
                gap: 2px;
            }
            
            .stTabs [data-baseweb="tab"] {
                background: var(--light-color);
                border-radius: 5px 5px 0 0;
                padding: 0.5rem 1rem;
                font-weight: bold;
            }
            
            .stTabs [aria-selected="true"] {
                background: var(--primary-color);
                color: white;
            }
            
            /* Custom progress bars */
            .stProgress > div > div > div > div {
                background: linear-gradient(90deg, var(--primary-color), var(--success-color));
            }
            
            /* Custom alerts */
            .stAlert {
                border-radius: 10px;
                border: none;
                box-shadow: 0 2px 10px rgba(0,0,0,0.1);
            }
            
            /* Custom data tables */
            .stDataFrame {
                border-radius: 10px;
                overflow: hidden;
                box-shadow: 0 2px 10px rgba(0,0,0,0.1);
            }
            
            /* Custom charts */
            .stPlotlyChart {
                border-radius: 10px;
                overflow: hidden;
                box-shadow: 0 2px 10px rgba(0,0,0,0.1);
            }
            
            /* Responsive design */
            @media (max-width: 768px) {
                .main-header h1 {
                    font-size: 2rem;
                }
                
                .main-header p {
                    font-size: 1rem;
                }
                
                .metric-card {
                    padding: 1rem;
                }
                
                .job-card {
                    padding: 1rem;
                }
            }
            
            /* Loading animation */
            .loading-spinner {
                display: inline-block;
                width: 20px;
                height: 20px;
                border: 3px solid var(--light-color);
                border-radius: 50%;
                border-top-color: var(--primary-color);
                animation: spin 1s ease-in-out infinite;
            }
            
            @keyframes spin {
                to { transform: rotate(360deg); }
            }
            
            /* Custom scrollbar */
            ::-webkit-scrollbar {
                width: 8px;
            }
            
            ::-webkit-scrollbar-track {
                background: var(--light-color);
            }
            
            ::-webkit-scrollbar-thumb {
                background: var(--primary-color);
                border-radius: 4px;
            }
            
            ::-webkit-scrollbar-thumb:hover {
                background: var(--secondary-color);
            }
            </style>
            """
            
            st.markdown(custom_css, unsafe_allow_html=True)
            
        except Exception as e:
            self.logger.error(f"Error setting up custom CSS: {str(e)}")
            st.error(f"Error setting up custom CSS: {str(e)}")
    
    def initialize_session_state(self) -> None:
        """Initialize Streamlit session state variables."""
        try:
            self.logger.info("Initializing session state")
            
            # Initialize default session state variables
            if 'jobs_data' not in st.session_state:
                st.session_state.jobs_data = pd.DataFrame()
            
            if 'filtered_jobs' not in st.session_state:
                st.session_state.filtered_jobs = pd.DataFrame()
            
            if 'current_page' not in st.session_state:
                st.session_state.current_page = 0
            
            if 'search_query' not in st.session_state:
                st.session_state.search_query = ""
            
            if 'filters' not in st.session_state:
                st.session_state.filters = {}
            
            if 'saved_jobs' not in st.session_state:
                st.session_state.saved_jobs = []
            
            if 'view_job' not in st.session_state:
                st.session_state.view_job = None
            
            if 'is_scraping' not in st.session_state:
                st.session_state.is_scraping = False
            
            if 'scraping_progress' not in st.session_state:
                st.session_state.scraping_progress = 0
            
            if 'scraping_status' not in st.session_state:
                st.session_state.scraping_status = ""
            
            if 'error_message' not in st.session_state:
                st.session_state.error_message = None
            
            if 'success_message' not in st.session_state:
                st.session_state.success_message = None
            
            if 'info_message' not in st.session_state:
                st.session_state.info_message = None
            
            if 'warning_message' not in st.session_state:
                st.session_state.warning_message = None
            
        except Exception as e:
            self.logger.error(f"Error initializing session state: {str(e)}")
            st.error(f"Error initializing session state: {str(e)}")
    
    def create_header(self, title: str = "LinkedIn Job Scraper & Analytics", 
                     subtitle: str = "Comprehensive job market analysis with AI-powered insights") -> None:
        """
        Create the main header section.
        
        Args:
            title: Main title
            subtitle: Subtitle text
        """
        try:
            self.logger.info("Creating header section")
            
            st.markdown(f"""
            <div class="main-header">
                <h1>{title}</h1>
                <p>{subtitle}</p>
            </div>
            """, unsafe_allow_html=True)
            
        except Exception as e:
            self.logger.error(f"Error creating header: {str(e)}")
            st.error(f"Error creating header: {str(e)}")
    
    def create_navigation(self) -> str:
        """
        Create navigation tabs.
        
        Returns:
            Selected tab name
        """
        try:
            self.logger.info("Creating navigation tabs")
            
            tabs = st.tabs([
                "🏠 Dashboard",
                "🔍 Job Search",
                "📊 Analytics",
                "🤖 AI Insights",
                "💾 Data Management",
                "⚙️ Settings"
            ])
            
            # Return the selected tab
            return "Dashboard"  # Default tab
            
        except Exception as e:
            self.logger.error(f"Error creating navigation: {str(e)}")
            st.error(f"Error creating navigation: {str(e)}")
            return "Dashboard"
    
    def create_sidebar(self, data: pd.DataFrame) -> Dict[str, Any]:
        """
        Create the sidebar with filters and controls.
        
        Args:
            data: Job data DataFrame
            
        Returns:
            Dictionary of filter values
        """
        try:
            self.logger.info("Creating sidebar")
            
            with st.sidebar:
                # Sidebar header
                st.markdown("## 🔍 Filters & Controls")
                
                # Search bar
                search_query = st.text_input(
                    "🔍 Search Jobs",
                    placeholder="Search by title, company, location...",
                    help="Search across job titles, companies, locations, and skills"
                )
                
                # Company filter
                if 'company' in data.columns and not data.empty:
                    companies = ['All'] + sorted(data['company'].unique().tolist())
                    selected_company = st.selectbox(
                        "🏢 Company",
                        companies,
                        index=0
                    )
                else:
                    selected_company = "All"
                
                # Location filter
                if 'location' in data.columns and not data.empty:
                    locations = ['All'] + sorted(data['location'].unique().tolist())
                    selected_location = st.selectbox(
                        "📍 Location",
                        locations,
                        index=0
                    )
                else:
                    selected_location = "All"
                
                # Job type filter
                if 'job_type' in data.columns and not data.empty:
                    job_types = ['All'] + sorted(data['job_type'].unique().tolist())
                    selected_job_type = st.selectbox(
                        "💼 Job Type",
                        job_types,
                        index=0
                    )
                else:
                    selected_job_type = "All"
                
                # Experience level filter
                if 'experience_level' in data.columns and not data.empty:
                    exp_levels = ['All'] + sorted(data['experience_level'].unique().tolist())
                    selected_exp_level = st.selectbox(
                        "🎯 Experience Level",
                        exp_levels,
                        index=0
                    )
                else:
                    selected_exp_level = "All"
                
                # Skills filter
                if 'skills' in data.columns and not data.empty:
                    all_skills = self._extract_all_skills(data)
                    if all_skills:
                        selected_skills = st.multiselect(
                            "🛠️ Skills",
                            all_skills,
                            default=[]
                        )
                    else:
                        selected_skills = []
                else:
                    selected_skills = []
                
                # Salary range filter
                if 'salary' in data.columns and not data.empty:
                    st.subheader("💰 Salary Range")
                    salary_ranges = self._extract_salary_ranges(data)
                    if salary_ranges:
                        min_salary = st.number_input(
                            "Min Salary ($)",
                            min_value=0,
                            max_value=salary_ranges['max'],
                            value=salary_ranges['min'],
                            step=1000
                        )
                        max_salary = st.number_input(
                            "Max Salary ($)",
                            min_value=0,
                            max_value=salary_ranges['max'],
                            value=salary_ranges['max'],
                            step=1000
                        )
                    else:
                        min_salary = 0
                        max_salary = 200000
                else:
                    min_salary = 0
                    max_salary = 200000
                
                # Date range filter
                if 'date_posted' in data.columns and not data.empty:
                    st.subheader("📅 Date Range")
                    date_range = self._extract_date_range(data)
                    if date_range:
                        start_date = st.date_input(
                            "Start Date",
                            value=date_range['min'],
                            min_value=date_range['min'],
                            max_value=date_range['max']
                        )
                        end_date = st.date_input(
                            "End Date",
                            value=date_range['max'],
                            min_value=date_range['min'],
                            max_value=date_range['max']
                        )
                    else:
                        start_date = datetime.now() - timedelta(days=30)
                        end_date = datetime.now()
                else:
                    start_date = datetime.now() - timedelta(days=30)
                    end_date = datetime.now()
                
                # Remote work filter
                st.subheader("🏠 Work Arrangement")
                remote_options = ['All', 'Remote', 'On-site', 'Hybrid']
                selected_remote = st.selectbox(
                    "Work Arrangement",
                    remote_options,
                    index=0
                )
                
                # Action buttons
                st.subheader("🎛️ Actions")
                
                col1, col2 = st.columns(2)
                
                with col1:
                    if st.button("🔍 Apply Filters", type="primary"):
                        st.rerun()
                
                with col2:
                    if st.button("🗑️ Clear Filters"):
                        st.rerun()
                
                # Export section
                st.subheader("📥 Export Data")
                
                if not data.empty:
                    col1, col2 = st.columns(2)
                    
                    with col1:
                        csv_data = data.to_csv(index=False)
                        st.download_button(
                            label="📄 CSV",
                            data=csv_data,
                            file_name=f"jobs_data_{datetime.now().strftime('%Y%m%d_%H%M%S')}.csv",
                            mime="text/csv"
                        )
                    
                    with col2:
                        json_data = data.to_json(orient='records', indent=2)
                        st.download_button(
                            label="📋 JSON",
                            data=json_data,
                            file_name=f"jobs_data_{datetime.now().strftime('%Y%m%d_%H%M%S')}.json",
                            mime="application/json"
                        )
                
                # Statistics section
                if not data.empty:
                    st.subheader("📊 Quick Stats")
                    
                    total_jobs = len(data)
                    unique_companies = data['company'].nunique() if 'company' in data.columns else 0
                    unique_locations = data['location'].nunique() if 'location' in data.columns else 0
                    
                    st.metric("Total Jobs", f"{total_jobs:,}")
                    st.metric("Companies", f"{unique_companies:,}")
                    st.metric("Locations", f"{unique_locations:,}")
                
                # Return filter values
                return {
                    'search_query': search_query,
                    'company': selected_company,
                    'location': selected_location,
                    'job_type': selected_job_type,
                    'experience_level': selected_exp_level,
                    'skills': selected_skills,
                    'salary_range': (min_salary, max_salary),
                    'date_range': (start_date, end_date),
                    'remote_work': selected_remote
                }
                
        except Exception as e:
            self.logger.error(f"Error creating sidebar: {str(e)}")
            st.error(f"Error creating sidebar: {str(e)}")
            return {}
    
    def create_footer(self) -> None:
        """Create the footer section."""
        try:
            self.logger.info("Creating footer section")
            
            st.markdown("---")
            
            col1, col2, col3 = st.columns(3)
            
            with col1:
                st.markdown("### 📚 Resources")
                st.markdown("""
                - [Documentation](https://github.com/your-repo/linkedin-job-scraper)
                - [API Reference](https://github.com/your-repo/linkedin-job-scraper)
                - [Tutorials](https://github.com/your-repo/linkedin-job-scraper)
                """)
            
            with col2:
                st.markdown("### 🔗 Links")
                st.markdown("""
                - [GitHub Repository](https://github.com/your-repo/linkedin-job-scraper)
                - [Issue Tracker](https://github.com/your-repo/linkedin-job-scraper/issues)
                - [Discussions](https://github.com/your-repo/linkedin-job-scraper/discussions)
                """)
            
            with col3:
                st.markdown("### 📞 Support")
                st.markdown("""
                - [Contact Us](mailto:support@example.com)
                - [Report Bug](https://github.com/your-repo/linkedin-job-scraper/issues)
                - [Feature Request](https://github.com/your-repo/linkedin-job-scraper/issues)
                """)
            
            st.markdown("---")
            st.markdown(
                "<div style='text-align: center; color: #666;'>"
                "© 2024 LinkedIn Job Scraper & Analytics. Built with ❤️ using Streamlit."
                "</div>",
                unsafe_allow_html=True
            )
            
        except Exception as e:
            self.logger.error(f"Error creating footer: {str(e)}")
            st.error(f"Error creating footer: {str(e)}")
    
    def create_loading_overlay(self, message: str = "Loading...") -> None:
        """
        Create a loading overlay.
        
        Args:
            message: Loading message
        """
        try:
            self.logger.info(f"Creating loading overlay: {message}")
            
            with st.spinner(message):
                st.write("Please wait...")
                
        except Exception as e:
            self.logger.error(f"Error creating loading overlay: {str(e)}")
            st.error(f"Error creating loading overlay: {str(e)}")
    
    def create_error_display(self, error: str, title: str = "Error") -> None:
        """
        Create an error display.
        
        Args:
            error: Error message
            title: Error title
        """
        try:
            self.logger.info(f"Creating error display: {title}")
            
            st.error(f"❌ **{title}**\n\n{error}")
            
        except Exception as e:
            self.logger.error(f"Error creating error display: {str(e)}")
            st.error(f"Error creating error display: {str(e)}")
    
    def create_success_display(self, message: str, title: str = "Success") -> None:
        """
        Create a success display.
        
        Args:
            message: Success message
            title: Success title
        """
        try:
            self.logger.info(f"Creating success display: {title}")
            
            st.success(f"✅ **{title}**\n\n{message}")
            
        except Exception as e:
            self.logger.error(f"Error creating success display: {str(e)}")
            st.error(f"Error creating success display: {str(e)}")
    
    def create_info_display(self, message: str, title: str = "Info") -> None:
        """
        Create an info display.
        
        Args:
            message: Info message
            title: Info title
        """
        try:
            self.logger.info(f"Creating info display: {title}")
            
            st.info(f"ℹ️ **{title}**\n\n{message}")
            
        except Exception as e:
            self.logger.error(f"Error creating info display: {str(e)}")
            st.error(f"Error creating info display: {str(e)}")
    
    def create_warning_display(self, message: str, title: str = "Warning") -> None:
        """
        Create a warning display.
        
        Args:
            message: Warning message
            title: Warning title
        """
        try:
            self.logger.info(f"Creating warning display: {title}")
            
            st.warning(f"⚠️ **{title}**\n\n{message}")
            
        except Exception as e:
            self.logger.error(f"Error creating warning display: {str(e)}")
            st.error(f"Error creating warning display: {str(e)}")
    
    # Helper methods
    def _extract_all_skills(self, data: pd.DataFrame) -> List[str]:
        """Extract all unique skills from job data."""
        try:
            all_skills = set()
            for _, job in data.iterrows():
                skills = job.get('skills', [])
                if isinstance(skills, list):
                    all_skills.update(skills)
                elif isinstance(skills, str):
                    try:
                        skills_list = json.loads(skills)
                        all_skills.update(skills_list)
                    except:
                        all_skills.add(skills)
            
            return sorted(list(all_skills))
        except Exception as e:
            self.logger.error(f"Error extracting all skills: {str(e)}")
            return []
    
    def _extract_salary_ranges(self, data: pd.DataFrame) -> Dict[str, int]:
        """Extract salary ranges from job data."""
        try:
            salaries = []
            for _, job in data.iterrows():
                salary = job.get('salary', '')
                if salary and '$' in salary:
                    # Extract numeric values from salary string
                    import re
                    numbers = re.findall(r'[\d,]+', salary.replace(',', ''))
                    if numbers:
                        try:
                            salary_value = int(numbers[0])
                            salaries.append(salary_value)
                        except ValueError:
                            continue
            
            if salaries:
                return {
                    'min': min(salaries),
                    'max': max(salaries)
                }
            
            return {'min': 0, 'max': 200000}
        except Exception as e:
            self.logger.error(f"Error extracting salary ranges: {str(e)}")
            return {'min': 0, 'max': 200000}
    
    def _extract_date_range(self, data: pd.DataFrame) -> Dict[str, datetime]:
        """Extract date range from job data."""
        try:
            dates = []
            for _, job in data.iterrows():
                date_posted = job.get('date_posted', '')
                if date_posted:
                    try:
                        if isinstance(date_posted, str):
                            parsed_date = pd.to_datetime(date_posted)
                        else:
                            parsed_date = date_posted
                        dates.append(parsed_date)
                    except:
                        continue
            
            if dates:
                return {
                    'min': min(dates),
                    'max': max(dates)
                }
            
            # Default to last 30 days
            today = datetime.now()
            return {
                'min': today - timedelta(days=30),
                'max': today
            }
        except Exception as e:
            self.logger.error(f"Error extracting date range: {str(e)}")
            today = datetime.now()
            return {
                'min': today - timedelta(days=30),
                'max': today
            }

# Usage example
if __name__ == "__main__":
    # Set up logging
    logging.basicConfig(
        level=logging.DEBUG,
        format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
    )
    
    # Example usage
    sample_data = pd.DataFrame({
        'title': ['Data Scientist', 'Software Engineer', 'Product Manager'],
        'company': ['TechCorp', 'DataCorp', 'ProductCorp'],
        'location': ['San Francisco, CA', 'New York, NY', 'Seattle, WA'],
        'salary': ['$120,000 - $150,000', '$100,000 - $130,000', '$110,000 - $140,000'],
        'experience_level': ['Mid-Senior level', 'Entry level', 'Mid-Senior level'],
        'job_type': ['Full-time', 'Full-time', 'Full-time'],
        'skills': [['python', 'machine learning'], ['javascript', 'react'], ['product management', 'analytics']],
        'date_posted': ['2024-01-15', '2024-01-16', '2024-01-17']
    })
    
    layout = DashboardLayout()
    
    # Create layout components
    layout.create_header()
    layout.create_navigation()
    layout.create_sidebar(sample_data)
    layout.create_footer()
