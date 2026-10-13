/**
 * TypeScript Data Contracts matching backend OpenAPI Schema (docs/openapi.json)
 */

export interface EnvelopeMeta {
  niche?: string;
  sample_size: number;
  as_of: string;
  data_mode: 'demo' | 'synthetic' | 'real' | 'mixed' | string;
  sources: string[];
  limitations: string[];
}

export interface EvidenceEnvelope<T> {
  data: T;
  meta: EnvelopeMeta;
}

export interface Product {
  asin: string;
  product_name: string;
  category: string;
  brand: string;
  price?: number | null;
  mrp?: number | null;
  discount_pct?: number | null;
  rating?: number | null;
  review_count: number;
  colour?: string | null;
  material?: string | null;
  pattern?: string | null;
  sizes: string[];
  seller?: string | null;
  availability?: string | null;
  product_url?: string | null;
  source: string;
  collected_at: string;
  // Position / percentiles when viewed in product details
  price_percentile?: number | null;
  rating_percentile?: number | null;
  quality_flags?: string[];
}

export interface ProductListResponse {
  items: Product[];
  total: number;
  page: number;
  page_size: number;
}

export interface Category {
  id?: number;
  name: string;
  display_name: string;
  active: boolean;
  product_count: number;
  last_updated?: string | null;
  data_mode: string;
}

export interface NicheFilter {
  category?: string;
  price_min?: number | null;
  price_max?: number | null;
  brands?: string[];
  colours?: string[];
  materials?: string[];
  patterns?: string[];
  sizes?: string[];
  min_rating?: number | null;
  min_reviews?: number | null;
  availability?: string | null;
  keyword?: string | null;
}

export interface Niche {
  id: string;
  name: string;
  category: string;
  description?: string;
  filter: NicheFilter;
  sample_size?: number;
  created_at?: string;
}

export interface MarketSummary {
  sample_size: number;
  price: {
    min: number | null;
    p25: number | null;
    median: number | null;
    p75: number | null;
    max: number | null;
    mean: number | null;
  };
  rating: {
    median: number | null;
    mean: number | null;
    unrated_count: number;
    distribution: Record<string, number>;
  };
  discount: {
    median: number | null;
    mean: number | null;
    zero_discount_count: number;
    deep_discount_count: number;
  };
  price_bands: Record<string, number>;
  brands: {
    unique_count: number;
    top_brands: Record<string, number>;
    top_5_share_pct: number | null;
  };
  colours: Record<string, number>;
  materials: Record<string, number>;
  patterns: Record<string, number>;
  sizes: Record<string, number>;
  availability: Record<string, number>;
  sellers: {
    unique_count: number;
    top_sellers: Record<string, number>;
  };
  completeness: Record<string, number>;
  concentration: {
    top_10_pct_listing_share: number | null;
    interpretation: string;
  };
}

export interface PreliminaryInsight {
  rule_id: string;
  rule_name: string;
  observation: string;
  hypothesis: string;
  evidence: Record<string, any>;
  sample_size: number;
  confidence: 'very_low' | 'low' | 'moderate' | string;
  limitations: string[];
}

export interface OpportunityAnalysis {
  sample_size: number;
  suppressed: boolean;
  suppression_reason?: string | null;
  insights: PreliminaryInsight[];
}

export interface ReviewItem {
  review_id: string;
  product_id: string;
  rating: number;
  review_title?: string | null;
  review_text?: string | null;
  review_date?: string | null;
  source: string;
  collected_at: string;
}

export interface ReviewSummary {
  total_reviews: number;
  avg_rating: number | null;
  rating_distribution: Record<string, number>;
  orphan_review_count: number;
  coverage_pct: number;
  sentiment_planned_notice: string;
}

export interface ReviewListResponse {
  items: ReviewItem[];
  total: number;
  page: number;
  page_size: number;
}

export interface Recommendation {
  id: string;
  rule_name: string;
  title: string;
  category: string;
  recommendation_type: string;
  confidence: 'very_low' | 'low' | 'moderate' | string;
  n: number;
  threshold_values: Record<string, any>;
  computed_evidence: Record<string, any>;
  why_this: string;
  sourcing_specs?: Record<string, string> | null;
  limitations: string[];
}

export interface RecommendationListResponse {
  items: Recommendation[];
  total: number;
}

export interface ChatRequest {
  question: string;
  niche_id?: string;
  niche_filter?: NicheFilter;
}

export interface ChatEvidenceItem {
  metric: string;
  value: any;
  n: number;
  tool: string;
  niche: string;
}

export interface ChatResponse {
  answer: string;
  evidence: ChatEvidenceItem[];
  confidence: 'very_low' | 'low' | 'moderate' | string;
  limitations: string[];
  follow_up_suggestions: string[];
  mode: 'gemini' | 'demo';
}

export interface UserProfile {
  name: string;
  age: number | string;
  gender: 'Female' | 'Male' | 'Non-binary' | 'Prefer not to say' | string;
  email: string;
  phone: string;
  address: string;
  city: string;
  state: string;
  pincode: string;
  businessName: string;
  sellerCategory: string;
  isVerified: boolean;
  registeredAt?: string;
}
