export interface Article {
  id: number;
  title: string;
  slug: string;
  body: string;
  site: string;
  sources?: string[];
  status: string;
  created_at: string;
}
