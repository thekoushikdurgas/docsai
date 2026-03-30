"""
Sample data constants for synthetic data generation.

This module contains all the static data arrays and mappings used to generate
realistic companies and contacts.
"""

from typing import Dict, List, Tuple

# ============================================
# Industries
# ============================================

INDUSTRIES: List[str] = [
    # Technology
    "Software Development", "Cloud Computing", "Artificial Intelligence", "Machine Learning",
    "Cybersecurity", "Data Analytics", "Internet of Things", "Blockchain", "FinTech",
    "EdTech", "HealthTech", "E-commerce", "SaaS", "PaaS", "IaaS", "DevOps",
    
    # Traditional
    "Manufacturing", "Retail", "Healthcare", "Pharmaceuticals", "Biotechnology",
    "Financial Services", "Banking", "Insurance", "Real Estate", "Construction",
    
    # Services
    "Consulting", "Legal Services", "Accounting", "Marketing", "Advertising",
    "Public Relations", "Human Resources", "Staffing", "Recruiting",
    
    # Media & Entertainment
    "Media", "Entertainment", "Gaming", "Music", "Film Production", "Publishing",
    "Broadcasting", "Streaming Services", "Social Media", "Content Creation",
    
    # Energy & Utilities
    "Oil & Gas", "Renewable Energy", "Solar Energy", "Wind Energy", "Utilities",
    "Electric Vehicles", "Clean Technology", "Energy Storage",
    
    # Transportation & Logistics
    "Transportation", "Logistics", "Supply Chain", "Shipping", "Aviation",
    "Automotive", "Railways", "Warehousing", "Last Mile Delivery",
    
    # Consumer Goods
    "Consumer Electronics", "Food & Beverage", "Fashion", "Apparel", "Cosmetics",
    "Home Goods", "Furniture", "Luxury Goods", "Sports Equipment",
    
    # Other
    "Telecommunications", "Aerospace", "Defense", "Agriculture", "Mining",
    "Hospitality", "Travel", "Tourism", "Education", "Non-Profit",
]

# ============================================
# Keywords
# ============================================

KEYWORDS: List[str] = [
    # Business Models
    "B2B", "B2C", "D2C", "Marketplace", "Platform", "Subscription", "Freemium",
    "Enterprise", "SMB", "Startup", "Scale-up", "Unicorn", "Decacorn",
    
    # Growth Stage
    "Pre-seed", "Seed", "Series A", "Series B", "Series C", "Late Stage",
    "IPO", "Public", "Private", "Bootstrapped", "Venture-backed",
    
    # Technology Focus
    "API-first", "Mobile-first", "Cloud-native", "Open Source", "Proprietary",
    "Low-code", "No-code", "AI-powered", "Data-driven", "Automation",
    
    # Market Position
    "Market Leader", "Disruptor", "Challenger", "Emerging", "Established",
    "Global", "Regional", "Local", "Niche", "Mass Market",
    
    # Business Attributes
    "Fast-growing", "Profitable", "High-growth", "Sustainable", "Innovation",
    "Remote-first", "Hybrid", "Distributed", "Agile", "Lean",
    
    # Industry Specific
    "RegTech", "InsurTech", "PropTech", "AgriTech", "FoodTech", "CleanTech",
    "BioTech", "MedTech", "LegalTech", "HRTech", "MarTech", "AdTech",
]

# ============================================
# Technologies
# ============================================

TECHNOLOGIES: List[str] = [
    # Programming Languages
    "Python", "JavaScript", "TypeScript", "Java", "Go", "Rust", "C++", "C#",
    "Ruby", "PHP", "Kotlin", "Swift", "Scala", "R", "MATLAB",
    
    # Frontend
    "React", "Vue.js", "Angular", "Next.js", "Nuxt.js", "Svelte", "jQuery",
    "Tailwind CSS", "Bootstrap", "Material UI", "Chakra UI",
    
    # Backend
    "Node.js", "Django", "Flask", "FastAPI", "Spring Boot", "Express.js",
    "Ruby on Rails", "Laravel", "ASP.NET", "Gin", "Echo",
    
    # Databases
    "PostgreSQL", "MySQL", "MongoDB", "Redis", "Elasticsearch", "Cassandra",
    "DynamoDB", "Firebase", "Supabase", "CockroachDB", "TimescaleDB",
    
    # Cloud & Infrastructure
    "AWS", "Google Cloud", "Azure", "DigitalOcean", "Heroku", "Vercel",
    "Netlify", "Cloudflare", "Kubernetes", "Docker", "Terraform",
    
    # Data & ML
    "TensorFlow", "PyTorch", "Scikit-learn", "Pandas", "NumPy", "Spark",
    "Hadoop", "Kafka", "Airflow", "dbt", "Snowflake", "Databricks",
    
    # DevOps & Tools
    "Git", "GitHub", "GitLab", "Jenkins", "CircleCI", "GitHub Actions",
    "Ansible", "Prometheus", "Grafana", "DataDog", "New Relic", "Sentry",
    
    # Communication & Collaboration
    "Slack", "Microsoft Teams", "Zoom", "Notion", "Confluence", "Jira",
    "Linear", "Asana", "Monday.com", "Figma", "Miro",
]

