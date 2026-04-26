"""
Dashboard Package
Contains modules for Streamlit dashboard components and visualizations.
"""

__version__ = "1.0.0"

from .visualizations import JobDashboard
from .filters import JobFilters
from .components import JobCard, MetricCard
from .pages import SearchPage, AnalyticsPage, SimilarJobsPage

__all__ = [
    'JobDashboard',
    'JobFilters',
    'JobCard',
    'MetricCard',
    'SearchPage',
    'AnalyticsPage',
    'SimilarJobsPage'
]
