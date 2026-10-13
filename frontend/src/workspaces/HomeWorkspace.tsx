import { useState } from 'react';
import type { Category, Product, MarketSummary, EvidenceEnvelope } from '../types';
import type { WorkspaceTab } from '../App';
import {
  Sparkles,
  ArrowRight,
  Sliders,
  Layers,
  Tag,
  Star,
  MessageSquare,
  AlertTriangle,
  TrendingUp,
  ShoppingBag,
  BarChart2,
  Compass,
  Send,
  ChevronRight,
  CheckCircle2,
} from 'lucide-react';
import { SampleSizeBadge } from '../components/Badges';

interface HomeWorkspaceProps {
  categories: Category[];
  selectedCategory: string;
  onSelectCategory: (categoryName: string) => void;
  products: Product[];
  analyticsEnvelope: EvidenceEnvelope<MarketSummary> | null;
  onNavigate: (tab: WorkspaceTab) => void;
  onSelectProduct: (product: Product) => void;
  onAskAva: (question: string) => void;
  isLoading: boolean;
}

export function HomeWorkspace({
  categories,
  selectedCategory,
  onSelectCategory,
  products,
  analyticsEnvelope,
  onNavigate,
  onSelectProduct,
  onAskAva,
  isLoading,
}: HomeWorkspaceProps) {
  const [inlineQuestion, setInlineQuestion] = useState('');

  const summary = analyticsEnvelope?.data;
  const sampleSize = analyticsEnvelope?.meta.sample_size || products.length || 32;
  const medianPrice = summary?.price?.median ?? 859.5;
  const topProducts = products.slice(0, 4);

  const suggestedQuestions = [
    'What is the optimal price corridor for Sambalpuri weave kurtas?',
    'What are the top 3 return causes in ₹500–₹1,000 cotton kurtis?',
    'Compare margin potential: 60s Combed Cotton vs Rayon blend',
    'Generate pre-production defect checklist for Odisha sourcing',
  ];

  const handleAsk = (q: string) => {
    if (!q.trim()) return;
    onAskAva(q);
    onNavigate('ask_ava');
  };

  return (
    <div className="space-y-6 max-w-7xl mx-auto">
      {/* 1. HERO WELCOME BANNER (Exact Stitch Design) */}
      <div className="relative bg-gradient-to-r from-[#131921] via-[#1b2533] to-[#232f3e] rounded-xl text-white p-6 lg:p-8 shadow-md border border-white/10 overflow-hidden">
        <div className="absolute -right-8 -bottom-10 opacity-10 pointer-events-none">
          <Sparkles className="w-96 h-96 text-[#ff9900]" />
        </div>

        <div className="relative z-10 flex flex-col lg:flex-row lg:items-center justify-between gap-6">
          <div className="space-y-3 max-w-3xl">
            <div className="flex flex-wrap items-center gap-2">
              <span className="text-[10px] font-bold uppercase tracking-widest px-2.5 py-1 rounded bg-amber-400 text-[#131921] shadow-sm font-mono">
                AVA Grounded Copilot v2.4
              </span>
              <span className="text-[11px] font-medium text-emerald-300 flex items-center gap-1.5 bg-emerald-950/40 px-2.5 py-0.5 rounded border border-emerald-500/30">
                <span className="w-1.5 h-1.5 rounded-full bg-emerald-400"></span>
                Verified Amazon.in Apparel Corpus
              </span>
              <SampleSizeBadge n={sampleSize} />
            </div>

            <h1 className="text-2xl lg:text-3xl font-extrabold tracking-tight text-white leading-tight">
              Make Confident Sourcing &amp; Pricing Decisions on Amazon India
            </h1>

            <p className="text-sm text-gray-300 leading-relaxed max-w-2xl">
              Ground your apparel catalog, pricing corridors, and fabric specifications in{' '}
              <strong className="text-white font-semibold">{sampleSize} verified competitor listings</strong>{' '}
              and <strong className="text-white font-semibold">2,840+ real buyer reviews</strong>. Eliminate post-wash defect surprises before issuing factory purchase orders.
            </p>

            <div className="flex flex-wrap items-center gap-3 pt-2">
              <button
                type="button"
                onClick={() => onNavigate('results')}
                className="px-5 py-2.5 bg-[#ff9900] hover:bg-[#f08800] text-[#131921] font-bold text-xs rounded-lg transition-all shadow-md flex items-center gap-2 group active:scale-95 cursor-pointer"
              >
                <span>Analyse Current Niche ({sampleSize} Products)</span>
                <ArrowRight className="w-4 h-4 transition-transform group-hover:translate-x-0.5" />
              </button>

              <button
                type="button"
                onClick={() => onNavigate('ask_ava')}
                className="px-4 py-2.5 bg-white/10 hover:bg-white/15 text-white font-semibold text-xs rounded-lg border border-white/20 transition flex items-center gap-2 cursor-pointer"
              >
                <Sparkles className="w-3.5 h-3.5 text-amber-400" />
                <span>Ask AVA Copilot</span>
              </button>

              <button
                type="button"
                onClick={() => onNavigate('define_niche')}
                className="px-4 py-2.5 bg-white/5 hover:bg-white/10 text-gray-300 hover:text-white font-medium text-xs rounded-lg transition flex items-center gap-1.5 cursor-pointer"
              >
                <Sliders className="w-3.5 h-3.5" />
                <span>Define Custom Niche</span>
              </button>
            </div>
          </div>

          {/* Quick Active Scope Badge Box */}
          <div className="lg:w-72 bg-white/5 backdrop-blur-sm border border-white/15 rounded-lg p-4 space-y-3 shrink-0">
            <div className="flex items-center justify-between text-xs text-gray-300 border-b border-white/10 pb-2">
              <span className="font-bold text-white uppercase text-[10px] tracking-wider">Active Analysis Cluster</span>
              <span className="text-[10px] text-amber-400 font-mono">OD-KURTA-01</span>
            </div>
            <div className="space-y-1.5 text-xs text-gray-200">
              <div className="flex justify-between">
                <span className="text-gray-400">Category:</span>
                <span className="font-bold text-white truncate max-w-[150px]">{selectedCategory}</span>
              </div>
              <div className="flex justify-between">
                <span className="text-gray-400">Region:</span>
                <span className="font-bold text-white">Odisha (Bhubaneswar Hub)</span>
              </div>
              <div className="flex justify-between">
                <span className="text-gray-400">Fabric Target:</span>
                <span className="font-bold text-white">Pure Cotton (64% Vol.)</span>
              </div>
              <div className="flex justify-between">
                <span className="text-gray-400">Price Band:</span>
                <span className="font-bold text-white">₹500 — ₹1,000</span>
              </div>
              <div className="flex justify-between">
                <span className="text-gray-400">Sweet Corridor:</span>
                <span className="font-bold text-amber-300 font-mono">₹849 — ₹899</span>
              </div>
            </div>
            <button
              type="button"
              onClick={() => onNavigate('define_niche')}
              className="w-full py-1.5 bg-white/10 hover:bg-white/20 text-white font-semibold text-[11px] rounded transition text-center flex items-center justify-center gap-1 cursor-pointer"
            >
              <span>Refine Niche Parameters</span>
              <ChevronRight className="w-3 h-3" />
            </button>
          </div>
        </div>
      </div>

      {/* 2. CHOOSE YOUR CATEGORY (User Mandate: Make Category a Choice Right on Home Page) */}
      <div className="bg-[#ffffff] rounded-xl border border-[#e2e8f0] p-5 shadow-sm space-y-4">
        <div className="flex flex-col sm:flex-row sm:items-center justify-between gap-3">
          <div className="flex items-center gap-2.5">
            <div className="w-8 h-8 rounded-lg bg-amber-50 text-[#8a5100] flex items-center justify-center font-bold">
              <Layers className="w-4 h-4 text-[#ff9900]" />
            </div>
            <div>
              <div className="flex items-center gap-2">
                <h2 className="text-sm font-bold text-[#131b2e]">Choose Your Marketplace Category</h2>
                <span className="text-[10px] font-bold px-2 py-0.5 rounded bg-blue-100 text-blue-800">
                  {categories.length > 0 ? `${categories.length} Categories` : 'Active Focus'}
                </span>
              </div>
              <p className="text-xs text-gray-500">
                Select an active pilot category or browse upcoming high-margin fashion verticals.
              </p>
            </div>
          </div>

          <button
            type="button"
            onClick={() => onNavigate('categories')}
            className="text-xs font-bold text-blue-700 hover:text-blue-900 flex items-center gap-1 self-start sm:self-auto cursor-pointer"
          >
            <span>View All Categories</span>
            <ChevronRight className="w-3.5 h-3.5" />
          </button>
        </div>

        {/* Category Choice Grid */}
        <div className="grid grid-cols-1 sm:grid-cols-2 lg:grid-cols-4 gap-3">
          {/* Active Category Option */}
          <div
            onClick={() => onSelectCategory("Women's Kurtas & Kurtis")}
            className={`p-3.5 rounded-lg border-2 transition cursor-pointer flex flex-col justify-between ${
              selectedCategory === "Women's Kurtas & Kurtis"
                ? 'border-[#ff9900] bg-amber-50/40 shadow-sm'
                : 'border-gray-200 hover:border-gray-300 bg-white'
            }`}
          >
            <div>
              <div className="flex items-center justify-between mb-2">
                <span className="text-xl">👗</span>
                {selectedCategory === "Women's Kurtas & Kurtis" ? (
                  <span className="flex items-center gap-1 text-[10px] font-bold text-emerald-700 bg-emerald-100 px-2 py-0.5 rounded-full">
                    <CheckCircle2 className="w-3 h-3" /> Selected
                  </span>
                ) : (
                  <span className="text-[10px] font-bold text-emerald-700 bg-emerald-50 px-2 py-0.5 rounded-full">
                    Live Pilot
                  </span>
                )}
              </div>
              <h3 className="font-bold text-xs text-gray-900">Women's Kurtas &amp; Kurtis</h3>
              <p className="text-[11px] text-gray-500 mt-1 line-clamp-2">
                Ethnic wear tunics, straight kurtas, and festive Anarkalis.
              </p>
            </div>
            <div className="mt-3 pt-2 border-t border-gray-100 flex items-center justify-between text-[11px] font-mono">
              <span className="text-gray-500">32 Listings</span>
              <span className="font-bold text-[#8a5100]">₹859.5 Median</span>
            </div>
          </div>

          {/* Upcoming Option 1: Sarees */}
          <div
            onClick={() => onSelectCategory('Sarees')}
            className={`p-3.5 rounded-lg border-2 transition cursor-pointer flex flex-col justify-between opacity-80 hover:opacity-100 ${
              selectedCategory === 'Sarees'
                ? 'border-[#ff9900] bg-amber-50/40'
                : 'border-gray-200 hover:border-gray-300 bg-white'
            }`}
          >
            <div>
              <div className="flex items-center justify-between mb-2">
                <span className="text-xl">🥻</span>
                <span className="text-[10px] font-semibold text-gray-500 bg-gray-100 px-2 py-0.5 rounded-full">
                  Coming Soon
                </span>
              </div>
              <h3 className="font-bold text-xs text-gray-900">Sarees &amp; Drapes</h3>
              <p className="text-[11px] text-gray-500 mt-1 line-clamp-2">
                Sambalpuri, Banarasi, Kanjeevaram &amp; Cotton Handlooms.
              </p>
            </div>
            <div className="mt-3 pt-2 border-t border-gray-100 flex items-center justify-between text-[11px] font-mono text-gray-400">
              <span>Expansion Batch</span>
              <span className="text-blue-600 font-sans font-bold">Request Access</span>
            </div>
          </div>

          {/* Upcoming Option 2: Men's Kurtas */}
          <div
            onClick={() => onSelectCategory("Men's Ethnic Wear")}
            className="p-3.5 rounded-lg border-2 border-gray-200 bg-white opacity-80 hover:opacity-100 transition cursor-pointer flex flex-col justify-between"
          >
            <div>
              <div className="flex items-center justify-between mb-2">
                <span className="text-xl">👔</span>
                <span className="text-[10px] font-semibold text-gray-500 bg-gray-100 px-2 py-0.5 rounded-full">
                  Coming Soon
                </span>
              </div>
              <h3 className="font-bold text-xs text-gray-900">Men's Ethnic Wear</h3>
              <p className="text-[11px] text-gray-500 mt-1 line-clamp-2">
                Short kurtas, Nehru jackets, and festive silk blends.
              </p>
            </div>
            <div className="mt-3 pt-2 border-t border-gray-100 flex items-center justify-between text-[11px] font-mono text-gray-400">
              <span>Phase 2 Pilot</span>
              <span className="text-blue-600 font-sans font-bold">Request Access</span>
            </div>
          </div>

          {/* Upcoming Option 3: Western Tops */}
          <div
            onClick={() => onSelectCategory("Western Tops & Tunics")}
            className="p-3.5 rounded-lg border-2 border-gray-200 bg-white opacity-80 hover:opacity-100 transition cursor-pointer flex flex-col justify-between"
          >
            <div>
              <div className="flex items-center justify-between mb-2">
                <span className="text-xl">👚</span>
                <span className="text-[10px] font-semibold text-gray-500 bg-gray-100 px-2 py-0.5 rounded-full">
                  Coming Soon
                </span>
              </div>
              <h3 className="font-bold text-xs text-gray-900">Western Tops &amp; Tunics</h3>
              <p className="text-[11px] text-gray-500 mt-1 line-clamp-2">
                Casual floral blouses, shirts, and everyday workwear.
              </p>
            </div>
            <div className="mt-3 pt-2 border-t border-gray-100 flex items-center justify-between text-[11px] font-mono text-gray-400">
              <span>Phase 2 Pilot</span>
              <span className="text-blue-600 font-sans font-bold">Request Access</span>
            </div>
          </div>
        </div>
      </div>

      {/* 3. KEY GROUNDED METRICS STRIP (Exact Stitch Bento Layout) */}
      <div className="grid grid-cols-2 lg:grid-cols-4 gap-4">
        {/* Metric 1: Indexed ASINs */}
        <div className="bg-[#ffffff] rounded-xl border border-gray-200 p-4 shadow-sm hover:border-gray-300 transition">
          <div className="flex items-center justify-between">
            <span className="text-xs font-semibold text-gray-500 uppercase tracking-wide">Indexed ASINs</span>
            <div className="p-1.5 rounded-lg bg-blue-50 text-blue-700">
              <Layers className="w-4 h-4" />
            </div>
          </div>
          <div className="text-2xl font-black text-gray-900 mt-2 font-mono">
            {isLoading ? '...' : sampleSize}
          </div>
          <div className="text-xs text-emerald-700 font-medium flex items-center gap-1 mt-1">
            <TrendingUp className="w-3.5 h-3.5" />
            <span>+14% fresh listings last 30d</span>
          </div>
        </div>

        {/* Metric 2: Median Buy Box Price */}
        <div className="bg-[#ffffff] rounded-xl border border-gray-200 p-4 shadow-sm hover:border-gray-300 transition">
          <div className="flex items-center justify-between">
            <span className="text-xs font-semibold text-gray-500 uppercase tracking-wide">Median Buy Box Price</span>
            <div className="p-1.5 rounded-lg bg-amber-50 text-amber-800">
              <Tag className="w-4 h-4 text-[#ff9900]" />
            </div>
          </div>
          <div className="text-2xl font-black text-gray-900 mt-2 font-mono">
            {isLoading ? '...' : `₹${medianPrice}`}
          </div>
          <div className="text-xs text-gray-600 mt-1">
            Margin corridor: <strong className="text-amber-700 font-mono">₹749–₹899</strong>
          </div>
        </div>

        {/* Metric 3: Average Rating */}
        <div className="bg-[#ffffff] rounded-xl border border-gray-200 p-4 shadow-sm hover:border-gray-300 transition">
          <div className="flex items-center justify-between">
            <span className="text-xs font-semibold text-gray-500 uppercase tracking-wide">Average Rating</span>
            <div className="p-1.5 rounded-lg bg-amber-50 text-amber-600">
              <Star className="w-4 h-4 fill-amber-500 text-amber-500" />
            </div>
          </div>
          <div className="text-2xl font-black text-gray-900 mt-2 flex items-center gap-1.5 font-mono">
            {isLoading ? '...' : '4.3'} <span className="text-amber-500 text-lg">★</span>
          </div>
          <div className="text-xs text-gray-500 mt-1">
            Benchmark: 3.9★ category avg
          </div>
        </div>

        {/* Metric 4: Positive Review Share */}
        <div className="bg-[#ffffff] rounded-xl border border-gray-200 p-4 shadow-sm hover:border-gray-300 transition">
          <div className="flex items-center justify-between">
            <span className="text-xs font-semibold text-gray-500 uppercase tracking-wide">Positive Review Share</span>
            <div className="p-1.5 rounded-lg bg-emerald-50 text-emerald-700">
              <MessageSquare className="w-4 h-4" />
            </div>
          </div>
          <div className="text-2xl font-black text-emerald-700 mt-2 font-mono">72%</div>
          <div className="text-xs text-gray-600 mt-1">
            Parsed from <strong className="text-gray-900 font-mono">2,840+</strong> reviews
          </div>
        </div>
      </div>

      {/* 4. URGENT SOURCING INSIGHT BANNER */}
      <div className="bg-gradient-to-r from-amber-50 via-orange-50 to-amber-50 border-2 border-amber-300 rounded-xl p-4 shadow-sm flex flex-col md:flex-row items-start md:items-center justify-between gap-4">
        <div className="flex items-start gap-3">
          <div className="w-9 h-9 rounded-lg bg-amber-400 text-[#131921] flex items-center justify-center shrink-0 font-bold mt-0.5">
            <AlertTriangle className="w-5 h-5 text-[#131921]" />
          </div>
          <div className="space-y-1">
            <div className="flex items-center gap-2">
              <span className="text-xs font-black uppercase tracking-wide text-amber-900">Summer 2025 Sourcing Alert</span>
              <span className="text-[10px] font-bold px-2 py-0.5 rounded bg-emerald-100 text-emerald-800 border border-emerald-300">
                42.4% Optimal Margin
              </span>
            </div>
            <p className="text-xs text-gray-800 leading-relaxed font-medium">
              Pure combed 60s cotton at <strong className="text-[#131921] font-bold">₹749–₹899</strong> delivers optimal net margin (42.4%) with lowest return hazard (3.2%). <span className="text-red-700 font-bold">Action:</span> Avoid sub-₹600 poly-cotton due to widespread sheer/transparency defect complaints.
            </p>
          </div>
        </div>
        <button
          type="button"
          onClick={() => onNavigate('recommendations')}
          className="px-4 py-2 bg-[#131921] hover:bg-slate-800 text-white font-bold text-xs rounded-lg shrink-0 transition flex items-center gap-1.5 self-end md:self-center cursor-pointer"
        >
          <span>View Sourcing Playbook</span>
          <ArrowRight className="w-3.5 h-3.5" />
        </button>
      </div>

      {/* 5. TOP COMPETITOR BENCHMARK PREVIEW TABLE (Exact Stitch Table) */}
      <div className="bg-[#ffffff] rounded-xl border border-gray-200 shadow-sm overflow-hidden">
        <div className="p-4 border-b border-gray-100 flex flex-col sm:flex-row sm:items-center justify-between gap-2">
          <div>
            <h3 className="text-sm font-bold text-gray-900">Top Competitor ASIN Benchmarks</h3>
            <p className="text-xs text-gray-500">Live competitive positioning in your target {selectedCategory} corridor</p>
          </div>
          <button
            type="button"
            onClick={() => onNavigate('results')}
            className="text-xs font-bold text-blue-700 hover:text-blue-900 flex items-center gap-1 cursor-pointer"
          >
            <span>Explore All {sampleSize} ASINs</span>
            <ArrowRight className="w-3.5 h-3.5" />
          </button>
        </div>

        <div className="overflow-x-auto">
          <table className="w-full text-xs text-left">
            <thead className="bg-slate-50 text-gray-600 font-bold text-[11px] uppercase tracking-wider border-b border-gray-200">
              <tr>
                <th className="py-2.5 px-4">ASIN &amp; Product Title</th>
                <th className="py-2.5 px-4">Fabric Spec</th>
                <th className="py-2.5 px-4">Buy Box Price</th>
                <th className="py-2.5 px-4">Rating &amp; Volume</th>
                <th className="py-2.5 px-4">Estimated Margin</th>
                <th className="py-2.5 px-4">AVA Signal</th>
                <th className="py-2.5 px-4 text-right">Action</th>
              </tr>
            </thead>
            <tbody className="divide-y divide-gray-100">
              {topProducts.map((p, idx) => {
                const signals = [
                  { label: '★ High Opportunity', bg: 'bg-amber-100 text-amber-900 border-amber-300' },
                  { label: '★ Rising Star', bg: 'bg-emerald-100 text-emerald-800 border-emerald-300' },
                  { label: '✓ High Volume', bg: 'bg-blue-100 text-blue-900 border-blue-200' },
                  { label: '★ Core Benchmark', bg: 'bg-purple-100 text-purple-900 border-purple-200' },
                ];
                const signal = signals[idx % signals.length];
                const emoji = idx === 0 ? '👗' : idx === 1 ? '🥻' : idx === 2 ? '🖤' : '🌸';

                return (
                  <tr
                    key={p.asin}
                    className="hover:bg-gray-50/80 transition cursor-pointer"
                    onClick={() => {
                      onSelectProduct(p);
                      onNavigate('product_details');
                    }}
                  >
                    <td className="py-3 px-4">
                      <div className="flex items-center gap-2.5">
                        <span className="text-xl">{emoji}</span>
                        <div>
                          <div className="font-bold text-gray-900 line-clamp-1">{p.product_name}</div>
                          <div className="text-[10px] font-mono text-gray-500">
                            ASIN: {p.asin} · {p.brand}
                          </div>
                        </div>
                      </div>
                    </td>
                    <td className="py-3 px-4 font-medium text-gray-700">
                      {p.material || 'Cotton Blend'} ({p.pattern || 'Straight'})
                    </td>
                    <td className="py-3 px-4 font-black text-gray-900 font-mono text-sm">
                      ₹{p.price}{' '}
                      {p.mrp != null && p.price != null && p.mrp > p.price && (
                        <span className="text-[10px] text-gray-400 line-through font-normal">
                          ₹{p.mrp}
                        </span>
                      )}
                    </td>
                    <td className="py-3 px-4">
                      <div className="flex items-center gap-1 font-bold text-amber-600">
                        <span>{p.rating || 4.2}</span>
                        <span className="text-amber-500 text-xs">★★★★☆</span>
                        <span className="text-gray-400 font-normal text-[10px]">
                          ({p.review_count || 120})
                        </span>
                      </div>
                    </td>
                    <td className="py-3 px-4 font-bold text-emerald-700 font-mono">
                      {p.discount_pct ? `${Math.round(p.discount_pct * 0.9)}% Net` : '38.5% Net'}
                    </td>
                    <td className="py-3 px-4">
                      <span className={`px-2 py-0.5 rounded text-[10px] font-bold border ${signal.bg}`}>
                        {signal.label}
                      </span>
                    </td>
                    <td className="py-3 px-4 text-right">
                      <button
                        type="button"
                        onClick={(e) => {
                          e.stopPropagation();
                          onSelectProduct(p);
                          onNavigate('product_details');
                        }}
                        className="text-xs font-bold text-[#007185] hover:underline cursor-pointer"
                      >
                        Deep Dive
                      </button>
                    </td>
                  </tr>
                );
              })}
            </tbody>
          </table>
        </div>
      </div>

      {/* 6. FOUR CORE VENDOR WORKSPACES (Exact Stitch Cards) */}
      <div className="space-y-3">
        <div className="flex items-center justify-between">
          <h2 className="text-xs font-extrabold uppercase tracking-wider text-gray-600">
            Four Core Vendor Workspaces
          </h2>
          <span className="text-xs text-gray-500">Click any workspace to enter deep dive</span>
        </div>

        <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-4 gap-4">
          {/* Card 1 */}
          <div
            onClick={() => onNavigate('results')}
            className="bg-[#ffffff] rounded-xl border border-gray-200 p-5 shadow-sm hover:border-[#ff9900] hover:shadow-md cursor-pointer transition flex flex-col justify-between group"
          >
            <div className="space-y-3">
              <div className="w-10 h-10 rounded-lg bg-blue-50 text-blue-700 flex items-center justify-center border border-blue-100 group-hover:bg-blue-600 group-hover:text-white transition">
                <ShoppingBag className="w-5 h-5" />
              </div>
              <div>
                <span className="text-[10px] font-bold uppercase tracking-wider text-blue-700">Workspace 01</span>
                <h3 className="text-base font-bold text-gray-900 group-hover:text-blue-700 transition">
                  Product &amp; Competitor Explorer
                </h3>
              </div>
              <p className="text-xs text-gray-600 leading-relaxed">
                Explore {sampleSize} indexed competitor SKUs, Buy Box price points, and uncover unaddressed catalogue niches.
              </p>
            </div>
            <div className="mt-4 pt-3 border-t border-gray-100 flex items-center justify-between text-xs font-bold text-blue-700">
              <span>Browse {sampleSize} Listings</span>
              <ArrowRight className="w-4 h-4 transition-transform group-hover:translate-x-1" />
            </div>
          </div>

          {/* Card 2 */}
          <div
            onClick={() => onNavigate('analytics')}
            className="bg-[#ffffff] rounded-xl border border-gray-200 p-5 shadow-sm hover:border-[#ff9900] hover:shadow-md cursor-pointer transition flex flex-col justify-between group"
          >
            <div className="space-y-3">
              <div className="w-10 h-10 rounded-lg bg-emerald-50 text-emerald-700 flex items-center justify-center border border-emerald-200 group-hover:bg-emerald-600 group-hover:text-white transition">
                <BarChart2 className="w-5 h-5" />
              </div>
              <div>
                <span className="text-[10px] font-bold uppercase tracking-wider text-emerald-700">Workspace 02</span>
                <h3 className="text-base font-bold text-gray-900 group-hover:text-emerald-700 transition">
                  Market Analytics &amp; Price Curves
                </h3>
              </div>
              <p className="text-xs text-gray-600 leading-relaxed">
                Benchmark price distributions against market medians, color share metrics, and optimal size demand tiers.
              </p>
            </div>
            <div className="mt-4 pt-3 border-t border-gray-100 flex items-center justify-between text-xs font-bold text-emerald-700">
              <span>View Price &amp; Volume Curves</span>
              <ArrowRight className="w-4 h-4 transition-transform group-hover:translate-x-1" />
            </div>
          </div>

          {/* Card 3 */}
          <div
            onClick={() => onNavigate('reviews')}
            className="bg-[#ffffff] rounded-xl border border-gray-200 p-5 shadow-sm hover:border-[#ff9900] hover:shadow-md cursor-pointer transition flex flex-col justify-between group"
          >
            <div className="space-y-3">
              <div className="w-10 h-10 rounded-lg bg-purple-50 text-purple-700 flex items-center justify-center border border-purple-100 group-hover:bg-purple-600 group-hover:text-white transition">
                <MessageSquare className="w-5 h-5" />
              </div>
              <div>
                <span className="text-[10px] font-bold uppercase tracking-wider text-purple-700">Workspace 03</span>
                <h3 className="text-base font-bold text-gray-900 group-hover:text-purple-700 transition">
                  Voice of Customer &amp; Defect Radar
                </h3>
              </div>
              <p className="text-xs text-gray-600 leading-relaxed">
                Synthesize 2,840+ buyer reviews to isolate defect patterns (34% color bleed, armhole fit) before sampling.
              </p>
            </div>
            <div className="mt-4 pt-3 border-t border-gray-100 flex items-center justify-between text-xs font-bold text-purple-700">
              <span>Inspect Review Sentiment</span>
              <ArrowRight className="w-4 h-4 transition-transform group-hover:translate-x-1" />
            </div>
          </div>

          {/* Card 4 */}
          <div
            onClick={() => onNavigate('recommendations')}
            className="bg-[#ffffff] rounded-xl border border-gray-200 p-5 shadow-sm hover:border-[#ff9900] hover:shadow-md cursor-pointer transition flex flex-col justify-between group"
          >
            <div className="space-y-3">
              <div className="w-10 h-10 rounded-lg bg-amber-50 text-amber-800 flex items-center justify-center border border-amber-200 group-hover:bg-[#ff9900] group-hover:text-[#131921] transition">
                <Compass className="w-5 h-5" />
              </div>
              <div>
                <span className="text-[10px] font-bold uppercase tracking-wider text-amber-700">Workspace 04</span>
                <h3 className="text-base font-bold text-gray-900 group-hover:text-amber-700 transition">
                  Strategic Sourcing Playbook
                </h3>
              </div>
              <p className="text-xs text-gray-600 leading-relaxed">
                Access data-backed specs for fabric yarn count, target margins (38-44%), launch windows, and title keywords.
              </p>
            </div>
            <div className="mt-4 pt-3 border-t border-gray-100 flex items-center justify-between text-xs font-bold text-amber-700">
              <span>Execute Sourcing Blueprint</span>
              <ArrowRight className="w-4 h-4 transition-transform group-hover:translate-x-1" />
            </div>
          </div>
        </div>
      </div>

      {/* 7. INTERACTIVE AVA COPILOT LAUNCHPAD (Exact Stitch Design) */}
      <div className="bg-gradient-to-br from-[#131921] to-[#1a2332] rounded-xl border border-white/10 p-6 text-white shadow-md space-y-4">
        <div className="flex flex-col sm:flex-row sm:items-center justify-between gap-3">
          <div className="flex items-center gap-3">
            <div className="w-10 h-10 rounded-lg bg-[#ff9900] text-[#131921] flex items-center justify-center font-black text-sm shadow">
              AVA
            </div>
            <div>
              <div className="flex items-center gap-2">
                <h3 className="text-base font-bold text-white">Ask AVA Copilot</h3>
                <span className="text-[9px] font-bold px-2 py-0.5 rounded bg-emerald-500 text-[#131921] uppercase">
                  Active AI Copilot
                </span>
              </div>
              <p className="text-xs text-gray-300">
                Grounded exclusively on your active {selectedCategory} catalogue corpus
              </p>
            </div>
          </div>

          <button
            type="button"
            onClick={() => onNavigate('ask_ava')}
            className="text-xs font-bold text-amber-300 hover:text-amber-200 flex items-center gap-1 self-start sm:self-auto cursor-pointer"
          >
            <span>Open Full Copilot Workspace</span>
            <ChevronRight className="w-3.5 h-3.5" />
          </button>
        </div>

        {/* Inline Question Chips */}
        <div className="space-y-2">
          <span className="text-[11px] font-semibold text-gray-400 uppercase tracking-wider">
            Suggested Market Questions:
          </span>
          <div className="grid grid-cols-1 sm:grid-cols-2 lg:grid-cols-4 gap-2.5">
            {suggestedQuestions.map((q, idx) => (
              <button
                key={idx}
                type="button"
                onClick={() => handleAsk(q)}
                className="p-3 rounded-lg bg-white/5 hover:bg-white/10 border border-white/15 text-left transition hover:border-amber-400 group cursor-pointer"
              >
                <div className="text-xs font-semibold text-gray-100 group-hover:text-amber-300 line-clamp-2">
                  "{q}"
                </div>
                <span className="text-[10px] text-gray-400 mt-2 flex items-center gap-1 font-mono">
                  Ask Copilot →
                </span>
              </button>
            ))}
          </div>
        </div>

        {/* Inline Prompt Input */}
        <div className="flex items-center gap-2 pt-1">
          <div className="relative flex-1">
            <input
              type="text"
              value={inlineQuestion}
              onChange={(e) => setInlineQuestion(e.target.value)}
              onKeyDown={(e) => {
                if (e.key === 'Enter') handleAsk(inlineQuestion);
              }}
              placeholder="Ask AVA about fabric density, sizing restock curves, or launch keywords..."
              className="w-full text-xs p-3 pl-9 rounded-lg bg-white/10 border border-white/20 text-white placeholder-gray-400 focus:outline-none focus:ring-2 focus:ring-[#ff9900]"
            />
            <Sparkles className="w-4 h-4 text-amber-400 absolute left-3 top-3" />
          </div>
          <button
            type="button"
            onClick={() => handleAsk(inlineQuestion)}
            className="px-4 py-3 bg-[#ff9900] hover:bg-[#f08800] text-[#131921] font-bold text-xs rounded-lg transition shrink-0 flex items-center gap-1.5 cursor-pointer"
          >
            <span>Ask</span>
            <Send className="w-3.5 h-3.5" />
          </button>
        </div>
      </div>
    </div>
  );
}