# ============================================
# Company Name Components
# ============================================

COMPANY_NAME_PREFIXES: List[str] = [
    "Tech", "Digital", "Smart", "Cloud", "Data", "Cyber", "Net", "Web",
    "App", "Soft", "Info", "Inno", "Pro", "Prime", "Elite", "Alpha",
    "Beta", "Gamma", "Delta", "Omega", "Hyper", "Ultra", "Meta", "Neo",
    "Quantum", "Vertex", "Apex", "Peak", "Summit", "Zenith", "Stellar",
    "Astro", "Cosmo", "Global", "Inter", "Trans", "Multi", "Omni", "Uni",
    "Flex", "Agile", "Swift", "Rapid", "Turbo", "Power", "Force", "Core",
    "Fusion", "Synergy", "Vector", "Matrix", "Nexus", "Pulse", "Wave",
]

COMPANY_NAME_SUFFIXES: List[str] = [
    "Labs", "Works", "Systems", "Solutions", "Technologies", "Tech", "Soft",
    "Ware", "Net", "Cloud", "Data", "Logic", "Minds", "Dynamics", "Ventures",
    "Group", "Corp", "Inc", "Co", "Hub", "Space", "Studio", "Digital",
    "Analytics", "AI", "Intelligence", "Innovations", "Partners", "Global",
    "Interactive", "Media", "Networks", "Services", "Consulting", "Platform",
    "Apps", "Mobile", "Connect", "Link", "Bridge", "Gate", "Port", "Base",
]

COMPANY_NAME_WORDS: List[str] = [
    "Acme", "Apex", "Horizon", "Pinnacle", "Summit", "Vanguard", "Pioneer",
    "Catalyst", "Momentum", "Velocity", "Altitude", "Latitude", "Longitude",
    "Spectrum", "Prism", "Helix", "Spiral", "Orbit", "Galaxy", "Nova",
    "Phoenix", "Titan", "Atlas", "Zeus", "Apollo", "Athena", "Hermes",
    "Artemis", "Poseidon", "Hera", "Mercury", "Venus", "Mars", "Jupiter",
    "Saturn", "Neptune", "Pluto", "Orion", "Andromeda", "Sirius", "Polaris",
    "Aurora", "Eclipse", "Equinox", "Solstice", "Ember", "Blaze", "Spark",
    "Thunder", "Lightning", "Storm", "Tempest", "Cyclone", "Tornado", "Vortex",
]

# ============================================
# Location Data
# ============================================

COUNTRIES: List[str] = [
    "USA", "UK", "Canada", "Germany", "France", "India", "Australia",
    "Japan", "Brazil", "Mexico", "Netherlands", "Sweden", "Singapore",
    "Israel", "South Korea", "China", "Spain", "Italy", "Switzerland",
]

STATES_BY_COUNTRY: Dict[str, List[str]] = {
    "USA": ["CA", "NY", "TX", "FL", "IL", "PA", "OH", "GA", "NC", "MI", "WA", "MA", "CO", "AZ", "VA"],
    "UK": ["England", "Scotland", "Wales", "Northern Ireland"],
    "Canada": ["ON", "BC", "QC", "AB", "MB", "SK", "NS", "NB"],
    "Germany": ["Bavaria", "Berlin", "Hamburg", "Hesse", "North Rhine-Westphalia", "Baden-Württemberg"],
    "France": ["Île-de-France", "Provence-Alpes-Côte d'Azur", "Auvergne-Rhône-Alpes", "Occitanie"],
    "India": ["Maharashtra", "Karnataka", "Delhi", "Tamil Nadu", "Telangana", "Gujarat", "West Bengal"],
    "Australia": ["NSW", "VIC", "QLD", "WA", "SA", "TAS"],
    "Japan": ["Tokyo", "Osaka", "Kanagawa", "Aichi", "Fukuoka", "Hokkaido"],
    "Brazil": ["São Paulo", "Rio de Janeiro", "Minas Gerais", "Bahia", "Rio Grande do Sul"],
    "Mexico": ["CDMX", "Jalisco", "Nuevo León", "Estado de México", "Puebla"],
    "Netherlands": ["North Holland", "South Holland", "Utrecht", "North Brabant"],
    "Sweden": ["Stockholm", "Västra Götaland", "Skåne", "Uppsala"],
    "Singapore": ["Central Region", "East Region", "North Region", "West Region"],
    "Israel": ["Tel Aviv", "Jerusalem", "Haifa", "Central"],
    "South Korea": ["Seoul", "Gyeonggi", "Busan", "Incheon"],
    "China": ["Beijing", "Shanghai", "Guangdong", "Zhejiang", "Jiangsu"],
    "Spain": ["Madrid", "Catalonia", "Andalusia", "Valencia"],
    "Italy": ["Lombardy", "Lazio", "Veneto", "Emilia-Romagna", "Piedmont"],
    "Switzerland": ["Zürich", "Geneva", "Bern", "Basel", "Vaud"],
}

