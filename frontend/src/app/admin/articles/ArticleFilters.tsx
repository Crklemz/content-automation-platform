'use client';

import { useRouter, useSearchParams } from 'next/navigation';
import { useState, useEffect } from 'react';
import { Site } from '@/types/admin';

interface ArticleFiltersProps {
  sites: Site[];
  currentFilters: {
    site: string;
    status: string;
    search: string;
  };
}

export default function ArticleFilters({ sites, currentFilters }: ArticleFiltersProps) {
  const router = useRouter();
  const searchParams = useSearchParams();
  
  const [filters, setFilters] = useState({
    site: currentFilters.site,
    status: currentFilters.status,
    search: currentFilters.search,
  });

  // Update URL when filters change
  useEffect(() => {
    const params = new URLSearchParams(searchParams);
    
    if (filters.site) {
      params.set('site', filters.site);
    } else {
      params.delete('site');
    }
    
    if (filters.status) {
      params.set('status', filters.status);
    } else {
      params.delete('status');
    }
    
    if (filters.search) {
      params.set('search', filters.search);
    } else {
      params.delete('search');
    }
    
    router.push(`/admin/articles?${params.toString()}`);
  }, [filters, router, searchParams]);

  const clearFilters = () => {
    setFilters({ site: '', status: '', search: '' });
  };

  const hasActiveFilters = filters.site || filters.status || filters.search;

  return (
    <div className="bg-white shadow rounded-lg">
      <div className="px-4 py-5 sm:p-6">
        <h3 className="text-lg leading-6 font-medium text-gray-900 mb-4">
          Filters
        </h3>
        
        <div className="grid grid-cols-1 md:grid-cols-4 gap-4">
          {/* Site Filter */}
          <div>
            <label htmlFor="site" className="block text-sm font-medium text-gray-700 mb-1">
              Site
            </label>
            <select
              id="site"
              value={filters.site}
              onChange={(e) => setFilters(prev => ({ ...prev, site: e.target.value }))}
              className="block w-full border-gray-300 rounded-md shadow-sm focus:ring-blue-500 focus:border-blue-500 sm:text-sm"
            >
              <option value="">All Sites</option>
              {sites.map((site) => (
                <option key={site.slug} value={site.slug}>
                  {site.name}
                </option>
              ))}
            </select>
          </div>

          {/* Status Filter */}
          <div>
            <label htmlFor="status" className="block text-sm font-medium text-gray-700 mb-1">
              Status
            </label>
            <select
              id="status"
              value={filters.status}
              onChange={(e) => setFilters(prev => ({ ...prev, status: e.target.value }))}
              className="block w-full border-gray-300 rounded-md shadow-sm focus:ring-blue-500 focus:border-blue-500 sm:text-sm"
            >
              <option value="">All Statuses</option>
              <option value="pending">Pending</option>
              <option value="approved">Approved</option>
              <option value="rejected">Rejected</option>
            </select>
          </div>

          {/* Search Filter */}
          <div>
            <label htmlFor="search" className="block text-sm font-medium text-gray-700 mb-1">
              Search
            </label>
            <input
              type="text"
              id="search"
              value={filters.search}
              onChange={(e) => setFilters(prev => ({ ...prev, search: e.target.value }))}
              placeholder="Search titles and content..."
              className="block w-full border-gray-300 rounded-md shadow-sm focus:ring-blue-500 focus:border-blue-500 sm:text-sm"
            />
          </div>

          {/* Clear Filters */}
          <div className="flex items-end">
            {hasActiveFilters && (
              <button
                onClick={clearFilters}
                className="w-full px-4 py-2 border border-gray-300 rounded-md shadow-sm text-sm font-medium text-gray-700 bg-white hover:bg-gray-50 focus:outline-none focus:ring-2 focus:ring-offset-2 focus:ring-blue-500"
              >
                Clear Filters
              </button>
            )}
          </div>
        </div>
      </div>
    </div>
  );
} 