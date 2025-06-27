# AI-Powered News Scraper

## Overview

The AI-powered news scraper (`AINewsScraper`) is an advanced content extraction and analysis system that goes far beyond traditional RSS scraping. It uses multiple AI/ML techniques to provide intelligent content understanding, quality assessment, and enhanced summarization.

## Key Features

### 🤖 AI-Enhanced Content Extraction
- **Multiple extraction methods** with intelligent fallbacks:
  - `newspaper3k` - Advanced news article extraction
  - `trafilatura` - ML-powered content extraction
  - Basic extraction as fallback
- **Intelligent content cleaning** and formatting
- **Metadata extraction** (authors, publish dates, language)

### 📊 Content Analysis
- **Quality scoring** based on multiple factors:
  - Content length and completeness
  - Source credibility
  - Title quality
  - Content structure
- **Sentiment analysis** (positive/negative/neutral)
- **Keyword extraction** using TF-IDF approach
- **Topic classification** (AI, tech, business, cybersecurity, etc.)
- **Entity recognition** (companies, products, technologies)

### 🎯 Smart Content Processing
- **Semantic duplicate detection** using content hashing
- **Relevance scoring** for site-specific content
- **Intelligent summarization** using sentence importance scoring
- **Reading time estimation**
- **Word count analysis**

## Installation

### 1. Install AI Scraping Dependencies

cd backend
pip install -r requirements_ai_scraping.txt

### 2. Optional: Install Advanced NLP (for even better results)

```bash
# Uncomment in requirements_ai_scraping.txt and install:
pip install transformers torch sentence-transformers
```

## Usage

### Basic Usage

```python
from services.ai_news_scraper import AINewsScraper

# Initialize the scraper
scraper = AINewsScraper()

# Get AI-enhanced trending topics
topics = scraper.get_trending_topics(category='ai', limit=5)

# Get site-specific relevant topics
site_topics = scraper.get_site_specific_topics(
    "AI and machine learning news for developers", 
    limit=3
)

# Get enhanced article summary
summary = scraper.get_article_summary("https://example.com/article")
```

### Django Management Commands

```bash
# Test the AI scraper with different categories
python manage.py test_ai_scraper --category ai --limit 5

# Test with tech category
python manage.py test_ai_scraper --category tech --limit 3

# Test with business category
python manage.py test_ai_scraper --category business --limit 3
```

### Python Test Scripts

```bash
cd backend

# Run the test script in the tests directory
python tests/test_ai_scraper.py

# Or run the management command version
python manage.py test_ai_scraper
```

## Comparison: Traditional vs AI Scraper

| Feature | Traditional Scraper | AI Scraper |
|---------|-------------------|------------|
| Content Extraction | Basic RSS parsing | Multiple AI-powered methods |
| Summarization | First 3 sentences | Intelligent sentence scoring |
| Quality Assessment | None | Multi-factor quality scoring |
| Sentiment Analysis | None | Built-in sentiment detection |
| Keyword Extraction | None | TF-IDF keyword extraction |
| Topic Classification | Manual category mapping | Automatic topic detection |
| Duplicate Detection | Exact title matching | Semantic similarity |
| Relevance Scoring | None | Site-specific relevance |
| Entity Recognition | None | Named entity extraction |
| Reading Time | None | Estimated reading time |

## Advanced Features

### Quality Scoring Algorithm

The quality score (0.0-1.0) is calculated based on:

- **Title Quality** (20%): Length and readability
- **Content Length** (30%): Optimal 100-2000 words
- **Source Credibility** (20%): Known reputable sources
- **Completeness** (10%): Has URL, publish date, etc.
- **Content Structure** (20%): Proper formatting and structure

### Sentiment Analysis

Uses a dictionary-based approach with:
- **Positive words**: good, great, excellent, success, growth, innovation
- **Negative words**: bad, terrible, failure, problem, issue, concern
- **Neutral**: Balanced or no clear sentiment

