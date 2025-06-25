import re
import hashlib
from typing import List, Dict, Optional, Tuple
from difflib import SequenceMatcher
from collections import defaultdict
import json
from datetime import datetime

class PlagiarismPrevention:
    """Comprehensive plagiarism prevention and source attribution system"""
    
    def __init__(self):
        # Common phrases that might indicate copying
        self.suspicious_patterns = [
            r'\baccording to\b',
            r'\bas reported by\b',
            r'\bsaid\b',
            r'\bannounced\b',
            r'\breleased\b',
            r'\bconfirmed\b',
            r'\bdeclared\b'
        ]
        
        # Minimum similarity threshold for plagiarism detection
        self.similarity_threshold = 0.8
        
        # Minimum sentence length to check
        self.min_sentence_length = 20
        
    def analyze_content_for_plagiarism(self, generated_content: str, sources: List[Dict]) -> Dict:
        """
        Analyze generated content for potential plagiarism
        
        Args:
            generated_content: The generated article content
            sources: List of source articles used for generation
            
        Returns:
            Dict containing plagiarism analysis results
        """
        analysis = {
            'is_original': True,
            'similarity_score': 0.0,
            'suspicious_sections': [],
            'source_attribution': [],
            'recommendations': [],
            'confidence_score': 0.0
        }
        
        try:
            # Check for direct copying from sources
            max_similarity = 0.0
            suspicious_sections = []
            
            for source in sources:
                source_content = source.get('content', '') or source.get('description', '')
                if source_content:
                    similarity = self._calculate_content_similarity(generated_content, source_content)
                    max_similarity = max(max_similarity, similarity)
                    
                    if similarity > self.similarity_threshold:
                        suspicious_sections.append({
                            'source': source.get('title', 'Unknown'),
                            'similarity': similarity,
                            'url': source.get('url', ''),
                            'source_name': source.get('source', 'Unknown')
                        })
            
            analysis['similarity_score'] = max_similarity
            analysis['suspicious_sections'] = suspicious_sections
            
            # Check for proper source attribution
            attribution_analysis = self._check_source_attribution(generated_content, sources)
            analysis['source_attribution'] = attribution_analysis
            
            # Determine if content is original
            analysis['is_original'] = max_similarity < self.similarity_threshold
            
            # Calculate confidence score
            analysis['confidence_score'] = self._calculate_confidence_score(analysis)
            
            # Generate recommendations
            analysis['recommendations'] = self._generate_recommendations(analysis)
            
        except Exception as e:
            print(f"Error in plagiarism analysis: {e}")
            analysis['is_original'] = False
            analysis['recommendations'].append("Error occurred during analysis - manual review recommended")
        
        return analysis
    
    def enhance_content_with_attribution(self, content: str, sources: List[Dict]) -> str:
        """
        Enhance content with proper source attribution
        
        Args:
            content: The generated content
            sources: List of sources used
            
        Returns:
            Enhanced content with proper attribution
        """
        if not sources:
            return content
        
        # Create attribution section
        attribution_section = self._create_attribution_section(sources)
        
        # Add inline citations if needed
        enhanced_content = self._add_inline_citations(content, sources)
        
        # Append attribution section
        enhanced_content += f"\n\n{attribution_section}"
        
        return enhanced_content
    
    def validate_source_quality(self, sources: List[Dict]) -> Dict:
        """
        Validate the quality and credibility of sources
        
        Args:
            sources: List of source articles
            
        Returns:
            Dict containing source quality analysis
        """
        quality_analysis = {
            'overall_quality': 0.0,
            'credible_sources': 0,
            'recent_sources': 0,
            'diverse_sources': 0,
            'recommendations': []
        }
        
        if not sources:
            quality_analysis['recommendations'].append("No sources provided - manual review required")
            return quality_analysis
        
        credible_domains = {
            'techcrunch.com', 'wired.com', 'arstechnica.com', 'theverge.com', 
            'venturebeat.com', 'reuters.com', 'bloomberg.com', 'wsj.com',
            'nytimes.com', 'washingtonpost.com', 'bbc.com', 'cnn.com'
        }
        
        source_domains = set()
        recent_sources = 0
        credible_sources = 0
        
        for source in sources:
            # Check domain credibility
            domain = self._extract_domain(source.get('url', ''))
            if domain in credible_domains:
                credible_sources += 1
            
            source_domains.add(domain)
            
            # Check recency (within last 30 days)
            published = source.get('published', '')
            if self._is_recent_source(published):
                recent_sources += 1
        
        quality_analysis['credible_sources'] = credible_sources
        quality_analysis['recent_sources'] = recent_sources
        quality_analysis['diverse_sources'] = len(source_domains)
        
        # Calculate overall quality score
        total_sources = len(sources)
        if total_sources > 0:
            credibility_score = credible_sources / total_sources
            recency_score = recent_sources / total_sources
            diversity_score = min(len(source_domains) / 3, 1.0)  # Cap at 3+ sources
            
            quality_analysis['overall_quality'] = (
                credibility_score * 0.4 + 
                recency_score * 0.3 + 
                diversity_score * 0.3
            )
        
        # Generate recommendations
        if quality_analysis['overall_quality'] < 0.6:
            quality_analysis['recommendations'].append("Consider adding more credible sources")
        
        if quality_analysis['recent_sources'] < len(sources) * 0.5:
            quality_analysis['recommendations'].append("Consider adding more recent sources")
        
        if quality_analysis['diverse_sources'] < 2:
            quality_analysis['recommendations'].append("Consider adding sources from different domains")
        
        return quality_analysis
    
    def _calculate_content_similarity(self, content1: str, content2: str) -> float:
        """Calculate similarity between two content pieces"""
        if not content1 or not content2:
            return 0.0
        
        # Clean and normalize content
        content1_clean = self._normalize_text(content1)
        content2_clean = self._normalize_text(content2)
        
        # Use sequence matcher for similarity
        matcher = SequenceMatcher(None, content1_clean, content2_clean)
        return matcher.ratio()
    
    def _normalize_text(self, text: str) -> str:
        """Normalize text for comparison"""
        # Convert to lowercase
        text = text.lower()
        
        # Remove extra whitespace
        text = re.sub(r'\s+', ' ', text)
        
        # Remove punctuation (keep basic structure)
        text = re.sub(r'[^\w\s]', '', text)
        
        return text.strip()
    
    def _check_source_attribution(self, content: str, sources: List[Dict]) -> List[Dict]:
        """Check if content properly attributes sources"""
        attribution_analysis = []
        
        for source in sources:
            source_title = source.get('title', '').lower()
            source_name = source.get('source', '').lower()
            
            # Check for direct mentions
            title_mentioned = source_title in content.lower() if source_title else False
            source_mentioned = source_name in content.lower() if source_name else False
            
            # Check for suspicious patterns
            suspicious_patterns_found = []
            for pattern in self.suspicious_patterns:
                if re.search(pattern, content.lower()):
                    suspicious_patterns_found.append(pattern)
            
            attribution_analysis.append({
                'source': source.get('title', 'Unknown'),
                'url': source.get('url', ''),
                'title_mentioned': title_mentioned,
                'source_mentioned': source_mentioned,
                'suspicious_patterns': suspicious_patterns_found,
                'needs_attribution': not (title_mentioned or source_mentioned)
            })
        
        return attribution_analysis
    
    def _create_attribution_section(self, sources: List[Dict]) -> str:
        """Create a comprehensive attribution section"""
        if not sources:
            return ""
        
        attribution_html = """
        <div class="sources-section">
            <h2>Sources and Further Reading</h2>
            <p>This article was informed by the following sources. We encourage readers to explore these sources for additional information and context.</p>
            <ul class="sources-list">
        """
        
        for i, source in enumerate(sources, 1):
            title = source.get('title', 'Unknown Source')
            url = source.get('url', '#')
            source_name = source.get('source', 'Unknown')
            published = source.get('published', '')
            
            # Format publication date if available
            date_str = ""
            if published:
                try:
                    # Try to parse and format the date
                    if isinstance(published, str):
                        date_str = f" - {published[:10]}"  # First 10 chars for date
                except:
                    pass
            
            attribution_html += f"""
                <li class="source-item">
                    <a href="{url}" target="_blank" rel="noopener noreferrer" class="source-link">
                        {title}
                    </a>
                    <span class="source-meta"> - {source_name}{date_str}</span>
                </li>
            """
        
        attribution_html += """
            </ul>
            <p class="attribution-note">
                <em>Note: This article provides original analysis and insights based on the information from the sources listed above. 
                We strive to create unique, valuable content while properly attributing our sources.</em>
            </p>
        </div>
        """
        
        return attribution_html
    
    def _add_inline_citations(self, content: str, sources: List[Dict]) -> str:
        """Add inline citations to content where appropriate"""
        if not sources:
            return content
        
        # Simple inline citation system
        # This could be enhanced with more sophisticated citation detection
        
        # Add source references in parentheses where appropriate
        enhanced_content = content
        
        for i, source in enumerate(sources, 1):
            source_name = source.get('source', 'Unknown')
            # Add citation markers for key information
            # This is a simplified approach - could be enhanced with NLP
            
        return enhanced_content
    
    def _extract_domain(self, url: str) -> str:
        """Extract domain from URL"""
        if not url:
            return ""
        
        # Simple domain extraction
        domain = url.replace('http://', '').replace('https://', '').replace('www.', '')
        return domain.split('/')[0] if '/' in domain else domain
    
    def _is_recent_source(self, published: str) -> bool:
        """Check if source is recent (within 30 days)"""
        if not published:
            return False
        
        try:
            # Try to parse the published date
            if isinstance(published, str):
                # Handle ISO format dates
                if 'T' in published:
                    published = published.split('T')[0]
                
                # Simple date parsing (could be enhanced)
                from datetime import datetime, timedelta
                pub_date = datetime.strptime(published[:10], '%Y-%m-%d')
                thirty_days_ago = datetime.now() - timedelta(days=30)
                
                return pub_date > thirty_days_ago
        except:
            pass
        
        return False
    
    def _calculate_confidence_score(self, analysis: Dict) -> float:
        """Calculate confidence score for the analysis"""
        confidence = 1.0
        
        # Reduce confidence for high similarity
        if analysis['similarity_score'] > 0.5:
            confidence -= 0.3
        
        # Reduce confidence for missing attributions
        missing_attributions = sum(1 for attr in analysis['source_attribution'] if attr.get('needs_attribution', False))
        if missing_attributions > 0:
            confidence -= 0.2
        
        # Reduce confidence for suspicious sections
        if analysis['suspicious_sections']:
            confidence -= 0.2
        
        return max(0.0, confidence)
    
    def _generate_recommendations(self, analysis: Dict) -> List[str]:
        """Generate recommendations based on analysis"""
        recommendations = []
        
        if analysis['similarity_score'] > 0.8:
            recommendations.append("High similarity detected - consider rewriting to be more original")
        elif analysis['similarity_score'] > 0.6:
            recommendations.append("Moderate similarity detected - review for potential copying")
        
        missing_attributions = sum(1 for attr in analysis['source_attribution'] if attr.get('needs_attribution', False))
        if missing_attributions > 0:
            recommendations.append(f"Add attribution for {missing_attributions} source(s)")
        
        if analysis['suspicious_sections']:
            recommendations.append("Review sections with high similarity to sources")
        
        if not recommendations:
            recommendations.append("Content appears to be original with proper attribution")
        
        return recommendations
    
    def create_source_summary(self, sources: List[Dict]) -> str:
        """Create a summary of sources used"""
        if not sources:
            return "No sources were used in the creation of this content."
        
        summary_parts = [f"This content was informed by {len(sources)} source(s):"]
        
        for i, source in enumerate(sources, 1):
            title = source.get('title', 'Unknown')
            source_name = source.get('source', 'Unknown')
            url = source.get('url', '')
            
            summary_parts.append(f"{i}. {title} ({source_name})")
            if url:
                summary_parts.append(f"   URL: {url}")
        
        return "\n".join(summary_parts) 