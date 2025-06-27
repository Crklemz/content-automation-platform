import { Site } from "@/types";

async function getSites(): Promise<Site[]> {
  try {
    const res = await fetch('http://localhost:8000/api/sites/', {
      cache: "no-store",
    });

    if (!res.ok) {
      console.error(`Sites API error: ${res.status} ${res.statusText}`);
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
    
    console.error('Unexpected sites API response format:', response);
    return [];
  } catch (error) {
    console.error('Error fetching sites:', error);
    return [];
  }
}

export default async function Home() {
  const sites = await getSites();

  return (
    <div className="min-h-screen bg-gray-50">
      {/* Hero Section */}
      <div className="bg-white border-b border-gray-200">
        <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8 py-16">
          <div className="text-center">
            <h1 className="text-4xl font-bold text-gray-900 sm:text-5xl md:text-6xl">
              Content Automation Platform
            </h1>
            <p className="mt-6 text-xl text-gray-600 max-w-3xl mx-auto">
              Discover curated content across multiple specialized sites. 
              From AI insights to sustainable living, find the information that matters to you.
            </p>
          </div>
        </div>
      </div>

      {/* Sites Grid */}
      <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8 py-12">
        <div className="text-center mb-12">
          <h2 className="text-3xl font-bold text-gray-900 mb-4">
            Explore Our Sites
          </h2>
          <p className="text-lg text-gray-600">
            Choose from our curated collection of specialized content sites
          </p>
        </div>

        {sites.length === 0 ? (
          <div className="text-center py-12">
            <h3 className="text-xl font-semibold text-gray-700 mb-4">
              No sites available yet
            </h3>
            <p className="text-gray-500">
              Check back soon for new content sites.
            </p>
          </div>
        ) : (
          <div className="grid gap-8 md:grid-cols-2 lg:grid-cols-3">
            {sites.map((site) => (
              <div
                key={site.slug}
                className="bg-white rounded-lg shadow-sm border border-gray-200 hover:shadow-md transition-shadow duration-200 overflow-hidden"
              >
                <a href={`/${site.slug}`} className="block">
                  <div className="p-6">
                    <div className="flex items-center mb-4">
                      <div 
                        className="w-12 h-12 rounded-lg flex items-center justify-center text-white font-bold text-lg"
                        style={{ backgroundColor: site.primary_color }}
                      >
                        {site.name.charAt(0).toUpperCase()}
                      </div>
                      <div className="ml-4">
                        <h3 className="text-xl font-semibold text-gray-900">
                          {site.name}
                        </h3>
                        <p className="text-sm text-gray-500">
                          {site.slug}
                        </p>
                      </div>
                    </div>
                    
                    <p className="text-gray-600 mb-4 line-clamp-3">
                      {site.description}
                    </p>
                    
                    <div className="flex items-center justify-between">
                      <span 
                        className="text-sm font-medium"
                        style={{ color: site.primary_color }}
                      >
                        Browse articles →
                      </span>
                      <div className="flex space-x-1">
                        <div 
                          className="w-3 h-3 rounded-full"
                          style={{ backgroundColor: site.primary_color }}
                        />
                        <div 
                          className="w-3 h-3 rounded-full"
                          style={{ backgroundColor: site.secondary_color }}
                        />
                      </div>
                    </div>
                  </div>
                </a>
              </div>
            ))}
          </div>
        )}
      </div>

      {/* Features Section */}
      <div className="bg-white border-t border-gray-200">
        <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8 py-16">
          <div className="text-center mb-12">
            <h2 className="text-3xl font-bold text-gray-900 mb-4">
              Why Choose Our Platform?
            </h2>
          </div>
          
          <div className="grid gap-8 md:grid-cols-3">
            <div className="text-center">
              <div className="w-16 h-16 bg-blue-100 rounded-lg flex items-center justify-center mx-auto mb-4">
                <svg className="w-8 h-8 text-blue-600" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                  <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M9.663 17h4.673M12 3v1m6.364 1.636l-.707.707M21 12h-1M4 12H3m3.343-5.657l-.707-.707m2.828 9.9a5 5 0 117.072 0l-.548.547A3.374 3.374 0 0014 18.469V19a2 2 0 11-4 0v-.531c0-.895-.356-1.754-.988-2.386l-.548-.547z" />
                </svg>
              </div>
              <h3 className="text-xl font-semibold text-gray-900 mb-2">
                AI-Generated Content
              </h3>
              <p className="text-gray-600">
                High-quality, relevant content generated using advanced AI technology
              </p>
            </div>
            
            <div className="text-center">
              <div className="w-16 h-16 bg-green-100 rounded-lg flex items-center justify-center mx-auto mb-4">
                <svg className="w-8 h-8 text-green-600" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                  <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M19 11H5m14 0a2 2 0 012 2v6a2 2 0 01-2 2H5a2 2 0 01-2-2v-6a2 2 0 012-2m14 0V9a2 2 0 00-2-2M5 11V9a2 2 0 012-2m0 0V5a2 2 0 012-2h6a2 2 0 012 2v2M7 7h10" />
                </svg>
              </div>
              <h3 className="text-xl font-semibold text-gray-900 mb-2">
                Curated Topics
              </h3>
              <p className="text-gray-600">
                Carefully selected topics relevant to each site's focus area
              </p>
            </div>
            
            <div className="text-center">
              <div className="w-16 h-16 bg-purple-100 rounded-lg flex items-center justify-center mx-auto mb-4">
                <svg className="w-8 h-8 text-purple-600" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                  <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M12 6.253v13m0-13C10.832 5.477 9.246 5 7.5 5S4.168 5.477 3 6.253v13C4.168 18.477 5.754 18 7.5 18s3.332.477 4.5 1.253m0-13C13.168 5.477 14.754 5 16.5 5c1.746 0 3.332.477 4.5 1.253v13C19.832 18.477 18.246 18 16.5 18c-1.746 0-3.332.477-4.5 1.253" />
                </svg>
              </div>
              <h3 className="text-xl font-semibold text-gray-900 mb-2">
                Quality Assurance
              </h3>
              <p className="text-gray-600">
                All content goes through review and approval processes
              </p>
            </div>
          </div>
        </div>
      </div>

      {/* Footer */}
      <footer className="bg-gray-900 text-white">
        <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8 py-12">
          <div className="text-center">
            <h3 className="text-2xl font-bold mb-4">
              Content Automation Platform
            </h3>
            <p className="text-gray-400 mb-6">
              Bringing you the latest insights across multiple specialized topics
            </p>
            <div className="flex justify-center space-x-6">
              <a href="/admin" className="text-gray-400 hover:text-white transition-colors">
                Admin
              </a>
              <span className="text-gray-600">•</span>
              <span className="text-gray-400">
                {sites.length} active site{sites.length !== 1 ? 's' : ''}
              </span>
            </div>
          </div>
        </div>
      </footer>
    </div>
  );
}