### Topic Classification

Automatically detects topics based on keyword matching:
- **AI**: artificial intelligence, machine learning, GPT, LLM
- **Tech**: technology, software, programming, development
- **Business**: business, startup, entrepreneur, funding
- **Cybersecurity**: security, hacking, privacy, encryption
- **Cloud**: cloud, AWS, Azure, infrastructure
- **Mobile**: mobile, iOS, Android, app

### Intelligent Summarization

Creates summaries using:
1. **Sentence scoring** based on:
   - Length and completeness
   - Keyword presence
   - Position in article
2. **Top sentence selection** (best 3 sentences)
3. **Length optimization** (max 300 characters)

## Configuration

### RSS Feeds

The scraper includes curated RSS feeds for different categories:

```python
rss_feeds = {
    'ai': [
        'https://feeds.feedburner.com/TechCrunch/artificial-intelligence',
        'https://www.artificialintelligence-news.com/feed/',
        # ... more feeds
    ],
    'tech': [
        'https://feeds.feedburner.com/TechCrunch/',
        'https://www.wired.com/feed/rss',
        # ... more feeds
    ],
    # ... other categories
}
```

### Topic Keywords

Customize topic detection by modifying `topic_keywords`:

```python
topic_keywords = {
    'ai': ['artificial intelligence', 'machine learning', 'GPT', 'LLM'],
    'tech': ['technology', 'software', 'programming'],
    # Add your own topics
}
```

## Performance Considerations

### Speed vs Quality Trade-offs

- **Fast mode**: Use basic extraction only
- **Quality mode**: Use all AI features (slower but better results)
- **Balanced mode**: Use newspaper3k + basic AI analysis

### Rate Limiting

The scraper includes built-in rate limiting:
- 1 second delay between RSS feed requests
- Respectful user agents
- Timeout handling (10 seconds per request)

### Caching

Consider implementing caching for:
- RSS feed results (cache for 15-30 minutes)
- Article summaries (cache for 1 hour)
- Quality scores (cache for 24 hours)

## Testing

### Available Test Commands

```bash
# Test AI scraper functionality
python manage.py test_ai_scraper --category ai --limit 5

# Test with different categories
python manage.py test_ai_scraper --category tech --limit 3
python manage.py test_ai_scraper --category business --limit 3

# Run the standalone test script
python tests/test_ai_scraper.py
```

### Test Output

The test commands provide detailed output including:
- Article titles and sources
- Quality scores and sentiment analysis
- Keywords and topics
- Reading time and word count
- Enhanced summaries
- Site-specific relevance scoring

## Error Handling

The scraper includes robust error handling:

- **Graceful fallbacks**: If one extraction method fails, try another
- **Mock data**: Provides realistic mock data when feeds are unavailable
- **Exception logging**: Detailed error messages for debugging
- **Timeout handling**: Prevents hanging on slow responses

## Future Enhancements

### Planned Features

1. **Advanced NLP Integration**
   - BERT-based sentiment analysis
   - Transformer-based summarization
   - Named entity recognition with spaCy

2. **Machine Learning Improvements**
   - Content quality prediction models
   - Topic clustering algorithms
   - Duplicate detection with embeddings

3. **Real-time Processing**
   - WebSocket-based live updates
   - Streaming content analysis
   - Real-time quality scoring

4. **Multi-language Support**
   - Language detection
   - Translation capabilities
   - Multi-language content extraction

## Troubleshooting

### Common Issues

1. **Import Errors**
   ```bash
   pip install trafilatura newspaper3k
   ```

2. **Slow Performance**
   - Reduce `limit` parameter
   - Use basic extraction only
   - Implement caching

3. **Empty Results**
   - Check RSS feed URLs
   - Verify internet connection
   - Check for rate limiting

4. **Memory Issues**
   - Reduce batch sizes
   - Clear caches regularly
   - Use streaming processing

## License

This AI scraper is part of the Content Automation Platform and follows the same license terms. 