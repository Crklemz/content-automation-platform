import os
import openai
from typing import Dict, List, Optional
from django.conf import settings
from articles.models import Article, Site

class AIContentGenerator:
    """AI-powered content generation service using OpenAI"""
    
    def __init__(self):
        # Check if OpenAI API key is available
        self.api_key = os.getenv('OPENAI_API_KEY')
        if self.api_key:
            try:
                self.client = openai.OpenAI(api_key=self.api_key)
                self.api_available = True
            except Exception as e:
                print(f"Warning: OpenAI client initialization failed: {e}")
                self.api_available = False
        else:
            print("Warning: OPENAI_API_KEY not found in environment variables")
            self.api_available = False
    
    def generate_article_from_topic(self, topic: str, site: Site, max_length: int = 800) -> Dict:
        """
        Generate an article from a given topic for a specific site
        
        Args:
            topic: The topic to write about
            site: The site object with branding info
            max_length: Maximum article length in words
            
        Returns:
            Dict containing title and body (no summary field)
        """
        if not self.api_available:
            # Fallback to mock content generation
            return self._generate_mock_content(topic, site, max_length)
        
        try:
            # Create site-specific prompt
            prompt = self._create_site_prompt(topic, site, max_length)
            
            response = self.client.chat.completions.create(
                model="gpt-4",
                messages=[
                    {
                        "role": "system",
                        "content": f"You are a professional content writer for {site.name}. "
                                  f"Write engaging, informative articles that match the site's "
                                  f"branding and style. Use a {site.primary_color} and {site.secondary_color} "
                                  f"color scheme in your writing style."
                    },
                    {
                        "role": "user",
                        "content": prompt
                    }
                ],
                max_tokens=2000,
                temperature=0.7
            )
            
            content = response.choices[0].message.content
            
            # Parse the response into title and body
            if content:
                parsed_content = self._parse_ai_response(content)
                
                return {
                    'title': parsed_content.get('title', f"Article about {topic}"),
                    'body': parsed_content.get('body', content),
                    'status': 'pending'
                }
            else:
                return self._generate_mock_content(topic, site, max_length)
            
        except Exception as e:
            print(f"Error generating article with OpenAI: {e}")
            # Fallback to mock content
            return self._generate_mock_content(topic, site, max_length)
    
    def _generate_mock_content(self, topic: str, site: Site, max_length: int) -> Dict:
        """Generate mock content when AI API is not available"""
        print(f"Generating mock content for topic: {topic}")
        
        # Create a structured mock article
        title = f"Understanding {topic}: A Comprehensive Guide for {site.name}"
        
        body = f"""
        <h2>Introduction to {topic}</h2>
        <p>In today's rapidly evolving digital landscape, understanding {topic} has become increasingly important for professionals and enthusiasts alike. This comprehensive guide explores the key aspects of {topic} and its relevance in modern technology.</p>
        
        <h2>Key Concepts</h2>
        <p>{topic} encompasses several fundamental principles that are essential for anyone looking to stay current in this field. From basic concepts to advanced applications, this topic offers a wealth of knowledge for continuous learning.</p>
        
        <h2>Practical Applications</h2>
        <p>The practical applications of {topic} are vast and varied. Whether you're a developer, business professional, or technology enthusiast, understanding these applications can provide significant advantages in your respective field.</p>
        
        <h2>Future Trends</h2>
        <p>As technology continues to advance, the landscape of {topic} is expected to evolve significantly. Staying informed about emerging trends and developments is crucial for maintaining a competitive edge.</p>
        
        <h2>Conclusion</h2>
        <p>{topic} represents a fundamental aspect of modern technology that continues to shape our digital world. By understanding its principles and applications, individuals and organizations can better navigate the complexities of today's technological landscape.</p>
        """
        
        return {
            'title': title,
            'body': body.strip(),
            'status': 'pending'
        }
    
    def _create_site_prompt(self, topic: str, site: Site, max_length: int) -> str:
        """Create a site-specific prompt for article generation"""
        return f"""
        Write an engaging article about "{topic}" for {site.name}.
        
        Site Description: {site.description}
        Brand Colors: {site.primary_color} and {site.secondary_color}
        Target Length: {max_length} words
        
        Please provide the article in this format:
        
        TITLE: [Engaging title here]
        
        BODY: [Article content here with HTML formatting]
        
        Make the content:
        - Engaging and informative
        - Relevant to the site's theme
        - SEO-friendly
        - Professional yet accessible
        - Include relevant keywords naturally
        """
    
    def _parse_ai_response(self, content: str) -> Dict:
        """Parse AI response into structured content"""
        lines = content.split('\n')
        title = ""
        body = ""
        
        current_section = None
        
        for line in lines:
            line = line.strip()
            if not line:
                continue
                
            if line.startswith('TITLE:'):
                current_section = 'title'
                title = line.replace('TITLE:', '').strip()
            elif line.startswith('BODY:'):
                current_section = 'body'
                body = line.replace('BODY:', '').strip()
            elif current_section == 'body':
                body += ' ' + line
        
        return {
            'title': title,
            'body': body.strip()
        }