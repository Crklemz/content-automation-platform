'use client';

import { useState, useEffect, useCallback, useRef } from 'react';
import ProtectedRoute from '../ProtectedRoute';
import { Article } from "@/types";
import { Site, ArticleFilters } from "@/types/admin";
import ArticleTable from "@/app/admin/articles/ArticleTable";
import ArticleFiltersComponent from "@/app/admin/articles/ArticleFilters";

export default function ArticlesPage() {
  const [articles, setArticles] = useState<Article[]>([]);
  const [sites, setSites] = useState<Site[]>([]);
  const [filters, setFilters] = useState<ArticleFilters>({
    site: '',
    status: '',
    search: '',
  });
  const [isLoading, setIsLoading] = useState(true);
  const prevFiltersRef = useRef<ArticleFilters>(filters);

  const getArticles = async (currentFilters: ArticleFilters): Promise<Article[]> => {
    try {
      const params = new URLSearchParams();
      
      if (currentFilters.site) params.append('site', currentFilters.site);
      if (currentFilters.status) params.append('status', currentFilters.status);
      if (currentFilters.search) params.append('search', currentFilters.search);
      
      const res = await fetch(`http://localhost:8000/api/articles/?${params.toString()}`, {
        credentials: 'include'
      });

      if (!res.ok) {
        console.error(`Articles API error: ${res.status} ${res.statusText}`);
        return [];
      }

      const response = await res.json();
      
      // Handle paginated response format
      let articles: Article[] = [];
      
      if (response && response.results && Array.isArray(response.results)) {
        articles = response.results;
      } else if (Array.isArray(response)) {
        // Fallback for direct array response
        articles = response;
      } else {
        console.error('Unexpected articles API response format:', response);
        articles = [];
      }
      
      return articles;
    } catch (error) {
      console.error('Error fetching articles:', error);
      return [];
    }
  };

  const getSites = async (): Promise<Site[]> => {
    try {
      const res = await fetch("http://localhost:8000/api/sites/", { 
        credentials: 'include'
      });
      
      if (!res.ok) {
        console.error(`Sites API error: ${res.status} ${res.statusText}`);
        return [];
      }
      
      const response = await res.json();
      
      // Handle paginated response format
      let sites: Site[] = [];
      if (response && response.results && Array.isArray(response.results)) {
        sites = response.results;
      } else if (Array.isArray(response)) {
        // Fallback for direct array response
        sites = response;
      }
      
      return sites;
    } catch (error) {
      console.error('Error fetching sites:', error);
      return [];
    }
  };

  // Load data when component mounts and when filters change
  useEffect(() => {
    const loadData = async () => {
      setIsLoading(true);
      try {
        const [articlesData, sitesData] = await Promise.all([
          getArticles(filters),
          getSites()
        ]);
        setArticles(articlesData);
        setSites(sitesData);
      } catch (error) {
        console.error('Error loading data:', error);
      } finally {
        setIsLoading(false);
      }
    };

    // Only load data if filters actually changed
    const filtersChanged = JSON.stringify(prevFiltersRef.current) !== JSON.stringify(filters);
    if (filtersChanged) {
      prevFiltersRef.current = filters;
      loadData();
    } else if (articles.length === 0) {
      // Initial load
      loadData();
    }
  }, [filters, articles.length]);

  const handleFilterChange = useCallback((newFilters: ArticleFilters) => {
    setFilters(newFilters);
  }, []);

  if (isLoading) {
    return (
      <ProtectedRoute>
        <div className="flex justify-center items-center h-64">
          <div className="text-gray-600">Loading articles...</div>
        </div>
      </ProtectedRoute>
    );
  }

  return (
    <ProtectedRoute>
      <div className="space-y-6">
        {/* Page Header */}
        <div className="flex justify-between items-center">
          <div>
            <h1 className="text-3xl font-bold text-gray-900">Articles</h1>
            <p className="mt-2 text-gray-600">
              Manage and review articles across all sites
            </p>
          </div>
          <div className="text-sm text-gray-500">
            {articles.length} article{articles.length !== 1 ? 's' : ''} found
          </div>
        </div>

        {/* Filters */}
        <ArticleFiltersComponent 
          sites={sites} 
          currentFilters={filters} 
          onFilterChange={handleFilterChange}
        />

        {/* Articles Table */}
        <ArticleTable articles={articles} sites={sites} />
      </div>
    </ProtectedRoute>
  );
} 