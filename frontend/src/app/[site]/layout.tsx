import { Site } from "@/types";
import { getSiteConfig } from "@/lib/getSiteConfig";
import { notFound } from "next/navigation";
import SiteNavigation from "./SiteNavigation";

interface SiteLayoutProps {
  children: React.ReactNode;
  params: Promise<{ site: string }>;
}

async function getSites(): Promise<Site[]> {
  try {
    const res = await fetch('http://localhost:8000/api/sites/', {
      cache: "no-store",
    });

    if (!res.ok) {
      return [];
    }

    const response = await res.json();
    
    if (response && response.results && Array.isArray(response.results)) {
      return response.results;
    }
    
    if (Array.isArray(response)) {
      return response;
    }
    
    return [];
  } catch (error) {
    return [];
  }
}

export default async function SiteLayout({ children, params }: SiteLayoutProps) {
  const { site } = await params;
  const [siteConfig, allSites] = await Promise.all([
    getSiteConfig(site),
    getSites()
  ]);
  
  if (!siteConfig) {
    notFound();
  }

  // Apply site-specific CSS variables for theming
  const siteStyles = {
    '--primary-color': siteConfig.primary_color,
    '--secondary-color': siteConfig.secondary_color,
  } as React.CSSProperties;

  return (
    <div className="min-h-screen bg-gray-50">
      {/* Site Navigation */}
      <SiteNavigation 
        currentSite={siteConfig}
        allSites={allSites}
      />
      
      {/* Site Header */}
      <header 
        className="bg-white shadow-sm border-b"
        style={{ borderColor: siteConfig.primary_color }}
      >
        <div className="max-w-4xl mx-auto px-8 py-4">
          <div className="flex items-center justify-between">
            <div className="flex items-center space-x-4">
              {/* Site Logo */}
              {siteConfig.logo && (
                <div className="w-8 h-8 rounded-full flex items-center justify-center text-white font-bold text-sm"
                     style={{ backgroundColor: siteConfig.primary_color }}>
                  {siteConfig.logo.includes('logo.svg') ? 'L' : siteConfig.name.charAt(0)}
                </div>
              )}
              
              {/* Site Name */}
              <h1 
                className="text-2xl font-bold"
                style={{ color: siteConfig.primary_color }}
              >
                {siteConfig.name}
              </h1>
            </div>
            
            {/* Site Description */}
            <p className="text-gray-600 text-sm hidden md:block">
              {siteConfig.description}
            </p>
          </div>
        </div>
      </header>

      {/* Main Content */}
      <main className="bg-gray-50 min-h-screen">
        {children}
      </main>

      {/* Site Footer */}
      <footer 
        className="bg-white border-t py-8"
        style={{ borderColor: siteConfig.secondary_color }}
      >
        <div className="max-w-4xl mx-auto px-8">
          <div className="text-center">
            <p 
              className="text-sm"
              style={{ color: siteConfig.primary_color }}
            >
              © 2024 {siteConfig.name}. All rights reserved.
            </p>
          </div>
        </div>
      </footer>
    </div>
  );
} 