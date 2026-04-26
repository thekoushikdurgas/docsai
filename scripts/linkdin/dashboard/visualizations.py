"""
Dashboard Visualizations Module
Provides comprehensive data visualization components for the job analytics dashboard.
Enhanced with interactive charts, real-time updates, and advanced analytics.
"""

import streamlit as st
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go
from plotly.subplots import make_subplots
import numpy as np
from typing import Dict, List, Any, Optional, Tuple
import logging
from datetime import datetime, timedelta
import json

# Set up logging
logger = logging.getLogger(__name__)

class JobDashboard:
    """
    Main dashboard class for job analytics visualizations.
    Enhanced with comprehensive logging and interactive features.
    """
    
    def __init__(self, data: pd.DataFrame):
        """
        Initialize the job dashboard.
        
        Args:
            data: Job data DataFrame
        """
        self.data = data
        self.logger = logging.getLogger(__name__)
        self.logger.info(f"JobDashboard initialized with {len(data)} jobs")
        
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
        
        # Chart themes
        self.chart_theme = {
            'layout': {
                'font': {'family': 'Arial, sans-serif'},
                'plot_bgcolor': 'rgba(0,0,0,0)',
                'paper_bgcolor': 'rgba(0,0,0,0)',
                'colorway': [self.colors['primary'], self.colors['secondary'], 
                           self.colors['success'], self.colors['warning'], 
                           self.colors['danger'], self.colors['info']]
            }
        }
    
    def show_overview_metrics(self) -> None:
        """Display overview metrics cards."""
        try:
            self.logger.info("Displaying overview metrics")
            
            # Calculate metrics
            total_jobs = len(self.data)
            unique_companies = self.data['company'].nunique()
            unique_locations = self.data['location'].nunique()
            avg_salary = self._calculate_average_salary()
            
            # Create metrics columns
            col1, col2, col3, col4 = st.columns(4)
            
            with col1:
                st.metric(
                    label="Total Jobs",
                    value=f"{total_jobs:,}",
                    delta=None
                )
            
            with col2:
                st.metric(
                    label="Unique Companies",
                    value=f"{unique_companies:,}",
                    delta=None
                )
            
            with col3:
                st.metric(
                    label="Locations",
                    value=f"{unique_locations:,}",
                    delta=None
                )
            
            with col4:
                st.metric(
                    label="Avg Salary",
                    value=f"${avg_salary:,.0f}",
                    delta=None
                )
                
        except Exception as e:
            self.logger.error(f"Error displaying overview metrics: {str(e)}")
            st.error(f"Error displaying metrics: {str(e)}")
    
    def show_salary_distribution(self, title: str = "Salary Distribution") -> None:
        """Display salary distribution chart."""
        try:
            self.logger.info("Creating salary distribution chart")
            
            # Extract salary data
            salary_data = self._extract_salary_data()
            
            if not salary_data:
                st.warning("No salary data available for visualization")
                return
            
            # Create histogram
            fig = px.histogram(
                salary_data,
                x='salary',
                nbins=20,
                title=title,
                labels={'salary': 'Salary ($)', 'count': 'Number of Jobs'},
                color_discrete_sequence=[self.colors['primary']]
            )
            
            # Update layout
            fig.update_layout(
                **self.chart_theme['layout'],
                xaxis_title="Salary ($)",
                yaxis_title="Number of Jobs",
                showlegend=False
            )
            
            st.plotly_chart(fig, use_container_width=True)
            
        except Exception as e:
            self.logger.error(f"Error creating salary distribution chart: {str(e)}")
            st.error(f"Error creating salary chart: {str(e)}")
    
    def show_top_companies(self, top_n: int = 10, title: str = "Top Companies by Job Postings") -> None:
        """Display top companies chart."""
        try:
            self.logger.info(f"Creating top companies chart (top {top_n})")
            
            # Get company counts
            company_counts = self.data['company'].value_counts().head(top_n)
            
            if company_counts.empty:
                st.warning("No company data available for visualization")
                return
            
            # Create horizontal bar chart
            fig = px.bar(
                x=company_counts.values,
                y=company_counts.index,
                orientation='h',
                title=title,
                labels={'x': 'Number of Jobs', 'y': 'Company'},
                color=company_counts.values,
                color_continuous_scale=[self.colors['light'], self.colors['primary']]
            )
            
            # Update layout
            fig.update_layout(
                **self.chart_theme['layout'],
                xaxis_title="Number of Jobs",
                yaxis_title="Company",
                showlegend=False,
                height=400
            )
            
            st.plotly_chart(fig, use_container_width=True)
            
        except Exception as e:
            self.logger.error(f"Error creating top companies chart: {str(e)}")
            st.error(f"Error creating companies chart: {str(e)}")
    
    def show_location_distribution(self, top_n: int = 10, title: str = "Job Distribution by Location") -> None:
        """Display location distribution chart."""
        try:
            self.logger.info(f"Creating location distribution chart (top {top_n})")
            
            # Get location counts
            location_counts = self.data['location'].value_counts().head(top_n)
            
            if location_counts.empty:
                st.warning("No location data available for visualization")
                return
            
            # Create pie chart
            fig = px.pie(
                values=location_counts.values,
                names=location_counts.index,
                title=title,
                color_discrete_sequence=px.colors.qualitative.Set3
            )
            
            # Update layout
            fig.update_layout(
                **self.chart_theme['layout'],
                showlegend=True,
                legend=dict(orientation="v", yanchor="top", y=1, xanchor="left", x=1.01)
            )
            
            st.plotly_chart(fig, use_container_width=True)
            
        except Exception as e:
            self.logger.error(f"Error creating location distribution chart: {str(e)}")
            st.error(f"Error creating location chart: {str(e)}")
    
    def show_skills_demand(self, top_n: int = 15, title: str = "Top Skills in Demand") -> None:
        """Display skills demand chart."""
        try:
            self.logger.info(f"Creating skills demand chart (top {top_n})")
            
            # Extract skills data
            skills_data = self._extract_skills_data()
            
            if not skills_data:
                st.warning("No skills data available for visualization")
                return
            
            # Get top skills
            top_skills = skills_data.head(top_n)
            
            # Create horizontal bar chart
            fig = px.bar(
                x=top_skills.values,
                y=top_skills.index,
                orientation='h',
                title=title,
                labels={'x': 'Number of Mentions', 'y': 'Skill'},
                color=top_skills.values,
                color_continuous_scale=[self.colors['light'], self.colors['success']]
            )
            
            # Update layout
            fig.update_layout(
                **self.chart_theme['layout'],
                xaxis_title="Number of Mentions",
                yaxis_title="Skill",
                showlegend=False,
                height=500
            )
            
            st.plotly_chart(fig, use_container_width=True)
            
        except Exception as e:
            self.logger.error(f"Error creating skills demand chart: {str(e)}")
            st.error(f"Error creating skills chart: {str(e)}")
    
    def show_job_type_distribution(self, title: str = "Job Type Distribution") -> None:
        """Display job type distribution chart."""
        try:
            self.logger.info("Creating job type distribution chart")
            
            # Get job type counts
            job_type_counts = self.data['job_type'].value_counts()
            
            if job_type_counts.empty:
                st.warning("No job type data available for visualization")
                return
            
            # Create pie chart
            fig = px.pie(
                values=job_type_counts.values,
                names=job_type_counts.index,
                title=title,
                color_discrete_sequence=px.colors.qualitative.Pastel
            )
            
            # Update layout
            fig.update_layout(
                **self.chart_theme['layout'],
                showlegend=True
            )
            
            st.plotly_chart(fig, use_container_width=True)
            
        except Exception as e:
            self.logger.error(f"Error creating job type distribution chart: {str(e)}")
            st.error(f"Error creating job type chart: {str(e)}")
    
    def show_experience_level_distribution(self, title: str = "Experience Level Distribution") -> None:
        """Display experience level distribution chart."""
        try:
            self.logger.info("Creating experience level distribution chart")
            
            # Get experience level counts
            exp_level_counts = self.data['experience_level'].value_counts()
            
            if exp_level_counts.empty:
                st.warning("No experience level data available for visualization")
                return
            
            # Create bar chart
            fig = px.bar(
                x=exp_level_counts.index,
                y=exp_level_counts.values,
                title=title,
                labels={'x': 'Experience Level', 'y': 'Number of Jobs'},
                color=exp_level_counts.values,
                color_continuous_scale=[self.colors['light'], self.colors['warning']]
            )
            
            # Update layout
            fig.update_layout(
                **self.chart_theme['layout'],
                xaxis_title="Experience Level",
                yaxis_title="Number of Jobs",
                showlegend=False
            )
            
            st.plotly_chart(fig, use_container_width=True)
            
        except Exception as e:
            self.logger.error(f"Error creating experience level distribution chart: {str(e)}")
            st.error(f"Error creating experience level chart: {str(e)}")
    
    def show_salary_by_experience(self, title: str = "Salary by Experience Level") -> None:
        """Display salary by experience level chart."""
        try:
            self.logger.info("Creating salary by experience level chart")
            
            # Extract salary and experience data
            salary_exp_data = self._extract_salary_experience_data()
            
            if salary_exp_data.empty:
                st.warning("No salary and experience data available for visualization")
                return
            
            # Create box plot
            fig = px.box(
                salary_exp_data,
                x='experience_level',
                y='salary',
                title=title,
                labels={'experience_level': 'Experience Level', 'salary': 'Salary ($)'},
                color='experience_level',
                color_discrete_sequence=px.colors.qualitative.Set2
            )
            
            # Update layout
            fig.update_layout(
                **self.chart_theme['layout'],
                xaxis_title="Experience Level",
                yaxis_title="Salary ($)",
                showlegend=False
            )
            
            st.plotly_chart(fig, use_container_width=True)
            
        except Exception as e:
            self.logger.error(f"Error creating salary by experience chart: {str(e)}")
            st.error(f"Error creating salary by experience chart: {str(e)}")
    
    def show_posting_trends(self, title: str = "Job Posting Trends Over Time") -> None:
        """Display job posting trends over time."""
        try:
            self.logger.info("Creating posting trends chart")
            
            # Extract time series data
            time_series_data = self._extract_time_series_data()
            
            if time_series_data.empty:
                st.warning("No time series data available for visualization")
                return
            
            # Create line chart
            fig = px.line(
                time_series_data,
                x='date',
                y='count',
                title=title,
                labels={'date': 'Date', 'count': 'Number of Jobs Posted'},
                color_discrete_sequence=[self.colors['primary']]
            )
            
            # Add trend line
            fig.add_scatter(
                x=time_series_data['date'],
                y=time_series_data['count'],
                mode='lines+markers',
                name='Trend',
                line=dict(dash='dash', color=self.colors['secondary'])
            )
            
            # Update layout
            fig.update_layout(
                **self.chart_theme['layout'],
                xaxis_title="Date",
                yaxis_title="Number of Jobs Posted",
                showlegend=True
            )
            
            st.plotly_chart(fig, use_container_width=True)
            
        except Exception as e:
            self.logger.error(f"Error creating posting trends chart: {str(e)}")
            st.error(f"Error creating trends chart: {str(e)}")
    
    def show_company_size_analysis(self, title: str = "Company Size Analysis") -> None:
        """Display company size analysis chart."""
        try:
            self.logger.info("Creating company size analysis chart")
            
            # Extract company size data
            company_size_data = self._extract_company_size_data()
            
            if company_size_data.empty:
                st.warning("No company size data available for visualization")
                return
            
            # Create bar chart
            fig = px.bar(
                x=company_size_data.index,
                y=company_size_data.values,
                title=title,
                labels={'x': 'Company Size', 'y': 'Number of Jobs'},
                color=company_size_data.values,
                color_continuous_scale=[self.colors['light'], self.colors['info']]
            )
            
            # Update layout
            fig.update_layout(
                **self.chart_theme['layout'],
                xaxis_title="Company Size",
                yaxis_title="Number of Jobs",
                showlegend=False
            )
            
            st.plotly_chart(fig, use_container_width=True)
            
        except Exception as e:
            self.logger.error(f"Error creating company size analysis chart: {str(e)}")
            st.error(f"Error creating company size chart: {str(e)}")
    
    def show_remote_work_analysis(self, title: str = "Remote Work Analysis") -> None:
        """Display remote work analysis chart."""
        try:
            self.logger.info("Creating remote work analysis chart")
            
            # Extract remote work data
            remote_data = self._extract_remote_work_data()
            
            if remote_data.empty:
                st.warning("No remote work data available for visualization")
                return
            
            # Create pie chart
            fig = px.pie(
                values=remote_data.values,
                names=remote_data.index,
                title=title,
                color_discrete_sequence=[self.colors['success'], self.colors['warning']]
            )
            
            # Update layout
            fig.update_layout(
                **self.chart_theme['layout'],
                showlegend=True
            )
            
            st.plotly_chart(fig, use_container_width=True)
            
        except Exception as e:
            self.logger.error(f"Error creating remote work analysis chart: {str(e)}")
            st.error(f"Error creating remote work chart: {str(e)}")
    
    def show_skills_correlation_matrix(self, title: str = "Skills Correlation Matrix") -> None:
        """Display skills correlation matrix heatmap."""
        try:
            self.logger.info("Creating skills correlation matrix")
            
            # Extract skills correlation data
            correlation_data = self._extract_skills_correlation_data()
            
            if correlation_data.empty:
                st.warning("No skills correlation data available for visualization")
                return
            
            # Create heatmap
            fig = px.imshow(
                correlation_data,
                title=title,
                color_continuous_scale='RdBu',
                aspect='auto'
            )
            
            # Update layout
            fig.update_layout(
                **self.chart_theme['layout'],
                xaxis_title="Skills",
                yaxis_title="Skills"
            )
            
            st.plotly_chart(fig, use_container_width=True)
            
        except Exception as e:
            self.logger.error(f"Error creating skills correlation matrix: {str(e)}")
            st.error(f"Error creating skills correlation chart: {str(e)}")
    
    def show_advanced_analytics(self) -> None:
        """Display advanced analytics dashboard."""
        try:
            self.logger.info("Creating advanced analytics dashboard")
            
            st.header("📊 Advanced Analytics")
            
            # Create tabs for different analytics
            tab1, tab2, tab3, tab4 = st.tabs([
                "📈 Trends", "🔍 Insights", "📊 Correlations", "🎯 Predictions"
            ])
            
            with tab1:
                self._show_trends_analysis()
            
            with tab2:
                self._show_insights_analysis()
            
            with tab3:
                self._show_correlations_analysis()
            
            with tab4:
                self._show_predictions_analysis()
                
        except Exception as e:
            self.logger.error(f"Error creating advanced analytics: {str(e)}")
            st.error(f"Error creating advanced analytics: {str(e)}")
    
    def _show_trends_analysis(self) -> None:
        """Show trends analysis."""
        st.subheader("📈 Market Trends Analysis")
        
        # Time series analysis
        self.show_posting_trends()
        
        # Salary trends
        self.show_salary_by_experience()
        
        # Skills trends
        st.subheader("🛠️ Skills Trends")
        skills_data = self._extract_skills_data()
        if not skills_data.empty:
            st.write("Top trending skills:")
            st.write(skills_data.head(10))
    
    def _show_insights_analysis(self) -> None:
        """Show insights analysis."""
        st.subheader("🔍 Market Insights")
        
        # Generate insights
        insights = self._generate_market_insights()
        
        for insight in insights:
            st.info(insight)
    
    def _show_correlations_analysis(self) -> None:
        """Show correlations analysis."""
        st.subheader("📊 Data Correlations")
        
        # Skills correlation
        self.show_skills_correlation_matrix()
        
        # Other correlations
        st.subheader("💼 Job Characteristics Correlations")
        correlation_data = self._calculate_job_correlations()
        if not correlation_data.empty:
            st.write(correlation_data)
    
    def _show_predictions_analysis(self) -> None:
        """Show predictions analysis."""
        st.subheader("🎯 Market Predictions")
        
        # Salary predictions
        st.write("**Salary Predictions by Experience Level:**")
        salary_predictions = self._predict_salaries()
        st.write(salary_predictions)
        
        # Demand predictions
        st.write("**Skills Demand Predictions:**")
        demand_predictions = self._predict_skills_demand()
        st.write(demand_predictions)
    
    # Helper methods
    def _calculate_average_salary(self) -> float:
        """Calculate average salary from job data."""
        try:
            salary_data = self._extract_salary_data()
            if not salary_data.empty:
                return salary_data['salary'].mean()
            return 0
        except Exception as e:
            self.logger.error(f"Error calculating average salary: {str(e)}")
            return 0
    
    def _extract_salary_data(self) -> pd.DataFrame:
        """Extract salary data for visualization."""
        try:
            salary_data = []
            for _, job in self.data.iterrows():
                salary = job.get('salary', '')
                if salary and '$' in salary:
                    # Extract numeric values from salary string
                    import re
                    numbers = re.findall(r'[\d,]+', salary.replace(',', ''))
                    if numbers:
                        try:
                            salary_value = int(numbers[0])
                            salary_data.append({'salary': salary_value})
                        except ValueError:
                            continue
            
            return pd.DataFrame(salary_data)
        except Exception as e:
            self.logger.error(f"Error extracting salary data: {str(e)}")
            return pd.DataFrame()
    
    def _extract_skills_data(self) -> pd.Series:
        """Extract skills data for visualization."""
        try:
            all_skills = []
            for _, job in self.data.iterrows():
                skills = job.get('skills', [])
                if isinstance(skills, list):
                    all_skills.extend(skills)
                elif isinstance(skills, str):
                    try:
                        skills_list = json.loads(skills)
                        all_skills.extend(skills_list)
                    except:
                        continue
            
            if all_skills:
                skills_series = pd.Series(all_skills)
                return skills_series.value_counts()
            
            return pd.Series()
        except Exception as e:
            self.logger.error(f"Error extracting skills data: {str(e)}")
            return pd.Series()
    
    def _extract_salary_experience_data(self) -> pd.DataFrame:
        """Extract salary and experience data for visualization."""
        try:
            data = []
            for _, job in self.data.iterrows():
                salary = job.get('salary', '')
                experience = job.get('experience_level', '')
                
                if salary and '$' in salary and experience:
                    # Extract numeric values from salary string
                    import re
                    numbers = re.findall(r'[\d,]+', salary.replace(',', ''))
                    if numbers:
                        try:
                            salary_value = int(numbers[0])
                            data.append({
                                'salary': salary_value,
                                'experience_level': experience
                            })
                        except ValueError:
                            continue
            
            return pd.DataFrame(data)
        except Exception as e:
            self.logger.error(f"Error extracting salary experience data: {str(e)}")
            return pd.DataFrame()
    
    def _extract_time_series_data(self) -> pd.DataFrame:
        """Extract time series data for visualization."""
        try:
            # Group by date
            date_counts = self.data['date_posted'].value_counts().sort_index()
            
            # Convert to DataFrame
            data = []
            for date, count in date_counts.items():
                try:
                    # Parse date
                    if isinstance(date, str):
                        parsed_date = pd.to_datetime(date)
                    else:
                        parsed_date = date
                    
                    data.append({
                        'date': parsed_date,
                        'count': count
                    })
                except:
                    continue
            
            df = pd.DataFrame(data)
            if not df.empty:
                df = df.sort_values('date')
            
            return df
        except Exception as e:
            self.logger.error(f"Error extracting time series data: {str(e)}")
            return pd.DataFrame()
    
    def _extract_company_size_data(self) -> pd.Series:
        """Extract company size data for visualization."""
        try:
            # This would need to be implemented based on available data
            # For now, return empty series
            return pd.Series()
        except Exception as e:
            self.logger.error(f"Error extracting company size data: {str(e)}")
            return pd.Series()
    
    def _extract_remote_work_data(self) -> pd.Series:
        """Extract remote work data for visualization."""
        try:
            remote_keywords = ['remote', 'work from home', 'wfh', 'distributed', 'anywhere']
            
            remote_count = 0
            onsite_count = 0
            
            for _, job in self.data.iterrows():
                location = job.get('location', '').lower()
                if any(keyword in location for keyword in remote_keywords):
                    remote_count += 1
                else:
                    onsite_count += 1
            
            return pd.Series([remote_count, onsite_count], index=['Remote', 'On-site'])
        except Exception as e:
            self.logger.error(f"Error extracting remote work data: {str(e)}")
            return pd.Series()
    
    def _extract_skills_correlation_data(self) -> pd.DataFrame:
        """Extract skills correlation data for visualization."""
        try:
            # This would need to be implemented based on available data
            # For now, return empty DataFrame
            return pd.DataFrame()
        except Exception as e:
            self.logger.error(f"Error extracting skills correlation data: {str(e)}")
            return pd.DataFrame()
    
    def _generate_market_insights(self) -> List[str]:
        """Generate market insights."""
        try:
            insights = []
            
            # Basic insights
            total_jobs = len(self.data)
            unique_companies = self.data['company'].nunique()
            
            insights.append(f"📊 Total of {total_jobs:,} jobs analyzed from {unique_companies:,} companies")
            
            # Skills insights
            skills_data = self._extract_skills_data()
            if not skills_data.empty:
                top_skill = skills_data.index[0]
                top_skill_count = skills_data.iloc[0]
                insights.append(f"🛠️ {top_skill} is the most in-demand skill with {top_skill_count} mentions")
            
            # Location insights
            location_counts = self.data['location'].value_counts()
            if not location_counts.empty:
                top_location = location_counts.index[0]
                top_location_count = location_counts.iloc[0]
                insights.append(f"🌍 {top_location} has the most job postings with {top_location_count} jobs")
            
            # Salary insights
            salary_data = self._extract_salary_data()
            if not salary_data.empty:
                avg_salary = salary_data['salary'].mean()
                insights.append(f"💰 Average salary is ${avg_salary:,.0f}")
            
            return insights
        except Exception as e:
            self.logger.error(f"Error generating market insights: {str(e)}")
            return ["Error generating insights"]
    
    def _calculate_job_correlations(self) -> pd.DataFrame:
        """Calculate job characteristics correlations."""
        try:
            # This would need to be implemented based on available data
            # For now, return empty DataFrame
            return pd.DataFrame()
        except Exception as e:
            self.logger.error(f"Error calculating job correlations: {str(e)}")
            return pd.DataFrame()
    
    def _predict_salaries(self) -> pd.DataFrame:
        """Predict salaries by experience level."""
        try:
            # This would need to be implemented with machine learning
            # For now, return empty DataFrame
            return pd.DataFrame()
        except Exception as e:
            self.logger.error(f"Error predicting salaries: {str(e)}")
            return pd.DataFrame()
    
    def _predict_skills_demand(self) -> pd.DataFrame:
        """Predict skills demand trends."""
        try:
            # This would need to be implemented with machine learning
            # For now, return empty DataFrame
            return pd.DataFrame()
        except Exception as e:
            self.logger.error(f"Error predicting skills demand: {str(e)}")
            return pd.DataFrame()

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
    
    dashboard = JobDashboard(sample_data)
    
    # Display charts
    dashboard.show_overview_metrics()
    dashboard.show_salary_distribution()
    dashboard.show_top_companies()
    dashboard.show_location_distribution()
    dashboard.show_skills_demand()
