'use client';

import { useState, useEffect } from 'react';
import { useRouter, useSearchParams } from 'next/navigation';
import { Site } from '@/types';

interface SearchAndFilterProps {
  site: string;
  currentSearch?: string;
  currentCategory?: string;
  siteConfig: Site;
}

export default function SearchAndFilter({ 
  site, 
  currentSearch, 
  currentCategory, 
  siteConfig 
}: SearchAndFilterProps) {
  const router = useRouter();
  const searchParams = useSearchParams();
  
  const [searchTerm, setSearchTerm] = useState(currentSearch || '');
  const [selectedCategory, setSelectedCategory] = useState(currentCategory || 'all');
  const [isSearching, setIsSearching] = useState(false);

  // Update URL when search or category changes
  useEffect(() => {
    const params = new URLSearchParams(searchParams);
    
    if (searchTerm) {
      params.set('search', searchTerm);
    } else {
      params.delete('search');
    }
    
    if (selectedCategory && selectedCategory !== 'all') {
      params.set('category', selectedCategory);
    } else {
      params.delete('category');
    }
    
    const newUrl = `/${site}${params.toString() ? '?' + params.toString() : ''}`;
    router.push(newUrl);
  }, [searchTerm, selectedCategory, site, router, searchParams]);

  // Debounced search
  useEffect(() => {
    const timer = setTimeout(() => {
      setIsSearching(false);
    }, 500);

    return () => clearTimeout(timer);
  }, [searchTerm]);

  const handleSearchChange = (e: React.ChangeEvent<HTMLInputElement>) => {
    setSearchTerm(e.target.value);
    setIsSearching(true);
  };

  const handleCategoryChange = (e: React.ChangeEvent<HTMLSelectElement>) => {
    setSelectedCategory(e.target.value);
  };

  const clearFilters = () => {
    setSearchTerm('');
    setSelectedCategory('all');
  };

  const hasActiveFilters = searchTerm || (selectedCategory && selectedCategory !== 'all');

  return (
    <div className="mb-8 bg-white rounded-lg border border-gray-200 p-6">
      <div className="flex flex-col md:flex-row gap-4">
        {/* Search Input */}
        <div className="flex-1">
          <label htmlFor="search" className="block text-sm font-medium text-gray-700 mb-2">
            Search Articles
          </label>
          <div className="relative">
            <input
              type="text"
              id="search"
              value={searchTerm}
              onChange={handleSearchChange}
              placeholder="Search by title or content..."
              className="w-full px-4 py-2 border border-gray-300 rounded-md focus:ring-2 focus:ring-offset-0 focus:outline-none transition-colors"
              style={{ 
                focusRingColor: siteConfig.primary_color,
                borderColor: searchTerm ? siteConfig.primary_color : undefined
              }}
            />
            {isSearching && (
              <div className="absolute right-3 top-1/2 transform -translate-y-1/2">
                <div className="animate-spin rounded-full h-4 w-4 border-2 border-gray-300 border-t-blue-600"></div>
              </div>
            )}
            {searchTerm && !isSearching && (
              <button
                onClick={() => setSearchTerm('')}
                className="absolute right-3 top-1/2 transform -translate-y-1/2 text-gray-400 hover:text-gray-600"
              >
                <svg className="w-4 h-4" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                  <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M6 18L18 6M6 6l12 12" />
                </svg>
              </button>
            )}
          </div>
        </div>

        {/* Category Filter */}
        <div className="md:w-48">
          <label htmlFor="category" className="block text-sm font-medium text-gray-700 mb-2">
            Category
          </label>
          <select
            id="category"
            value={selectedCategory}
            onChange={handleCategoryChange}
            className="w-full px-4 py-2 border border-gray-300 rounded-md focus:ring-2 focus:ring-offset-0 focus:outline-none transition-colors"
            style={{ 
              focusRingColor: siteConfig.primary_color,
              borderColor: selectedCategory && selectedCategory !== 'all' ? siteConfig.primary_color : undefined
            }}
          >
            <option value="all">All Categories</option>
            <option value="ai">AI & Technology</option>
            <option value="business">Business</option>
            <option value="sustainability">Sustainability</option>
            <option value="green-living">Green Living</option>
            <option value="general">General</option>
          </select>
        </div>

        {/* Clear Filters Button */}
        {hasActiveFilters && (
          <div className="flex items-end">
            <button
              onClick={clearFilters}
              className="px-4 py-2 text-sm font-medium text-gray-600 hover:text-gray-800 transition-colors"
            >
              Clear filters
            </button>
          </div>
        )}
      </div>

      {/* Active Filters Display */}
      {hasActiveFilters && (
        <div className="mt-4 pt-4 border-t border-gray-200">
          <div className="flex flex-wrap gap-2">
            {searchTerm && (
              <span className="inline-flex items-center px-2.5 py-0.5 rounded-full text-xs font-medium bg-blue-100 text-blue-800">
                Search: "{searchTerm}"
                <button
                  onClick={() => setSearchTerm('')}
                  className="ml-1 text-blue-600 hover:text-blue-800"
                >
                  ×
                </button>
              </span>
            )}
            {selectedCategory && selectedCategory !== 'all' && (
              <span className="inline-flex items-center px-2.5 py-0.5 rounded-full text-xs font-medium bg-green-100 text-green-800">
                Category: {selectedCategory}
                <button
                  onClick={() => setSelectedCategory('all')}
                  className="ml-1 text-green-600 hover:text-green-800"
                >
                  ×
                </button>
              </span>
            )}
          </div>
        </div>
      )}
    </div>
  );
} 