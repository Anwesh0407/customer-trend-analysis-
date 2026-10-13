import { useState, useEffect } from 'react';
import type { Product, ReviewItem } from '../types';
import { api } from '../services/api';
import { ObservationEstimateBadge } from '../components/Badges';
import {
  FileText,
  ExternalLink,
  Star,
  ArrowLeft,
  Package,
  Sparkles,
} from 'lucide-react';

interface ProductDetailsWorkspaceProps {
  product: Product | null;
  onBack: () => void;
  onSelectSimilar: (product: Product) => void;
}

export function ProductDetailsWorkspace({
  product,
  onBack,
  onSelectSimilar,
}: ProductDetailsWorkspaceProps) {
  const [similarProducts, setSimilarProducts] = useState<Product[]>([]);
  const [reviews, setReviews] = useState<ReviewItem[]>([]);
  const [activeTab, setActiveTab] = useState<'overview' | 'attributes' | 'reviews'>('overview');

  useEffect(() => {
    if (!product) return;

    let isMounted = true;

    Promise.all([
      api.getSimilarProducts(product.asin),
      api.getReviews({ asin: product.asin }),
    ])
      .then(([simRes, revRes]) => {
        if (!isMounted) return;
        setSimilarProducts(simRes.similar_products || []);
        if (revRes?.data?.items) {
          setReviews(revRes.data.items);
        }
      })
      .catch((e) => console.warn('Could not load product extras:', e));

    return () => {
      isMounted = false;
    };
  }, [product]);

  if (!product) {
    return (
      <div className="bg-white p-12 text-center rounded-xl border border-[#e2e8f0] shadow-sm">
        <Package size={36} className="mx-auto text-gray-300 mb-2" />
        <h3 className="text-base font-bold text-gray-800">No Product Selected</h3>
        <p className="text-xs text-gray-500 mt-1 mb-4">
          Select a product from Market Results to inspect all 18 attributes and benchmark percentiles.
        </p>
        <button
          type="button"
          onClick={onBack}
          className="px-4 py-2 bg-[#ff9900] hover:bg-[#f08800] text-[#131921] text-xs font-bold rounded-lg shadow-sm transition"
        >
          Go to Market Results
        </button>
      </div>
    );
  }

  return (
    <div className="space-y-6">
      {/* Top Breadcrumb & Back Action */}
      <div className="flex flex-wrap items-center justify-between gap-4 pb-2 border-b border-[#e2e8f0]">
        <button
          type="button"
          onClick={onBack}
          className="inline-flex items-center gap-1.5 text-xs font-bold text-gray-700 hover:text-black transition cursor-pointer"
        >
          <ArrowLeft size={16} />
          <span>Back to Market Results</span>
        </button>

        <div className="flex items-center gap-2">
          <span className="font-mono text-xs bg-[#f2f3ff] text-[#131b2e] px-2.5 py-1 rounded border border-[#dae2fd] font-bold">
            ASIN: {product.asin}
          </span>
          <ObservationEstimateBadge type="observation" />
        </div>
      </div>

      {/* Main Product Hero (Exact Stitch Design) */}
      <div className="bg-white rounded-xl border border-[#e2e8f0] shadow-sm p-6 space-y-4">
        {/* Badges & Identity */}
        <div className="flex items-center gap-2 flex-wrap text-xs font-mono text-[#75777c]">
          <span className="px-2 py-0.5 rounded bg-[#f2f3ff] text-[#131b2e] font-semibold">
            Brand: {product.brand}
          </span>
          <span>•</span>
          <span className="text-[#131b2e]">ASIN: {product.asin}</span>
          <span>•</span>
          <span className="text-[#8a5100] font-semibold flex items-center gap-1">
            <Sparkles size={13} />
            Verified Catalog Snapshot
          </span>
        </div>

        {/* Title & Price Header */}
        <div className="flex flex-col md:flex-row justify-between items-start gap-4">
          <div className="max-w-3xl">
            <h1 className="text-xl font-bold text-[#131b2e] tracking-tight leading-snug">
              {product.product_name}
            </h1>

            {/* Stars Block */}
            <div className="flex items-center gap-2 mt-2 text-xs">
              <div className="flex items-center text-[#ff9900]">
                <Star size={15} className="fill-[#ff9900]" />
              </div>
              <span className="font-mono font-bold text-sm text-[#131b2e]">
                {product.rating ? `${product.rating} out of 5` : 'Unrated'}
              </span>
              <span className="font-mono text-gray-500">
                ({product.review_count.toLocaleString()} customer ratings)
              </span>
            </div>
          </div>

          <div className="text-right shrink-0">
            {product.product_url && (
              <a
                href={product.product_url}
                target="_blank"
                rel="noopener noreferrer"
                className="text-xs text-[#8a5100] hover:underline font-bold inline-flex items-center gap-1"
              >
                <span>View Amazon Listing</span>
                <ExternalLink size={12} />
              </a>
            )}
          </div>
        </div>

        {/* Tab Bar (Stitch Design) */}
        <div className="flex items-center gap-2 border-b border-[#e2e8f0] pb-1 pt-2 text-xs">
          <button
            type="button"
            onClick={() => setActiveTab('overview')}
            className={`px-3 py-1 rounded font-semibold transition cursor-pointer ${
              activeTab === 'overview'
                ? 'bg-[#131921] text-white'
                : 'text-gray-600 hover:bg-[#f2f3ff]'
            }`}
          >
            Overview & Pricing
          </button>
          <button
            type="button"
            onClick={() => setActiveTab('attributes')}
            className={`px-3 py-1 rounded font-semibold transition cursor-pointer ${
              activeTab === 'attributes'
                ? 'bg-[#131921] text-white'
                : 'text-gray-600 hover:bg-[#f2f3ff]'
            }`}
          >
            18 Attributes & Specs
          </button>
          <button
            type="button"
            onClick={() => setActiveTab('reviews')}
            className={`px-3 py-1 rounded font-semibold transition cursor-pointer ${
              activeTab === 'reviews'
                ? 'bg-[#131921] text-white'
                : 'text-gray-600 hover:bg-[#f2f3ff]'
            }`}
          >
            Reviews & Customer Feedback ({reviews.length})
          </button>
        </div>

        {/* Pricing Diagnostic Box (Stitch Design) */}
        <div className="p-4 rounded-xl bg-[#f2f3ff] border border-[#dae2fd] flex flex-col sm:flex-row sm:items-center justify-between gap-4">
          <div className="flex flex-col">
            <span className="text-[10px] font-bold uppercase tracking-wider text-[#75777c]">
              Observed Catalog Price
            </span>
            <div className="flex items-baseline gap-2.5 mt-1">
              <span className="font-mono text-3xl font-bold text-[#131b2e]">
                {product.price ? `₹${product.price}` : 'Unlisted'}
              </span>
              {product.mrp && (
                <span className="font-mono text-sm text-gray-400 line-through">
                  MRP ₹{product.mrp}
                </span>
              )}
              {product.discount_pct !== null && product.discount_pct !== undefined && (
                <span className="px-2 py-0.5 rounded bg-[#ffdcbd] text-[#2c1600] font-mono text-xs font-bold">
                  {product.discount_pct}% off
                </span>
              )}
            </div>
          </div>

          <div className="flex flex-col text-left sm:text-right sm:border-l sm:border-[#dae2fd] sm:pl-4">
            <span className="text-[10px] font-bold uppercase tracking-wider text-[#75777c]">
              Stock Status
            </span>
            <span className="font-mono text-sm font-bold text-emerald-800 uppercase mt-1">
              {product.availability || 'in_stock'}
            </span>
            <span className="text-[11px] text-gray-500">
              Seller: <strong className="text-gray-800">{product.seller || 'Direct'}</strong>
            </span>
          </div>
        </div>
      </div>

      {/* Grid: 18 Canonical Attributes (2 cols) + Similar Benchmarks (1 col) */}
      <div className="grid grid-cols-1 lg:grid-cols-12 gap-6 items-start">
        {/* 18 Canonical Product Attributes (8 cols) */}
        <div className="lg:col-span-8 bg-white rounded-xl border border-[#e2e8f0] shadow-sm p-6 space-y-4">
          <div className="flex items-center justify-between pb-2 border-b border-gray-100">
            <span className="text-xs font-bold uppercase tracking-wider text-[#131b2e] flex items-center gap-1.5">
              <FileText size={16} className="text-[#ff9900]" />
              18 Canonical Catalog Attributes
            </span>
            <span className="text-[11px] text-gray-400 font-mono">Pydantic Validated</span>
          </div>

          <div className="grid grid-cols-1 sm:grid-cols-2 gap-3 text-xs font-sans">
            {[
              { label: '1. ASIN', val: product.asin, mono: true },
              { label: '2. Product Name', val: product.product_name },
              { label: '3. Category', val: product.category },
              { label: '4. Brand', val: product.brand },
              { label: '5. Price (INR)', val: product.price ? `₹${product.price}` : '—', mono: true },
              { label: '6. MRP (INR)', val: product.mrp ? `₹${product.mrp}` : '—', mono: true },
              { label: '7. Discount %', val: `${product.discount_pct ?? 0}%`, mono: true },
              { label: '8. Rating', val: product.rating ? `${product.rating} ★` : '—' },
              { label: '9. Review Count', val: product.review_count.toLocaleString(), mono: true },
              { label: '10. Colour', val: product.colour || 'Unspecified' },
              { label: '11. Material', val: product.material || 'Unspecified' },
              { label: '12. Pattern', val: product.pattern || 'Unspecified' },
              { label: '13. Sizes', val: product.sizes?.join(', ') || '—' },
              { label: '14. Seller', val: product.seller || 'Unspecified' },
              { label: '15. Availability', val: product.availability || 'unknown' },
              { label: '16. Product URL', val: product.product_url || '—', mono: true },
              { label: '17. Source', val: product.source, mono: true },
              { label: '18. Collected At', val: new Date(product.collected_at).toLocaleDateString(), mono: true },
            ].map((f) => (
              <div key={f.label} className="p-3 rounded-lg bg-[#f2f3ff] border border-[#dae2fd] space-y-0.5">
                <span className="text-[10px] font-bold uppercase text-[#75777c] font-mono block">
                  {f.label}
                </span>
                <span className={`text-[#131b2e] font-semibold truncate block ${f.mono ? 'font-mono' : ''}`}>
                  {f.val}
                </span>
              </div>
            ))}
          </div>
        </div>

        {/* Similar Listings Benchmark (4 cols) */}
        <div className="lg:col-span-4 space-y-4">
          <div className="bg-white rounded-xl border border-[#e2e8f0] shadow-sm p-5 space-y-3">
            <div className="flex items-center justify-between pb-2 border-b border-gray-100">
              <span className="text-xs font-bold uppercase tracking-wider text-[#131b2e]">
                Benchmark Listings
              </span>
              <span className="text-[11px] font-mono text-gray-500">n={similarProducts.length}</span>
            </div>
            <p className="text-[11px] text-gray-500 leading-relaxed">
              Competitor listings sharing category, fabric ({product.material}), and comparable price band.
            </p>

            {similarProducts.length === 0 ? (
              <p className="text-xs text-gray-400 italic">No similar listings in current sample.</p>
            ) : (
              <div className="space-y-2">
                {similarProducts.map((sim) => (
                  <div
                    key={sim.asin}
                    onClick={() => onSelectSimilar(sim)}
                    className="p-3 rounded-lg border border-[#e2e8f0] hover:border-[#ff9900] hover:bg-[#f2f3ff] transition cursor-pointer"
                  >
                    <div className="flex items-center justify-between font-mono text-xs">
                      <span className="font-bold text-[#131b2e]">{sim.asin}</span>
                      <span className="font-bold text-[#8a5100]">₹{sim.price}</span>
                    </div>
                    <p className="text-xs text-gray-700 truncate mt-1">{sim.product_name}</p>
                    <div className="mt-1 flex items-center justify-between text-[10px] text-gray-500">
                      <span>{sim.brand}</span>
                      <span className="font-mono text-amber-700 font-bold">{sim.rating ? `${sim.rating}★` : '—'}</span>
                    </div>
                  </div>
                ))}
              </div>
            )}
          </div>

          {/* ASIN Customer Feedback */}
          <div className="bg-white rounded-xl border border-[#e2e8f0] shadow-sm p-5 space-y-3">
            <span className="text-xs font-bold uppercase tracking-wider text-[#131b2e] block pb-2 border-b border-gray-100">
              ASIN Customer Feedback ({reviews.length})
            </span>

            {reviews.length === 0 ? (
              <p className="text-xs text-gray-400 italic">No text reviews on record for this ASIN.</p>
            ) : (
              <div className="space-y-2 max-h-60 overflow-y-auto">
                {reviews.map((r) => (
                  <div key={r.review_id} className="p-2.5 rounded bg-[#f2f3ff] text-xs space-y-1">
                    <div className="flex items-center justify-between">
                      <span className="font-bold text-[#ff9900]">{r.rating}.0 ★</span>
                      <span className="text-[10px] text-gray-400 font-mono">{r.review_date}</span>
                    </div>
                    <p className="font-bold text-gray-800">{r.review_title}</p>
                    <p className="text-gray-600 line-clamp-2">{r.review_text}</p>
                  </div>
                ))}
              </div>
            )}
          </div>
        </div>
      </div>
    </div>
  );
}
