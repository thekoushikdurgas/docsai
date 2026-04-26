"""
Dashboard Components Module
Provides reusable UI components for the job analytics dashboard.
Enhanced with interactive elements, filters, and advanced functionality.
"""

import streamlit as st
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go
from typing import Dict, List, Any, Optional, Tuple, Callable
import logging
from datetime import datetime, timedelta
import json

# Set up logging
logger = logging.getLogger(__name__)

class DashboardComponents:
    """
    Reusable dashboard components for job analytics.
    Enhanced with comprehensive logging and interactive features.
    """
    
    def __init__(self):
        """Initialize dashboard components."""
        self.logger = logging.getLogger(__name__)
        self.logger.info("DashboardComponents initialized")
        
        # Color schemes
        self.colors = {
            'primary': '#0077B5',
            'secondary': '#005885',
            'success': '#28a745',
            'warning': '#ffc107',
            'danger': '#dc3545',
            'info': '#17a2b8',
            'light': '#f8f9fa',
            'dark': '#343a40'
        }
    
    def create_sidebar_filters(self, data: pd.DataFrame) -> Dict[str, Any]:
        """
        Create sidebar filters for job data.
        
        Args:
            data: Job data DataFrame
            
        Returns:
            Dictionary of filter values
        """
        try:
            self.logger.info("Creating sidebar filters")
            
            st.sidebar.header("🔍 Filters")
            
            # Initialize filters
            filters = {}
            
            # Company filter
            if 'company' in data.columns:
                companies = ['All'] + sorted(data['company'].unique().tolist())
                selected_company = st.sidebar.selectbox(
                    "Company",
                    companies,
                    index=0
                )
                filters['company'] = selected_company
            
            # Location filter
            if 'location' in data.columns:
                locations = ['All'] + sorted(data['location'].unique().tolist())
                selected_location = st.sidebar.selectbox(
                    "Location",
                    locations,
                    index=0
                )
                filters['location'] = selected_location
            
            # Job type filter
            if 'job_type' in data.columns:
                job_types = ['All'] + sorted(data['job_type'].unique().tolist())
                selected_job_type = st.sidebar.selectbox(
                    "Job Type",
                    job_types,
                    index=0
                )
                filters['job_type'] = selected_job_type
            
            # Experience level filter
            if 'experience_level' in data.columns:
                exp_levels = ['All'] + sorted(data['experience_level'].unique().tolist())
                selected_exp_level = st.sidebar.selectbox(
                    "Experience Level",
                    exp_levels,
                    index=0
                )
                filters['experience_level'] = selected_exp_level
            
            # Salary range filter
            if 'salary' in data.columns:
                st.sidebar.subheader("💰 Salary Range")
                
                # Extract salary ranges
                salary_ranges = self._extract_salary_ranges(data)
                if salary_ranges:
                    min_salary = st.sidebar.number_input(
                        "Min Salary ($)",
                        min_value=0,
                        max_value=salary_ranges['max'],
                        value=salary_ranges['min'],
                        step=1000
                    )
                    max_salary = st.sidebar.number_input(
                        "Max Salary ($)",
                        min_value=0,
                        max_value=salary_ranges['max'],
                        value=salary_ranges['max'],
                        step=1000
                    )
                    filters['salary_range'] = (min_salary, max_salary)
            
            # Skills filter
            if 'skills' in data.columns:
                st.sidebar.subheader("🛠️ Skills")
                all_skills = self._extract_all_skills(data)
                if all_skills:
                    selected_skills = st.sidebar.multiselect(
                        "Select Skills",
                        all_skills,
                        default=[]
                    )
                    filters['skills'] = selected_skills
            
            # Date range filter
            if 'date_posted' in data.columns:
                st.sidebar.subheader("📅 Date Range")
                
                # Extract date range
                date_range = self._extract_date_range(data)
                if date_range:
                    start_date = st.sidebar.date_input(
                        "Start Date",
                        value=date_range['min'],
                        min_value=date_range['min'],
                        max_value=date_range['max']
                    )
                    end_date = st.sidebar.date_input(
                        "End Date",
                        value=date_range['max'],
                        min_value=date_range['min'],
                        max_value=date_range['max']
                    )
                    filters['date_range'] = (start_date, end_date)
            
            # Remote work filter
            st.sidebar.subheader("🏠 Work Arrangement")
            remote_options = ['All', 'Remote', 'On-site', 'Hybrid']
            selected_remote = st.sidebar.selectbox(
                "Work Arrangement",
                remote_options,
                index=0
            )
            filters['remote_work'] = selected_remote
            
            # Apply filters button
            if st.sidebar.button("Apply Filters", type="primary"):
                st.rerun()
            
            # Clear filters button
            if st.sidebar.button("Clear Filters"):
                st.rerun()
            
            return filters
            
        except Exception as e:
            self.logger.error(f"Error creating sidebar filters: {str(e)}")
            st.error(f"Error creating filters: {str(e)}")
            return {}
    
    def create_search_bar(self, placeholder: str = "Search jobs...") -> str:
        """
        Create search bar component.
        
        Args:
            placeholder: Placeholder text for search bar
            
        Returns:
            Search query string
        """
        try:
            self.logger.info("Creating search bar")
            
            search_query = st.text_input(
                "🔍 Search Jobs",
                placeholder=placeholder,
                help="Search by job title, company, location, or skills"
            )
            
            return search_query
            
        except Exception as e:
            self.logger.error(f"Error creating search bar: {str(e)}")
            return ""
    
    def create_job_card(self, job: Dict[str, Any], index: int = 0) -> None:
        """
        Create a job card component.
        
        Args:
            job: Job data dictionary
            index: Job index for unique key
        """
        try:
            self.logger.info(f"Creating job card for job {index}")
            
            # Create job card container
            with st.container():
                # Job header
                col1, col2 = st.columns([3, 1])
                
                with col1:
                    st.subheader(f"💼 {job.get('title', 'N/A')}")
                    st.write(f"🏢 **{job.get('company', 'N/A')}**")
                
                with col2:
                    # Job type badge
                    job_type = job.get('job_type', 'N/A')
                    if job_type != 'N/A':
                        st.markdown(f"**Type:** {job_type}")
                    
                    # Experience level badge
                    exp_level = job.get('experience_level', 'N/A')
                    if exp_level != 'N/A':
                        st.markdown(f"**Level:** {exp_level}")
                
                # Job details
                col1, col2, col3 = st.columns(3)
                
                with col1:
                    st.write(f"📍 **Location:** {job.get('location', 'N/A')}")
                
                with col2:
                    salary = job.get('salary', 'N/A')
                    if salary != 'N/A':
                        st.write(f"💰 **Salary:** {salary}")
                
                with col3:
                    date_posted = job.get('date_posted', 'N/A')
                    if date_posted != 'N/A':
                        st.write(f"📅 **Posted:** {date_posted}")
                
                # Skills section
                skills = job.get('skills', [])
                if skills:
                    if isinstance(skills, str):
                        try:
                            skills = json.loads(skills)
                        except:
                            skills = [skills]
                    
                    st.write("🛠️ **Skills:**")
                    skill_tags = []
                    for skill in skills[:10]:  # Limit to 10 skills
                        skill_tags.append(f"`{skill}`")
                    
                    if skill_tags:
                        st.markdown(" ".join(skill_tags))
                
                # Job description preview
                description = job.get('description', '')
                if description:
                    # Truncate description
                    preview = description[:200] + "..." if len(description) > 200 else description
                    with st.expander("📝 Job Description Preview"):
                        st.write(preview)
                
                # Action buttons
                col1, col2, col3 = st.columns(3)
                
                with col1:
                    if st.button(f"View Details", key=f"view_{index}"):
                        st.session_state[f"view_job_{index}"] = True
                
                with col2:
                    if st.button(f"Save Job", key=f"save_{index}"):
                        st.session_state[f"saved_job_{index}"] = True
                        st.success("Job saved!")
                
                with col3:
                    if st.button(f"Share", key=f"share_{index}"):
                        st.session_state[f"share_job_{index}"] = True
                        st.info("Job shared!")
                
                # Divider
                st.divider()
                
        except Exception as e:
            self.logger.error(f"Error creating job card: {str(e)}")
            st.error(f"Error creating job card: {str(e)}")
    
    def create_job_list(self, jobs: List[Dict[str, Any]], page_size: int = 10) -> None:
        """
        Create a paginated job list.
        
        Args:
            jobs: List of job dictionaries
            page_size: Number of jobs per page
        """
        try:
            self.logger.info(f"Creating job list with {len(jobs)} jobs")
            
            # Pagination
            total_pages = (len(jobs) - 1) // page_size + 1
            
            if total_pages > 1:
                col1, col2, col3 = st.columns([1, 2, 1])
                
                with col1:
                    if st.button("⬅️ Previous", disabled=st.session_state.get('current_page', 0) == 0):
                        st.session_state['current_page'] = max(0, st.session_state.get('current_page', 0) - 1)
                        st.rerun()
                
                with col2:
                    current_page = st.session_state.get('current_page', 0)
                    st.write(f"Page {current_page + 1} of {total_pages}")
                
                with col3:
                    if st.button("Next ➡️", disabled=st.session_state.get('current_page', 0) >= total_pages - 1):
                        st.session_state['current_page'] = min(total_pages - 1, st.session_state.get('current_page', 0) + 1)
                        st.rerun()
            
            # Display jobs for current page
            current_page = st.session_state.get('current_page', 0)
            start_idx = current_page * page_size
            end_idx = start_idx + page_size
            
            for i, job in enumerate(jobs[start_idx:end_idx]):
                self.create_job_card(job, start_idx + i)
                
        except Exception as e:
            self.logger.error(f"Error creating job list: {str(e)}")
            st.error(f"Error creating job list: {str(e)}")
    
    def create_metrics_cards(self, data: pd.DataFrame) -> None:
        """
        Create metrics cards for dashboard overview.
        
        Args:
            data: Job data DataFrame
        """
        try:
            self.logger.info("Creating metrics cards")
            
            # Calculate metrics
            total_jobs = len(data)
            unique_companies = data['company'].nunique() if 'company' in data.columns else 0
            unique_locations = data['location'].nunique() if 'location' in data.columns else 0
            avg_salary = self._calculate_average_salary(data)
            
            # Create metrics columns
            col1, col2, col3, col4 = st.columns(4)
            
            with col1:
                st.metric(
                    label="📊 Total Jobs",
                    value=f"{total_jobs:,}",
                    delta=None
                )
            
            with col2:
                st.metric(
                    label="🏢 Companies",
                    value=f"{unique_companies:,}",
                    delta=None
                )
            
            with col3:
                st.metric(
                    label="📍 Locations",
                    value=f"{unique_locations:,}",
                    delta=None
                )
            
            with col4:
                st.metric(
                    label="💰 Avg Salary",
                    value=f"${avg_salary:,.0f}",
                    delta=None
                )
                
        except Exception as e:
            self.logger.error(f"Error creating metrics cards: {str(e)}")
            st.error(f"Error creating metrics cards: {str(e)}")
    
    def create_export_buttons(self, data: pd.DataFrame) -> None:
        """
        Create export buttons for job data.
        
        Args:
            data: Job data DataFrame
        """
        try:
            self.logger.info("Creating export buttons")
            
            st.subheader("📥 Export Data")
            
            col1, col2, col3, col4 = st.columns(4)
            
            with col1:
                # CSV export
                csv_data = data.to_csv(index=False)
                st.download_button(
                    label="📄 Download CSV",
                    data=csv_data,
                    file_name=f"jobs_data_{datetime.now().strftime('%Y%m%d_%H%M%S')}.csv",
                    mime="text/csv"
                )
            
            with col2:
                # Excel export
                excel_data = data.to_excel(index=False)
                st.download_button(
                    label="📊 Download Excel",
                    data=excel_data,
                    file_name=f"jobs_data_{datetime.now().strftime('%Y%m%d_%H%M%S')}.xlsx",
                    mime="application/vnd.openxmlformats-officedocument.spreadsheetml.sheet"
                )
            
            with col3:
                # JSON export
                json_data = data.to_json(orient='records', indent=2)
                st.download_button(
                    label="📋 Download JSON",
                    data=json_data,
                    file_name=f"jobs_data_{datetime.now().strftime('%Y%m%d_%H%M%S')}.json",
                    mime="application/json"
                )
            
            with col4:
                # PDF export (placeholder)
                st.button(
                    label="📄 Download PDF",
                    disabled=True,
                    help="PDF export coming soon"
                )
                
        except Exception as e:
            self.logger.error(f"Error creating export buttons: {str(e)}")
            st.error(f"Error creating export buttons: {str(e)}")
    
    def create_loading_spinner(self, message: str = "Loading...") -> None:
        """
        Create a loading spinner component.
        
        Args:
            message: Loading message to display
        """
        try:
            self.logger.info(f"Creating loading spinner: {message}")
            
            with st.spinner(message):
                st.write("Please wait...")
                
        except Exception as e:
            self.logger.error(f"Error creating loading spinner: {str(e)}")
            st.error(f"Error creating loading spinner: {str(e)}")
    
    def create_error_message(self, error: str, title: str = "Error") -> None:
        """
        Create an error message component.
        
        Args:
            error: Error message to display
            title: Error title
        """
        try:
            self.logger.info(f"Creating error message: {title}")
            
            st.error(f"❌ **{title}**\n\n{error}")
            
        except Exception as e:
            self.logger.error(f"Error creating error message: {str(e)}")
            st.error(f"Error creating error message: {str(e)}")
    
    def create_success_message(self, message: str, title: str = "Success") -> None:
        """
        Create a success message component.
        
        Args:
            message: Success message to display
            title: Success title
        """
        try:
            self.logger.info(f"Creating success message: {title}")
            
            st.success(f"✅ **{title}**\n\n{message}")
            
        except Exception as e:
            self.logger.error(f"Error creating success message: {str(e)}")
            st.error(f"Error creating success message: {str(e)}")
    
    def create_info_message(self, message: str, title: str = "Info") -> None:
        """
        Create an info message component.
        
        Args:
            message: Info message to display
            title: Info title
        """
        try:
            self.logger.info(f"Creating info message: {title}")
            
            st.info(f"ℹ️ **{title}**\n\n{message}")
            
        except Exception as e:
            self.logger.error(f"Error creating info message: {str(e)}")
            st.error(f"Error creating info message: {str(e)}")
    
    def create_warning_message(self, message: str, title: str = "Warning") -> None:
        """
        Create a warning message component.
        
        Args:
            message: Warning message to display
            title: Warning title
        """
        try:
            self.logger.info(f"Creating warning message: {title}")
            
            st.warning(f"⚠️ **{title}**\n\n{message}")
            
        except Exception as e:
            self.logger.error(f"Error creating warning message: {str(e)}")
            st.error(f"Error creating warning message: {str(e)}")
    
    def create_progress_bar(self, current: int, total: int, message: str = "Progress") -> None:
        """
        Create a progress bar component.
        
        Args:
            current: Current progress value
            total: Total progress value
            message: Progress message
        """
        try:
            self.logger.info(f"Creating progress bar: {current}/{total}")
            
            progress = current / total if total > 0 else 0
            st.progress(progress, text=f"{message}: {current}/{total}")
            
        except Exception as e:
            self.logger.error(f"Error creating progress bar: {str(e)}")
            st.error(f"Error creating progress bar: {str(e)}")
    
    def create_data_table(self, data: pd.DataFrame, title: str = "Data Table") -> None:
        """
        Create a data table component.
        
        Args:
            data: DataFrame to display
            title: Table title
        """
        try:
            self.logger.info(f"Creating data table: {title}")
            
            st.subheader(title)
            
            # Display data table
            st.dataframe(
                data,
                use_container_width=True,
                height=400
            )
            
        except Exception as e:
            self.logger.error(f"Error creating data table: {str(e)}")
            st.error(f"Error creating data table: {str(e)}")
    
    def create_chart_container(self, chart_func: Callable, title: str = "Chart") -> None:
        """
        Create a chart container component.
        
        Args:
            chart_func: Function that creates the chart
            title: Chart title
        """
        try:
            self.logger.info(f"Creating chart container: {title}")
            
            st.subheader(title)
            
            # Create chart
            chart_func()
            
        except Exception as e:
            self.logger.error(f"Error creating chart container: {str(e)}")
            st.error(f"Error creating chart container: {str(e)}")
    
    # Helper methods
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
    
    def _calculate_average_salary(self, data: pd.DataFrame) -> float:
        """Calculate average salary from job data."""
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
                return sum(salaries) / len(salaries)
            
            return 0
        except Exception as e:
            self.logger.error(f"Error calculating average salary: {str(e)}")
            return 0

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
    
    components = DashboardComponents()
    
    # Create components
    components.create_metrics_cards(sample_data)
    components.create_search_bar()
    components.create_export_buttons(sample_data)
