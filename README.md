# Content Automation Platform

A comprehensive Django + Next.js platform that uses AI to generate, manage, and publish content across multiple branded sites. Each site has its own topic, branding, and dynamic content pipeline with full admin controls and plagiarism prevention.

---

## 🧠 What It Does

- **AI Content Generation**: Uses OpenAI GPT-4 to generate professional articles from trending topics
- **Multi-Site Management**: Supports multiple branded sites with dynamic theming and routing
- **Content Workflow**: Complete approval system with draft, pending, approved, and rejected states
- **Advanced News Scraping**: Automated content discovery from RSS feeds with AI-enhanced analysis
- **Admin Interface**: Full-featured admin dashboard for content management and site oversight
- **Authentication**: Secure session-based authentication with CSRF protection
- **Plagiarism Prevention**: Built-in content originality checking and source attribution
- **Daily Top 3 Articles**: Automated compilation of trending topics into comprehensive articles

---

## 🛠 Tech Stack

**Backend:**
- Django 5.2.3 + Django REST Framework 3.16.0
- PostgreSQL database with psycopg2-binary 2.9.10
- Python-dotenv 1.1.0 for environment management
- OpenAI API integration (openai 1.12.0)
- Django CORS headers 4.3.1 for cross-origin requests
- Django Filter 24.1 for advanced querying
- BeautifulSoup4 4.12.2 for web scraping
- Feedparser 6.0.11 for RSS feed processing
- Newspaper3k 0.2.8 for advanced content extraction

**Frontend:**
- Next.js 15.3.4 with App Router
- React 19.0.0
- TypeScript 5.x
- Tailwind CSS 4.x for styling
- Client-side components for admin functionality

**AI & Automation:**
- OpenAI GPT-4 for content generation
- RSS feed aggregation with feedparser
- Web scraping with beautifulsoup4 and newspaper3k
- Advanced content extraction with trafilatura
- Plagiarism detection and prevention system
- AI-enhanced topic analysis and sentiment detection

**Dev & Infra:**
- Git version control
- Environment-based configuration
- CSRF token protection
- Session-based authentication
- Comprehensive logging and error handling

---

## 📁 Project Structure

```
content-automation-platform/
├── backend/                 # Django backend
│   ├── core/               # Django settings and configuration
│   │   ├── settings.py     # Main Django settings
│   │   ├── urls.py         # URL routing with auth endpoints
│   │   └── management/     # Django management commands
│   ├── articles/           # Article models, views, and management
│   │   ├── models.py       # Article model with status workflow
│   │   ├── views.py        # Article API views and filtering
│   │   ├── serializers.py  # DRF serializers
│   │   └── management/     # Article generation commands
│   ├── sites/              # Site models and configuration
│   │   ├── models.py       # Site model with branding
│   │   ├── views.py        # Site API views
│   │   └── serializers.py  # Site serializers
│   ├── services/           # AI services and content automation
│   │   ├── ai_generator.py # OpenAI content generation
│   │   ├── ai_news_scraper.py # RSS scraping and analysis
│   │   ├── content_automation.py # Content orchestration
│   │   └── plagiarism_prevention.py # Plagiarism detection
│   ├── tests/              # Test files and management commands
│   ├── requirements.txt    # Python dependencies
│   ├── requirements_ai_scraping.txt # Advanced AI dependencies
│   ├── AI_SCRAPER_README.md # AI scraper documentation
│   └── PLAGIARISM_PREVENTION_README.md # Plagiarism system docs
├── frontend/               # Next.js frontend
│   ├── src/
│   │   ├── app/           # Next.js app router pages
│   │   │   ├── admin/     # Admin interface pages
│   │   │   │   ├── articles/ # Article management
│   │   │   │   ├── ai-content/ # AI content generation
│   │   │   │   └── login/ # Authentication
│   │   │   └── [site]/    # Dynamic site pages
│   │   │       └── [slug]/ # Individual article pages
│   │   ├── lib/           # Utility functions
│   │   │   ├── auth.tsx   # Authentication utilities
│   │   │   └── getSiteConfig.ts # Site configuration
│   │   └── types/         # TypeScript type definitions
│   ├── package.json       # Node.js dependencies
│   └── tsconfig.json      # TypeScript configuration
├── data/                   # Configuration files
│   └── site_config.json   # Site configuration and branding
└── assets/                 # Static assets and images
```

---

## ✅ Getting Started (Local Development)

### Prerequisites
- Python 3.8+
- Node.js 18+
- PostgreSQL
- OpenAI API key

### Backend Setup

1. **Clone the repository**
   ```bash
   git clone <repository-url>
   cd content-automation-platform
   ```

2. **Set up Python environment**
   ```bash
   cd backend
   python -m venv .venv
   source .venv/bin/activate  # On Windows: .venv\Scripts\activate
   pip install -r requirements.txt
   ```

3. **Configure environment variables**
   Create a `.env` file in the `backend/` directory:
   ```env
   DEBUG=True
   DJANGO_SECRET_KEY=your-secret-key
   POSTGRES_DB=content_automation
   POSTGRES_USER=your_db_user
   POSTGRES_PASSWORD=your_db_password
   POSTGRES_HOST=localhost
   POSTGRES_PORT=5432
   OPENAI_API_KEY=your-openai-api-key
   ```

4. **Set up database**
   ```bash
   python manage.py migrate
   python manage.py createsuperuser
   ```

