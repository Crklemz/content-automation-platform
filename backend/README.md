# Content Automation Platform - Backend

A comprehensive Django 5.2.3 backend with AI-powered content generation, advanced news scraping, plagiarism prevention, and a complete REST API for the Content Automation Platform.

## Features

- **AI Content Generation**: OpenAI GPT-4 integration with fallback mock content
- **Advanced News Scraping**: RSS feed aggregation with AI-enhanced analysis
- **Plagiarism Prevention**: Content originality checking and source attribution
- **Multi-Site Management**: Dynamic site configuration and branding
- **Article Workflow**: Complete approval system (pending/approved/rejected)
- **REST API**: Full CRUD operations with filtering and pagination
- **Authentication**: Session-based auth with CSRF protection
- **Management Commands**: Content generation and testing utilities

## Tech Stack

- **Django 5.2.3** with Django REST Framework 3.16.0
- **PostgreSQL** database with psycopg2-binary
- **OpenAI API** integration (openai 1.12.0)
- **Advanced Scraping**: newspaper3k, trafilatura, beautifulsoup4, feedparser
- **AI/ML**: NLTK, spaCy, scikit-learn (optional)
- **Security**: CSRF protection, session management, rate limiting

## Project Structure

```
backend/
├── core/                           # Django settings and configuration
│   ├── settings.py                # Main Django settings
│   ├── urls.py                    # URL routing with auth endpoints
│   ├── wsgi.py                    # WSGI configuration
│   └── management/                # Django management commands
│       └── commands/
│           ├── create_admin_user.py
│           └── check_admin_users.py
├── articles/                       # Article management app
│   ├── models.py                  # Article model with status workflow
│   ├── views.py                   # Article API views and filtering
│   ├── serializers.py             # DRF serializers
│   ├── admin.py                   # Django admin interface
│   └── management/                # Article generation commands
│       └── commands/
│           ├── generate_test_articles.py
│           └── test_ai_scraper.py
├── sites/                         # Site configuration app
│   ├── models.py                  # Site model with branding
│   ├── views.py                   # Site API views
│   ├── serializers.py             # Site serializers
│   └── management/                # Site management commands
│       └── commands/
│           └── sync_sites.py
├── services/                      # AI services and automation
│   ├── ai_generator.py            # OpenAI content generation
│   ├── ai_news_scraper.py         # RSS scraping and analysis
│   ├── content_automation.py      # Content orchestration
│   └── plagiarism_prevention.py   # Plagiarism detection
├── tests/                         # Test files and commands
│   ├── test_ai_scraper.py         # AI scraper tests
│   ├── test_plagiarism_prevention.py
│   └── management/                # Test management commands
│       └── commands/
│           ├── test_ai_scraper.py
│           └── test_plagiarism_prevention.py
├── requirements.txt               # Core Python dependencies
├── requirements_ai_scraping.txt   # Advanced AI dependencies
├── manage.py                      # Django management script
└── README.md                      # This file
```

## Quick Start

### Prerequisites
- Python 3.8+
- PostgreSQL
- OpenAI API key

### Installation

1. **Clone and navigate to backend**
   ```bash
   cd backend
   ```

2. **Create virtual environment**
   ```bash
   python -m venv .venv
   source .venv/bin/activate  # On Windows: .venv\Scripts\activate
   ```

3. **Install dependencies**
   ```bash
   pip install -r requirements.txt
   pip install -r requirements_ai_scraping.txt
   ```

4. **Configure environment variables**
   Create a `.env` file:
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

5. **Set up database**
   ```bash
   python manage.py migrate
   python manage.py createsuperuser
   ```

6. **Create admin user**
   ```bash
   python manage.py create_admin_user
   ```

7. **Start development server**
   ```bash
   python manage.py runserver
   ```

## API Endpoints

### Authentication
- `POST /api/auth/login/` - User login with rate limiting
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

## Management Commands

### Content Generation
```bash
# Generate AI content for a specific site
python manage.py generate_ai_content --site "AI Skills"

# Generate test articles
python manage.py generate_test_articles
```

### User Management
```bash
# Create admin user
python manage.py create_admin_user

# Check admin users
python manage.py check_admin_users
```

### Testing
```bash
# Test AI scraper functionality
python manage.py test_ai_scraper --category ai --limit 5

# Test plagiarism prevention system
python manage.py test_plagiarism_prevention --test-type full
```

### Site Management
```bash
# Sync sites from configuration
python manage.py sync_sites
```

