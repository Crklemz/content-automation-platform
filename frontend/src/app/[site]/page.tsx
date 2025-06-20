import { notFound } from "next/navigation";
import { Article } from "@/types";

async function getArticles(site: string): Promise<Article[]> {
  const res = await fetch(`http://localhost:8000/api/articles/?site=${site}&status=approved`, {
    cache: "no-store",
  });

  if (!res.ok) return [];
  return await res.json();
}

export default async function SitePage(props: { params: { site: string } }) {
  const { site } = await props.params;

  const articles = await getArticles(site);
  if (!articles || articles.length === 0) {
    notFound();
  }

  return (
    <main className="max-w-4xl mx-auto p-8">
      <h1 className="text-4xl font-bold mb-6 capitalize">{site.replace(/-/g, " ")}</h1>
      <ul className="space-y-6">
        {articles.map((article) => (
          <li key={article.slug}>
            <a
              href={`/${site}/${article.slug}`}
              className="block hover:bg-gray-100 p-4 rounded border border-gray-200 transition"
            >
              <h2 className="text-2xl font-semibold">{article.title}</h2>
              <p className="text-gray-600 text-sm mt-1">
                {new Date(article.created_at).toLocaleDateString()}
              </p>
              <p className="text-gray-700 mt-2 line-clamp-2">
                {article.body.replace(/<[^>]+>/g, "")}
              </p>
            </a>
          </li>
        ))}
      </ul>
    </main>
  );
}
