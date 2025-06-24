export interface Site {
  id: number;
  slug: string;
  name: string;
  description: string;
  logo: string;
  primary_color: string;
  secondary_color: string;
}

export interface ArticleFilters {
  site: string;
  status: string;
  search: string;
} 