## Key Services

### AI Content Generator (`services/ai_generator.py`)
- OpenAI GPT-4 integration with fallback mock content
- Plagiarism prevention integration
- Daily Top 3 article compilation
- Professional HTML formatting

### AI News Scraper (`services/ai_news_scraper.py`)
- RSS feed aggregation from multiple sources
- AI-enhanced content analysis
- Quality scoring and sentiment analysis
- Topic classification and keyword extraction

### Plagiarism Prevention (`services/plagiarism_prevention.py`)
- Content similarity analysis
- Source quality validation
- Automatic attribution generation
- Confidence scoring

### Content Automation (`services/content_automation.py`)
- Orchestrates content generation workflow
- Integrates all AI services
- Manages content pipeline

## Models

### Article Model
```python
class Article(models.Model):
    STATUS_CHOICES = [
        ('pending', 'Pending'),
        ('approved', 'Approved'),
        ('rejected', 'Rejected'),
    ]
    
    site = models.ForeignKey(Site, on_delete=models.CASCADE)
    title = models.CharField(max_length=200)
    slug = models.SlugField(unique=True, max_length=200)
    body = models.TextField()
    sources = models.JSONField(blank=True, null=True)
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='pending')
    created_at = models.DateTimeField(auto_now_add=True)
```

### Site Model
```python
class Site(models.Model):
    slug = models.SlugField(unique=True)
    name = models.CharField(max_length=100)
    description = models.TextField()
    logo = models.CharField(max_length=255)
    primary_color = models.CharField(max_length=7)
    secondary_color = models.CharField(max_length=7)
```

## Security Features

- **Session-based Authentication**: Secure user sessions with configurable timeouts
- **CSRF Protection**: Comprehensive CSRF token protection on all forms
- **Rate Limiting**: Basic rate limiting on authentication endpoints
- **Input Validation**: Comprehensive input sanitization and validation
- **Secure Headers**: XSS protection and content type sniffing prevention
- **CORS Configuration**: Proper cross-origin request handling

## Development

### Running Tests
```bash
# Run all tests
python manage.py test

# Run specific app tests
python manage.py test articles
python manage.py test sites

# Run with coverage
coverage run --source='.' manage.py test
coverage report
```

### Code Quality
```bash
# Run linting
flake8 .
black .
isort .

# Type checking (if using mypy)
mypy .
```

### Database Management
```bash
# Create migrations
python manage.py makemigrations

# Apply migrations
python manage.py migrate

# Reset database
python manage.py flush

# Create superuser
python manage.py createsuperuser
```

## Configuration

### Environment Variables
- `DEBUG`: Enable debug mode
- `DJANGO_SECRET_KEY`: Django secret key
- `POSTGRES_*`: Database configuration
- `OPENAI_API_KEY`: OpenAI API key for content generation

### Django Settings
- **Database**: PostgreSQL with connection pooling
- **Caching**: Redis (optional, for production)
- **Static Files**: Configured for production deployment
- **Media Files**: File upload handling
- **Logging**: Comprehensive logging configuration

## Deployment

### Production Checklist
- [ ] Set `DEBUG=False`
- [ ] Configure production database
- [ ] Set up static file serving
- [ ] Configure HTTPS
- [ ] Set up monitoring and logging
- [ ] Configure backup systems
- [ ] Set up environment variables
- [ ] Test all management commands

### Docker Support
```dockerfile
# Example Dockerfile
FROM python:3.11-slim
WORKDIR /app
COPY requirements.txt .
RUN pip install -r requirements.txt
COPY . .
EXPOSE 8000
CMD ["python", "manage.py", "runserver", "0.0.0.0:8000"]
```

## Troubleshooting

### Common Issues

1. **OpenAI API Errors**
   - Check API key configuration
   - Verify API quota and billing
   - Check network connectivity

2. **Database Connection Issues**
   - Verify PostgreSQL is running
   - Check database credentials
   - Ensure database exists

3. **Import Errors**
   - Activate virtual environment
   - Install all requirements
   - Check Python version compatibility

### Debug Mode
```bash
# Enable debug logging
export DJANGO_DEBUG=True
python manage.py runserver --verbosity=2
```

## Documentation

- **AI Scraper**: See `AI_SCRAPER_README.md`
- **Plagiarism Prevention**: See `PLAGIARISM_PREVENTION_README.md`
- **API Documentation**: Check the main project README
- **Frontend Integration**: See `../frontend/README.md` 