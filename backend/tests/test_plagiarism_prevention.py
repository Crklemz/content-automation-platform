#!/usr/bin/env python3
"""
Test script for plagiarism prevention and source attribution system
Demonstrates how the system ensures proper attribution and prevents plagiarism
"""

import sys
import os
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

from services.plagiarism_prevention import PlagiarismPrevention
from services.ai_news_scraper import AINewsScraper

def test_plagiarism_prevention():
    """Test the plagiarism prevention system"""
    print("🛡️ Testing Plagiarism Prevention System")
    print("=" * 60)
    
    # Initialize the plagiarism prevention system
    plagiarism_checker = PlagiarismPrevention()
    
    # Test 1: Sample sources
    print("\n1. Testing with sample sources:")
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
    
    # Test 2: Original content (should pass)
    print("\n2. Testing original content:")
    original_content = """
    <h2>The Future of AI in Technology</h2>
    <p>Artificial intelligence continues to transform various industries, bringing unprecedented opportunities and challenges. In healthcare, AI systems are demonstrating remarkable capabilities in diagnostic accuracy, often outperforming traditional methods.</p>
    
    <p>Software development has also seen significant AI integration, with machine learning algorithms automating complex tasks like code generation and quality assurance. This technological advancement is reshaping how developers approach their work.</p>
    
    <p>As we look toward the future, the integration of AI across different sectors promises to create more efficient, accurate, and innovative solutions for complex problems.</p>
    """
    
    analysis = plagiarism_checker.analyze_content_for_plagiarism(original_content, sample_sources)
    
    print(f"   Is Original: {analysis['is_original']}")
    print(f"   Similarity Score: {analysis['similarity_score']:.3f}")
    print(f"   Confidence Score: {analysis['confidence_score']:.3f}")
    print(f"   Recommendations: {analysis['recommendations']}")
    
    # Test 3: Plagiarized content (should fail)
    print("\n3. Testing plagiarized content:")
    plagiarized_content = """
    <h2>AI Breakthrough in Healthcare</h2>
    <p>Artificial intelligence has made significant breakthroughs in healthcare, particularly in medical diagnosis and treatment planning. Recent studies show that AI systems can now detect diseases with higher accuracy than human doctors in many cases.</p>
    
    <p>Machine learning is revolutionizing software development by automating code generation, bug detection, and testing processes. Developers are increasingly using AI-powered tools to improve productivity and code quality.</p>
    """
    
    analysis = plagiarism_checker.analyze_content_for_plagiarism(plagiarized_content, sample_sources)
    
    print(f"   Is Original: {analysis['is_original']}")
    print(f"   Similarity Score: {analysis['similarity_score']:.3f}")
    print(f"   Confidence Score: {analysis['confidence_score']:.3f}")
    print(f"   Suspicious Sections: {len(analysis['suspicious_sections'])}")
    print(f"   Recommendations: {analysis['recommendations']}")
    
    # Test 4: Source quality validation
    print("\n4. Testing source quality validation:")
    quality_analysis = plagiarism_checker.validate_source_quality(sample_sources)
    
    print(f"   Overall Quality: {quality_analysis['overall_quality']:.3f}")
    print(f"   Credible Sources: {quality_analysis['credible_sources']}")
    print(f"   Recent Sources: {quality_analysis['recent_sources']}")
    print(f"   Diverse Sources: {quality_analysis['diverse_sources']}")
    print(f"   Recommendations: {quality_analysis['recommendations']}")
    
    # Test 5: Enhanced content with attribution
    print("\n5. Testing enhanced content with attribution:")
    enhanced_content = plagiarism_checker.enhance_content_with_attribution(original_content, sample_sources)
    
    print("   Enhanced content includes proper attribution section")
    print("   Attribution section preview:")
    attribution_start = enhanced_content.find('<div class="sources-section">')
    if attribution_start != -1:
        attribution_preview = enhanced_content[attribution_start:attribution_start + 200] + "..."
        print(f"   {attribution_preview}")
    
    # Test 6: Source attribution analysis
    print("\n6. Testing source attribution analysis:")
    attribution_analysis = analysis['source_attribution']
    
    for i, attr in enumerate(attribution_analysis, 1):
        print(f"   Source {i}: {attr['source']}")
        print(f"      Title mentioned: {attr['title_mentioned']}")
        print(f"      Source mentioned: {attr['source_mentioned']}")
        print(f"      Needs attribution: {attr['needs_attribution']}")
        print(f"      Suspicious patterns: {attr['suspicious_patterns']}")
    
    # Test 7: Real-world test with AI scraper
    print("\n7. Testing with real AI scraper sources:")
    try:
        ai_scraper = AINewsScraper()
        real_sources = ai_scraper.get_trending_topics(category='ai', limit=2)
        
        if real_sources:
            print(f"   Found {len(real_sources)} real sources")
            
            # Test with real sources
            real_analysis = plagiarism_checker.analyze_content_for_plagiarism(original_content, real_sources)
            print(f"   Real sources analysis - Is Original: {real_analysis['is_original']}")
            print(f"   Real sources analysis - Similarity Score: {real_analysis['similarity_score']:.3f}")
            
            # Test source quality with real sources
            real_quality = plagiarism_checker.validate_source_quality(real_sources)
            print(f"   Real sources quality: {real_quality['overall_quality']:.3f}")
        else:
            print("   No real sources found")
    except Exception as e:
        print(f"   Error testing with real sources: {e}")
    
    print("\n" + "=" * 60)
    print("✅ Plagiarism Prevention Test Completed!")
    print("\nKey Features Demonstrated:")
    print("• Content similarity analysis")
    print("• Source attribution validation")
    print("• Source quality assessment")
    print("• Automatic attribution enhancement")
    print("• Plagiarism detection with confidence scoring")
    print("• Comprehensive recommendations for improvement")

if __name__ == "__main__":
    test_plagiarism_prevention() 