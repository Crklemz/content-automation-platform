'use client';

import { useState, useEffect } from 'react';
import ProtectedRoute from '../ProtectedRoute';
import { Site } from '@/types/admin';
import { createHeaders } from '@/lib/auth';

interface TrendingTopic {
  title: string;
  description: string;
  category: string;
  source?: string;
  url?: string;
  topics?: string[];
}

interface ArticleSection {
  type: 'heading' | 'paragraph' | 'list' | 'metadata';
  level?: number;
  content: string;
  url?: string;
  style?: 'unordered' | 'ordered';
  items?: Array<{
    type: 'list_item';
    content: string;
    url?: string;
  }>;
  category?: string;
  source?: string;
}

interface StructuredArticleData {
  title: string;
  sections: ArticleSection[];
  sources: Array<{
    title: string;
    url: string;
    source: string;
  }>;
  status: string;
  plagiarism_analysis: any;
  source_quality: any;
  is_original: boolean;
  confidence_score: number;
}

export default function AIContentPage() {
  const [sites, setSites] = useState<Site[]>([]);
  const [selectedSite, setSelectedSite] = useState('');
  const [topics, setTopics] = useState<TrendingTopic[]>([]);
  const [isLoading, setIsLoading] = useState(false);
  const [isGenerating, setIsGenerating] = useState(false);
  const [message, setMessage] = useState('');
  const [customTopic, setCustomTopic] = useState('');
  const [generatedArticle, setGeneratedArticle] = useState<StructuredArticleData | null>(null);

  useEffect(() => {
    fetchSites();
  }, []);

  const fetchSites = async () => {
    try {
      const response = await fetch('http://localhost:8000/api/sites/', {
        credentials: 'include'
      });
      const data = await response.json();
      setSites(data.results || data);
    } catch (error) {
      console.error('Error fetching sites:', error);
    }
  };

  const fetchTrendingTopics = async () => {
    if (!selectedSite) return;
    
    setIsLoading(true);
    try {
      const response = await fetch(
        `http://localhost:8000/api/articles/trending_topics/?site_slug=${selectedSite}&limit=3`,
        {
          credentials: 'include'
        }
      );
      const data = await response.json();
      setTopics(data.topics || []);
    } catch (error) {
      console.error('Error fetching topics:', error);
      setMessage('Error fetching trending topics');
    } finally {
      setIsLoading(false);
    }
  };

  const generateStructuredContent = async (topic?: string) => {
    if (!selectedSite) {
      setMessage('Please select a site first');
      return;
    }

    setIsGenerating(true);
    setMessage('');
    setGeneratedArticle(null);

    try {
      const payload: { site_slug: string; count: number; topic?: string } = {
        site_slug: selectedSite,
        count: 1
      };

      if (topic) {
        payload.topic = topic;
      }

      const response = await fetch('http://localhost:8000/api/articles/generate_structured_content/', {
        method: 'POST',
        headers: createHeaders(),
        body: JSON.stringify(payload),
        credentials: 'include'
      });

      const data = await response.json();

      if (response.ok) {
        setMessage(`✅ ${data.message}`);
        setGeneratedArticle(data.article_data);
        
        // Save the generated content as an actual article
        await saveGeneratedArticle(data.article_data);
        
        // Refresh topics after generation
        fetchTrendingTopics();
      } else {
        setMessage(`❌ Error: ${data.error}`);
      }
    } catch (error) {
      setMessage('❌ Error generating content');
    } finally {
      setIsGenerating(false);
    }
  };

  const generateDailyTop3 = async () => {
    if (!selectedSite) {
      setMessage('Please select a site first');
      return;
    }

    if (topics.length < 3) {
      setMessage('Please refresh topics to get 3 trending topics for Daily Top 3');
      return;
    }

    setIsGenerating(true);
    setMessage('');
    setGeneratedArticle(null);

    try {
      const response = await fetch('http://localhost:8000/api/articles/generate_structured_content/', {
        method: 'POST',
        headers: createHeaders(),
        body: JSON.stringify({
          site_slug: selectedSite,
          count: 3
        }),
        credentials: 'include'
      });

      const data = await response.json();

      if (response.ok) {
        setMessage(`✅ ${data.message}`);
        setGeneratedArticle(data.article_data);
        
        // Save the generated content as an actual article
        await saveGeneratedArticle(data.article_data);
        
        // Refresh topics after generation
        fetchTrendingTopics();
      } else {
        setMessage(`❌ Error: ${data.error}`);
      }
    } catch (error) {
      setMessage('❌ Error generating Daily Top 3 content');
    } finally {
      setIsGenerating(false);
    }
  };

  const saveGeneratedArticle = async (articleData: StructuredArticleData) => {
    try {
      // Convert structured data to HTML for storage
      const bodyHtml = convertSectionsToHtml(articleData.sections);
      
      // Create slug from title
      const slug = createSlug(articleData.title);
      
      const response = await fetch('http://localhost:8000/api/articles/', {
        method: 'POST',
        headers: createHeaders(),
        body: JSON.stringify({
          title: articleData.title,
          body: bodyHtml,
          slug: slug,
          site: selectedSite,
          status: 'pending',
          sources: articleData.sources
        }),
        credentials: 'include'
      });

      if (response.ok) {
        const savedArticle = await response.json();
        setMessage(prev => `${prev} - Article saved with ID: ${savedArticle.id}`);
      } else {
        const errorData = await response.json();
        console.error('Save article error:', errorData);
        setMessage(prev => `${prev} - Warning: Could not save article: ${errorData.error || 'Unknown error'}`);
      }
    } catch (error) {
      console.error('Save article error:', error);
      setMessage(prev => `${prev} - Warning: Could not save article: ${error}`);
    }
  };

  const convertSectionsToHtml = (sections: ArticleSection[]): string => {
    const htmlParts: string[] = [];
    
    for (const section of sections) {
      switch (section.type) {
        case 'heading':
          const level = section.level || 2;
          const headingClasses = level === 1 ? 'text-3xl font-bold mb-6' :
                                level === 2 ? 'text-2xl font-bold mb-4' :
                                level === 3 ? 'text-xl font-bold mb-3' :
                                'text-lg font-bold mb-2';
          
          if (section.url) {
            htmlParts.push(`<h${level} class="${headingClasses}"><a href="${section.url}" target="_blank" rel="noopener noreferrer" class="text-blue-600 hover:text-blue-800 underline">${section.content}</a></h${level}>`);
          } else {
            htmlParts.push(`<h${level} class="${headingClasses}">${section.content}</h${level}>`);
          }
          break;
          
        case 'paragraph':
          htmlParts.push(`<p class="mb-4 text-gray-700 leading-relaxed">${section.content}</p>`);
          break;
          
        case 'list':
          const listTag = section.style === 'ordered' ? 'ol' : 'ul';
          const listClasses = section.style === 'ordered' ? 'list-decimal ml-6 mb-4' : 'list-disc ml-6 mb-4';
          const listItems = section.items?.map(item => {
            if (item.url) {
              return `<li class="mb-2"><a href="${item.url}" target="_blank" rel="noopener noreferrer" class="text-blue-600 hover:text-blue-800 underline">${item.content}</a></li>`;
            }
            return `<li class="mb-2">${item.content}</li>`;
          }).join('') || '';
          htmlParts.push(`<${listTag} class="${listClasses}">${listItems}</${listTag}>`);
          break;
          
        case 'metadata':
          let metaHtml = '<div class="mb-4 p-3 bg-gray-50 rounded-lg">';
          if (section.category) {
            metaHtml += `<span class="inline-block bg-blue-100 text-blue-800 text-xs px-2 py-1 rounded mr-2">${section.category}</span>`;
          }
          if (section.source) {
            if (section.url) {
              metaHtml += `<span class="text-sm text-gray-600">Source: <a href="${section.url}" target="_blank" rel="noopener noreferrer" class="text-blue-600 hover:text-blue-800 underline">${section.source}</a></span>`;
            } else {
              metaHtml += `<span class="text-sm text-gray-600">Source: ${section.source}</span>`;
            }
          }
          metaHtml += '</div>';
          htmlParts.push(metaHtml);
          break;
      }
    }
    
    return htmlParts.join('\n');
  };

  const createSlug = (title: string): string => {
    const baseSlug = title
      .toLowerCase()
      .replace(/[^\w\s-]/g, '')
      .replace(/[-\s]+/g, '-')
      .trim()
      .replace(/^-+|-+$/g, '')
      .substring(0, 150); // Leave room for timestamp
    
    // Add timestamp to ensure uniqueness
    const timestamp = new Date().toISOString().replace(/[^0-9]/g, '').slice(0, 14);
    return `${baseSlug}-${timestamp}`;
  };

  const getMainTopic = (topic: TrendingTopic): string => {
    if (topic.topics && topic.topics.length > 0) {
      return topic.topics[0].replace(/\b\w/g, l => l.toUpperCase());
    }
    return topic.category || 'General';
  };

  const truncateDescription = (description: string, maxLength: number = 200): string => {
    if (description.length <= maxLength) return description;
    return description.substring(0, maxLength).replace(/\s+\S*$/, '') + '...';
  };

  const renderSection = (section: ArticleSection, index: number) => {
    switch (section.type) {
      case 'heading':
        const level = section.level || 2;
        if (section.url) {
          const headingContent = (
            <a 
              href={section.url} 
              target="_blank" 
              rel="noopener noreferrer"
              className="text-blue-600 hover:text-blue-800 underline"
            >
              {section.content}
            </a>
          );
          
          switch (level) {
            case 1:
              return <h1 key={index} className="text-2xl font-bold mb-4">{headingContent}</h1>;
            case 2:
              return <h2 key={index} className="text-xl font-bold mb-4">{headingContent}</h2>;
            case 3:
              return <h3 key={index} className="text-lg font-bold mb-4">{headingContent}</h3>;
            case 4:
              return <h4 key={index} className="text-base font-bold mb-4">{headingContent}</h4>;
            case 5:
              return <h5 key={index} className="text-sm font-bold mb-4">{headingContent}</h5>;
            case 6:
              return <h6 key={index} className="text-xs font-bold mb-4">{headingContent}</h6>;
            default:
              return <h2 key={index} className="text-xl font-bold mb-4">{headingContent}</h2>;
          }
        } else {
          switch (level) {
            case 1:
              return <h1 key={index} className="text-2xl font-bold mb-4">{section.content}</h1>;
            case 2:
              return <h2 key={index} className="text-xl font-bold mb-4">{section.content}</h2>;
            case 3:
              return <h3 key={index} className="text-lg font-bold mb-4">{section.content}</h3>;
            case 4:
              return <h4 key={index} className="text-base font-bold mb-4">{section.content}</h4>;
            case 5:
              return <h5 key={index} className="text-sm font-bold mb-4">{section.content}</h5>;
            case 6:
              return <h6 key={index} className="text-xs font-bold mb-4">{section.content}</h6>;
            default:
              return <h2 key={index} className="text-xl font-bold mb-4">{section.content}</h2>;
          }
        }

      case 'paragraph':
        return (
          <p key={index} className="mb-4 text-gray-700 leading-relaxed">
            {section.content}
          </p>
        );

      case 'list':
        const ListTag = section.style === 'ordered' ? 'ol' : 'ul';
        return (
          <ListTag key={index} className={`mb-4 ${section.style === 'ordered' ? 'list-decimal' : 'list-disc'} ml-6`}>
            {section.items?.map((item, itemIndex) => (
              <li key={itemIndex} className="mb-2">
                {item.url ? (
                  <a 
                    href={item.url} 
                    target="_blank" 
                    rel="noopener noreferrer"
                    className="text-blue-600 hover:text-blue-800 underline"
                  >
                    {item.content}
                  </a>
                ) : (
                  item.content
                )}
              </li>
            ))}
          </ListTag>
        );

      case 'metadata':
        return (
          <div key={index} className="mb-4 p-3 bg-gray-50 rounded-lg">
            {section.category && (
              <span className="inline-block bg-blue-100 text-blue-800 text-xs px-2 py-1 rounded mr-2">
                {section.category}
              </span>
            )}
            {section.source && (
              <span className="text-sm text-gray-600">
                Source: {section.url ? (
                  <a 
                    href={section.url} 
                    target="_blank" 
                    rel="noopener noreferrer"
                    className="text-blue-600 hover:text-blue-800 underline"
                  >
                    {section.source}
                  </a>
                ) : (
                  section.source
                )}
              </span>
            )}
          </div>
        );

      default:
        return null;
    }
  };

  return (
    <ProtectedRoute>
      <div className="space-y-6">
        {/* Page Header */}
        <div>
          <h1 className="text-3xl font-bold text-gray-900">AI Content Generation</h1>
          <p className="mt-2 text-gray-600">
            Generate AI-powered content for your sites using trending topics
          </p>
        </div>

        {/* Site Selection */}
        <div className="bg-white shadow rounded-lg p-6">
          <h2 className="text-lg font-medium text-gray-900 mb-4">Select Site</h2>
          <select
            value={selectedSite}
            onChange={(e) => setSelectedSite(e.target.value)}
            className="block w-full border-gray-300 rounded-md shadow-sm focus:ring-blue-500 focus:border-blue-500 sm:text-sm"
          >
            <option value="">Choose a site...</option>
            {sites.map((site) => (
              <option key={site.id} value={site.slug}>
                {site.name}
              </option>
            ))}
          </select>
        </div>

        {/* Trending Topics */}
        {selectedSite && (
          <div className="bg-white shadow rounded-lg p-6">
            <div className="flex justify-between items-center mb-6">
              <h2 className="text-lg font-medium text-gray-900">Trending Articles (Top 3)</h2>
              <div className="flex gap-2">
                <button
                  onClick={fetchTrendingTopics}
                  disabled={isLoading}
                  className="px-4 py-2 bg-blue-600 text-white rounded-md hover:bg-blue-700 disabled:opacity-50"
                >
                  {isLoading ? 'Loading...' : 'Refresh Articles'}
                </button>
                {topics.length >= 3 && (
                  <button
                    onClick={generateDailyTop3}
                    disabled={isGenerating}
                    className="px-4 py-2 bg-green-600 text-white rounded-md hover:bg-green-700 disabled:opacity-50"
                  >
                    {isGenerating ? 'Generating...' : 'Generate Daily Top 3'}
                  </button>
                )}
              </div>
            </div>

            {topics.length > 0 ? (
              <div className="grid gap-4">
                {topics.slice(0, 3).map((topic, index) => (
                  <div key={index} className="border rounded-lg p-4">
                    <div className="flex justify-between items-start mb-2">
                      <h3 className="font-medium text-gray-900">{topic.title}</h3>
                      <span className="text-xs bg-gray-100 text-gray-600 px-2 py-1 rounded">
                        {getMainTopic(topic)}
                      </span>
                    </div>
                    <p className="text-sm text-gray-600 mb-2">
                      {truncateDescription(topic.description)}
                    </p>
                    <div className="flex justify-between items-center text-xs text-gray-500">
                      <span>{topic.source || 'Unknown source'}</span>
                      {topic.url && (
                        <a
                          href={topic.url}
                          target="_blank"
                          rel="noopener noreferrer"
                          className="text-blue-600 hover:text-blue-800"
                        >
                          Read more →
                        </a>
                      )}
                    </div>
                  </div>
                ))}
              </div>
            ) : (
              <p className="text-gray-500">No trending topics available. Click "Refresh Articles" to load them.</p>
            )}
          </div>
        )}

        {/* Custom Topic Generation */}
        {selectedSite && (
          <div className="bg-white shadow rounded-lg p-6">
            <h2 className="text-lg font-medium text-gray-900 mb-4">Generate Custom Content</h2>
            <div className="flex gap-4">
              <input
                type="text"
                value={customTopic}
                onChange={(e) => setCustomTopic(e.target.value)}
                placeholder="Enter a topic to write about..."
                className="flex-1 border-gray-300 rounded-md shadow-sm focus:ring-blue-500 focus:border-blue-500 sm:text-sm"
              />
              <button
                onClick={() => generateStructuredContent(customTopic)}
                disabled={isGenerating || !customTopic.trim()}
                className="px-4 py-2 bg-purple-600 text-white rounded-md hover:bg-purple-700 disabled:opacity-50"
              >
                {isGenerating ? 'Generating...' : 'Generate Article'}
              </button>
            </div>
          </div>
        )}

        {/* Status Message */}
        {message && (
          <div className={`p-4 rounded-lg ${
            message.startsWith('✅') ? 'bg-green-50 text-green-800' : 'bg-red-50 text-red-800'
          }`}>
            {message}
          </div>
        )}

        {/* Generated Article Preview */}
        {generatedArticle && (
          <div className="bg-white shadow rounded-lg p-6">
            <div className="flex justify-between items-center mb-6">
              <h2 className="text-lg font-medium text-gray-900">Generated Article Preview</h2>
              <div className="flex gap-2 text-sm">
                <span className={`px-2 py-1 rounded ${
                  generatedArticle.is_original 
                    ? 'bg-green-100 text-green-800' 
                    : 'bg-yellow-100 text-yellow-800'
                }`}>
                  {generatedArticle.is_original ? 'Original' : 'Needs Review'}
                </span>
                <span className="bg-blue-100 text-blue-800 px-2 py-1 rounded">
                  {Math.round(generatedArticle.confidence_score * 100)}% Confidence
                </span>
              </div>
            </div>

            <div className="prose max-w-none">
              <h1 className="text-2xl font-bold mb-6">{generatedArticle.title}</h1>
              
              {generatedArticle.sections.map((section, index) => renderSection(section, index))}
              
              {generatedArticle.sources.length > 0 && (
                <div className="mt-8 p-4 bg-gray-50 rounded-lg">
                  <h3 className="font-medium text-gray-900 mb-3">Sources and Further Reading</h3>
                  <ul className="space-y-2">
                    {generatedArticle.sources.map((source, index) => (
                      <li key={index} className="text-sm">
                        <a
                          href={source.url}
                          target="_blank"
                          rel="noopener noreferrer"
                          className="text-blue-600 hover:text-blue-800 underline"
                        >
                          {source.title}
                        </a>
                        {' - '}{source.source}
                      </li>
                    ))}
                  </ul>
                </div>
              )}
            </div>
          </div>
        )}
      </div>
    </ProtectedRoute>
  );
} 