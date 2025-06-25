from django.core.management.base import BaseCommand
from services.plagiarism_prevention import PlagiarismPrevention
from services.ai_news_scraper import AINewsScraper

class Command(BaseCommand):
    help = 'Test the plagiarism prevention and source attribution system'

    def add_arguments(self, parser):
        parser.add_argument(
            '--test-type',
            type=str,
            choices=['basic', 'ai-sources', 'full'],
            default='basic',
            help='Type of test to run (basic, ai-sources, full)'
        )

    def handle(self, *args, **options):
        test_type = options['test_type']
        
        self.stdout.write(
            self.style.SUCCESS('🛡️ Testing Plagiarism Prevention System')
        )
        self.stdout.write('=' * 60)
        
        # Initialize the plagiarism prevention system
        plagiarism_checker = PlagiarismPrevention()
        
        if test_type in ['basic', 'full']:
            self._test_basic_functionality(plagiarism_checker)
        
        if test_type in ['ai-sources', 'full']:
            self._test_with_ai_sources(plagiarism_checker)
        
        self.stdout.write('\n' + '=' * 60)
        self.stdout.write(
            self.style.SUCCESS('✅ Plagiarism Prevention Test Completed!')
        )
    
    def _test_basic_functionality(self, plagiarism_checker):
        """Test basic plagiarism prevention functionality"""
        self.stdout.write('\n1. Testing basic functionality:')
        
        # Sample sources
        sample_sources = [
            {
                'title': 'AI Breakthrough in Healthcare',
                'content': 'Artificial intelligence has made significant breakthroughs in healthcare, particularly in medical diagnosis and treatment planning. Recent studies show that AI systems can now detect diseases with higher accuracy than human doctors in many cases.',
                'url': 'https://techcrunch.com/ai-healthcare-breakthrough',
                'source': 'TechCrunch',
                'published': '2024-01-15'
            },
            {
                'title': 'Machine Learning in Software Development',
                'content': 'Machine learning is revolutionizing software development by automating code generation, bug detection, and testing processes. Developers are increasingly using AI-powered tools to improve productivity and code quality.',
                'url': 'https://wired.com/ml-software-development',
                'source': 'Wired',
                'published': '2024-01-10'
            }
        ]
        
        # Test original content
        self.stdout.write('\n   Testing original content:')
        original_content = """
        <h2>The Future of AI in Technology</h2>
        <p>Artificial intelligence continues to transform various industries, bringing unprecedented opportunities and challenges. In healthcare, AI systems are demonstrating remarkable capabilities in diagnostic accuracy, often outperforming traditional methods.</p>
        
        <p>Software development has also seen significant AI integration, with machine learning algorithms automating complex tasks like code generation and quality assurance. This technological advancement is reshaping how developers approach their work.</p>
        """
        
        analysis = plagiarism_checker.analyze_content_for_plagiarism(original_content, sample_sources)
        
        self.stdout.write(f'   Is Original: {analysis["is_original"]}')
        self.stdout.write(f'   Similarity Score: {analysis["similarity_score"]:.3f}')
        self.stdout.write(f'   Confidence Score: {analysis["confidence_score"]:.3f}')
        
        # Test plagiarized content
        self.stdout.write('\n   Testing plagiarized content:')
        plagiarized_content = """
        <h2>AI Breakthrough in Healthcare</h2>
        <p>Artificial intelligence has made significant breakthroughs in healthcare, particularly in medical diagnosis and treatment planning. Recent studies show that AI systems can now detect diseases with higher accuracy than human doctors in many cases.</p>
        """
        
        analysis = plagiarism_checker.analyze_content_for_plagiarism(plagiarized_content, sample_sources)
        
        self.stdout.write(f'   Is Original: {analysis["is_original"]}')
        self.stdout.write(f'   Similarity Score: {analysis["similarity_score"]:.3f}')
        self.stdout.write(f'   Suspicious Sections: {len(analysis["suspicious_sections"])}')
        
        # Test source quality
        self.stdout.write('\n   Testing source quality validation:')
        quality_analysis = plagiarism_checker.validate_source_quality(sample_sources)
        
        self.stdout.write(f'   Overall Quality: {quality_analysis["overall_quality"]:.3f}')
        self.stdout.write(f'   Credible Sources: {quality_analysis["credible_sources"]}')
        self.stdout.write(f'   Recent Sources: {quality_analysis["recent_sources"]}')
        self.stdout.write(f'   Diverse Sources: {quality_analysis["diverse_sources"]}')
        
        # Test enhanced content
        self.stdout.write('\n   Testing enhanced content with attribution:')
        enhanced_content = plagiarism_checker.enhance_content_with_attribution(original_content, sample_sources)
        
        if '<div class="sources-section">' in enhanced_content:
            self.stdout.write(self.style.SUCCESS('   ✅ Attribution section added successfully'))
        else:
            self.stdout.write(self.style.WARNING('   ⚠️ Attribution section not found'))
    
    def _test_with_ai_sources(self, plagiarism_checker):
        """Test with real AI scraper sources"""
        self.stdout.write('\n2. Testing with AI scraper sources:')
        
        try:
            ai_scraper = AINewsScraper()
            real_sources = ai_scraper.get_trending_topics(category='ai', limit=3)
            
            if real_sources:
                self.stdout.write(f'   Found {len(real_sources)} real sources')
                
                # Test source quality with real sources
                quality_analysis = plagiarism_checker.validate_source_quality(real_sources)
                self.stdout.write(f'   Source Quality: {quality_analysis["overall_quality"]:.3f}')
                self.stdout.write(f'   Credible Sources: {quality_analysis["credible_sources"]}')
                self.stdout.write(f'   Recent Sources: {quality_analysis["recent_sources"]}')
                
                # Test with sample content
                test_content = """
                <h2>AI Technology Trends</h2>
                <p>Artificial intelligence continues to evolve rapidly, with new applications emerging across various industries. The technology is becoming more accessible and practical for everyday use.</p>
                """
                
                analysis = plagiarism_checker.analyze_content_for_plagiarism(test_content, real_sources)
                self.stdout.write(f'   Content Analysis - Is Original: {analysis["is_original"]}')
                self.stdout.write(f'   Content Analysis - Similarity Score: {analysis["similarity_score"]:.3f}')
                
                # Show source details
                self.stdout.write('\n   Source Details:')
                for i, source in enumerate(real_sources, 1):
                    self.stdout.write(f'   {i}. {source.get("title", "Unknown")} - {source.get("source", "Unknown")}')
                    self.stdout.write(f'      Quality Score: {source.get("quality_score", 0):.2f}')
                    self.stdout.write(f'      Sentiment: {source.get("sentiment", "unknown")}')
            else:
                self.stdout.write(self.style.WARNING('   No real sources found'))
                
        except Exception as e:
            self.stdout.write(
                self.style.ERROR(f'   Error testing with AI sources: {e}')
            ) 