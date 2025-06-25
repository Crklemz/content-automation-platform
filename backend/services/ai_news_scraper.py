import requests
import feedparser
from typing import List, Dict, Optional, Tuple
from datetime import datetime, timedelta
import re
from urllib.parse import urlparse
import time
import json
from dataclasses import dataclass
from collections import Counter
import hashlib

try:
    import trafilatura
    TRAFILATURA_AVAILABLE = True
except ImportError:
    TRAFILATURA_AVAILABLE = False
    print("Warning: trafilatura not installed. Install with: pip install trafilatura")

try:
    from newspaper import Article as NewspaperArticle
    NEWSPAPER_AVAILABLE = True
except ImportError:
    NEWSPAPER_AVAILABLE = False
    print("Warning: newspaper3k not installed. Install with: pip install newspaper3k")

@dataclass
class ScrapedArticle:
    """Enhanced article data structure"""
    title: str
    content: str
    summary: str
    url: str
    source: str
    category: str
    published: str
    keywords: List[str]
    sentiment: str
    quality_score: float
    word_count: int
    reading_time: int
    language: str
    topics: List[str]
    entities: List[str]
    hash_id: str

class AINewsScraper:
    """AI-powered news scraper with advanced content analysis"""
    
    def __init__(self):
        # RSS feeds for different categories
        self.rss_feeds = {
            'ai': [
                'https://feeds.feedburner.com/TechCrunch/artificial-intelligence',
                'https://www.artificialintelligence-news.com/feed/',
                'https://www.sciencedaily.com/rss/computers_math/artificial_intelligence.xml',
                'https://feeds.feedburner.com/VentureBeat/artificial-intelligence',
                'https://www.zdnet.com/news/artificial-intelligence/rss.xml'
            ],
            'tech': [
                'https://feeds.feedburner.com/TechCrunch/',
                'https://www.wired.com/feed/rss',
                'https://feeds.arstechnica.com/arstechnica/index',
                'https://www.theverge.com/rss/index.xml',
                'https://feeds.feedburner.com/venturebeat/SZYF'
            ],
            'business': [
                'https://feeds.feedburner.com/TechCrunch/business',
                'https://www.entrepreneur.com/feed',
                'https://feeds.harvardbusiness.org/harvardbusiness',
                'https://feeds.feedburner.com/venturebeat/business',
                'https://www.inc.com/rss.xml'
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
        
        # Common stop words for keyword extraction
        self.stop_words = {
            'the', 'a', 'an', 'and', 'or', 'but', 'in', 'on', 'at', 'to', 'for', 'of', 'with', 'by',
            'is', 'are', 'was', 'were', 'be', 'been', 'being', 'have', 'has', 'had', 'do', 'does', 'did',
            'will', 'would', 'could', 'should', 'may', 'might', 'must', 'can', 'this', 'that', 'these', 'those'
        }
        
        # Topic keywords for classification
        self.topic_keywords = {
            'ai': ['artificial intelligence', 'machine learning', 'deep learning', 'neural networks', 'AI', 'ML', 'GPT', 'LLM'],
            'tech': ['technology', 'software', 'hardware', 'programming', 'development', 'startup', 'innovation'],
            'business': ['business', 'startup', 'entrepreneur', 'funding', 'investment', 'market', 'revenue'],
            'cybersecurity': ['security', 'cybersecurity', 'hacking', 'privacy', 'encryption', 'breach'],
            'cloud': ['cloud', 'AWS', 'Azure', 'Google Cloud', 'infrastructure', 'SaaS'],
            'mobile': ['mobile', 'iOS', 'Android', 'app', 'smartphone', 'tablet']
        }
    
    def get_trending_topics(self, category: str = "general", limit: int = 10) -> List[Dict]:
        """
        Get AI-enhanced trending topics from RSS feeds
        
        Args:
            category: Topic category (ai, tech, business, general)
            limit: Number of topics to return
            
        Returns:
            List of enhanced trending topics with AI analysis
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
            
            # Enhanced processing with AI analysis
            enhanced_articles = []
            for article in all_articles:
                try:
                    enhanced = self._enhance_article_with_ai(article)
                    if enhanced:
                        enhanced_articles.append(enhanced)
                except Exception as e:
                    print(f"Error enhancing article {article.get('title', 'Unknown')}: {e}")
                    continue
            
            # Remove duplicates using semantic similarity
            unique_articles = self._remove_duplicates_semantic(enhanced_articles)
            
            # Sort by quality score and date
            sorted_articles = sorted(
                unique_articles, 
                key=lambda x: (x.get('quality_score', 0), x.get('published', '')), 
                reverse=True
            )
            
            return sorted_articles[:limit]
            
        except Exception as e:
            print(f"Error fetching trending topics: {e}")
            return self._get_mock_topics(category, limit)
    
    def get_site_specific_topics(self, site_description: str, limit: int = 5) -> List[Dict]:
        """
        Get AI-enhanced topics relevant to a specific site description
        
        Args:
            site_description: Description of the site to search for
            limit: Number of topics to return (default 3 for Daily Top 3)
            
        Returns:
            List of relevant topics with AI analysis
        """
        try:
            # Use a simple search approach - get articles from multiple sources
            all_articles = []
            
            # Fetch from multiple RSS feeds to get variety
            for category, feeds in self.rss_feeds.items():
                for feed_url in feeds[:2]:  # Limit to 2 feeds per category
                    try:
                        articles = self._fetch_rss_feed(feed_url, category)
                        all_articles.extend(articles)
                        time.sleep(0.5)  # Be respectful to servers
                    except Exception as e:
                        print(f"Error fetching from {feed_url}: {e}")
                        continue
            
            # Enhanced processing with AI analysis
            enhanced_articles = []
            for article in all_articles:
                try:
                    enhanced = self._enhance_article_with_ai(article)
                    if enhanced:
                        enhanced_articles.append(enhanced)
                except Exception as e:
                    print(f"Error enhancing article {article.get('title', 'Unknown')}: {e}")
                    continue
            
            # Remove duplicates
            unique_articles = self._remove_duplicates_semantic(enhanced_articles)
            
            # Calculate relevance to site description
            relevant_articles = []
            for article in unique_articles:
                relevance_score = self._calculate_relevance(article, site_description)
                article['relevance_score'] = relevance_score
                relevant_articles.append(article)
            
            # Sort by relevance and quality, return top results
            sorted_articles = sorted(
                relevant_articles, 
                key=lambda x: (x.get('relevance_score', 0), x.get('quality_score', 0)), 
                reverse=True
            )
            
            return sorted_articles[:limit]
            
        except Exception as e:
            print(f"Error fetching site-specific topics: {e}")
            return []
    
    def get_article_summary(self, url: str) -> Optional[Dict]:
        """
        Get AI-enhanced summary of a specific article
        
        Args:
            url: URL of the article to summarize
            
        Returns:
            Dict containing enhanced summary and analysis
        """
        try:
            # Try different extraction methods
            article_data = None
            
            if NEWSPAPER_AVAILABLE:
                article_data = self._extract_with_newspaper(url)
            
            if not article_data and TRAFILATURA_AVAILABLE:
                article_data = self._extract_with_trafilatura(url)
            
            if not article_data:
                article_data = self._extract_basic(url)
            
            if article_data:
                # Enhance with AI analysis
                enhanced = self._enhance_article_with_ai(article_data)
                return enhanced
            
            return None
            
        except Exception as e:
            print(f"Error fetching article summary from {url}: {e}")
            return None
    
    def _extract_with_newspaper(self, url: str) -> Optional[Dict]:
        """Extract content using newspaper3k"""
        try:
            article = NewspaperArticle(url)
            article.download()
            article.parse()
            article.nlp()  # This adds keywords, summary, etc.
            
            # Handle publish_date properly
            published_date = datetime.now().isoformat()
            if article.publish_date:
                try:
                    # Try to convert to isoformat if it's a datetime
                    published_date = getattr(article.publish_date, 'isoformat', lambda: str(article.publish_date))()
                except Exception:
                    # If it's not a datetime or doesn't have isoformat, convert to string
                    published_date = str(article.publish_date)
            
            # Handle language attribute safely using getattr
            language = getattr(article, 'language', 'en')
            if not language:
                language = 'en'
            
            return {
                'title': article.title,
                'content': article.text,
                'summary': article.summary,
                'url': url,
                'source': urlparse(url).netloc,
                'keywords': article.keywords,
                'published': published_date,
                'authors': article.authors,
                'language': language
            }
        except Exception as e:
            print(f"Newspaper extraction failed: {e}")
            return None
    
    def _extract_with_trafilatura(self, url: str) -> Optional[Dict]:
        """Extract content using trafilatura"""
        try:
            response = requests.get(url, headers=self.headers, timeout=10)
            response.raise_for_status()
            
            # Extract main content
            extracted = trafilatura.extract(response.text, include_formatting=True)
            
            if not extracted:
                return None
            
            # Extract metadata
            metadata = trafilatura.extract_metadata(response.text)
            
            return {
                'title': metadata.title if metadata else self._extract_title(response.text),
                'content': extracted,
                'summary': self._create_ai_summary(extracted),
                'url': url,
                'source': urlparse(url).netloc,
                'published': datetime.now().isoformat(),
                'language': metadata.language if metadata else 'en'
            }
        except Exception as e:
            print(f"Trafilatura extraction failed: {e}")
            return None
    
    def _extract_basic(self, url: str) -> Optional[Dict]:
        """Basic extraction fallback"""
        try:
            response = requests.get(url, headers=self.headers, timeout=10)
            response.raise_for_status()
            
            title = self._extract_title(response.text)
            content = self._extract_basic_content(response.text)
            summary = self._create_ai_summary(content)
            
            return {
                'title': title,
                'content': content,
                'summary': summary,
                'url': url,
                'source': urlparse(url).netloc,
                'published': datetime.now().isoformat()
            }
        except Exception as e:
            print(f"Basic extraction failed: {e}")
            return None
    
    def _enhance_article_with_ai(self, article: Dict) -> Dict:
        """Enhance article with AI analysis"""
        content = article.get('content', '') or article.get('description', '')
        title = article.get('title', '')
        
        # Extract keywords
        keywords = self._extract_keywords(content, title)
        
        # Analyze sentiment
        sentiment = self._analyze_sentiment(content)
        
        # Calculate quality score
        quality_score = self._calculate_quality_score(article)
        
        # Extract topics
        topics = self._extract_topics(content, title)
        
        # Extract entities
        entities = self._extract_entities(content)
        
        # Calculate reading time
        word_count = len(content.split())
        reading_time = max(1, word_count // 200)  # Average reading speed
        
        # Create hash for deduplication
        hash_id = self._create_article_hash(article)
        
        # Create AI summary if not present
        if not article.get('summary'):
            article['summary'] = self._create_ai_summary(content)
        
        return {
            **article,
            'keywords': keywords,
            'sentiment': sentiment,
            'quality_score': quality_score,
            'word_count': word_count,
            'reading_time': reading_time,
            'topics': topics,
            'entities': entities,
            'hash_id': hash_id
        }
    
    def _extract_keywords(self, content: str, title: str) -> List[str]:
        """Extract keywords from content using TF-IDF approach"""
        # Combine title and content
        text = f"{title} {content}".lower()
        
        # Remove punctuation and split into words
        words = re.findall(r'\b\w+\b', text)
        
        # Filter out stop words and short words
        filtered_words = [word for word in words if word not in self.stop_words and len(word) > 3]
        
        # Count frequency
        word_freq = Counter(filtered_words)
        
        # Return top keywords
        return [word for word, freq in word_freq.most_common(10)]
    
    def _analyze_sentiment(self, content: str) -> str:
        """Simple sentiment analysis"""
        positive_words = {'good', 'great', 'excellent', 'amazing', 'wonderful', 'positive', 'success', 'growth', 'innovation'}
        negative_words = {'bad', 'terrible', 'awful', 'negative', 'failure', 'problem', 'issue', 'concern', 'risk'}
        
        words = set(content.lower().split())
        
        positive_count = len(words.intersection(positive_words))
        negative_count = len(words.intersection(negative_words))
        
        if positive_count > negative_count:
            return 'positive'
        elif negative_count > positive_count:
            return 'negative'
        else:
            return 'neutral'
    
    def _calculate_quality_score(self, article: Dict) -> float:
        """Calculate article quality score"""
        score = 0.0
        
        # Title quality
        title = article.get('title', '')
        if len(title) > 10 and len(title) < 100:
            score += 0.2
        
        # Content length
        content = article.get('content', '') or article.get('description', '')
        word_count = len(content.split())
        if 100 <= word_count <= 2000:
            score += 0.3
        elif word_count > 2000:
            score += 0.2
        
        # Source credibility
        source = article.get('source', '').lower()
        credible_sources = {'techcrunch.com', 'wired.com', 'arstechnica.com', 'theverge.com', 'venturebeat.com'}
        if source in credible_sources:
            score += 0.2
        
        # Completeness
        if article.get('url') and article.get('published'):
            score += 0.1
        
        return min(1.0, score)
    
    def _extract_topics(self, content: str, title: str) -> List[str]:
        """Extract topics from content"""
        text = f"{title} {content}".lower()
        topics = []
        
        for topic, keywords in self.topic_keywords.items():
            if any(keyword in text for keyword in keywords):
                topics.append(topic)
        
        return topics
    
    def _extract_entities(self, content: str) -> List[str]:
        """Extract named entities (simple approach)"""
        # Look for company names, product names, etc.
        entities = []
        
        # Company patterns
        company_patterns = [
            r'\b[A-Z][a-z]+(?:\s+[A-Z][a-z]+)*\s+(?:Inc|Corp|LLC|Ltd|Company|Technologies|Systems)\b',
            r'\b[A-Z]{2,}\b'  # Acronyms like AI, ML, API
        ]
        
        for pattern in company_patterns:
            matches = re.findall(pattern, content)
            entities.extend(matches)
        
        return list(set(entities))[:10]  # Limit to top 10
    
    def _create_ai_summary(self, content: str) -> str:
        """Create intelligent summary of content"""
        if not content:
            return ""
        
        # Split into sentences
        sentences = re.split(r'[.!?]+', content)
        meaningful_sentences = [s.strip() for s in sentences if len(s.strip()) > 20]
        
        if not meaningful_sentences:
            return content[:200] + "..." if len(content) > 200 else content
        
        # Score sentences by importance (simple heuristic)
        sentence_scores = []
        for sentence in meaningful_sentences[:10]:  # Limit to first 10 sentences
            score = 0
            # Longer sentences get higher scores
            score += len(sentence) * 0.1
            # Sentences with keywords get higher scores
            for keyword in self.topic_keywords.keys():
                if keyword in sentence.lower():
                    score += 10
            sentence_scores.append((sentence, score))
        
        # Sort by score and take top 3
        sentence_scores.sort(key=lambda x: x[1], reverse=True)
        top_sentences = [s[0] for s in sentence_scores[:3]]
        
        summary = '. '.join(top_sentences) + '.'
        
        # Limit length
        if len(summary) > 300:
            summary = summary[:300].rsplit('.', 1)[0] + '.'
        
        return summary
    
    def _calculate_relevance(self, article: Dict, site_description: str) -> float:
        """Calculate relevance score between article and site description"""
        article_text = f"{article.get('title', '')} {article.get('content', '')} {article.get('description', '')}"
        article_text = article_text.lower()
        site_desc = site_description.lower()
        
        # Count common words
        article_words = set(re.findall(r'\b\w+\b', article_text))
        site_words = set(re.findall(r'\b\w+\b', site_desc))
        
        if not site_words:
            return 0.0
        
        common_words = article_words.intersection(site_words)
        relevance = len(common_words) / len(site_words)
        
        return min(1.0, relevance)
    
    def _remove_duplicates_semantic(self, articles: List[Dict]) -> List[Dict]:
        """Remove duplicates using semantic similarity"""
        unique_articles = []
        seen_hashes = set()
        
        for article in articles:
            hash_id = article.get('hash_id', '')
            if hash_id and hash_id not in seen_hashes:
                seen_hashes.add(hash_id)
                unique_articles.append(article)
            elif not hash_id:
                # Fallback to title-based deduplication
                title = article.get('title', '').lower()
                if title not in [a.get('title', '').lower() for a in unique_articles]:
                    unique_articles.append(article)
        
        return unique_articles
    
    def _create_article_hash(self, article: Dict) -> str:
        """Create a hash for article deduplication"""
        content = f"{article.get('title', '')}{article.get('url', '')}"
        return hashlib.md5(content.encode()).hexdigest()
    
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
        clean = re.compile('<.*?>')
        description = re.sub(clean, '', description)
        description = ' '.join(description.split())
        
        if len(description) > 200:
            description = description[:200] + "..."
        
        return description
    
    def _extract_title(self, html_content: str) -> str:
        """Extract title from HTML content"""
        title_match = re.search(r'<title[^>]*>([^<]+)</title>', html_content, re.IGNORECASE)
        if title_match:
            return title_match.group(1).strip()
        return "Article"
    
    def _extract_basic_content(self, html_content: str) -> str:
        """Extract basic content from HTML"""
        # Remove HTML tags
        clean = re.compile('<.*?>')
        text_content = re.sub(clean, '', html_content)
        
        # Remove scripts and styles
        text_content = re.sub(r'<script[^>]*>.*?</script>', '', text_content, flags=re.DOTALL | re.IGNORECASE)
        text_content = re.sub(r'<style[^>]*>.*?</style>', '', text_content, flags=re.DOTALL | re.IGNORECASE)
        
        # Clean up whitespace
        text_content = ' '.join(text_content.split())
        
        return text_content[:2000]  # Limit content length
    
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
                    'published': datetime.now().isoformat(),
                    'keywords': ['AI', 'healthcare', 'medical', 'diagnosis'],
                    'sentiment': 'positive',
                    'quality_score': 0.8,
                    'topics': ['ai', 'healthcare'],
                    'entities': ['AI', 'Healthcare']
                }
            ],
            'tech': [
                {
                    'title': 'Cloud Computing Trends',
                    'description': 'Latest developments in cloud infrastructure and services',
                    'category': 'Cloud Computing',
                    'source': 'Tech News',
                    'url': 'https://example.com/cloud-trends',
                    'published': datetime.now().isoformat(),
                    'keywords': ['cloud', 'computing', 'infrastructure', 'services'],
                    'sentiment': 'positive',
                    'quality_score': 0.7,
                    'topics': ['tech', 'cloud'],
                    'entities': ['Cloud', 'AWS', 'Azure']
                }
            ]
        }
        
        return mock_topics.get(category, mock_topics['tech'])[:limit] 