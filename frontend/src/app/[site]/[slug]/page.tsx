import { notFound } from "next/navigation";
import { Article } from "@/types";

async function getArticle(site: string, slug: string): Promise<Article | null> {
  const res = await fetch(`http://localhost:8000/api/articles/?site=${site}`, {
    cache: "no-store",
  });

  if (!res.ok) return null;

  const articles = await res.json();
  return articles.find((a: Article) => a.slug === slug) || null;
}

export default async function ArticlePage(props: {
  params: { site: string; slug: string };
}) {
  const { site, slug } = await props.params;

  const article = await getArticle(site, slug);
  if (!article) {
    notFound();
  }

  return (
    <main className="max-w-3xl mx-auto p-8">
      <h1 className="text-3xl font-bold mb-4">{article.title}</h1>
      <p className="text-sm text-gray-500 mb-6">
        Published: {new Date(article.created_at).toLocaleDateString()}
      </p>
      <article className="prose prose-lg" dangerouslySetInnerHTML={{ __html: article.body }} />
      {Array.isArray(article.sources) && article.sources.length > 0 && (
        <section className="mt-10">
          <h2 className="text-xl font-semibold mb-2">Sources</h2>
          <ul className="list-disc list-inside text-blue-600">
            {article.sources.map((src, i) => (
              <li key={i}>
                <a href={src} target="_blank" rel="noopener noreferrer">
                  {src}
                </a>
              </li>
            ))}
          </ul>
        </section>
      )}
    </main>
  );
}
