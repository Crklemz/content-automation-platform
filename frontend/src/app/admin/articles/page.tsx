import ProtectedRoute from '../ProtectedRoute';
import { Article } from "@/types";
import { Site, ArticleFilters } from "@/types/admin";
import ArticleTable from "@/app/admin/articles/ArticleTable";
import ArticleFiltersComponent from "@/app/admin/articles/ArticleFilters";

interface ArticlesPageProps {
  searchParams: Promise<{ [key: string]: string | string[] | undefined }>;
}

async function getArticles(filters: ArticleFilters): Promise<Article[]> {
  try {
    const params = new URLSearchParams();
    
    if (filters.site) params.append('site', filters.site);
    if (filters.status) params.append('status', filters.status);
    if (filters.search) params.append('search', filters.search);
    
    const res = await fetch(`http://localhost:8000/api/articles/?${params.toString()}`, {
      cache: "no-store",
      credentials: 'include'
    });

    if (!res.ok) {
      console.error(`Articles API error: ${res.status} ${res.statusText}`);
      return [];
    }

    const response = await res.json();
    
    // Handle paginated response format
    let articles: Article[] = [];
    let totalCount = 0;
    
    if (response && response.results && Array.isArray(response.results)) {
      articles = response.results;
      totalCount = response.count || 0;
    } else if (Array.isArray(response)) {
      // Fallback for direct array response
      articles = response;
      totalCount = response.length;
    } else {
      console.error('Unexpected articles API response format:', response);
      articles = [];
      totalCount = 0;
    }
    
    return articles;
  } catch (error) {
    console.error('Error fetching articles:', error);
    return [];
  }
}

async function getSites(): Promise<Site[]> {
  try {
    const res = await fetch("http://localhost:8000/api/sites/", { 
      cache: "no-store",
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
}

export default async function ArticlesPage({ searchParams }: ArticlesPageProps) {
  // Await searchParams before using its properties
  const params = await searchParams;
  
  // Extract filters from search params
  const filters: ArticleFilters = {
    site: typeof params.site === 'string' ? params.site : '',
    status: typeof params.status === 'string' ? params.status : '',
    search: typeof params.search === 'string' ? params.search : '',
  };

  // Fetch articles and sites
  const [articles, sites] = await Promise.all([
    getArticles(filters),
    getSites()
  ]);

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
        <ArticleFiltersComponent sites={sites} currentFilters={filters} />

        {/* Articles Table */}
        <ArticleTable articles={articles} sites={sites} />
      </div>
    </ProtectedRoute>
  );
} 