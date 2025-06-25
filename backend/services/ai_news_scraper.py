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
            'sustainability': [
                'https://feeds.feedburner.com/TreeHugger',
                'https://www.greenbiz.com/rss.xml',
                'https://www.ecowatch.com/rss.xml',
                'https://www.sustainablebrands.com/rss.xml',
                'https://www.environmentalleader.com/feed/'
            ],
            'green_living': [
                'https://feeds.feedburner.com/TreeHugger',
                'https://www.greenbiz.com/rss.xml',
                'https://www.ecowatch.com/rss.xml',
                'https://www.sustainablebrands.com/rss.xml',
                'https://www.environmentalleader.com/feed/'
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
            'mobile': ['mobile', 'iOS', 'Android', 'app', 'smartphone', 'tablet'],
            'sustainability': ['sustainable', 'sustainability', 'green', 'environment', 'climate', 'eco-friendly', 'renewable', 'carbon'],
            'green_living': ['sustainable', 'green', 'environment', 'climate', 'eco-friendly', 'renewable', 'carbon', 'living', 'lifestyle', 'organic']
        }
        
        # Site-specific keyword mappings
        self.site_keywords = {
            'sustainable living made simple': ['sustainable', 'green', 'environment', 'climate', 'eco-friendly', 'renewable', 'carbon', 'living', 'lifestyle', 'organic', 'zero waste', 'minimalism'],
            'ai insights daily': ['artificial intelligence', 'machine learning', 'deep learning', 'neural networks', 'AI', 'ML', 'GPT', 'LLM', 'automation', 'data science'],
            'tech startup insights': ['startup', 'entrepreneur', 'business', 'funding', 'investment', 'innovation', 'technology', 'venture capital', 'growth']
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
            print(f"Getting site-specific topics for: {site_description}, limit: {limit}")
            
            # Determine which RSS feeds to use based on site description
            site_desc_lower = site_description.lower()
            
            if any(keyword in site_desc_lower for keyword in ['sustainable', 'green', 'environment', 'climate']):
                # Use sustainability/green living feeds
                target_feeds = self.rss_feeds.get('sustainability', []) + self.rss_feeds.get('green_living', [])
                category = 'sustainability'
                print(f"Using sustainability feeds: {len(target_feeds)} feeds")
            elif any(keyword in site_desc_lower for keyword in ['ai', 'artificial intelligence', 'machine learning']):
                # Use AI/tech feeds
                target_feeds = self.rss_feeds.get('ai', []) + self.rss_feeds.get('tech', [])
                category = 'ai'
                print(f"Using AI feeds: {len(target_feeds)} feeds")
            elif any(keyword in site_desc_lower for keyword in ['startup', 'business', 'entrepreneur']):
                # Use business feeds
                target_feeds = self.rss_feeds.get('business', []) + self.rss_feeds.get('tech', [])
                category = 'business'
                print(f"Using business feeds: {len(target_feeds)} feeds")
            else:
                # Use general feeds
                target_feeds = self.rss_feeds.get('general', [])
                category = 'general'
                print(f"Using general feeds: {len(target_feeds)} feeds")
            
            all_articles = []
            
            # Fetch from selected RSS feeds
            for feed_url in target_feeds[:4]:  # Limit to 4 feeds to avoid rate limiting
                try:
                    print(f"Fetching from feed: {feed_url}")
                    articles = self._fetch_rss_feed(feed_url, category)
                    print(f"Got {len(articles)} articles from {feed_url}")
                    all_articles.extend(articles)
                    time.sleep(0.5)  # Be respectful to servers
                except Exception as e:
                    print(f"Error fetching from {feed_url}: {e}")
                    continue
            
            print(f"Total articles fetched: {len(all_articles)}")
            
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
            
            print(f"Enhanced articles: {len(enhanced_articles)}")
            
            # Remove duplicates
            unique_articles = self._remove_duplicates_semantic(enhanced_articles)
            print(f"Unique articles: {len(unique_articles)}")
            
            # Calculate relevance to site description
            relevant_articles = []
            for article in unique_articles:
                relevance_score = self._calculate_relevance(article, site_description)
                article['relevance_score'] = relevance_score
                
                # Use stricter threshold for sustainability content
                if 'sustainable' in site_description.lower() or 'green' in site_description.lower():
                    # Higher threshold for sustainability content
                    if relevance_score > 0.3:
                        relevant_articles.append(article)
                else:
                    # Lower threshold for other content
                    if relevance_score > 0.1:
                        relevant_articles.append(article)
            
            print(f"Relevant articles: {len(relevant_articles)}")
            
            # Sort by relevance score and quality score
            sorted_articles = sorted(
                relevant_articles, 
                key=lambda x: (x.get('relevance_score', 0), x.get('quality_score', 0)), 
                reverse=True
            )
            
            # If we don't have enough relevant articles, include some general ones
            if len(sorted_articles) < limit:
                remaining_articles = [a for a in unique_articles if a not in sorted_articles]
                sorted_articles.extend(remaining_articles[:limit - len(sorted_articles)])
                print(f"Added {limit - len(sorted_articles)} general articles")
            
            result = sorted_articles[:limit]
            print(f"Returning {len(result)} topics")
            return result
            
        except Exception as e:
            print(f"Error fetching site-specific topics: {e}")
            print(f"Falling back to mock topics for category: {category}")
            return self._get_mock_topics(category, limit)
    
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
        try:
            # Extract content from URL if available
            content = article.get('content', '')
            if not content and article.get('url'):
                try:
                    url = article.get('url')
                    if url and isinstance(url, str):
                        extracted_content = self.get_article_summary(url)
                        if extracted_content:
                            content = extracted_content.get('content', '')
                except Exception as e:
                    print(f"Error extracting content from {article.get('url')}: {e}")
            
            # Use description as fallback content
            if not content:
                content = article.get('description', '')
            
            # Extract keywords
            keywords = self._extract_keywords(content, article.get('title', ''))
            
            # Analyze sentiment
            sentiment = self._analyze_sentiment(content)
            
            # Calculate quality score
            quality_score = self._calculate_quality_score(article)
            
            # Extract topics
            topics = self._extract_topics(content, article.get('title', ''))
            
            # Extract entities
            entities = self._extract_entities(content)
            
            # Create AI summary
            ai_summary = self._create_ai_summary(content)
            
            # Create hash for deduplication
            hash_id = self._create_article_hash(article)
            
            # Return enhanced article
            enhanced = {
                'title': article.get('title', ''),
                'description': article.get('description', ''),
                'content': content,
                'summary': ai_summary,
                'url': article.get('url', ''),
                'source': article.get('source', 'Unknown'),
                'category': article.get('category', 'General'),
                'published': article.get('published', ''),
                'keywords': keywords,
                'sentiment': sentiment,
                'quality_score': quality_score,
                'word_count': len(content.split()),
                'reading_time': max(1, len(content.split()) // 200),  # 200 words per minute
                'language': 'en',
                'topics': topics,
                'entities': entities,
                'hash_id': hash_id
            }
            
            return enhanced
            
        except Exception as e:
            print(f"Error enhancing article: {e}")
            # Return basic article with minimal enhancement
            return {
                'title': article.get('title', ''),
                'description': article.get('description', ''),
                'content': article.get('description', ''),
                'summary': article.get('description', ''),
                'url': article.get('url', ''),
                'source': article.get('source', 'Unknown'),
                'category': article.get('category', 'General'),
                'published': article.get('published', ''),
                'keywords': [],
                'sentiment': 'neutral',
                'quality_score': 0.5,
                'word_count': len(article.get('description', '').split()),
                'reading_time': 1,
                'language': 'en',
                'topics': [],
                'entities': [],
                'hash_id': self._create_article_hash(article)
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
        
        # Get site-specific keywords
        site_keywords = self.site_keywords.get(site_description.lower(), [])
        
        # Calculate relevance using multiple methods
        relevance_scores = []
        
        # Method 1: Direct keyword matching
        if site_keywords:
            keyword_matches = sum(1 for keyword in site_keywords if keyword in article_text)
            keyword_score = keyword_matches / len(site_keywords)
            relevance_scores.append(keyword_score * 2)  # Weight keyword matching higher
        
        # Method 2: Common word matching
        article_words = set(re.findall(r'\b\w+\b', article_text))
        site_words = set(re.findall(r'\b\w+\b', site_desc))
        
        if site_words:
            common_words = article_words.intersection(site_words)
            word_score = len(common_words) / len(site_words)
            relevance_scores.append(word_score)
        
        # Method 3: Topic category matching
        article_topics = article.get('topics', [])
        if article_topics:
            # Check if any article topics match site keywords
            topic_matches = sum(1 for topic in article_topics if any(keyword in topic for keyword in site_keywords))
            topic_score = topic_matches / len(article_topics) if article_topics else 0
            relevance_scores.append(topic_score)
        
        # Method 4: Semantic similarity for specific site descriptions
        if 'sustainable' in site_desc or 'green' in site_desc:
            # Boost relevance for sustainability-related content
            sustainability_keywords = ['sustainable', 'green', 'environment', 'climate', 'eco', 'renewable', 'carbon', 'zero waste', 'organic', 'natural']
            sustainability_matches = sum(1 for keyword in sustainability_keywords if keyword in article_text)
            if sustainability_matches > 0:
                relevance_scores.append(0.9)  # Very high relevance for sustainability content
            else:
                # Penalize non-sustainability content for green living sites
                relevance_scores.append(0.1)  # Low relevance for non-sustainability content
        
        if 'ai' in site_desc or 'artificial intelligence' in site_desc:
            # Boost relevance for AI-related content
            ai_keywords = ['artificial intelligence', 'machine learning', 'deep learning', 'neural networks', 'AI', 'ML', 'GPT']
            ai_matches = sum(1 for keyword in ai_keywords if keyword in article_text)
            if ai_matches > 0:
                relevance_scores.append(0.8)  # High relevance for AI content
        
        if 'startup' in site_desc or 'business' in site_desc:
            # Boost relevance for business/startup content
            business_keywords = ['startup', 'business', 'entrepreneur', 'funding', 'investment', 'venture']
            business_matches = sum(1 for keyword in business_keywords if keyword in article_text)
            if business_matches > 0:
                relevance_scores.append(0.8)  # High relevance for business content
        
        # Calculate final relevance score
        if relevance_scores:
            final_score = sum(relevance_scores) / len(relevance_scores)
            return min(1.0, final_score)
        
        return 0.0
    
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
                },
                {
                    'title': 'Machine Learning in Finance',
                    'description': 'AI-powered trading algorithms and risk assessment',
                    'category': 'AI & Finance',
                    'source': 'Tech News',
                    'url': 'https://example.com/ai-finance',
                    'published': datetime.now().isoformat(),
                    'keywords': ['AI', 'finance', 'trading', 'algorithms'],
                    'sentiment': 'positive',
                    'quality_score': 0.7,
                    'topics': ['ai', 'finance'],
                    'entities': ['AI', 'Finance']
                },
                {
                    'title': 'GPT-4 Applications in Business',
                    'description': 'How businesses are leveraging GPT-4 for productivity',
                    'category': 'AI & Business',
                    'source': 'Business Tech',
                    'url': 'https://example.com/gpt4-business',
                    'published': datetime.now().isoformat(),
                    'keywords': ['GPT-4', 'business', 'productivity', 'AI'],
                    'sentiment': 'positive',
                    'quality_score': 0.9,
                    'topics': ['ai', 'business'],
                    'entities': ['GPT-4', 'Business']
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
                },
                {
                    'title': 'Cybersecurity Best Practices',
                    'description': 'Essential security measures for modern businesses',
                    'category': 'Cybersecurity',
                    'source': 'Security Weekly',
                    'url': 'https://example.com/cybersecurity',
                    'published': datetime.now().isoformat(),
                    'keywords': ['cybersecurity', 'security', 'business', 'protection'],
                    'sentiment': 'neutral',
                    'quality_score': 0.8,
                    'topics': ['tech', 'security'],
                    'entities': ['Cybersecurity', 'Business']
                },
                {
                    'title': 'Mobile App Development Trends',
                    'description': 'Latest innovations in mobile application development',
                    'category': 'Mobile Development',
                    'source': 'Mobile Tech',
                    'url': 'https://example.com/mobile-trends',
                    'published': datetime.now().isoformat(),
                    'keywords': ['mobile', 'app', 'development', 'innovation'],
                    'sentiment': 'positive',
                    'quality_score': 0.6,
                    'topics': ['tech', 'mobile'],
                    'entities': ['Mobile', 'Apps']
                }
            ],
            'sustainability': [
                {
                    'title': 'Sustainable Energy Solutions',
                    'description': 'Innovative renewable energy technologies for a greener future',
                    'category': 'Renewable Energy',
                    'source': 'Green Tech',
                    'url': 'https://example.com/sustainable-energy',
                    'published': datetime.now().isoformat(),
                    'keywords': ['sustainable', 'energy', 'renewable', 'green'],
                    'sentiment': 'positive',
                    'quality_score': 0.8,
                    'topics': ['sustainability', 'energy'],
                    'entities': ['Renewable Energy', 'Green Tech']
                },
                {
                    'title': 'Zero Waste Living Tips',
                    'description': 'Practical strategies for reducing household waste',
                    'category': 'Green Living',
                    'source': 'Eco Living',
                    'url': 'https://example.com/zero-waste',
                    'published': datetime.now().isoformat(),
                    'keywords': ['zero waste', 'living', 'sustainable', 'household'],
                    'sentiment': 'positive',
                    'quality_score': 0.7,
                    'topics': ['sustainability', 'lifestyle'],
                    'entities': ['Zero Waste', 'Eco Living']
                },
                {
                    'title': 'Climate Change Solutions',
                    'description': 'Innovative approaches to addressing climate challenges',
                    'category': 'Climate Action',
                    'source': 'Climate News',
                    'url': 'https://example.com/climate-solutions',
                    'published': datetime.now().isoformat(),
                    'keywords': ['climate', 'change', 'solutions', 'environment'],
                    'sentiment': 'neutral',
                    'quality_score': 0.9,
                    'topics': ['sustainability', 'climate'],
                    'entities': ['Climate Change', 'Environment']
                }
            ],
            'business': [
                {
                    'title': 'Startup Funding Trends',
                    'description': 'Latest developments in venture capital and startup financing',
                    'category': 'Venture Capital',
                    'source': 'Startup News',
                    'url': 'https://example.com/startup-funding',
                    'published': datetime.now().isoformat(),
                    'keywords': ['startup', 'funding', 'venture', 'capital'],
                    'sentiment': 'positive',
                    'quality_score': 0.8,
                    'topics': ['business', 'startup'],
                    'entities': ['Startup', 'Venture Capital']
                },
                {
                    'title': 'Digital Transformation Strategies',
                    'description': 'How businesses are adapting to the digital age',
                    'category': 'Business Strategy',
                    'source': 'Business Weekly',
                    'url': 'https://example.com/digital-transformation',
                    'published': datetime.now().isoformat(),
                    'keywords': ['digital', 'transformation', 'business', 'strategy'],
                    'sentiment': 'positive',
                    'quality_score': 0.7,
                    'topics': ['business', 'technology'],
                    'entities': ['Digital', 'Business']
                },
                {
                    'title': 'Remote Work Best Practices',
                    'description': 'Effective strategies for managing remote teams',
                    'category': 'Workplace',
                    'source': 'HR Today',
                    'url': 'https://example.com/remote-work',
                    'published': datetime.now().isoformat(),
                    'keywords': ['remote', 'work', 'teams', 'management'],
                    'sentiment': 'positive',
                    'quality_score': 0.6,
                    'topics': ['business', 'workplace'],
                    'entities': ['Remote Work', 'Management']
                }
            ],
            'general': [
                {
                    'title': 'Technology Innovation Trends',
                    'description': 'Latest breakthroughs in technology and innovation',
                    'category': 'Innovation',
                    'source': 'Tech Trends',
                    'url': 'https://example.com/innovation-trends',
                    'published': datetime.now().isoformat(),
                    'keywords': ['technology', 'innovation', 'trends', 'breakthroughs'],
                    'sentiment': 'positive',
                    'quality_score': 0.8,
                    'topics': ['tech', 'innovation'],
                    'entities': ['Technology', 'Innovation']
                },
                {
                    'title': 'Digital Privacy Concerns',
                    'description': 'Growing concerns about data privacy and protection',
                    'category': 'Privacy',
                    'source': 'Privacy Watch',
                    'url': 'https://example.com/privacy-concerns',
                    'published': datetime.now().isoformat(),
                    'keywords': ['privacy', 'data', 'protection', 'digital'],
                    'sentiment': 'neutral',
                    'quality_score': 0.7,
                    'topics': ['tech', 'privacy'],
                    'entities': ['Privacy', 'Data Protection']
                },
                {
                    'title': 'Future of Work',
                    'description': 'How automation and AI are reshaping employment',
                    'category': 'Workplace',
                    'source': 'Future Work',
                    'url': 'https://example.com/future-work',
                    'published': datetime.now().isoformat(),
                    'keywords': ['future', 'work', 'automation', 'AI'],
                    'sentiment': 'neutral',
                    'quality_score': 0.6,
                    'topics': ['workplace', 'automation'],
                    'entities': ['Future', 'Work', 'AI']
                }
            ]
        }
        
        # Return mock topics for the requested category, or fallback to general
        category_topics = mock_topics.get(category, mock_topics['general'])
        return category_topics[:limit] 