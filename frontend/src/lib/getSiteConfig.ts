export async function getSiteConfig(slug: string) {
  const res = await fetch("http://localhost:8000/api/sites", { cache: "no-store" });
  const sites = await res.json();
  return sites.find((s: any) => s.slug === slug);
}
