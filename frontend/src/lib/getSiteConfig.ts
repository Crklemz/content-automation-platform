export async function getSiteConfig(slug: string) {
  try {
    const res = await fetch("http://localhost:8000/api/sites/", { cache: "no-store" });
    
    if (!res.ok) {
      console.error(`Sites API error: ${res.status} ${res.statusText}`);
      return null;
    }
    
    const response = await res.json();
    
    // Handle paginated response format
    if (response && response.results && Array.isArray(response.results)) {
      return response.results.find((s: any) => s.slug === slug);
    }
    
    // Fallback for direct array response
    if (Array.isArray(response)) {
      return response.find((s: any) => s.slug === slug);
    }
    
    console.error('Unexpected sites API response format:', response);
    return null;
  } catch (error) {
    console.error('Error fetching site config:', error);
    return null;
  }
}
