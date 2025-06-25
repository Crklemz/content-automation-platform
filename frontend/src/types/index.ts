export interface Article {
  id: number;
  title: string;
  slug: string;
  body: string;
  site: string;
  sources?: Array<{
    url: string;
    title: string;
    source: string;
  }> | string[];
  status: string;
  created_at: string;
}
