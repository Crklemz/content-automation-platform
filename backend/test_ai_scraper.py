#!/usr/bin/env python3
"""
Test script for AI-powered news scraper
Demonstrates advanced content extraction and analysis capabilities
"""

import sys
import os
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

from services.ai_news_scraper import AINewsScraper

def test_ai_scraper():
    """Test the AI-powered news scraper"""
    print("🤖 Testing AI-Powered News Scraper")
    print("=" * 50)
    
    scraper = AINewsScraper()
    
    # Test 1: Get AI-enhanced trending topics
    print("\n1. Testing AI-enhanced trending topics (AI category):")
    ai_topics = scraper.get_trending_topics(category='ai', limit=3)
    
    for i, topic in enumerate(ai_topics, 1):
        print(f"\n   {i}. {topic.get('title', 'No title')}")
        print(f"      Source: {topic.get('source', 'Unknown')}")
        print(f"      Quality Score: {topic.get('quality_score', 0):.2f}")
        print(f"      Sentiment: {topic.get('sentiment', 'unknown')}")
        print(f"      Keywords: {', '.join(topic.get('keywords', [])[:5])}")
        print(f"      Topics: {', '.join(topic.get('topics', []))}")
        print(f"      Reading Time: {topic.get('reading_time', 0)} min")
        print(f"      Word Count: {topic.get('word_count', 0)}")
        
        # Show enhanced summary
        summary = topic.get('summary', '')
        if summary:
            print(f"      Summary: {summary[:150]}...")
    
    # Test 2: Get site-specific topics
    print("\n2. Testing site-specific topic relevance:")
    site_description = "AI and machine learning news, tutorials, and insights for developers"
    site_topics = scraper.get_site_specific_topics(site_description, limit=3)
    
    for i, topic in enumerate(site_topics, 1):
        print(f"\n   {i}. {topic.get('title', 'No title')}")
        print(f"      Relevance Score: {topic.get('relevance_score', 0):.2f}")
        print(f"      Quality Score: {topic.get('quality_score', 0):.2f}")
        print(f"      Source: {topic.get('source', 'Unknown')}")
    
    # Test 3: Test article summary extraction (if we have a URL)
    if ai_topics and ai_topics[0].get('url'):
        print("\n3. Testing AI-enhanced article summary:")
        url = ai_topics[0]['url']
        print(f"   URL: {url}")
        
        try:
            summary = scraper.get_article_summary(url)
            if summary:
                print(f"   Title: {summary.get('title', 'No title')}")
                print(f"   Quality Score: {summary.get('quality_score', 0):.2f}")
                print(f"   Sentiment: {summary.get('sentiment', 'unknown')}")
                print(f"   Keywords: {', '.join(summary.get('keywords', [])[:5])}")
                print(f"   Topics: {', '.join(summary.get('topics', []))}")
                print(f"   Entities: {', '.join(summary.get('entities', [])[:5])}")
                print(f"   Reading Time: {summary.get('reading_time', 0)} min")
                print(f"   Word Count: {summary.get('word_count', 0)}")
                
                # Show AI-generated summary
                ai_summary = summary.get('summary', '')
                if ai_summary:
                    print(f"   AI Summary: {ai_summary[:200]}...")
            else:
                print("   Failed to get summary")
        except Exception as e:
            print(f"   Error: {e}")
    
    # Test 4: Compare with old scraper
    print("\n4. Comparing AI scraper with traditional scraper:")
    from services.news_scraper import NewsScraper
    
    old_scraper = NewsScraper()
    old_topics = old_scraper.get_trending_topics(category='ai', limit=2)
    
    print("\n   Traditional Scraper Results:")
    for i, topic in enumerate(old_topics, 1):
        print(f"   {i}. {topic.get('title', 'No title')}")
        print(f"      Source: {topic.get('source', 'Unknown')}")
        print(f"      Description: {topic.get('description', 'No description')[:100]}...")
    
    print("\n   AI Scraper Results:")
    for i, topic in enumerate(ai_topics[:2], 1):
        print(f"   {i}. {topic.get('title', 'No title')}")
        print(f"      Source: {topic.get('source', 'Unknown')}")
        print(f"      Quality: {topic.get('quality_score', 0):.2f}")
        print(f"      Sentiment: {topic.get('sentiment', 'unknown')}")
        print(f"      Keywords: {', '.join(topic.get('keywords', [])[:3])}")
    
    print("\n" + "=" * 50)
    print("✅ AI Scraper Test Completed!")
    print("\nKey Improvements:")
    print("• Intelligent content extraction with multiple fallback methods")
    print("• Quality scoring based on content length, source credibility, etc.")
    print("• Sentiment analysis and keyword extraction")
    print("• Topic classification and entity recognition")
    print("• Semantic duplicate detection")
    print("• Relevance scoring for site-specific content")
    print("• Enhanced summaries using AI-powered sentence scoring")

if __name__ == "__main__":
    test_ai_scraper() 