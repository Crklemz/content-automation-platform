from typing import List, Dict, Optional
from django.utils import timezone
from datetime import datetime, timedelta
from articles.models import Article, Site
from .ai_generator import AIContentGenerator
from .ai_news_scraper import AINewsScraper

class ContentAutomation:
    """Orchestrates content generation and automation"""
    
    def __init__(self):
        self.ai_generator = AIContentGenerator()
        self.news_scraper = AINewsScraper()
    
    def generate_content_for_site(self, site: Site, num_articles: int = 3) -> List[Article]:
        """
        Generate Daily Top 3 content for a specific site
        
        Args:
            site: The site to generate content for
            num_articles: Number of articles to include (default 3 for Daily Top 3)
            
        Returns:
            List of created Article objects
        """
        try:
            # Get trending topics for the site
            trending_topics = self.news_scraper.get_site_specific_topics(site.description, num_articles)
            
            if not trending_topics:
                print(f"No trending topics found for {site.name}")
                return []
            
            # Generate Daily Top 3 article using AI
            article_data = self.ai_generator.generate_daily_top_3_article(
                site.description, 
                trending_topics, 
                site
            )
            
            # Create article slug from title
            slug = self._create_slug(article_data['title'])
            
            # Create the article
            article = Article.objects.create(
                title=article_data['title'],
                body=article_data['body'],
                slug=slug,
                site=site,
                status='pending',
                sources=article_data.get('sources', [])
            )
            
            print(f"Generated Daily Top 3 article: {article.title} for {site.name}")
            return [article]
            
        except Exception as e:
            print(f"Error generating content for site {site.name}: {e}")
            return []
    
    def generate_content_for_all_sites(self, articles_per_site: int = 2) -> Dict[str, List[Article]]:
        """
        Generate content for all sites
        
        Args:
            articles_per_site: Number of articles to generate per site
            
        Returns:
            Dict mapping site names to lists of created articles
        """
        sites = Site.objects.all()
        results = {}
        
        for site in sites:
            articles = self.generate_content_for_site(site, articles_per_site)
            results[site.name] = articles
        
        return results
    
    def generate_content_from_topic(self, topic: str, site: Site) -> Optional[Article]:
        """
        Generate a single article from a specific topic
        
        Args:
            topic: The topic to write about
            site: The site to create the article for
            
        Returns:
            Created Article object or None if failed
        """
        try:
            # Get relevant news sources for the topic
            sources = self._get_relevant_sources(topic, site)
            
            # Generate article content using AI with sources
            article_data = self.ai_generator.generate_article_from_topic(topic, site, sources=sources)
            
            # Create article slug from title
            slug = self._create_slug(article_data['title'])
            
            # Create the article (only use fields that exist in the model)
            article = Article.objects.create(
                title=article_data['title'],
                body=article_data['body'],
                slug=slug,
                site=site,
                status='pending',
                sources=article_data.get('sources', [])
            )
            
            print(f"Generated article from topic '{topic}': {article.title}")
            return article
            
        except Exception as e:
            print(f"Error generating article from topic '{topic}': {e}")
            return None
    
    def _get_relevant_sources(self, topic: str, site: Site) -> List[Dict]:
        """
        Get relevant news sources for a topic
        
        Args:
            topic: The topic to find sources for
            site: The site context
            
        Returns:
            List of relevant source articles
        """
        try:
            # Get trending topics for the site
            trending_topics = self.news_scraper.get_site_specific_topics(site.description, limit=10)
            
            # Find topics that are relevant to our target topic
            relevant_sources = []
            topic_lower = topic.lower()
            
            for trending_topic in trending_topics:
                trending_title = trending_topic.get('title', '').lower()
                trending_desc = trending_topic.get('description', '').lower()
                
                # Check if the trending topic is relevant to our target topic
                if (topic_lower in trending_title or 
                    topic_lower in trending_desc or
                    any(word in trending_title for word in topic_lower.split()) or
                    any(word in trending_desc for word in topic_lower.split())):
                    
                    relevant_sources.append(trending_topic)
            
            # If no relevant sources found, get some general sources for context
            if not relevant_sources:
                relevant_sources = trending_topics[:3]  # Get first 3 trending topics
            
            return relevant_sources
            
        except Exception as e:
            print(f"Error getting relevant sources: {e}")
            return []
    
    def _create_topic_summary(self, topic: str, sources: List[Dict]) -> str:
        """
        Create a summary of a topic based on available sources
        
        Args:
            topic: The topic to summarize
            sources: List of source articles
            
        Returns:
            Summary of the topic
        """
        if not sources:
            return f"Currently, there is limited information available about {topic}. This topic represents an emerging area of interest in the technology landscape."
        
        # Create a summary based on the sources
        summary_parts = [f"Based on recent news and developments, {topic} is currently a trending topic in the technology sector."]
        
        # Add insights from sources
        for source in sources[:3]:  # Use first 3 sources
            title = source.get('title', '')
            description = source.get('description', '')
            source_name = source.get('source', 'Unknown')
            
            if description:
                summary_parts.append(f"According to {source_name}, {description}")
        
        summary_parts.append(f"These developments suggest that {topic} is gaining significant attention and may have important implications for the industry.")
        
        return ' '.join(summary_parts)
    
    def get_trending_topics_for_site(self, site: Site, limit: int = 5) -> List[Dict]:
        """
        Get trending topics relevant to a specific site
        
        Args:
            site: The site to get topics for
            limit: Number of topics to return
            
        Returns:
            List of trending topics
        """
        return self.news_scraper.get_site_specific_topics(site.description, limit)
    
    def get_general_trending_topics(self, category: str = "general", limit: int = 10) -> List[Dict]:
        """
        Get general trending topics
        
        Args:
            category: News category
            limit: Number of topics to return
            
        Returns:
            List of trending topics
        """
        return self.news_scraper.get_trending_topics(category, limit=limit)
    
    def _create_slug(self, title: str) -> str:
        """Create a URL-friendly slug from title"""
        import re
        
        # Convert to lowercase and replace spaces with hyphens
        slug = title.lower()
        slug = re.sub(r'[^\w\s-]', '', slug)  # Remove special characters
        slug = re.sub(r'[-\s]+', '-', slug)   # Replace spaces and multiple hyphens with single hyphen
        slug = slug.strip('-')                # Remove leading/trailing hyphens
        
        # Ensure slug is not too long
        if len(slug) > 200:
            slug = slug[:200].rsplit('-', 1)[0]
        
        # Add timestamp to ensure uniqueness
        timestamp = timezone.now().strftime('%Y%m%d-%H%M%S')
        slug = f"{slug}-{timestamp}"
        
        return slug
    
    def cleanup_old_articles(self, days_old: int = 30) -> int:
        """
        Clean up old rejected articles
        
        Args:
            days_old: Number of days after which to delete rejected articles
            
        Returns:
            Number of articles deleted
        """
        cutoff_date = timezone.now() - timedelta(days=days_old)
        old_rejected_articles = Article.objects.filter(
            status='rejected',
            created_at__lt=cutoff_date
        )
        
        count = old_rejected_articles.count()
        old_rejected_articles.delete()
        
        print(f"Cleaned up {count} old rejected articles")
        return count 