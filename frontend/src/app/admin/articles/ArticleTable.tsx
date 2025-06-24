'use client';

import { useState } from 'react';
import { Article } from '@/types';
import { Site } from '@/types/admin';

interface ArticleTableProps {
  articles: Article[];
  sites: Site[];
}

export default function ArticleTable({ articles, sites }: ArticleTableProps) {
  const [selectedArticles, setSelectedArticles] = useState<Set<number>>(new Set());
  const [loading, setLoading] = useState<Set<number>>(new Set());

  const getSiteName = (siteSlug: string) => {
    const site = sites.find(s => s.slug === siteSlug);
    return site?.name || siteSlug;
  };

  const getStatusBadge = (status: string) => {
    const statusConfig = {
      pending: { color: 'bg-yellow-100 text-yellow-800', label: 'Pending' },
      approved: { color: 'bg-green-100 text-green-800', label: 'Approved' },
      rejected: { color: 'bg-red-100 text-red-800', label: 'Rejected' },
    };
    
    const config = statusConfig[status as keyof typeof statusConfig] || statusConfig.pending;
    
    return (
      <span className={`inline-flex items-center px-2.5 py-0.5 rounded-full text-xs font-medium ${config.color}`}>
        {config.label}
      </span>
    );
  };

  const handleSelectAll = (checked: boolean) => {
    if (checked) {
      setSelectedArticles(new Set(articles.map(a => a.id)));
    } else {
      setSelectedArticles(new Set());
    }
  };

  const handleSelectArticle = (articleId: number, checked: boolean) => {
    const newSelected = new Set(selectedArticles);
    if (checked) {
      newSelected.add(articleId);
    } else {
      newSelected.delete(articleId);
    }
    setSelectedArticles(newSelected);
  };

  const updateArticleStatus = async (articleId: number, status: string) => {
    setLoading(prev => new Set(prev).add(articleId));
    
    try {
      const response = await fetch(`http://localhost:8000/api/articles/${articleId}/${status}/`, {
        method: 'POST',
        headers: {
          'Content-Type': 'application/json',
        },
      });

      if (response.ok) {
        // Refresh the page to show updated data
        window.location.reload();
      } else {
        console.error('Failed to update article status');
      }
    } catch (error) {
      console.error('Error updating article status:', error);
    } finally {
      setLoading(prev => {
        const newSet = new Set(prev);
        newSet.delete(articleId);
        return newSet;
      });
    }
  };

  const bulkUpdateStatus = async (status: string) => {
    if (selectedArticles.size === 0) return;
    
    setLoading(new Set(selectedArticles));
    
    try {
      const promises = Array.from(selectedArticles).map(articleId =>
        fetch(`http://localhost:8000/api/articles/${articleId}/${status}/`, {
          method: 'POST',
          headers: { 'Content-Type': 'application/json' },
        })
      );
      
      await Promise.all(promises);
      window.location.reload();
    } catch (error) {
      console.error('Error updating articles:', error);
    } finally {
      setLoading(new Set());
    }
  };

  if (articles.length === 0) {
    return (
      <div className="bg-white shadow rounded-lg">
        <div className="px-4 py-12 text-center">
          <h3 className="text-lg font-medium text-gray-900 mb-2">No articles found</h3>
          <p className="text-gray-500">Try adjusting your filters or create some new articles.</p>
        </div>
      </div>
    );
  }

  return (
    <div className="bg-white shadow rounded-lg">
      {/* Bulk Actions */}
      {selectedArticles.size > 0 && (
        <div className="px-4 py-3 border-b border-gray-200 bg-gray-50">
          <div className="flex items-center justify-between">
            <span className="text-sm text-gray-700">
              {selectedArticles.size} article{selectedArticles.size !== 1 ? 's' : ''} selected
            </span>
            <div className="flex space-x-2">
              <button
                onClick={() => bulkUpdateStatus('approve')}
                disabled={loading.size > 0}
                className="px-3 py-1 text-sm font-medium text-white bg-green-600 rounded hover:bg-green-700 disabled:opacity-50"
              >
                Approve Selected
              </button>
              <button
                onClick={() => bulkUpdateStatus('reject')}
                disabled={loading.size > 0}
                className="px-3 py-1 text-sm font-medium text-white bg-red-600 rounded hover:bg-red-700 disabled:opacity-50"
              >
                Reject Selected
              </button>
            </div>
          </div>
        </div>
      )}

      {/* Table */}
      <div className="overflow-x-auto">
        <table className="min-w-full divide-y divide-gray-200">
          <thead className="bg-gray-50">
            <tr>
              <th className="px-6 py-3 text-left">
                <input
                  type="checkbox"
                  checked={selectedArticles.size === articles.length && articles.length > 0}
                  onChange={(e) => handleSelectAll(e.target.checked)}
                  className="rounded border-gray-300 text-blue-600 focus:ring-blue-500"
                />
              </th>
              <th className="px-6 py-3 text-left text-xs font-medium text-gray-500 uppercase tracking-wider">
                Article
              </th>
              <th className="px-6 py-3 text-left text-xs font-medium text-gray-500 uppercase tracking-wider">
                Site
              </th>
              <th className="px-6 py-3 text-left text-xs font-medium text-gray-500 uppercase tracking-wider">
                Status
              </th>
              <th className="px-6 py-3 text-left text-xs font-medium text-gray-500 uppercase tracking-wider">
                Created
              </th>
              <th className="px-6 py-3 text-left text-xs font-medium text-gray-500 uppercase tracking-wider">
                Actions
              </th>
            </tr>
          </thead>
          <tbody className="bg-white divide-y divide-gray-200">
            {articles.map((article) => (
              <tr key={article.id} className="hover:bg-gray-50">
                <td className="px-6 py-4 whitespace-nowrap">
                  <input
                    type="checkbox"
                    checked={selectedArticles.has(article.id)}
                    onChange={(e) => handleSelectArticle(article.id, e.target.checked)}
                    className="rounded border-gray-300 text-blue-600 focus:ring-blue-500"
                  />
                </td>
                <td className="px-6 py-4">
                  <div>
                    <div className="text-sm font-medium text-gray-900">{article.title}</div>
                    <div className="text-sm text-gray-500 truncate max-w-xs">
                      {article.body.replace(/<[^>]+>/g, "").substring(0, 100)}...
                    </div>
                  </div>
                </td>
                <td className="px-6 py-4 whitespace-nowrap text-sm text-gray-900">
                  {getSiteName(article.site)}
                </td>
                <td className="px-6 py-4 whitespace-nowrap">
                  {getStatusBadge(article.status)}
                </td>
                <td className="px-6 py-4 whitespace-nowrap text-sm text-gray-500">
                  {new Date(article.created_at).toLocaleDateString()}
                </td>
                <td className="px-6 py-4 whitespace-nowrap text-sm font-medium">
                  <div className="flex space-x-2">
                    {article.status === 'pending' && (
                      <>
                        <button
                          onClick={() => updateArticleStatus(article.id, 'approve')}
                          disabled={loading.has(article.id)}
                          className="text-green-600 hover:text-green-900 disabled:opacity-50"
                        >
                          Approve
                        </button>
                        <button
                          onClick={() => updateArticleStatus(article.id, 'reject')}
                          disabled={loading.has(article.id)}
                          className="text-red-600 hover:text-red-900 disabled:opacity-50"
                        >
                          Reject
                        </button>
                      </>
                    )}
                    <a
                      href={`/${article.site}/${article.slug}`}
                      target="_blank"
                      rel="noopener noreferrer"
                      className="text-blue-600 hover:text-blue-900"
                    >
                      View
                    </a>
                  </div>
                </td>
              </tr>
            ))}
          </tbody>
        </table>
      </div>
    </div>
  );
} 