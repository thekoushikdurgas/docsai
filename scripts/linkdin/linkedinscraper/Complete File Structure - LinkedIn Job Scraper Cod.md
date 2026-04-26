<img src="https://r2cdn.perplexity.ai/pplx-full-logo-primary-dark%402x.png" style="height:64px;margin-right:32px"/>

# Complete File Structure - LinkedIn Job Scraper Codebase

Here's the comprehensive file structure for the LinkedIn Job Scraper project with vector database integration:

## 📁 Root Directory Structure

```          # Root project directory
├── main_app.py                      # Main Streamlit application (~15KB)
├── requirements.txt                 # Python dependencies (~1KB)
├── README.md                        # Project documentation (~8KB)
├── .env.example                     # Environment variables template (~0.5KB)
├── .gitignore                       # Git ignore patterns (~1KB)
├── config.yaml                      # Application configuration (~2KB)
```


## 📁 Core Modules

### 🔍 **scraper/** - Job Scraping Engine

```
scraper/
├── __init__.py                      # Package initialization (~0.5KB)
├── linkedin_scraper.py              # Main scraping functionality (~12KB)
├── data_processor.py                # Data cleaning & processing (~6KB)
├── url_builder.py                   # URL construction utilities (~3KB)
└── rate_limiter.py                  # Request rate limiting (~2KB)
```


### 💾 **database/** - Vector Database Operations

```
database/
├── __init__.py                      # Package initialization (~0.5KB)
├── vector_db.py                     # ChromaDB operations (~18KB)
├── schemas.py                       # Data models & validation (~4KB)
├── embeddings.py                    # Text embedding utilities (~3KB)
└── migrations.py                    # Database migrations (~2KB)
```


### 📊 **dashboard/** - Streamlit Interface

```
dashboard/
├── __init__.py                      # Package initialization (~0.5KB)
├── visualizations.py               # Charts & graphs (~8KB)
├── filters.py                       # Search filtering UI (~5KB)
├── components.py                    # Reusable UI components (~6KB)
└── pages.py                         # Multi-page navigation (~4KB)
```


### 🛠️ **utils/** - Utility Functions

```
utils/
├── __init__.py                      # Package initialization (~0.5KB)
├── helpers.py                       # Comprehensive utilities (~15KB)
├── config.py                        # Configuration management (~3KB)
├── logger.py                        # Logging utilities (~2KB)
├── cache.py                         # Streamlit caching (~2KB)
└── validators.py                    # Data validation (~3KB)
```


## 🧪 **tests/** - Test Suite

```
tests/
├── __init__.py                      # Test package init (~0.2KB)
├── conftest.py                      # Pytest configuration (~2KB)
├── test_scraper.py                  # Scraper functionality tests (~4KB)
├── test_database.py                 # Database operation tests (~5KB)
├── test_dashboard.py                # Dashboard component tests (~3KB)
├── test_utils.py                    # Utility function tests (~4KB)
└── fixtures/                        # Test data directory
    ├── sample_jobs.json             # Sample job data (~10KB)
    └── mock_responses.json          # Mock HTTP responses (~5KB)
```


## 📚 **docs/** - Documentation

```
docs/
├── api_reference.md                 # Complete API docs (~12KB)
├── deployment_guide.md              # Deployment instructions (~6KB)
├── user_guide.md                    # User documentation (~8KB)
├── architecture.md                  # System architecture (~5KB)
└── images/                          # Documentation images
    ├── architecture_diagram.png     # System diagram
    ├── dashboard_screenshot.png     # Dashboard UI
    └── search_interface.png         # Search interface
```


## 🚀 **scripts/** - Automation \& Utilities

```
scripts/
├── setup.sh                        # Environment setup (~1KB)
├── deploy.sh                       # Deployment automation (~1.5KB)
├── backup_db.py                    # Database backup (~2KB)
├── migrate_data.py                 # Data migration (~3KB)
└── performance_test.py             # Performance testing (~2KB)
```


## 📁 **data/** - Data Storage (Git-ignored)

```
data/
├── sample_data.csv                  # Development sample data (~5KB)
├── .gitkeep                        # Keep directory in git
├── exports/                        # Exported data files (ignored)
└── backups/                        # Database backups (ignored)
```


## 📝 **logs/** \& **chroma_db/** - Runtime Directories

```
logs/                               # Application logs (ignored)
└── .gitkeep                       # Keep directory structure

chroma_db/                         # ChromaDB files (auto-created, ignored)
```


## 📊 Project Statistics

- **Total Directories**: 15
- **Total Files**: 50+
- **Estimated Size**: ~150KB
- **Main Languages**: Python, Markdown, YAML, Shell Script
- **Key Dependencies**: Streamlit, ChromaDB, BeautifulSoup, Plotly, Sentence-Transformers


## 🔑 Key File Descriptions

### **Core Application Files**

- **`main_app.py`**: Complete Streamlit dashboard with search, analytics, and visualization
- **`linkedin_scraper.py`**: Ethical web scraping with rate limiting and anti-detection
- **`vector_db.py`**: ChromaDB integration with semantic search capabilities
- **`helpers.py`**: Comprehensive data processing and utility functions


### **Configuration Files**

- **`requirements.txt`**: All Python dependencies with versions
- **`config.yaml`**: Centralized application configuration
- **`.env.example`**: Environment variables template


### **Development Files**

- **`README.md`**: Complete setup and usage guide
- **Test files**: Comprehensive test coverage for all modules
- **Documentation**: API reference, user guides, and architecture docs

This structure provides a production-ready, scalable codebase with proper separation of concerns, comprehensive testing, and complete documentation for the LinkedIn Job Scraper with vector database integration.

