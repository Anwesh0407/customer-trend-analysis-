export interface Product {
  asin: string;
  product_name: string;
  category: string;
  subcategory: string;
  brand: string;
  price_inr: number;
  mrp_inr: number;
  discount_pct: number;
  rating: number;
  review_count: number;
  color: string;
  material: string;
  pattern: string;
  available_sizes: string[];
  seller: string;
  availability: string;
  product_url: string;
  badge?: string;
  badge_type?: string;
  sentiment?: string;
  price_position?: string;
  rating_position?: string;
  competition?: string;
  opportunity?: string;
}

export interface ReviewItem {
  review_id: string;
  product_id: string;
  rating: number;
  title: string;
  text: string;
  date: string;
  source: string;
  sentiment: string;
}

export interface ReviewInsight {
  positive_drivers: string[];
  recurring_complaints: string[];
  sentiment_distribution: {
    positive_pct: number;
    neutral_pct: number;
    negative_pct: number;
  };
  total_reviews_analyzed: number;
  avg_rating: number;
  samples: ReviewItem[];
}

export interface AnalyticsOverview {
  total_products: number;
  median_price_inr: number;
  min_price_inr: number;
  max_price_inr: number;
  avg_rating: number;
  median_rating: number;
  sample_size: number;
  avg_discount_pct: number;
  dominant_material: string;
  dominant_color: string;
  dominant_price_band: string;
}

export interface PriceBand {
  band_name: string;
  min_price: number;
  max_price: number;
  product_count: number;
  avg_rating: number;
  competition_density: string;
  opportunity_level: string;
}

export interface PriceAnalytics {
  price_bands: PriceBand[];
  sweet_spot: {
    band: string;
    recommended_launch_price: string;
    intro_coupon_target: string;
    rationale: string;
  };
}

export interface AttributeBreakdown {
  materials: Record<string, number>;
  colors: Record<string, number>;
  patterns: Record<string, number>;
  brands: Record<string, number>;
}

export interface Recommendation {
  id: string;
  title: string;
  badge: string;
  confidence_pct: number;
  what_observed: string;
  why_it_matters: string;
  evidence_sample_size: string;
  what_to_do: string;
  limitations: string;
  sourcing_specs?: {
    fabric: string;
    test_range: string;
    colors: string;
    priority_sizes: string;
  };
  estimated_margin?: string;
}

export interface NicheState {
  category: string;
  location: string;
  priceMax: number;
  material: string;
  activeTab: string;
  searchQuery: string;
}

export interface ChatMessage {
  id: string;
  sender: 'user' | 'assistant';
  text: string;
  evidence?: string[];
  actions?: string[];
}
