from typing import List, Dict
import random

class NewsScraper:
    """Mock news scraper service that provides trending topics"""
    
    def __init__(self):
        # Mock trending topics for different categories
        self.mock_topics = {
            'ai': [
                {
                    'title': 'Artificial Intelligence in Healthcare',
                    'description': 'How AI is revolutionizing medical diagnosis and treatment',
                    'category': 'AI & Healthcare',
                    'source': 'Tech Trends'
                },
                {
                    'title': 'Machine Learning for Business',
                    'description': 'Practical applications of ML in modern business operations',
                    'category': 'AI & Business',
                    'source': 'Business Tech'
                },
                {
                    'title': 'Natural Language Processing Advances',
                    'description': 'Latest developments in NLP and language models',
                    'category': 'AI & NLP',
                    'source': 'AI Research'
                },
                {
                    'title': 'Computer Vision Applications',
                    'description': 'Real-world applications of computer vision technology',
                    'category': 'AI & Vision',
                    'source': 'Computer Science'
                },
                {
                    'title': 'AI Ethics and Responsibility',
                    'description': 'Important considerations for ethical AI development',
                    'category': 'AI & Ethics',
                    'source': 'Tech Ethics'
                }
            ],
            'tech': [
                {
                    'title': 'Cloud Computing Trends',
                    'description': 'Latest developments in cloud infrastructure and services',
                    'category': 'Cloud Computing',
                    'source': 'Tech News'
                },
                {
                    'title': 'Cybersecurity Best Practices',
                    'description': 'Essential security measures for modern applications',
                    'category': 'Cybersecurity',
                    'source': 'Security Weekly'
                },
                {
                    'title': 'DevOps Automation',
                    'description': 'Streamlining development and deployment processes',
                    'category': 'DevOps',
                    'source': 'DevOps Daily'
                },
                {
                    'title': 'Mobile App Development',
                    'description': 'Trends in mobile application development and design',
                    'category': 'Mobile Development',
                    'source': 'Mobile Tech'
                },
                {
                    'title': 'Data Science Applications',
                    'description': 'Real-world applications of data science and analytics',
                    'category': 'Data Science',
                    'source': 'Data Insights'
                }
            ],
            'general': [
                {
                    'title': 'Digital Transformation',
                    'description': 'How businesses are adapting to digital-first strategies',
                    'category': 'Business',
                    'source': 'Business Weekly'
                },
                {
                    'title': 'Remote Work Technology',
                    'description': 'Tools and strategies for effective remote collaboration',
                    'category': 'Workplace',
                    'source': 'Work Tech'
                },
                {
                    'title': 'Sustainable Technology',
                    'description': 'Green tech solutions for environmental challenges',
                    'category': 'Sustainability',
                    'source': 'Green Tech'
                },
                {
                    'title': 'Blockchain Applications',
                    'description': 'Beyond cryptocurrency: practical blockchain use cases',
                    'category': 'Blockchain',
                    'source': 'Crypto News'
                },
                {
                    'title': 'Internet of Things (IoT)',
                    'description': 'Connected devices and smart technology integration',
                    'category': 'IoT',
                    'source': 'IoT Daily'
                }
            ]
        }
    
    def get_trending_topics(self, category: str = "general", limit: int = 10) -> List[Dict]:
        """
        Get mock trending topics for a specific category
        
        Args:
            category: Topic category (ai, tech, general)
            limit: Number of topics to return
            
        Returns:
            List of trending topics
        """
        category = category.lower()
        if category not in self.mock_topics:
            category = 'general'
        
        topics = self.mock_topics[category].copy()
        random.shuffle(topics)  # Randomize order
        
        return topics[:limit]
    
    def get_site_specific_topics(self, site_description: str, limit: int = 5) -> List[Dict]:
        """
        Get topics relevant to a specific site based on its description
        
        Args:
            site_description: Description of the site
            limit: Number of topics to return
            
        Returns:
            List of relevant topics
        """
        description_lower = site_description.lower()
        
        # Determine relevant category based on site description
        if any(keyword in description_lower for keyword in ['ai', 'artificial intelligence', 'machine learning']):
            category = 'ai'
        elif any(keyword in description_lower for keyword in ['tech', 'technology', 'software', 'development']):
            category = 'tech'
        else:
            category = 'general'
        
        return self.get_trending_topics(category, limit) 