CITIES_BY_COUNTRY: Dict[str, List[str]] = {
    "USA": ["New York", "San Francisco", "Los Angeles", "Chicago", "Boston", "Seattle", "Austin", "Denver", "Miami", "Atlanta"],
    "UK": ["London", "Manchester", "Birmingham", "Edinburgh", "Bristol", "Leeds", "Glasgow", "Cambridge", "Oxford"],
    "Canada": ["Toronto", "Vancouver", "Montreal", "Calgary", "Ottawa", "Edmonton", "Waterloo"],
    "Germany": ["Berlin", "Munich", "Hamburg", "Frankfurt", "Cologne", "Stuttgart", "Düsseldorf"],
    "France": ["Paris", "Lyon", "Marseille", "Toulouse", "Nice", "Nantes", "Bordeaux"],
    "India": ["Bangalore", "Mumbai", "Delhi", "Hyderabad", "Chennai", "Pune", "Gurgaon", "Noida"],
    "Australia": ["Sydney", "Melbourne", "Brisbane", "Perth", "Adelaide", "Canberra"],
    "Japan": ["Tokyo", "Osaka", "Yokohama", "Nagoya", "Fukuoka", "Kyoto", "Sapporo"],
    "Brazil": ["São Paulo", "Rio de Janeiro", "Belo Horizonte", "Brasília", "Curitiba", "Porto Alegre"],
    "Mexico": ["Mexico City", "Guadalajara", "Monterrey", "Puebla", "Tijuana", "León"],
    "Netherlands": ["Amsterdam", "Rotterdam", "The Hague", "Utrecht", "Eindhoven"],
    "Sweden": ["Stockholm", "Gothenburg", "Malmö", "Uppsala"],
    "Singapore": ["Singapore"],
    "Israel": ["Tel Aviv", "Jerusalem", "Haifa", "Herzliya", "Ra'anana"],
    "South Korea": ["Seoul", "Busan", "Incheon", "Daegu", "Daejeon"],
    "China": ["Beijing", "Shanghai", "Shenzhen", "Hangzhou", "Guangzhou", "Chengdu"],
    "Spain": ["Madrid", "Barcelona", "Valencia", "Seville", "Bilbao"],
    "Italy": ["Milan", "Rome", "Turin", "Florence", "Bologna", "Naples"],
    "Switzerland": ["Zürich", "Geneva", "Basel", "Bern", "Lausanne"],
}

DOMAIN_EXTENSIONS: List[str] = [
    ".com", ".io", ".co", ".ai", ".tech", ".app", ".dev", ".cloud",
    ".net", ".org", ".biz", ".info", ".solutions", ".digital", ".software",
]

# ============================================
# Company Size and Funding Data
# ============================================

EmployeeCountRange = Tuple[int, int]
AnnualRevenueRange = Tuple[int, int]
TotalFundingRange = Tuple[int, int]

EMPLOYEE_COUNT_RANGES: Dict[str, EmployeeCountRange] = {
    "startup": (1, 50),
    "small": (51, 200),
    "medium": (201, 1000),
    "large": (1001, 10000),
    "enterprise": (10001, 500000),
}

ANNUAL_REVENUE_RANGES: Dict[str, AnnualRevenueRange] = {
    "startup": (0, 5_000_000),
    "small": (5_000_001, 50_000_000),
    "medium": (50_000_001, 500_000_000),
    "large": (500_000_001, 5_000_000_000),
    "enterprise": (5_000_000_001, 100_000_000_000),
}

TOTAL_FUNDING_RANGES: Dict[str, TotalFundingRange] = {
    "bootstrapped": (0, 100_000),
    "pre_seed": (100_001, 500_000),
    "seed": (500_001, 3_000_000),
    "series_a": (3_000_001, 15_000_000),
    "series_b": (15_000_001, 50_000_000),
    "series_c": (50_000_001, 150_000_000),
    "late_stage": (150_000_001, 1_000_000_000),
    "public": (0, 0),
}

COMPANY_SIZE_WEIGHTS: Dict[str, float] = {
    "startup": 0.30,
    "small": 0.30,
    "medium": 0.20,
    "large": 0.12,
    "enterprise": 0.08,
}

