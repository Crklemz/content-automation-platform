import requests
import feedparser
from typing import List, Dict, Optional
from datetime import datetime, timedelta
import re
from urllib.parse import urlparse
import time

class NewsScraper:
    """Real news scraper service that fetches trending topics and articles"""
    
    def __init__(self):
        # RSS feeds for different categories
        self.rss_feeds = {
            'ai': [
                'https://feeds.feedburner.com/TechCrunch/artificial-intelligence',
                'https://www.artificialintelligence-news.com/feed/',
                'https://www.sciencedaily.com/rss/computers_math/artificial_intelligence.xml'
            ],
            'tech': [
                'https://feeds.feedburner.com/TechCrunch/',
                'https://www.wired.com/feed/rss',
                'https://feeds.arstechnica.com/arstechnica/index'
            ],
            'business': [
                'https://feeds.feedburner.com/TechCrunch/business',
                'https://www.entrepreneur.com/feed',
                'https://feeds.harvardbusiness.org/harvardbusiness'
            ],
            'general': [
                'https://feeds.feedburner.com/TechCrunch/',
                'https://www.wired.com/feed/rss',
                'https://feeds.arstechnica.com/arstechnica/index'
            ]
        }
        
        # Headers to avoid being blocked
        self.headers = {
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36'
        }
    
    def get_trending_topics(self, category: str = "general", limit: int = 10) -> List[Dict]:
        """
        Get real trending topics from RSS feeds
        
        Args:
            category: Topic category (ai, tech, business, general)
            limit: Number of topics to return
            
        Returns:
            List of trending topics with sources
        """
        try:
            category = category.lower()
            if category not in self.rss_feeds:
                category = 'general'
            
            all_articles = []
            
            # Fetch from RSS feeds
            for feed_url in self.rss_feeds[category]:
                try:
                    articles = self._fetch_rss_feed(feed_url, category)
                    all_articles.extend(articles)
                    time.sleep(1)  # Be respectful to servers
                except Exception as e:
                    print(f"Error fetching from {feed_url}: {e}")
                    continue
            
            # Sort by date and remove duplicates
            unique_articles = self._remove_duplicates(all_articles)
            sorted_articles = sorted(unique_articles, key=lambda x: x.get('published', ''), reverse=True)
            
            return sorted_articles[:limit]
            
        except Exception as e:
            print(f"Error fetching trending topics: {e}")
            # Fallback to mock data
            return self._get_mock_topics(category, limit)
    
    def get_site_specific_topics(self, site_description: str, limit: int = 5) -> List[Dict]:
        """
        Get topics relevant to a specific site based on its description
        
        Args:
            site_description: Description of the site
            limit: Number of topics to return
            
        Returns:
            List of relevant topics with sources
        """
        description_lower = site_description.lower()
        
        # Determine relevant category based on site description
        if any(keyword in description_lower for keyword in ['ai', 'artificial intelligence', 'machine learning']):
            category = 'ai'
        elif any(keyword in description_lower for keyword in ['tech', 'technology', 'software', 'development']):
            category = 'tech'
        elif any(keyword in description_lower for keyword in ['business', 'startup', 'entrepreneur']):
            category = 'business'
        else:
            category = 'general'
        
        return self.get_trending_topics(category, limit)
    
    def get_article_summary(self, url: str) -> Optional[Dict]:
        """
        Get a summary of a specific article with source attribution
        
        Args:
            url: URL of the article to summarize
            
        Returns:
            Dict containing summary, title, and source info
        """
        try:
            response = requests.get(url, headers=self.headers, timeout=10)
            response.raise_for_status()
            
            # Extract basic info
            title = self._extract_title(response.text)
            domain = urlparse(url).netloc
            
            # Create a summary using the article content
            summary = self._create_summary_from_content(response.text, title)
            
            return {
                'title': title,
                'summary': summary,
                'url': url,
                'source': domain,
                'published': datetime.now().isoformat()
            }
            
        except Exception as e:
            print(f"Error fetching article summary from {url}: {e}")
            return None
    
    def _fetch_rss_feed(self, feed_url: str, category: str) -> List[Dict]:
        """Fetch articles from an RSS feed"""
        try:
            feed = feedparser.parse(feed_url)
            articles = []
            
            for entry in feed.entries[:10]:  # Limit to 10 articles per feed
                article = {
                    'title': entry.get('title', ''),
                    'description': self._clean_description(entry.get('summary', '')),
                    'url': entry.get('link', ''),
                    'source': urlparse(entry.get('link', '')).netloc,
                    'category': category,
                    'published': entry.get('published', ''),
                    'published_parsed': entry.get('published_parsed')
                }
                articles.append(article)
            
            return articles
            
        except Exception as e:
            print(f"Error parsing RSS feed {feed_url}: {e}")
            return []
    
    def _clean_description(self, description: str) -> str:
        """Clean HTML from description"""
        # Remove HTML tags
        clean = re.compile('<.*?>')
        description = re.sub(clean, '', description)
        
        # Remove extra whitespace
        description = ' '.join(description.split())
        
        # Limit length
        if len(description) > 200:
            description = description[:200] + "..."
        
        return description
    
    def _extract_title(self, html_content: str) -> str:
        """Extract title from HTML content"""
        title_match = re.search(r'<title[^>]*>([^<]+)</title>', html_content, re.IGNORECASE)
        if title_match:
            return title_match.group(1).strip()
        return "Article"
    
    def _create_summary_from_content(self, html_content: str, title: str) -> str:
        """Create a summary from article content"""
        # Remove HTML tags
        clean = re.compile('<.*?>')
        text_content = re.sub(clean, '', html_content)
        
        # Extract meaningful text (remove scripts, styles, etc.)
        text_content = re.sub(r'<script[^>]*>.*?</script>', '', text_content, flags=re.DOTALL | re.IGNORECASE)
        text_content = re.sub(r'<style[^>]*>.*?</style>', '', text_content, flags=re.DOTALL | re.IGNORECASE)
        
        # Get first few sentences
        sentences = re.split(r'[.!?]+', text_content)
        meaningful_sentences = [s.strip() for s in sentences if len(s.strip()) > 20]
        
        if meaningful_sentences:
            summary = '. '.join(meaningful_sentences[:3]) + '.'
            if len(summary) > 300:
                summary = summary[:300] + "..."
            return summary
        
        return f"Summary of {title}"
    
    def _remove_duplicates(self, articles: List[Dict]) -> List[Dict]:
        """Remove duplicate articles based on title similarity"""
        seen_titles = set()
        unique_articles = []
        
        for article in articles:
            title = article.get('title', '').lower()
            # Simple deduplication - could be improved with fuzzy matching
            if title not in seen_titles and len(title) > 10:
                seen_titles.add(title)
                unique_articles.append(article)
        
        return unique_articles
    
    def _get_mock_topics(self, category: str, limit: int) -> List[Dict]:
        """Fallback mock topics when RSS feeds fail"""
        mock_topics = {
            'ai': [
                {
                    'title': 'Artificial Intelligence in Healthcare',
                    'description': 'How AI is revolutionizing medical diagnosis and treatment',
                    'category': 'AI & Healthcare',
                    'source': 'Tech Trends',
                    'url': 'https://example.com/ai-healthcare',
                    'published': datetime.now().isoformat()
                }
            ],
            'tech': [
                {
                    'title': 'Cloud Computing Trends',
                    'description': 'Latest developments in cloud infrastructure and services',
                    'category': 'Cloud Computing',
                    'source': 'Tech News',
                    'url': 'https://example.com/cloud-trends',
                    'published': datetime.now().isoformat()
                }
            ]
        }
        
        return mock_topics.get(category, mock_topics['tech'])[:limit] 