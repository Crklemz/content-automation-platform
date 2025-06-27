'use client';

import { useState, useEffect } from 'react';
import { notFound } from "next/navigation";
import { Article } from "@/types";
import { getSiteConfig } from "@/lib/getSiteConfig";

interface ArticlePageProps {
  params: Promise<{ site: string; slug: string }>;
}

export default function ArticlePage({ params }: ArticlePageProps) {
  const [article, setArticle] = useState<Article | null>(null);
  const [siteConfig, setSiteConfig] = useState<any>(null);
  const [isLoading, setIsLoading] = useState(true);
  const [error, setError] = useState<string | null>(null);

  const getArticle = async (site: string, slug: string): Promise<Article | null> => {
    try {
      const res = await fetch(`http://localhost:8000/api/articles/?site=${site}`, {
        credentials: 'include'
      });

      if (!res.ok) {
        console.error(`Articles API error: ${res.status} ${res.statusText}`);
        return null;
      }

      const response = await res.json();
      
      let articles: Article[] = [];
      
      // Handle paginated response format
      if (response && response.results && Array.isArray(response.results)) {
        articles = response.results;
      } else if (Array.isArray(response)) {
        // Fallback for direct array response
        articles = response;
      } else {
        console.error('Unexpected articles API response format:', response);
        return null;
      }
      
      return articles.find((a: Article) => a.slug === slug) || null;
    } catch (error) {
      console.error('Error fetching article:', error);
      return null;
    }
  };

  useEffect(() => {
    const loadData = async () => {
      try {
        const { site, slug } = await params;
        
        // Fetch both site config and article
        const [config, articleData] = await Promise.all([
          getSiteConfig(site),
          getArticle(site, slug)
        ]);

        if (!config) {
          setError('Site not found');
          return;
        }

        if (!articleData) {
          setError('Article not found');
          return;
        }

        setSiteConfig(config);
        setArticle(articleData);
      } catch (error) {
        console.error('Error loading article page:', error);
        setError('Failed to load article');
      } finally {
        setIsLoading(false);
      }
    };

    loadData();
  }, [params]);

  if (isLoading) {
    return (
      <div className="flex justify-center items-center h-64">
        <div className="text-gray-600">Loading article...</div>
      </div>
    );
  }

  if (error || !siteConfig || !article) {
    notFound();
  }

  return (
    <div className="max-w-3xl mx-auto p-8">
      {/* Article Header */}
      <header className="mb-8">
        <div className="mb-4">
          <a 
            href={`/${article.site}`}
            className="inline-flex items-center text-sm font-medium mb-4 hover:underline"
            style={{ color: siteConfig.primary_color }}
          >
            ← Back to {siteConfig.name}
          </a>
        </div>
        
        <h1 className="text-4xl font-bold mb-4 text-gray-900 leading-tight">
          {article.title}
        </h1>
        
        <div className="flex items-center text-gray-600 text-sm mb-6">
          <span>
            Published on {new Date(article.created_at).toLocaleDateString('en-US', {
              year: 'numeric',
              month: 'long',
              day: 'numeric'
            })}
          </span>
          <span className="mx-2">•</span>
          <span style={{ color: siteConfig.primary_color }}>
            {siteConfig.name}
          </span>
          {/* Show status for admin users */}
          <span className="mx-2">•</span>
          <span className={`px-2 py-1 rounded text-xs font-medium ${
            article.status === 'approved' ? 'bg-green-100 text-green-800' :
            article.status === 'rejected' ? 'bg-red-100 text-red-800' :
            'bg-yellow-100 text-yellow-800'
          }`}>
            {article.status.charAt(0).toUpperCase() + article.status.slice(1)}
          </span>
        </div>
      </header>

      {/* Article Content */}
      <article className="prose prose-lg max-w-none">
        <div 
          className="text-gray-800 leading-relaxed"
          dangerouslySetInnerHTML={{ __html: article.body }}
        />
      </article>

      {/* Sources Section */}
      {Array.isArray(article.sources) && article.sources.length > 0 && (
        <section className="mt-12 pt-8 border-t border-gray-200">
          <h2 className="text-xl font-semibold mb-4" style={{ color: siteConfig.primary_color }}>
            Sources & References
          </h2>
          <ul className="space-y-2">
            {article.sources.map((src, i) => {
              // Handle both string and object formats
              const url = typeof src === 'string' ? src : src.url;
              const title = typeof src === 'string' ? src : (src.title || src.source);
              
              return (
                <li key={i} className="text-sm">
                  <a 
                    href={url} 
                    target="_blank" 
                    rel="noopener noreferrer"
                    className="text-blue-600 hover:text-blue-800 hover:underline break-all"
                  >
                    {title}
                  </a>
                </li>
              );
            })}
          </ul>
        </section>
      )}

      {/* Back to Site */}
      <div className="mt-12 pt-8 border-t border-gray-200">
        <a 
          href={`/${article.site}`}
          className="inline-flex items-center px-4 py-2 rounded-md font-medium transition-colors"
          style={{ 
            backgroundColor: siteConfig.primary_color,
            color: 'white'
          }}
        >
          ← Back to {siteConfig.name}
        </a>
      </div>
    </div>
  );
}
