import os
import openai
from typing import Dict, List, Optional
from django.conf import settings
from articles.models import Article, Site
from .plagiarism_prevention import PlagiarismPrevention

class AIContentGenerator:
    """AI-powered content generation service using OpenAI with plagiarism prevention"""
    
    def __init__(self):
        # Check if OpenAI API key is available
        self.api_key = os.getenv('OPENAI_API_KEY')
        if self.api_key:
            try:
                # Try to initialize OpenAI client with custom session
                try:
                    from httpx import Client
                    http_client = Client()
                    self.client = openai.OpenAI(
                        api_key=self.api_key,
                        http_client=http_client
                    )
                    self.api_available = True
                except Exception:
                    # Try with basic configuration
                    try:
                        # Clear any global state
                        openai.api_key = None
                        openai.base_url = None
                        
                        # Try with minimal configuration
                        self.client = openai.OpenAI(api_key=self.api_key)
                        self.api_available = True
                    except Exception:
                        self.api_available = False
                
            except Exception:
                self.api_available = False
        else:
            self.api_available = False
        
        # Initialize plagiarism prevention system
        self.plagiarism_checker = PlagiarismPrevention()
    
    def generate_article_from_topic(self, topic: str, site: Site, max_length: int = 800, sources: Optional[List[Dict]] = None) -> Dict:
        """
        Generate an article from a given topic for a specific site with plagiarism prevention
        
        Args:
            topic: The topic to write about
            site: The site object with branding info
            max_length: Maximum article length in words
            sources: List of source articles for attribution
            
        Returns:
            Dict containing title, body, sources, and plagiarism analysis
        """
        if not self.api_available:
            # Fallback to mock content generation
            return self._generate_mock_content(topic, site, max_length, sources)
        
        try:
            # Validate source quality first
            source_quality = self.plagiarism_checker.validate_source_quality(sources or [])
            
            # Create site-specific prompt with enhanced source attribution
            prompt = self._create_enhanced_prompt_with_sources(topic, site, max_length, sources)
            
            response = self.client.chat.completions.create(
                model="gpt-4",
                messages=[
                    {
                        "role": "system",
                        "content": f"You are a professional content writer for {site.name}. "
                                  f"Write engaging, informative articles that match the site's "
                                  f"branding and style. Use a {site.primary_color} and {site.secondary_color} "
                                  f"color scheme in your writing style. "
                                  f"CRITICAL: Always create original content based on the information provided. "
                                  f"Never copy text directly from sources. "
                                  f"Use sources for facts and insights, but write in your own words. "
                                  f"Always provide proper attribution to sources and avoid plagiarism."
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
                
                # Get the generated content
                generated_content = parsed_content.get('body', content)
                
                # Analyze for plagiarism
                plagiarism_analysis = self.plagiarism_checker.analyze_content_for_plagiarism(
                    generated_content, sources or []
                )
                
                # Enhance content with proper attribution
                enhanced_content = self.plagiarism_checker.enhance_content_with_attribution(
                    generated_content, sources or []
                )
                
                return {
                    'title': parsed_content.get('title', f"Article about {topic}"),
                    'body': enhanced_content,
                    'sources': sources or [],
                    'status': 'pending',
                    'plagiarism_analysis': plagiarism_analysis,
                    'source_quality': source_quality,
                    'is_original': plagiarism_analysis.get('is_original', True),
                    'confidence_score': plagiarism_analysis.get('confidence_score', 0.0)
                }
            else:
                return self._generate_mock_content(topic, site, max_length, sources)
            
        except Exception as e:
            # Fallback to mock content
            return self._generate_mock_content(topic, site, max_length, sources)
    
    def _generate_mock_content(self, topic: str, site: Site, max_length: int, sources: Optional[List[Dict]] = None) -> Dict:
        """Generate mock content when AI API is not available with plagiarism prevention"""
        
        # Create a structured mock article with source attribution
        title = f"Understanding {topic}: A Comprehensive Guide for {site.name}"
        
        # Create source attribution section if sources are provided
        sources_section = ""
        if sources:
            sources_section = self.plagiarism_checker._create_attribution_section(sources)
        
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
        {sources_section}
        """
        
        # Analyze for plagiarism even in mock content
        plagiarism_analysis = self.plagiarism_checker.analyze_content_for_plagiarism(
            body, sources or []
        )
        
        # Validate source quality
        source_quality = self.plagiarism_checker.validate_source_quality(sources or [])
        
        return {
            'title': title,
            'body': body.strip(),
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
        - Include a "Sources and Further Reading" section at the end
        
        Please provide the article in this format:
        
        TITLE: [Engaging title here]
        
        BODY: [Article content here with HTML formatting]
        
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
                    'body': f"<p>Currently, there are limited trending articles available for {site_description}. Please check back later for the latest updates.</p>",
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
            
            # Create individual article summaries with proper formatting
            article_summaries = []
            sources = []
            
            for i, article in enumerate(scraped_articles[:3]):
                title = article.get('title', '')
                url = article.get('url', '')
                source = article.get('source', 'Unknown')
                summary = article.get('summary', '')
                category = article.get('category', 'General')
                main_topic = main_topics[i] if i < len(main_topics) else 'General'
                
                # Use the summary as-is (no enhancement needed)
                article_summary = summary
                
                # Create clickable title link
                title_link = f'<a href="{url}" target="_blank" rel="noopener noreferrer" class="article-title-link">{title}</a>' if url else title
                
                # Create individual summary with proper HTML formatting
                individual_summary = f"""
                <div class="article-item">
                    <h3><strong>{title_link}</strong></h3>
                    <p class="article-summary">{article_summary}</p>
                    <div class="article-meta">
                        <span class="category">{main_topic}</span>
                        <span class="source">Source: <a href="{url}" target="_blank" rel="noopener noreferrer">{source}</a></span>
                    </div>
                </div>
                """
                article_summaries.append(individual_summary)
                
                # Add to sources list
                sources.append({
                    'title': title,
                    'url': url,
                    'source': source
                })
            
            # Combine everything into the final article with proper HTML structure
            article_body = f"""
            <div class="daily-top-3">
                <div class="overview">
                    <h2><strong>Today's Trending Summary</strong></h2>
                    <p>{overall_summary}</p>
                </div>
                
                <div class="articles">
                    <h2><strong>Top Stories</strong></h2>
                    {''.join(article_summaries)}
                </div>
                
                <div class="sources">
                    <h3><strong>Sources and Further Reading</strong></h3>
                    <ul>
                        {''.join([f'<li><a href="{source["url"]}" target="_blank" rel="noopener noreferrer">{source["title"]}</a> - {source["source"]}</li>' for source in sources])}
                    </ul>
                </div>
            </div>
            """
            
            return {
                'title': main_title,
                'body': article_body,
                'sources': sources
            }
            
        except Exception as e:
            print(f"Error generating Daily Top 3 article: {e}")
            return {
                'title': f"Top 3 {site_description}: Error Generating Content",
                'body': f"<p>Error generating content for {site_description}. Please try again later.</p>",
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