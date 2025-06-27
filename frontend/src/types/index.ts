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

export interface Site {
  id: number;
  name: string;
  slug: string;
  description: string;
  primary_color: string;
  secondary_color: string;
  created_at: string;
}