5. **Create admin user**
   ```bash
   python manage.py create_admin_user
   ```

6. **Start the backend server**
   ```bash
   python manage.py runserver
   ```

### Frontend Setup

1. **Install dependencies**
   ```bash
   cd frontend
   npm install
   ```

2. **Start the development server**
   ```bash
   npm run dev
   ```

3. **Access the application**
   - Frontend: http://localhost:3000
   - Admin interface: http://localhost:3000/admin
   - Backend API: http://localhost:8000/api/

---

## 🚀 Key Features

### Multi-Site Content Management
- Dynamic site configuration with custom branding (colors, logos, descriptions)
- Site-specific article routing and theming
- Centralized content management across all sites
- Support for multiple branded sites (AI Skills, Green Living, etc.)

### AI-Powered Content Generation
- **OpenAI Integration**: GPT-4 powered article generation with professional formatting
- **Trending Topic Discovery**: AI-enhanced analysis of RSS feeds for relevant content
- **Daily Top 3 Articles**: Automated compilation of multiple topics into comprehensive articles
- **Plagiarism Prevention**: Built-in content originality checking and source attribution
- **Content Quality Analysis**: AI-powered sentiment analysis and quality scoring

### Advanced News Scraping
- **RSS Feed Aggregation**: Multiple reliable RSS sources for different categories
- **AI-Enhanced Analysis**: Content analysis with keyword extraction and sentiment detection
- **Source Quality Validation**: Automatic assessment of content reliability
- **Duplicate Detection**: Semantic similarity checking to avoid content duplication
- **Category-Specific Feeds**: Specialized feeds for AI, tech, business, sustainability, etc.

### Admin Interface
- **Comprehensive Dashboard**: Article statistics and overview
- **Article Approval Workflow**: Pending/approved/rejected status management
- **Bulk Operations**: Mass article management capabilities
- **Site Configuration**: Branding and theme management
- **User Management**: Authentication and authorization controls
- **AI Content Generation**: Direct interface for creating AI-generated content

### Content Workflow
- **Draft Creation**: AI-generated content with plagiarism checking
- **Admin Review**: Approval/rejection system with status tracking
- **Source Attribution**: Automatic source linking and attribution
- **Content Filtering**: Advanced search and filter capabilities
- **Publication Management**: Status-based content publishing

---

## 🔧 Management Commands

The platform includes several Django management commands for content generation and testing:

```bash
# Generate AI content for a specific site
python manage.py generate_ai_content --site "AI Skills"

# Generate test articles
python manage.py generate_test_articles

# Create admin user
python manage.py create_admin_user

# Check admin users
python manage.py check_admin_users

# Test AI scraper functionality
python manage.py test_ai_scraper

# Test plagiarism prevention system
python manage.py test_plagiarism_prevention
```

---

## 📊 API Endpoints

### Authentication
- `POST /api/auth/login/` - Secure user login with rate limiting
- `POST /api/auth/logout/` - User logout
- `GET /api/auth/check/` - Check authentication status

### Articles
- `GET /api/articles/` - List articles with advanced filtering
- `POST /api/articles/` - Create new article
- `GET /api/articles/{id}/` - Get article details
- `PUT /api/articles/{id}/` - Update article
- `DELETE /api/articles/{id}/` - Delete article
- `POST /api/articles/{id}/approve/` - Approve article
- `POST /api/articles/{id}/reject/` - Reject article

### AI Content Generation
- `POST /api/ai/generate-content/` - Generate AI content with plagiarism checking
- `GET /api/ai/trending-topics/` - Get AI-enhanced trending topics

### Sites
- `GET /api/sites/` - List sites with branding information
- `GET /api/sites/{id}/` - Get site details

---

## 🔒 Security Features

- **Session-based Authentication**: Secure user sessions with configurable timeouts
- **CSRF Protection**: Comprehensive CSRF token protection on all forms
- **Admin-only Access**: Protected endpoints for sensitive operations
- **Input Validation**: Comprehensive input sanitization and validation
- **Rate Limiting**: Basic rate limiting on authentication endpoints
- **Secure Headers**: Security headers for XSS protection and content type sniffing
- **CORS Configuration**: Proper cross-origin request handling

---

## 🎯 Current Status

The platform is **fully functional** with the following completed features:

✅ **Core Platform**: Django 5.2.3 backend, Next.js 15.3.4 frontend, PostgreSQL database  
✅ **Authentication**: Complete admin authentication system with session management  
✅ **AI Integration**: OpenAI GPT-4 content generation with fallback mock content  
✅ **Advanced Scraping**: RSS feed aggregation with AI-enhanced analysis  
✅ **Admin Interface**: Full-featured content management dashboard  
✅ **Multi-Site Support**: Dynamic site configuration and branding  
✅ **Content Workflow**: Article approval and status management  
✅ **Plagiarism Prevention**: Content originality checking and source attribution  
✅ **Security**: CSRF protection, session management, and secure headers  

**Next Phase**: AI content quality improvements, advanced scraping capabilities, and UI/UX enhancements.

---

## 📚 Documentation

The project includes comprehensive documentation:

- **AI Scraper Documentation**: `backend/AI_SCRAPER_README.md`
- **Plagiarism Prevention**: `backend/PLAGIARISM_PREVENTION_README.md`
- **Frontend README**: `frontend/README.md`

---

## 📄 License

This project is licensed under the MIT License - see the LICENSE file for details.
