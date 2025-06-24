from typing import List, Dict, Optional
from django.utils import timezone
from datetime import datetime, timedelta
from articles.models import Article, Site
from .ai_generator import AIContentGenerator
from .news_scraper import NewsScraper

class ContentAutomation:
    """Orchestrates content generation and automation"""
    
    def __init__(self):
        self.ai_generator = AIContentGenerator()
        self.news_scraper = NewsScraper()
    
    def generate_content_for_site(self, site: Site, num_articles: int = 3) -> List[Article]:
        """
        Generate content for a specific site
        
        Args:
            site: The site to generate content for
            num_articles: Number of articles to generate
            
        Returns:
            List of created Article objects
        """
        try:
            # Get trending topics relevant to the site
            topics = self.news_scraper.get_site_specific_topics(
                site.description, 
                limit=num_articles
            )
            
            created_articles = []
            
            for topic in topics:
                # Generate article content using AI
                article_data = self.ai_generator.generate_article_from_topic(
                    topic['title'], 
                    site
                )
                
                # Create article slug from title
                slug = self._create_slug(article_data['title'])
                
                # Create the article (only use fields that exist in the model)
                article = Article.objects.create(
                    title=article_data['title'],
                    body=article_data['body'],
                    slug=slug,
                    site=site,
                    status='pending'
                )
                
                created_articles.append(article)
                print(f"Generated article: {article.title} for {site.name}")
            
            return created_articles
            
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
            # Generate article content using AI
            article_data = self.ai_generator.generate_article_from_topic(topic, site)
            
            # Create article slug from title
            slug = self._create_slug(article_data['title'])
            
            # Create the article (only use fields that exist in the model)
            article = Article.objects.create(
                title=article_data['title'],
                body=article_data['body'],
                slug=slug,
                site=site,
                status='pending'
            )
            
            print(f"Generated article from topic '{topic}': {article.title}")
            return article
            
        except Exception as e:
            print(f"Error generating article from topic '{topic}': {e}")
            return None
    
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