FUNDING_STAGE_WEIGHTS: Dict[str, float] = {
    "bootstrapped": 0.20,
    "pre_seed": 0.10,
    "seed": 0.20,
    "series_a": 0.18,
    "series_b": 0.12,
    "series_c": 0.08,
    "late_stage": 0.07,
    "public": 0.05,
}

FUNDING_STAGES: List[str] = [
    "Bootstrapped", "Pre-Seed", "Seed", "Series A", "Series B",
    "Series C", "Series D", "Series E", "Late Stage", "IPO", "Public",
]

# ============================================
# Contact Data
# ============================================

TITLES: List[str] = [
    # Engineering & Tech
    "Software Engineer", "Senior Software Engineer", "Staff Engineer", "Principal Engineer",
    "Full Stack Developer", "Frontend Developer", "Backend Developer", "Mobile Developer",
    "DevOps Engineer", "Site Reliability Engineer", "Cloud Architect", "Infrastructure Engineer",
    "Security Engineer", "Cybersecurity Specialist", "Penetration Tester", "Security Architect",
    "Machine Learning Engineer", "AI Engineer", "Data Engineer", "Data Scientist", "MLOps Engineer",
    "QA Engineer", "Test Automation Engineer", "Quality Assurance Lead", "Performance Engineer",
    "Blockchain Developer", "Smart Contract Developer", "Web3 Engineer", "Cryptocurrency Analyst",
    
    # Product & Design
    "Product Manager", "Senior Product Manager", "Product Owner", "Technical Product Manager",
    "UI/UX Designer", "Product Designer", "Visual Designer", "Interaction Designer",
    "Design Systems Lead", "Creative Director", "User Experience Researcher", "Design Strategist",
    
    # Data & Analytics
    "Data Analyst", "Business Intelligence Analyst", "Data Architect", "Analytics Engineer",
    "Business Analyst", "Product Analyst", "Growth Analyst", "Marketing Analyst",
    
    # Marketing & Growth
    "Marketing Manager", "Digital Marketing Specialist", "Content Marketing Manager",
    "Growth Marketing Manager", "SEO Specialist", "Social Media Manager", "Brand Manager",
    "Marketing Automation Specialist", "Performance Marketing Manager", "Community Manager",
    "Influencer Relations Manager", "Content Creator", "Copywriter", "Marketing Technologist",
    
    # Sales & Business Development
    "Sales Representative", "Account Executive", "Sales Development Representative",
    "Business Development Manager", "Enterprise Sales Manager", "Sales Engineer",
    "Customer Success Manager", "Account Manager", "Partnership Manager", "Channel Manager",
    
    # Operations & Strategy
    "Operations Manager", "Business Operations Analyst", "Strategy Manager",
    "Program Manager", "Project Manager", "Scrum Master", "Agile Coach",
    "Process Improvement Specialist", "Operations Analyst", "Supply Chain Manager",
    
    # HR & People
    "HR Manager", "Talent Acquisition Specialist", "People Operations Manager",
    "HR Business Partner", "Learning & Development Manager", "Compensation Analyst",
    "Employee Experience Manager", "Diversity & Inclusion Manager", "Recruiter",
    
    # Finance & Accounting
    "Finance Analyst", "Financial Controller", "Accounting Manager", "FP&A Analyst",
    "Treasury Analyst", "Tax Specialist", "Auditor", "Financial Planning Manager",
    
    # Executive & Leadership
    "CEO", "CTO", "CFO", "COO", "CMO", "CPO", "CHRO", "Chief Data Officer",
    "VP of Engineering", "VP of Product", "VP of Sales", "VP of Marketing",
    "Director of Engineering", "Director of Product", "Director of Sales",
    
    # Specialized & Emerging Roles
    "Customer Experience Designer", "Voice of Customer Analyst", "Technical Writer",
    "Developer Advocate", "Developer Relations Manager", "Open Source Program Manager",
    "Ethics Engineer", "Privacy Engineer", "Compliance Manager", "Legal Counsel",
    "Research Scientist", "Applied Scientist", "Technical Program Manager",
    "Solutions Architect", "Customer Success Engineer", "Implementation Specialist",
]

DEPARTMENTS: List[str] = [
    "Engineering", "Product", "Sales", "Marketing", "HR", "Finance",
    "Operations", "Customer Success", "Support", "Legal",
]

SENIORITY_LEVELS: List[str] = [
    "Junior", "Mid", "Senior", "Lead", "Principal", "Executive",
]

EMAIL_STATUSES: List[str] = [
    "verified", "unverified", "bounced", "invalid",
]

CONTACT_STAGES: List[str] = [
    "Lead", "Contacted", "Qualified", "Proposal", "Negotiation", "Closed Won", "Closed Lost",
]

