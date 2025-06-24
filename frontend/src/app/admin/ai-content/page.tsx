'use client';

import { useState, useEffect } from 'react';
import ProtectedRoute from '../ProtectedRoute';
import { Site } from '@/types/admin';

interface TrendingTopic {
  title: string;
  description: string;
  category: string;
  source?: string;
}

export default function AIContentPage() {
  const [sites, setSites] = useState<Site[]>([]);
  const [selectedSite, setSelectedSite] = useState('');
  const [topics, setTopics] = useState<TrendingTopic[]>([]);
  const [isLoading, setIsLoading] = useState(false);
  const [isGenerating, setIsGenerating] = useState(false);
  const [message, setMessage] = useState('');
  const [customTopic, setCustomTopic] = useState('');

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
        `http://localhost:8000/api/articles/trending_topics/?site_slug=${selectedSite}&limit=5`
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

  const generateContent = async (topic?: string) => {
    if (!selectedSite) {
      setMessage('Please select a site first');
      return;
    }

    setIsGenerating(true);
    setMessage('');

    try {
      const payload: { site_slug: string; count: number; topic?: string } = {
        site_slug: selectedSite,
        count: 1
      };

      if (topic) {
        payload.topic = topic;
      }

      const response = await fetch('http://localhost:8000/api/articles/generate_content/', {
        method: 'POST',
        headers: {
          'Content-Type': 'application/json',
        },
        body: JSON.stringify(payload)
      });

      const data = await response.json();

      if (response.ok) {
        setMessage(`✅ ${data.message}`);
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
            <div className="flex justify-between items-center mb-4">
              <h2 className="text-lg font-medium text-gray-900">Trending Topics</h2>
              <button
                onClick={fetchTrendingTopics}
                disabled={isLoading}
                className="px-4 py-2 bg-blue-600 text-white rounded-md hover:bg-blue-700 disabled:opacity-50"
              >
                {isLoading ? 'Loading...' : 'Refresh Topics'}
              </button>
            </div>

            {topics.length > 0 ? (
              <div className="space-y-4">
                {topics.map((topic, index) => (
                  <div key={index} className="border rounded-lg p-4">
                    <h3 className="font-medium text-gray-900 mb-2">{topic.title}</h3>
                    <p className="text-gray-600 text-sm mb-3">{topic.description}</p>
                    <div className="flex justify-between items-center">
                      <span className="text-xs text-gray-500 bg-gray-100 px-2 py-1 rounded">
                        {topic.category}
                      </span>
                      <button
                        onClick={() => generateContent(topic.title)}
                        disabled={isGenerating}
                        className="px-3 py-1 bg-green-600 text-white text-sm rounded hover:bg-green-700 disabled:opacity-50"
                      >
                        {isGenerating ? 'Generating...' : 'Generate Article'}
                      </button>
                    </div>
                  </div>
                ))}
              </div>
            ) : (
              <p className="text-gray-500">No trending topics available. Click "Refresh Topics" to load them.</p>
            )}
          </div>
        )}

        {/* Custom Topic Generation */}
        <div className="bg-white shadow rounded-lg p-6">
          <h2 className="text-lg font-medium text-gray-900 mb-4">Custom Topic</h2>
          <div className="space-y-4">
            <input
              type="text"
              value={customTopic}
              onChange={(e) => setCustomTopic(e.target.value)}
              placeholder="Enter a custom topic..."
              className="block w-full border-gray-300 rounded-md shadow-sm focus:ring-blue-500 focus:border-blue-500 sm:text-sm"
            />
            <button
              onClick={() => generateContent(customTopic)}
              disabled={!selectedSite || !customTopic.trim() || isGenerating}
              className="px-4 py-2 bg-purple-600 text-white rounded-md hover:bg-purple-700 disabled:opacity-50"
            >
              {isGenerating ? 'Generating...' : 'Generate from Custom Topic'}
            </button>
          </div>
        </div>

        {/* Status Message */}
        {message && (
          <div className={`p-4 rounded-md ${
            message.startsWith('✅') ? 'bg-green-50 text-green-700' : 'bg-red-50 text-red-700'
          }`}>
            {message}
          </div>
        )}
      </div>
    </ProtectedRoute>
  );
} 