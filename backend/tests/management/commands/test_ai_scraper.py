from django.core.management.base import BaseCommand
from services.ai_news_scraper import AINewsScraper

class Command(BaseCommand):
    help = 'Test the AI-powered news scraper and compare with traditional scraper'

    def add_arguments(self, parser):
        parser.add_argument(
            '--category',
            type=str,
            default='ai',
            help='Category to test (ai, tech, business, general)'
        )
        parser.add_argument(
            '--limit',
            type=int,
            default=3,
            help='Number of articles to fetch'
        )

    def handle(self, *args, **options):
        category = options['category']
        limit = options['limit']

        self.stdout.write(
            self.style.SUCCESS('🤖 Testing AI-Powered News Scraper')
        )
        self.stdout.write('=' * 50)

        # Test AI scraper
        ai_scraper = AINewsScraper()
        
        self.stdout.write(f'\n1. Testing AI-enhanced trending topics ({category} category):')
        ai_topics = ai_scraper.get_trending_topics(category=category, limit=limit)
        
        for i, topic in enumerate(ai_topics, 1):
            self.stdout.write(f'\n   {i}. {topic.get("title", "No title")}')
            self.stdout.write(f'      Source: {topic.get("source", "Unknown")}')
            self.stdout.write(f'      Quality Score: {topic.get("quality_score", 0):.2f}')
            self.stdout.write(f'      Sentiment: {topic.get("sentiment", "unknown")}')
            self.stdout.write(f'      Keywords: {", ".join(topic.get("keywords", [])[:5])}')
            self.stdout.write(f'      Topics: {", ".join(topic.get("topics", []))}')
            self.stdout.write(f'      Reading Time: {topic.get("reading_time", 0)} min')
            self.stdout.write(f'      Word Count: {topic.get("word_count", 0)}')
            
            # Show enhanced summary
            summary = topic.get('summary', '')
            if summary:
                self.stdout.write(f'      Summary: {summary[:150]}...')

        # Test site-specific topics
        self.stdout.write('\n2. Testing site-specific topic relevance:')
        site_description = "AI and machine learning news, tutorials, and insights for developers"
        site_topics = ai_scraper.get_site_specific_topics(site_description, limit=limit)
        
        for i, topic in enumerate(site_topics, 1):
            self.stdout.write(f'\n   {i}. {topic.get("title", "No title")}')
            self.stdout.write(f'      Relevance Score: {topic.get("relevance_score", 0):.2f}')
            self.stdout.write(f'      Quality Score: {topic.get("quality_score", 0):.2f}')
            self.stdout.write(f'      Source: {topic.get("source", "Unknown")}')

        self.stdout.write('\n' + '=' * 50)
        self.stdout.write(
            self.style.SUCCESS('✅ AI Scraper Test Completed!')
        )
        self.stdout.write('\nKey Improvements:')
        self.stdout.write('• Intelligent content extraction with multiple fallback methods')
        self.stdout.write('• Quality scoring based on content length, source credibility, etc.')
        self.stdout.write('• Sentiment analysis and keyword extraction')
        self.stdout.write('• Topic classification and entity recognition')
        self.stdout.write('• Semantic duplicate detection')
        self.stdout.write('• Relevance scoring for site-specific content')
        self.stdout.write('• Enhanced summaries using AI-powered sentence scoring') 