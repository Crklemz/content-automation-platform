import os
import openai
from typing import Dict, List, Optional
from django.conf import settings
from articles.models import Article, Site
from .plagiarism_prevention import PlagiarismPrevention

class AIContentGenerator:
    """AI-powered content generator with plagiarism prevention"""
    
    def __init__(self):
        # Check if OpenAI API key is available
        self.api_key = os.getenv('OPENAI_API_KEY')
        self.api_available = bool(self.api_key)
        
        if self.api_available:
            try:
                self.client = openai.OpenAI(api_key=self.api_key)
                # Test the connection
                self.client.models.list()
                print("OpenAI API connection successful")
            except Exception as e:
                print(f"OpenAI API connection failed: {e}")
                self.api_available = False
        
        self.plagiarism_checker = PlagiarismPrevention()
    
    def generate_article_from_topic(self, topic: str, site: Site, max_length: int = 800, sources: Optional[List[Dict]] = None) -> Dict:
        """
        Generate an article from a topic using AI with plagiarism prevention
        
        Args:
            topic: The topic to write about
            site: The site to create content for
            max_length: Maximum word count
            sources: Optional list of source articles
            
        Returns:
            Dict containing structured article data
        """
        try:
            if self.api_available:
                return self._generate_ai_content(topic, site, max_length, sources)
            else:
                return self._generate_mock_content(topic, site, max_length, sources)
        except Exception as e:
            print(f"Error generating article: {e}")
            return self._generate_mock_content(topic, site, max_length, sources)
    
    def _generate_ai_content(self, topic: str, site: Site, max_length: int, sources: Optional[List[Dict]] = None) -> Dict:
        """Generate content using OpenAI API with plagiarism prevention"""
        try:
            prompt = self._create_enhanced_prompt_with_sources(topic, site, max_length, sources)
            
            response = self.client.chat.completions.create(
                model="gpt-4",
                messages=[
                    {
                        "role": "system",
                        "content": "You are a professional content writer creating engaging, original articles. Always write in your own words and provide proper attribution to sources."
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
            if content:
                parsed_content = self._parse_ai_response(content)
            else:
                return self._generate_mock_content(topic, site, max_length, sources)
            
            # Analyze for plagiarism
            body_text = ' '.join([section['content'] for section in parsed_content.get('sections', []) if section['type'] == 'paragraph'])
            plagiarism_analysis = self.plagiarism_checker.analyze_content_for_plagiarism(
                body_text, sources or []
            )
            
            # Validate source quality
            source_quality = self.plagiarism_checker.validate_source_quality(sources or [])
            
            return {
                'title': parsed_content['title'],
                'sections': parsed_content.get('sections', []),
                'sources': sources or [],
                'status': 'pending',
                'plagiarism_analysis': plagiarism_analysis,
                'source_quality': source_quality,
                'is_original': plagiarism_analysis.get('is_original', True),
                'confidence_score': plagiarism_analysis.get('confidence_score', 0.0)
            }
            
        except Exception as e:
            print(f"Error generating AI content: {e}")
            return self._generate_mock_content(topic, site, max_length, sources)
    
    def _generate_mock_content(self, topic: str, site: Site, max_length: int, sources: Optional[List[Dict]] = None) -> Dict:
        """Generate mock content when AI API is not available with plagiarism prevention"""
        
        # Create structured mock article data
        title = f"Understanding {topic}: A Comprehensive Guide for {site.name}"
        
        # Create structured content sections
        sections = [
            {
                'type': 'heading',
                'level': 2,
                'content': f'Introduction to {topic}'
            },
            {
                'type': 'paragraph',
                'content': f'In today\'s rapidly evolving digital landscape, understanding {topic} has become increasingly important for professionals and enthusiasts alike. This comprehensive guide explores the key aspects of {topic} and its relevance in modern technology.'
            },
            {
                'type': 'heading',
                'level': 2,
                'content': 'Key Concepts'
            },
            {
                'type': 'paragraph',
                'content': f'{topic} encompasses several fundamental principles that are essential for anyone looking to stay current in this field. From basic concepts to advanced applications, this topic offers a wealth of knowledge for continuous learning.'
            },
            {
                'type': 'heading',
                'level': 2,
                'content': 'Practical Applications'
            },
            {
                'type': 'paragraph',
                'content': f'The practical applications of {topic} are vast and varied. Whether you\'re a developer, business professional, or technology enthusiast, understanding these applications can provide significant advantages in your respective field.'
            },
            {
                'type': 'heading',
                'level': 2,
                'content': 'Future Trends'
            },
            {
                'type': 'paragraph',
                'content': f'As technology continues to advance, the landscape of {topic} is expected to evolve significantly. Staying informed about emerging trends and developments is crucial for maintaining a competitive edge.'
            },
            {
                'type': 'heading',
                'level': 2,
                'content': 'Conclusion'
            },
            {
                'type': 'paragraph',
                'content': f'{topic} represents a fundamental aspect of modern technology that continues to shape our digital world. By understanding its principles and applications, individuals and organizations can better navigate the complexities of today\'s technological landscape.'
            }
        ]
        
        # Analyze for plagiarism even in mock content
        body_text = ' '.join([section['content'] for section in sections if section['type'] == 'paragraph'])
        plagiarism_analysis = self.plagiarism_checker.analyze_content_for_plagiarism(
            body_text, sources or []
        )
        
        # Validate source quality
        source_quality = self.plagiarism_checker.validate_source_quality(sources or [])
        
        return {
            'title': title,
            'sections': sections,
            'sources': sources or [],
            'status': 'pending',
            'plagiarism_analysis': plagiarism_analysis,
            'source_quality': source_quality,
            'is_original': plagiarism_analysis.get('is_original', True),
            'confidence_score': plagiarism_analysis.get('confidence_score', 0.0)
        }
    
    def _create_enhanced_prompt_with_sources(self, topic: str, site: Site, max_length: int, sources: Optional[List[Dict]] = None) -> str:
        """Create an enhanced site-specific prompt for article generation with strong plagiarism prevention"""
        sources_text = ""
        if sources:
            sources_text = "\n\nSources for reference (use for facts and insights, but write in your own words):\n"
            for i, source in enumerate(sources, 1):
                sources_text += f"{i}. {source.get('title', 'Unknown')} - {source.get('source', 'Unknown')} ({source.get('url', 'No URL')})\n"
                if source.get('description'):
                    sources_text += f"   Summary: {source.get('description', '')}\n"
        
        return f"""
        Write an engaging article about "{topic}" for {site.name}.
        
        Site Description: {site.description}
        Brand Colors: {site.primary_color} and {site.secondary_color}
        Target Length: {max_length} words
        
        {sources_text}
        
        CRITICAL REQUIREMENTS:
        - Create COMPLETELY ORIGINAL content based on the information provided
        - NEVER copy text directly from sources
        - Use sources for facts, data, and insights only
        - Write everything in your own unique voice and style
        - Provide proper attribution to sources
        - DO NOT include a "Sources and Further Reading" section (this is handled separately)
        
        Please provide the article in this JSON format:
        
        {{
            "title": "Engaging title here",
            "sections": [
                {{
                    "type": "heading",
                    "level": 2,
                    "content": "Section heading"
                }},
                {{
                    "type": "paragraph",
                    "content": "Paragraph content here"
                }},
                {{
                    "type": "list",
                    "style": "unordered",
                    "items": [
                        {{
                            "type": "list_item",
                            "content": "List item content",
                            "url": "optional_url"
                        }}
                    ]
                }}
            ]
        }}
        
        Writing guidelines:
        - Make the content engaging and informative
        - Relevant to the site's theme
        - SEO-friendly
        - Professional yet accessible
        - Include relevant keywords naturally
        - Use the information as inspiration to create unique insights
        - Always attribute facts and quotes to their sources
        - Create original analysis and commentary
        """
    
    def _parse_ai_response(self, content: str) -> Dict:
        """Parse AI response into structured content"""
        try:
            # Try to parse as JSON first
            import json
            parsed = json.loads(content)
            return parsed
        except json.JSONDecodeError:
            # Fallback to old format parsing
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
            
            # Convert old format to new structured format
            sections = [
                {
                    'type': 'paragraph',
                    'content': body.strip()
                }
            ]
            
            return {
                'title': title,
                'sections': sections
            }
    
    def validate_article_originality(self, content: str, sources: List[Dict]) -> Dict:
        """
        Validate that an article is original and properly attributed
        
        Args:
            content: The article content to validate
            sources: List of sources used
            
        Returns:
            Dict containing validation results
        """
        return self.plagiarism_checker.analyze_content_for_plagiarism(content, sources)
    
    def get_source_quality_report(self, sources: List[Dict]) -> Dict:
        """
        Get a quality report for sources used
        
        Args:
            sources: List of sources to analyze
            
        Returns:
            Dict containing source quality analysis
        """
        return self.plagiarism_checker.validate_source_quality(sources)
    
    def generate_daily_top_3_article(self, site_description: str, scraped_articles: List[Dict], site: Site) -> Dict:
        """
        Generate a "Daily Top 3" format article from scraped content using AI
        
        Args:
            site_description: The site's description/topic
            scraped_articles: List of scraped articles with analysis
            site: The site object
            
        Returns:
            Dict containing the formatted article
        """
        try:
            if not scraped_articles:
                return {
                    'title': f"Top 3 {site_description}: No Articles Available",
                    'sections': [
                        {
                            'type': 'paragraph',
                            'content': f"Currently, there are limited trending articles available for {site_description}. Please check back later for the latest updates."
                        }
                    ],
                    'sources': []
                }
            
            # Extract main topics from each article
            main_topics = []
            for article in scraped_articles[:3]:
                topics = article.get('topics', [])
                if topics:
                    # Use the first topic as main topic, or create one from title
                    main_topic = topics[0].replace('_', ' ').title() if topics else self._extract_main_topic(article.get('title', ''))
                    main_topics.append(main_topic)
                else:
                    main_topic = self._extract_main_topic(article.get('title', ''))
                    main_topics.append(main_topic)
            
            # Create main title with main topics
            main_topics_text = ", ".join(main_topics)
            # Remove any periods from site description
            clean_site_description = site_description.rstrip('.')
            main_title = f"Top 3 {clean_site_description}: {main_topics_text}"
            
            # Use AI to create better overall summary if available
            if self.api_available:
                overall_summary = self._create_ai_overall_summary(scraped_articles[:3], site_description, site)
            else:
                overall_summary = self._create_overall_summary(scraped_articles[:3], site_description)
            
            # Create structured sections
            sections = []
            
            # Overview section
            sections.append({
                'type': 'heading',
                'level': 2,
                'content': "Today's Trending Summary"
            })
            sections.append({
                'type': 'paragraph',
                'content': overall_summary
            })
            
            # Articles section
            sections.append({
                'type': 'heading',
                'level': 2,
                'content': "Top Stories"
            })
            
            # Add individual articles
            sources = []
            for i, article in enumerate(scraped_articles[:3]):
                title = article.get('title', '')
                url = article.get('url', '')
                source = article.get('source', 'Unknown')
                summary = article.get('summary', '')
                category = article.get('category', 'General')
                main_topic = main_topics[i] if i < len(main_topics) else 'General'
                
                # Article heading
                sections.append({
                    'type': 'heading',
                    'level': 3,
                    'content': title,
                    'url': url
                })
                
                # Article summary
                sections.append({
                    'type': 'paragraph',
                    'content': summary
                })
                
                # Article metadata
                sections.append({
                    'type': 'metadata',
                    'category': main_topic,
                    'source': source,
                    'url': url
                })
                
                # Add to sources list
                sources.append({
                    'title': title,
                    'url': url,
                    'source': source
                })
            
            return {
                'title': main_title,
                'sections': sections,
                'sources': sources
            }
            
        except Exception as e:
            print(f"Error generating Daily Top 3 article: {e}")
            return {
                'title': f"Top 3 {site_description}: Error Generating Content",
                'sections': [
                    {
                        'type': 'paragraph',
                        'content': f"Error generating content for {site_description}. Please try again later."
                    }
                ],
                'sources': []
            }
    
    def _extract_main_topic(self, title: str) -> str:
        """Extract a main topic from an article title"""
        # Simple keyword extraction for main topics
        title_lower = title.lower()
        
        if any(word in title_lower for word in ['ai', 'artificial intelligence', 'machine learning']):
            return "AI & Technology"
        elif any(word in title_lower for word in ['sustainable', 'green', 'environment', 'climate']):
            return "Sustainability"
        elif any(word in title_lower for word in ['business', 'startup', 'entrepreneur']):
            return "Business & Innovation"
        elif any(word in title_lower for word in ['health', 'medical', 'wellness']):
            return "Health & Wellness"
        elif any(word in title_lower for word in ['cybersecurity', 'security', 'privacy']):
            return "Cybersecurity"
        elif any(word in title_lower for word in ['cloud', 'aws', 'azure']):
            return "Cloud Computing"
        else:
            return "Latest Trends"
    
    def _create_overall_summary(self, articles: List[Dict], site_description: str) -> str:
        """Create an overall summary of all articles"""
        if not articles:
            return f"Currently, there are limited trending articles available for {site_description}."
        
        # Extract key themes and topics from articles
        themes = []
        topics = []
        for article in articles:
            article_topics = article.get('topics', [])
            topics.extend(article_topics)
            
            # Extract theme from title and description
            title = article.get('title', '').lower()
            description = article.get('description', '').lower()
            
            if any(word in title or word in description for word in ['ai', 'artificial intelligence', 'machine learning']):
                themes.append('Artificial Intelligence')
            elif any(word in title or word in description for word in ['sustainable', 'green', 'environment', 'climate']):
                themes.append('Sustainability')
            elif any(word in title or word in description for word in ['business', 'startup', 'entrepreneur']):
                themes.append('Business Innovation')
            elif any(word in title or word in description for word in ['security', 'cybersecurity', 'privacy']):
                themes.append('Cybersecurity')
            elif any(word in title or word in description for word in ['cloud', 'aws', 'azure']):
                themes.append('Cloud Computing')
            else:
                themes.append('Technology Trends')
        
        # Create a comprehensive summary
        unique_themes = list(set(themes))[:3]  # Top 3 unique themes
        unique_topics = list(set(topics))[:5]  # Top 5 unique topics
        
        if unique_themes:
            themes_text = ", ".join(unique_themes)
            summary = f"Today's top stories highlight significant developments in {themes_text} within the context of {site_description}. "
        else:
            summary = f"Today's trending articles showcase important developments related to {site_description}. "
        
        if unique_topics:
            topics_text = ", ".join([topic.replace('_', ' ').title() for topic in unique_topics])
            summary += f"Key areas of focus include {topics_text}. "
        
        summary += f"These stories represent the most relevant and engaging content currently circulating in this space, providing valuable insights for anyone interested in staying current with {site_description}. The articles demonstrate the dynamic nature of this field and highlight emerging trends that could have significant implications for the industry."
        
        return summary
    
    def _create_ai_overall_summary(self, articles: List[Dict], site_description: str, site: Site) -> str:
        """Create an AI-enhanced overall summary of all articles"""
        if not articles:
            return f"Currently, there are limited trending articles available for {site_description}."
        
        try:
            # Prepare article data for AI
            articles_text = ""
            for i, article in enumerate(articles, 1):
                title = article.get('title', '')
                summary = article.get('summary', '')
                source = article.get('source', 'Unknown')
                articles_text += f"{i}. {title} (Source: {source})\n   Summary: {summary}\n\n"
            
            prompt = f"""
            Create a compelling overall summary for a "Daily Top 3" article about {site_description}.
            
            Site: {site.name}
            Site Description: {site_description}
            
            Here are the 3 top articles for today:
            
            {articles_text}
            
            Please create a 2-3 sentence summary that:
            - Highlights the key themes and trends across these articles
            - Explains why these stories matter for {site_description}
            - Provides context about the broader implications
            - Uses engaging, professional language
            - Avoids repetition and creates a cohesive narrative
            
            Write only the summary text, no additional formatting.
            """
            
            response = self.client.chat.completions.create(
                model="gpt-4",
                messages=[
                    {
                        "role": "system",
                        "content": "You are a professional content writer creating engaging summaries for technology and business articles."
                    },
                    {
                        "role": "user",
                        "content": prompt
                    }
                ],
                max_tokens=300,
                temperature=0.7
            )
            
            content = response.choices[0].message.content
            return content.strip() if content else self._create_overall_summary(articles, site_description)
            
        except Exception as e:
            print(f"Error creating AI overall summary: {e}")
            # Fallback to non-AI summary
            return self._create_overall_summary(articles, site_description)