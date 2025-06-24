import { notFound } from "next/navigation";
import { Article } from "@/types";
import { getSiteConfig } from "@/lib/getSiteConfig";

async function getArticles(site: string): Promise<Article[]> {
  try {
    const res = await fetch(`http://localhost:8000/api/articles/?site=${site}&status=approved`, {
      cache: "no-store",
    });

    if (!res.ok) {
      console.error(`Articles API error: ${res.status} ${res.statusText}`);
      return [];
    }

    const response = await res.json();
    
    // Handle paginated response format
    if (response && response.results && Array.isArray(response.results)) {
      return response.results;
    }
    
    // Fallback for direct array response
    if (Array.isArray(response)) {
      return response;
    }
    
    console.error('Unexpected articles API response format:', response);
    return [];
  } catch (error) {
    console.error('Error fetching articles:', error);
    return [];
  }
}

export default async function SitePage(props: { params: Promise<{ site: string }> }) {
  const { site } = await props.params;

  // Fetch both site config and articles
  const [siteConfig, articles] = await Promise.all([
    getSiteConfig(site),
    getArticles(site)
  ]);

  if (!siteConfig) {
    notFound();
  }

  if (!articles || articles.length === 0) {
    return (
      <div className="max-w-4xl mx-auto p-8">
        <div className="text-center py-12">
          <h2 className="text-2xl font-semibold text-gray-700 mb-4">
            No articles available yet
          </h2>
          <p className="text-gray-500">
            Check back soon for new content from {siteConfig.name}.
          </p>
        </div>
      </div>
    );
  }

  return (
    <div className="max-w-4xl mx-auto p-8">
      {/* Page Header */}
      <div className="mb-8">
        <h1 className="text-4xl font-bold mb-2" style={{ color: siteConfig.primary_color }}>
          Latest Articles
        </h1>
        <p className="text-gray-600">
          Stay updated with the latest insights from {siteConfig.name}
        </p>
      </div>

      {/* Articles Grid */}
      <div className="grid gap-6 md:grid-cols-2 lg:grid-cols-1">
        {articles.map((article) => (
          <article 
            key={article.slug}
            className="bg-white rounded-lg shadow-sm border border-gray-200 hover:shadow-md transition-shadow duration-200 overflow-hidden"
          >
            <a href={`/${site}/${article.slug}`} className="block">
              <div className="p-6">
                <h2 className="text-xl font-semibold mb-2 text-gray-900 hover:text-gray-700 transition-colors">
                  {article.title}
                </h2>
                
                <p className="text-gray-600 text-sm mb-3">
                  {new Date(article.created_at).toLocaleDateString('en-US', {
                    year: 'numeric',
                    month: 'long',
                    day: 'numeric'
                  })}
                </p>
                
                <p className="text-gray-700 leading-relaxed line-clamp-3">
                  {article.body.replace(/<[^>]+>/g, "").substring(0, 200)}...
                </p>
                
                <div className="mt-4 flex items-center">
                  <span 
                    className="text-sm font-medium"
                    style={{ color: siteConfig.primary_color }}
                  >
                    Read more →
                  </span>
                </div>
              </div>
            </a>
          </article>
        ))}
      </div>

      {/* Articles Count */}
      <div className="mt-8 text-center">
        <p className="text-sm text-gray-500">
          Showing {articles.length} article{articles.length !== 1 ? 's' : ''}
        </p>
      </div>
    </div>
  );
}
