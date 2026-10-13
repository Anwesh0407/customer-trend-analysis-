import type {
  Product,
  ReviewInsight,
  AnalyticsOverview,
  PriceAnalytics,
  AttributeBreakdown,
  Recommendation
} from '../types';

const API_BASE = '/api';

export const api = {
  async getHealth() {
    try {
      const res = await fetch(`${API_BASE}/health`);
      if (!res.ok) throw new Error('Health check failed');
      return await res.json();
    } catch (e) {
      console.warn('Backend offline or health unreachable:', e);
      return { status: 'offline', mode: 'frontend_standalone_fallback' };
    }
  },

  async getProducts(params: Record<string, any> = {}): Promise<{ total: number; items: Product[] }> {
    try {
      const query = new URLSearchParams();
      Object.entries(params).forEach(([k, v]) => {
        if (v !== undefined && v !== null && v !== '') {
          query.append(k, String(v));
        }
      });
      const res = await fetch(`${API_BASE}/products?${query.toString()}`);
      if (!res.ok) throw new Error('Failed to fetch products');
      return await res.json();
    } catch (e) {
      console.warn('Falling back to local products:', e);
      return { total: 0, items: [] };
    }
  },

  async getProduct(asin: string): Promise<Product | null> {
    try {
      const res = await fetch(`${API_BASE}/products/${asin}`);
      if (!res.ok) throw new Error('Product not found');
      return await res.json();
    } catch (e) {
      return null;
    }
  },

  async getAnalyticsOverview(): Promise<AnalyticsOverview | null> {
    try {
      const res = await fetch(`${API_BASE}/analytics/overview`);
      if (!res.ok) throw new Error('Failed to fetch analytics');
      return await res.json();
    } catch (e) {
      return null;
    }
  },

  async getPriceAnalytics(): Promise<PriceAnalytics | null> {
    try {
      const res = await fetch(`${API_BASE}/analytics/prices`);
      if (!res.ok) throw new Error('Failed to fetch price analytics');
      return await res.json();
    } catch (e) {
      return null;
    }
  },

  async getAttributeAnalytics(): Promise<AttributeBreakdown | null> {
    try {
      const res = await fetch(`${API_BASE}/analytics/attributes`);
      if (!res.ok) throw new Error('Failed to fetch attribute analytics');
      return await res.json();
    } catch (e) {
      return null;
    }
  },

  async getReviews(productId?: string): Promise<ReviewInsight | null> {
    try {
      const url = productId ? `${API_BASE}/reviews?product_id=${productId}` : `${API_BASE}/reviews`;
      const res = await fetch(url);
      if (!res.ok) throw new Error('Failed to fetch reviews');
      return await res.json();
    } catch (e) {
      return null;
    }
  },

  async getRecommendations(): Promise<{ total_recommendations: number; items: Recommendation[] } | null> {
    try {
      const res = await fetch(`${API_BASE}/recommendations`);
      if (!res.ok) throw new Error('Failed to fetch recommendations');
      return await res.json();
    } catch (e) {
      return null;
    }
  },

  async chat(message: string, productId?: string) {
    try {
      const res = await fetch(`${API_BASE}/assistant/chat`, {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify({
          message,
          product_id: productId,
          context_type: productId ? 'product' : 'market'
        })
      });
      if (!res.ok) throw new Error('Failed to chat');
      return await res.json();
    } catch (e) {
      return {
        reply: "I am currently in local fallback mode. Here is a market observation: Women's pure cotton straight kurtas in ₹849–₹949 with Indigo Blue & Maroon prints show optimal margin and customer satisfaction.",
        grounded_evidence: ["Scope: Odisha & Eastern India Kurtas", "Local Fallback Mode active"],
        suggested_actions: ["Check pricing sweet spots", "Review sizing charts"],
        mode: "local_fallback"
      };
    }
  }
};
