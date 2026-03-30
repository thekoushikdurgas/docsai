"""Data analysis module."""
from .analyze_company_names import main as analyze_company_names
from .comprehensive_data_analysis import main as comprehensive_data_analysis

__all__ = [
    "analyze_company_names",
    "comprehensive_data_analysis",
]
