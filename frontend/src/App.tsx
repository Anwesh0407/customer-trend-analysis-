import React, { useState, useEffect } from 'react';
import {
  Sparkles,
  Search,
  ArrowRight,
  Compass,
  Sliders,
  ShoppingBag,
  BarChart2,
  Home,
  CheckCircle2,
  AlertCircle,
  X,
  Send,
  Lightbulb
} from 'lucide-react';
import { api } from './services/api';
import type { Product, ReviewInsight, AnalyticsOverview, PriceAnalytics, Recommendation, ChatMessage } from './types';

export function App() {
  const [activeTab, setActiveTab] = useState<'landing' | 'category' | 'niche' | 'results' | 'analytics' | 'product' | 'reviews' | 'recommendations'>('landing');
  
  // Niche State
  const [location, setLocation] = useState('Odisha');
  const [priceMax, setPriceMax] = useState(1000);
  const [selectedMaterial, setSelectedMaterial] = useState('Cotton');
  const [searchQuery, setSearchQuery] = useState('');
  const [sortBy, setSortBy] = useState('opportunity');

  // Data State
  const [products, setProducts] = useState<Product[]>([]);
  const [selectedProduct, setSelectedProduct] = useState<Product | null>(null);
  const [analytics, setAnalytics] = useState<AnalyticsOverview | null>(null);
  const [priceAnalytics, setPriceAnalytics] = useState<PriceAnalytics | null>(null);
  const [reviewsData, setReviewsData] = useState<ReviewInsight | null>(null);
  const [recommendations, setRecommendations] = useState<Recommendation[]>([]);
  const [backendStatus, setBackendStatus] = useState<{ status: string; mode?: string } | null>(null);

  // Assistant Chat State
  const [isChatOpen, setIsChatOpen] = useState(false);
  const [chatInput, setChatInput] = useState('');
  const [chatMessages, setChatMessages] = useState<ChatMessage[]>([
    {
      id: 'm1',
      sender: 'assistant',
      text: "Hello! I am **AVA**, your AI vendor assistant. I have analyzed women's Kurtas & Kurtis across Odisha and Eastern India. Ask me about pricing sweet spots, competitor weaknesses, or sourcing recommendations!",
      evidence: ["Scope: Odisha & Eastern India", "Market Median: ₹849", "Average Rating: 4.2 ★"],
      actions: ["What is the best price range to target?", "What do buyers complain about most?", "Which colors sell fastest?"]
    }
  ]);
  const [isTyping, setIsTyping] = useState(false);

  // Load initial backend data
  useEffect(() => {
    async function loadData() {
      const health = await api.getHealth();
      setBackendStatus(health);

      const [prodRes, anRes, prRes, revRes, recRes] = await Promise.all([
        api.getProducts({ max_price: priceMax, material: selectedMaterial !== 'All' ? selectedMaterial : undefined, sort: sortBy }),
        api.getAnalyticsOverview(),
        api.getPriceAnalytics(),
        api.getReviews(),
        api.getRecommendations()
      ]);

      if (prodRes && prodRes.items) {
        setProducts(prodRes.items);
        if (prodRes.items.length > 0) {
          setSelectedProduct(prodRes.items[0]);
        }
      }
      if (anRes) setAnalytics(anRes);
      if (prRes) setPriceAnalytics(prRes);
      if (revRes) setReviewsData(revRes);
      if (recRes && recRes.items) setRecommendations(recRes.items);
    }
    loadData();
  }, [priceMax, selectedMaterial, sortBy]);

  // Handle Search
  const handleSearch = async (e?: React.FormEvent) => {
    if (e) e.preventDefault();
    if (!searchQuery.trim()) {
      setActiveTab('results');
      return;
    }
    const res = await api.getProducts({ search: searchQuery });
    if (res && res.items) {
      setProducts(res.items);
    }
    setActiveTab('results');
  };

  // Handle Send Chat
  const handleSendMessage = async (customText?: string) => {
    const text = customText || chatInput;
    if (!text.trim()) return;

    const userMsg: ChatMessage = {
      id: String(Date.now()),
      sender: 'user',
      text: text
    };
    setChatMessages(prev => [...prev, userMsg]);
    if (!customText) setChatInput('');
    setIsTyping(true);

    const resp = await api.chat(text, selectedProduct?.asin);
    setIsTyping(false);

    const botMsg: ChatMessage = {
      id: String(Date.now() + 1),
      sender: 'assistant',
      text: resp.reply,
      evidence: resp.grounded_evidence,
      actions: resp.suggested_actions
    };
    setChatMessages(prev => [...prev, botMsg]);
  };

  const currentScopeSummary = `Kurtas & Kurtis · ${location} · ₹500–₹${priceMax.toLocaleString()} · ${selectedMaterial}`;

  return (
    <div className="min-h-screen bg-slate-50 text-gray-900 flex flex-col font-sans selection:bg-amber-200">
      {/* ============================================================== */}
      {/* 1. PERSISTENT GLOBAL HEADER (Amazon Navy #131921 Theme)       */}
      {/* ============================================================== */}
      <header className="sticky top-0 z-40 bg-[#131921] text-white shadow-md">
        {/* Top Strip */}
        <div className="max-w-7xl mx-auto px-4 py-2.5 flex items-center justify-between gap-3">
          {/* Brand Identity */}
          <div 
            onClick={() => setActiveTab('landing')}
            className="flex items-center gap-2.5 cursor-pointer select-none group"
          >
            <div className="w-8 h-8 rounded bg-gradient-to-br from-amber-400 to-[#ff9900] flex items-center justify-center font-black text-[#131921] text-base tracking-tighter shadow-sm border border-amber-300 group-hover:scale-105 transition-transform">
              AVA
            </div>
            <div>
              <div className="flex items-center gap-1.5 leading-none">
                <span className="font-extrabold text-sm tracking-tight text-white">VENDOR ASSIST</span>
                <span className="text-[9px] font-bold tracking-wider uppercase px-1.5 py-0.5 rounded bg-[#232f3e] text-amber-400 border border-white/10">PRO</span>
                {backendStatus?.status === 'ok' && (
                  <span className="hidden sm:inline-flex items-center gap-1 text-[9px] text-emerald-400 bg-emerald-950/60 px-1.5 py-0.5 rounded border border-emerald-500/30">
                    <span className="w-1.5 h-1.5 rounded-full bg-emerald-400 animate-pulse"></span> API Online
                  </span>
                )}
              </div>
              <p className="text-[9.5px] text-gray-300 mt-0.5 tracking-tight font-medium">Sell smarter. Sell what people want.</p>
            </div>
          </div>

          {/* Persistent Search Bar */}
          <form onSubmit={handleSearch} className="flex-1 max-w-xl mx-2 hidden md:block">
            <div className="relative flex items-center">
              <input
                type="text"
                value={searchQuery}
                onChange={e => setSearchQuery(e.target.value)}
                placeholder="Search kurtas, cotton fabrics, price sweet spots..."
                className="w-full h-8 pl-8 pr-12 text-xs rounded bg-white text-gray-900 border border-gray-300 focus:outline-none focus:ring-2 focus:ring-[#ff9900] shadow-inner"
              />
              <Search className="w-3.5 h-3.5 text-gray-500 absolute left-2.5 pointer-events-none" />
              <button
                type="submit"
                className="absolute right-0 h-8 px-3 bg-amber-400 hover:bg-amber-500 text-[#131921] font-bold rounded-r flex items-center justify-center transition"
              >
                <ArrowRight className="w-3.5 h-3.5 stroke-[2.5]" />
              </button>
            </div>
          </form>

          {/* Ask AVA Quick Trigger */}
          <div className="flex items-center gap-2">
            <button
              onClick={() => setIsChatOpen(true)}
              className="relative flex items-center gap-1.5 px-3 py-1.5 rounded-full bg-gradient-to-r from-amber-400 to-[#ff9900] text-[#131921] font-extrabold text-xs shadow-sm hover:brightness-105 active:scale-95 transition-all"
            >
              <Sparkles className="w-3.5 h-3.5 text-[#131921]" />
              <span>Ask AVA</span>
              <span className="w-2 h-2 rounded-full bg-emerald-700 animate-ping"></span>
            </button>
          </div>
        </div>

        {/* Mobile Search Bar Strip */}
        <div className="px-3.5 pb-2 md:hidden">
          <form onSubmit={handleSearch} className="relative flex items-center">
            <input
              type="text"
              value={searchQuery}
              onChange={e => setSearchQuery(e.target.value)}
              placeholder="Search kurtas, price bands..."
              className="w-full h-8 pl-8 pr-10 text-xs rounded bg-white text-gray-900 border border-gray-300 focus:outline-none focus:ring-2 focus:ring-[#ff9900]"
            />
            <Search className="w-3.5 h-3.5 text-gray-500 absolute left-2.5 pointer-events-none" />
            <button
              type="submit"
              className="absolute right-0 h-8 px-2.5 bg-amber-400 text-[#131921] rounded-r flex items-center justify-center"
            >
              <ArrowRight className="w-3.5 h-3.5" />
            </button>
          </form>
        </div>

        {/* Marketplace Sub-Navigation Horizontal Bar */}
        <nav className="bg-[#232f3e] px-4 overflow-x-auto flex items-center gap-5 text-xs font-semibold border-t border-gray-700 whitespace-nowrap scrollbar-none">
          <button
            onClick={() => setActiveTab('landing')}
            className={`py-2 border-b-2 transition ${activeTab === 'landing' ? 'text-amber-400 border-amber-400' : 'text-gray-300 border-transparent hover:text-white'}`}
          >
            Home
          </button>
          <button
            onClick={() => setActiveTab('category')}
            className={`py-2 border-b-2 transition ${activeTab === 'category' ? 'text-amber-400 border-amber-400' : 'text-gray-300 border-transparent hover:text-white'}`}
          >
            Categories
          </button>
          <button
            onClick={() => setActiveTab('niche')}
            className={`py-2 border-b-2 transition ${activeTab === 'niche' ? 'text-amber-400 border-amber-400' : 'text-gray-300 border-transparent hover:text-white'}`}
          >
            Define Niche
          </button>
          <button
            onClick={() => setActiveTab('results')}
            className={`py-2 border-b-2 transition ${activeTab === 'results' ? 'text-amber-400 border-amber-400' : 'text-gray-300 border-transparent hover:text-white'}`}
          >
            Market Results
          </button>
          <button
            onClick={() => setActiveTab('analytics')}
            className={`py-2 border-b-2 transition ${activeTab === 'analytics' ? 'text-amber-400 border-amber-400' : 'text-gray-300 border-transparent hover:text-white'}`}
          >
            Analytics Dashboard
          </button>
          <button
            onClick={() => setActiveTab('reviews')}
            className={`py-2 border-b-2 transition ${activeTab === 'reviews' ? 'text-amber-400 border-amber-400' : 'text-gray-300 border-transparent hover:text-white'}`}
          >
            Reviews &amp; Voice
          </button>
          <button
            onClick={() => setActiveTab('recommendations')}
            className={`py-2 border-b-2 transition ${activeTab === 'recommendations' ? 'text-amber-400 border-amber-400' : 'text-gray-300 border-transparent hover:text-white'}`}
          >
            Recommendations
          </button>
        </nav>

        {/* Active Market Scope Bar */}
        <div className="bg-amber-50 px-4 py-1.5 border-b border-amber-200 flex items-center justify-between text-xs text-amber-950 font-medium">
          <div className="flex items-center gap-2 truncate">
            <Compass className="w-3.5 h-3.5 text-[#ff9900] shrink-0" />
            <span className="font-bold text-gray-900">Current Scope:</span>
            <span className="truncate text-gray-700">{currentScopeSummary}</span>
          </div>
          <button
            onClick={() => setActiveTab('niche')}
            className="shrink-0 text-[11px] font-bold text-[#007185] hover:underline"
          >
            Change
          </button>
        </div>
      </header>

      {/* ============================================================== */}
      {/* MAIN WORKSPACES                                               */}
      {/* ============================================================== */}
      <main className="flex-1 max-w-7xl w-full mx-auto p-4 pb-20">
        {/* PAGE 1: LANDING */}
        {activeTab === 'landing' && (
          <div className="space-y-6">
            {/* Hero Banner */}
            <div className="bg-gradient-to-r from-[#131921] to-[#232f3e] rounded-xl p-6 md:p-8 text-white shadow-lg relative overflow-hidden border border-slate-700">
              <div className="absolute -right-10 -bottom-10 w-48 h-48 bg-amber-500/10 rounded-full blur-3xl pointer-events-none"></div>
              <div className="inline-flex items-center gap-1.5 px-2.5 py-1 rounded bg-amber-400/20 text-amber-300 text-xs font-bold tracking-wide uppercase mb-3 border border-amber-400/30">
                <Sparkles className="w-3.5 h-3.5" /> AI Marketplace Intelligence for Small Vendors
              </div>
              <h1 className="text-2xl sm:text-3xl md:text-4xl font-black tracking-tight leading-tight uppercase">
                SELL SMARTER.<br />
                <span className="text-amber-400">SELL WHAT PEOPLE WANT.</span>
              </h1>
              <p className="text-sm text-gray-300 mt-3 max-w-2xl leading-relaxed">
                Turn Amazon marketplace data into concrete sourcing, pricing, and merchandising decisions for small and local businesses.
                Currently analyzing Women's Kurtas &amp; Kurtis across Odisha and nearby Eastern markets.
              </p>

              <div className="mt-6 flex flex-wrap gap-3">
                <button
                  onClick={() => setActiveTab('niche')}
                  className="px-5 py-2.5 bg-[#ff9900] hover:bg-[#f08800] text-[#131921] font-extrabold text-sm rounded-lg shadow-md flex items-center gap-2 transition active:scale-95"
                >
                  Start Market Analysis <ArrowRight className="w-4 h-4" />
                </button>
                <button
                  onClick={() => setActiveTab('recommendations')}
                  className="px-5 py-2.5 bg-white/10 hover:bg-white/15 text-white font-semibold text-sm rounded-lg border border-white/20 flex items-center gap-2 transition"
                >
                  <Lightbulb className="w-4 h-4 text-amber-400" /> View Actionable Blueprints
                </button>
                <button
                  onClick={() => setIsChatOpen(true)}
                  className="px-4 py-2.5 bg-[#232f3e] hover:bg-slate-800 text-amber-300 font-bold text-sm rounded-lg border border-amber-400/30 flex items-center gap-2 transition"
                >
                  <Sparkles className="w-4 h-4" /> Ask AVA Assistant
                </button>
              </div>

              {/* Metric Snapshot */}
              <div className="mt-8 pt-6 border-t border-slate-700/80 grid grid-cols-2 sm:grid-cols-4 gap-4">
                <div>
                  <div className="text-[11px] text-gray-400 uppercase font-semibold">Active Catalog Sample</div>
                  <div className="text-xl font-black text-white mt-0.5">{analytics?.total_products || 20} Products</div>
                  <div className="text-[10px] text-emerald-400">Deduplicated &amp; Cleaned</div>
                </div>
                <div>
                  <div className="text-[11px] text-gray-400 uppercase font-semibold">Market Median Price</div>
                  <div className="text-xl font-black text-amber-400 mt-0.5">₹{analytics?.median_price_inr || 849}</div>
                  <div className="text-[10px] text-gray-300">Min: ₹449 · Max: ₹1,349</div>
                </div>
                <div>
                  <div className="text-[11px] text-gray-400 uppercase font-semibold">High Opportunity Band</div>
                  <div className="text-xl font-black text-emerald-400 mt-0.5">₹800 — ₹1,000</div>
                  <div className="text-[10px] text-gray-300">38–44% Est. Margin</div>
                </div>
                <div>
                  <div className="text-[11px] text-gray-400 uppercase font-semibold">Top Review Driver</div>
                  <div className="text-xl font-black text-white mt-0.5">Pure Combed Cotton</div>
                  <div className="text-[10px] text-amber-300">Breathable &amp; Colorfast</div>
                </div>
              </div>
            </div>

            {/* Quick Navigation Cards */}
            <div className="grid grid-cols-1 sm:grid-cols-3 gap-4">
              <div 
                onClick={() => setActiveTab('niche')}
                className="bg-white p-5 rounded-xl border border-gray-200 shadow-sm hover:border-[#ff9900] cursor-pointer transition"
              >
                <div className="w-10 h-10 rounded-lg bg-amber-50 text-[#ff9900] flex items-center justify-center mb-3">
                  <Sliders className="w-5 h-5" />
                </div>
                <h3 className="font-bold text-base text-gray-900">1. Define Niche Scope</h3>
                <p className="text-xs text-gray-500 mt-1">Configure target region, max price band, and fabric categories to narrow down market signals.</p>
              </div>

              <div 
                onClick={() => setActiveTab('results')}
                className="bg-white p-5 rounded-xl border border-gray-200 shadow-sm hover:border-[#ff9900] cursor-pointer transition"
              >
                <div className="w-10 h-10 rounded-lg bg-blue-50 text-blue-600 flex items-center justify-center mb-3">
                  <ShoppingBag className="w-5 h-5" />
                </div>
                <h3 className="font-bold text-base text-gray-900">2. Inspect Market Results</h3>
                <p className="text-xs text-gray-500 mt-1">View listed competitor ASINs, AVA opportunity signals, price positions, and rating strength.</p>
              </div>

              <div 
                onClick={() => setActiveTab('recommendations')}
                className="bg-white p-5 rounded-xl border border-gray-200 shadow-sm hover:border-[#ff9900] cursor-pointer transition"
              >
                <div className="w-10 h-10 rounded-lg bg-emerald-50 text-emerald-700 flex items-center justify-center mb-3">
                  <Lightbulb className="w-5 h-5" />
                </div>
                <h3 className="font-bold text-base text-gray-900">3. Actionable Blueprints</h3>
                <p className="text-xs text-gray-500 mt-1">Evidence-backed vendor actions detailing fabric specs, test launch pricing, and listing keywords.</p>
              </div>
            </div>
          </div>
        )}

        {/* PAGE 2: CATEGORIES */}
        {activeTab === 'category' && (
          <div className="space-y-4">
            <div>
              <span className="text-xs font-bold text-[#ff9900] uppercase tracking-wider">Catalog Architecture</span>
              <h2 className="text-xl font-black text-gray-900">Market Categories</h2>
              <p className="text-xs text-gray-500">Explore supported merchandise niches for regional sellers.</p>
            </div>

            <div className="grid grid-cols-1 md:grid-cols-3 gap-4">
              {/* Active Category */}
              <div className="bg-white rounded-xl border-2 border-[#ff9900] p-5 shadow-sm space-y-3">
                <div className="flex items-center justify-between">
                  <span className="px-2 py-0.5 rounded bg-emerald-100 text-emerald-800 text-[10px] font-bold uppercase">Active Niche</span>
                  <span className="text-xs font-bold text-gray-500">20 Products</span>
                </div>
                <div className="flex items-center gap-3">
                  <div className="w-12 h-12 rounded-lg bg-amber-50 text-[#ff9900] flex items-center justify-center text-2xl">
                    👗
                  </div>
                  <div>
                    <h3 className="font-extrabold text-base text-gray-900">Women's Kurtas &amp; Kurtis</h3>
                    <p className="text-xs text-gray-500">Ethnic tunics, straight cuts, and festive anarkalis</p>
                  </div>
                </div>
                <div className="pt-2 border-t border-gray-100 text-xs text-gray-600 space-y-1">
                  <div><strong>Focus Markets:</strong> Odisha, Eastern India</div>
                  <div><strong>Key Fabrics:</strong> Combed Cotton, Chanderi, Khadi, Rayon</div>
                </div>
                <button
                  onClick={() => setActiveTab('results')}
                  className="w-full py-2 bg-[#ff9900] hover:bg-[#f08800] text-[#131921] font-bold text-xs rounded-lg transition"
                >
                  Explore Kurtas Market Results →
                </button>
              </div>

              {/* Inactive Category 1 */}
              <div className="bg-white rounded-xl border border-gray-200 p-5 opacity-75 space-y-3">
                <div className="flex items-center justify-between">
                  <span className="px-2 py-0.5 rounded bg-gray-100 text-gray-600 text-[10px] font-bold uppercase">Coming Soon</span>
                  <span className="text-xs text-gray-400">Roadmap</span>
                </div>
                <div className="flex items-center gap-3">
                  <div className="w-12 h-12 rounded-lg bg-gray-100 text-gray-500 flex items-center justify-center text-2xl">
                    🥻
                  </div>
                  <div>
                    <h3 className="font-extrabold text-base text-gray-800">Sarees &amp; Blouses</h3>
                    <p className="text-xs text-gray-500">Sambalpuri, Bomkai, Handloom silks</p>
                  </div>
                </div>
                <p className="text-xs text-gray-400 pt-2 border-t border-gray-100">
                  Data collection adapter planned for Phase 4 expansion.
                </p>
              </div>

              {/* Inactive Category 2 */}
              <div className="bg-white rounded-xl border border-gray-200 p-5 opacity-75 space-y-3">
                <div className="flex items-center justify-between">
                  <span className="px-2 py-0.5 rounded bg-gray-100 text-gray-600 text-[10px] font-bold uppercase">Coming Soon</span>
                  <span className="text-xs text-gray-400">Roadmap</span>
                </div>
                <div className="flex items-center gap-3">
                  <div className="w-12 h-12 rounded-lg bg-gray-100 text-gray-500 flex items-center justify-center text-2xl">
                    👘
                  </div>
                  <div>
                    <h3 className="font-extrabold text-base text-gray-800">Kurta Sets &amp; Salwars</h3>
                    <p className="text-xs text-gray-500">Matching 3-piece sets with dupatta</p>
                  </div>
                </div>
                <p className="text-xs text-gray-400 pt-2 border-t border-gray-100">
                  Data collection adapter planned for Phase 4 expansion.
                </p>
              </div>
            </div>
          </div>
        )}

        {/* PAGE 3: DEFINE NICHE */}
        {activeTab === 'niche' && (
          <div className="space-y-5 max-w-3xl">
            <div>
              <span className="text-xs font-bold text-[#ff9900] uppercase tracking-wider">Opportunity Discovery</span>
              <h2 className="text-xl font-black text-gray-900">Define Your Niche</h2>
              <p className="text-xs text-gray-500">Calibrate the parameters to filter competitors and target price sweet spots.</p>
            </div>

            <div className="bg-white rounded-xl border border-gray-200 p-6 shadow-sm space-y-5">
              {/* Category */}
              <div>
                <label className="block text-xs font-bold text-gray-700 uppercase tracking-wide mb-1.5">Category</label>
                <input
                  type="text"
                  disabled
                  value="Women's Kurtas & Kurtis (Default Focus)"
                  className="w-full text-xs p-2.5 rounded-lg bg-gray-50 border border-gray-300 text-gray-700 font-semibold cursor-not-allowed"
                />
              </div>

              {/* Region */}
              <div>
                <label className="block text-xs font-bold text-gray-700 uppercase tracking-wide mb-1.5">Target Location</label>
                <select
                  value={location}
                  onChange={e => setLocation(e.target.value)}
                  className="w-full text-xs p-2.5 rounded-lg bg-white border border-gray-300 font-medium focus:ring-2 focus:ring-[#ff9900]"
                >
                  <option value="Odisha">Odisha (Bhubaneswar, Cuttack, Puri regional demand)</option>
                  <option value="Eastern India">Eastern India (Odisha, West Bengal, Jharkhand)</option>
                  <option value="All India">All India Marketplace</option>
                </select>
              </div>

              {/* Price Max Slider */}
              <div>
                <div className="flex items-center justify-between mb-1.5">
                  <label className="text-xs font-bold text-gray-700 uppercase tracking-wide">Max Price Cap</label>
                  <span className="text-xs font-extrabold text-[#131921] bg-amber-100 px-2.5 py-0.5 rounded border border-amber-300">
                    Up to ₹{priceMax.toLocaleString()}
                  </span>
                </div>
                <input
                  type="range"
                  min="500"
                  max="2000"
                  step="50"
                  value={priceMax}
                  onChange={e => setPriceMax(Number(e.target.value))}
                  className="w-full accent-[#ff9900]"
                />
                <div className="flex gap-2 mt-2">
                  <button
                    onClick={() => setPriceMax(500)}
                    className={`text-[11px] px-2.5 py-1 rounded border transition ${priceMax === 500 ? 'bg-[#131921] text-white border-[#131921]' : 'bg-gray-50 text-gray-700 border-gray-200'}`}
                  >
                    Under ₹500
                  </button>
                  <button
                    onClick={() => setPriceMax(1000)}
                    className={`text-[11px] px-2.5 py-1 rounded border transition ${priceMax === 1000 ? 'bg-[#131921] text-white border-[#131921]' : 'bg-gray-50 text-gray-700 border-gray-200'}`}
                  >
                    ₹500 — ₹1,000 (Sweet Spot)
                  </button>
                  <button
                    onClick={() => setPriceMax(1500)}
                    className={`text-[11px] px-2.5 py-1 rounded border transition ${priceMax === 1500 ? 'bg-[#131921] text-white border-[#131921]' : 'bg-gray-50 text-gray-700 border-gray-200'}`}
                  >
                    Over ₹1,000
                  </button>
                </div>
              </div>

              {/* Fabric Material */}
              <div>
                <label className="block text-xs font-bold text-gray-700 uppercase tracking-wide mb-1.5">Fabric Material</label>
                <div className="flex flex-wrap gap-2">
                  {['All', 'Cotton', 'Rayon', 'Chanderi', 'Cotton Silk', 'Khadi'].map(m => (
                    <button
                      key={m}
                      onClick={() => setSelectedMaterial(m)}
                      className={`text-xs px-3 py-1.5 rounded-lg border font-medium transition ${selectedMaterial === m ? 'bg-[#ff9900] text-[#131921] font-bold border-amber-500 shadow-sm' : 'bg-white text-gray-700 border-gray-200 hover:bg-gray-50'}`}
                    >
                      {m}
                    </button>
                  ))}
                </div>
              </div>

              {/* Live Scope Preview Box */}
              <div className="p-3.5 rounded-lg bg-amber-50/70 border border-amber-200 flex items-center justify-between">
                <div>
                  <div className="text-[10px] font-bold uppercase tracking-wider text-amber-900">Active Scope</div>
                  <div className="text-xs font-bold text-gray-900">{currentScopeSummary}</div>
                </div>
                <button
                  onClick={() => setActiveTab('results')}
                  className="px-4 py-2 bg-[#ff9900] hover:bg-[#f08800] text-[#131921] font-bold text-xs rounded-lg shadow transition"
                >
                  View Market Results →
                </button>
              </div>
            </div>
          </div>
        )}

        {/* PAGE 4: MARKET RESULTS */}
        {activeTab === 'results' && (
          <div className="space-y-4">
            <div className="flex flex-col sm:flex-row sm:items-center justify-between gap-2">
              <div>
                <span className="text-xs font-bold text-[#ff9900] uppercase tracking-wider">Market Intelligence</span>
                <h2 className="text-xl font-black text-gray-900">Market Results</h2>
                <p className="text-xs text-gray-500">Showing {products.length} products matching {currentScopeSummary}</p>
              </div>

              {/* Sort selector */}
              <div className="flex items-center gap-2">
                <span className="text-xs text-gray-500 font-medium">Sort by:</span>
                <select
                  value={sortBy}
                  onChange={e => setSortBy(e.target.value)}
                  className="text-xs p-1.5 rounded-lg bg-white border border-gray-300 font-semibold focus:ring-2 focus:ring-[#ff9900]"
                >
                  <option value="opportunity">AVA High Opportunity</option>
                  <option value="price_asc">Price: Low to High</option>
                  <option value="price_desc">Price: High to Low</option>
                  <option value="rating">Customer Rating</option>
                  <option value="reviews">Review Volume</option>
                </select>
              </div>
            </div>

            {/* Products Grid */}
            <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-4">
              {products.map(p => (
                <div
                  key={p.asin}
                  onClick={() => {
                    setSelectedProduct(p);
                    setActiveTab('product');
                  }}
                  className="bg-white rounded-xl border border-gray-200 p-4 shadow-sm hover:shadow-md hover:border-[#ff9900] cursor-pointer transition flex flex-col justify-between"
                >
                  <div>
                    {/* Top Badges */}
                    <div className="flex items-center justify-between gap-1 mb-2">
                      <span className={`text-[10px] font-bold px-2 py-0.5 rounded ${p.badge_type || 'badge-opportunity'}`}>
                        ★ AVA: {p.badge || 'High Opportunity'}
                      </span>
                      <span className="text-[10px] text-gray-400 font-mono">{p.asin}</span>
                    </div>

                    {/* Title */}
                    <h3 className="text-xs font-bold text-gray-900 leading-snug line-clamp-2">
                      {p.product_name}
                    </h3>

                    {/* Visual Attributes */}
                    <div className="mt-2 flex items-center gap-2 text-[11px] text-gray-600">
                      <span className="bg-slate-100 px-2 py-0.5 rounded font-medium">{p.material}</span>
                      <span className="bg-slate-100 px-2 py-0.5 rounded font-medium">{p.color}</span>
                      <span className="bg-slate-100 px-2 py-0.5 rounded font-medium">{p.pattern}</span>
                    </div>

                    {/* Rating & Reviews */}
                    <div className="flex items-center gap-1.5 mt-2 text-xs">
                      <span className="font-extrabold text-amber-600">{p.rating} ★</span>
                      <span className="text-amber-500">★★★★☆</span>
                      <span className="text-gray-400 text-[11px]">({p.review_count.toLocaleString()} reviews)</span>
                    </div>

                    {/* Price & MRP */}
                    <div className="mt-2 flex items-baseline gap-2">
                      <span className="text-base font-black text-gray-950">₹{p.price_inr}</span>
                      <span className="text-xs text-gray-400 line-through">₹{p.mrp_inr}</span>
                      <span className="text-xs font-bold text-[#b12704]">({p.discount_pct}% off)</span>
                    </div>
                  </div>

                  {/* Footer */}
                  <div className="mt-3 pt-2.5 border-t border-gray-100 flex items-center justify-between text-[11px] text-gray-500">
                    <span className="truncate">Seller: <strong>{p.seller}</strong></span>
                    <span className="text-[#007185] font-bold hover:underline">Deep Dive →</span>
                  </div>
                </div>
              ))}
            </div>
          </div>
        )}

        {/* PAGE 5: ANALYTICS DASHBOARD */}
        {activeTab === 'analytics' && (
          <div className="space-y-6">
            <div>
              <span className="text-xs font-bold text-[#ff9900] uppercase tracking-wider">Quantitative Diagnostics</span>
              <h2 className="text-xl font-black text-gray-900">Analytics Dashboard</h2>
              <p className="text-xs text-gray-500">Aggregated marketplace metrics for Women's Kurtas &amp; Kurtis in Odisha.</p>
            </div>

            {/* Top KPI Cards */}
            <div className="grid grid-cols-2 sm:grid-cols-4 gap-4">
              <div className="bg-white p-4 rounded-xl border border-gray-200 shadow-sm">
                <span className="text-[10px] uppercase font-bold text-gray-400 tracking-wider">Catalog Sample</span>
                <div className="text-2xl font-black text-gray-900 mt-1">{analytics?.total_products || 20}</div>
                <div className="text-[11px] text-emerald-600 font-semibold mt-1">Verified ASINs</div>
              </div>

              <div className="bg-white p-4 rounded-xl border border-gray-200 shadow-sm">
                <span className="text-[10px] uppercase font-bold text-gray-400 tracking-wider">Market Median Price</span>
                <div className="text-2xl font-black text-[#131921] mt-1">₹{analytics?.median_price_inr || 849}</div>
                <div className="text-[11px] text-gray-500 mt-1">Min ₹{analytics?.min_price_inr} – Max ₹{analytics?.max_price_inr}</div>
              </div>

              <div className="bg-white p-4 rounded-xl border border-gray-200 shadow-sm">
                <span className="text-[10px] uppercase font-bold text-gray-400 tracking-wider">Average Rating</span>
                <div className="text-2xl font-black text-amber-500 mt-1">{analytics?.avg_rating || 4.2} ★</div>
                <div className="text-[11px] text-gray-500 mt-1">Median: {analytics?.median_rating || 4.2} ★</div>
              </div>

              <div className="bg-white p-4 rounded-xl border border-gray-200 shadow-sm">
                <span className="text-[10px] uppercase font-bold text-gray-400 tracking-wider">Average Discount</span>
                <div className="text-2xl font-black text-[#b12704] mt-1">{analytics?.avg_discount_pct || 34}%</div>
                <div className="text-[11px] text-gray-500 mt-1">High promo penetration</div>
              </div>
            </div>

            {/* Price Band Distribution */}
            <div className="bg-white p-5 rounded-xl border border-gray-200 shadow-sm space-y-4">
              <div className="flex items-center justify-between">
                <h3 className="font-extrabold text-sm text-gray-900">Price Band Competition &amp; Opportunity</h3>
                <span className="text-xs text-emerald-700 font-bold bg-emerald-50 px-2.5 py-0.5 rounded border border-emerald-200">
                  Sweet Spot Identified
                </span>
              </div>

              <div className="space-y-3">
                {priceAnalytics?.price_bands.map(b => (
                  <div key={b.band_name} className="p-3 rounded-lg border border-gray-100 bg-gray-50/60">
                    <div className="flex items-center justify-between text-xs mb-1">
                      <span className="font-bold text-gray-900">{b.band_name}</span>
                      <span className="font-extrabold text-gray-700">{b.product_count} listings ({b.avg_rating} ★ avg)</span>
                    </div>
                    {/* Visual Bar */}
                    <div className="w-full h-2 rounded-full bg-gray-200 overflow-hidden mb-2">
                      <div
                        className={`h-full rounded-full ${b.band_name === '₹500 — ₹1,000' ? 'bg-[#ff9900]' : 'bg-slate-600'}`}
                        style={{ width: `${Math.max(15, (b.product_count / (analytics?.total_products || 20)) * 100)}%` }}
                      ></div>
                    </div>
                    <div className="flex items-center justify-between text-[11px] text-gray-500">
                      <span>Density: <strong>{b.competition_density}</strong></span>
                      <span className="font-semibold text-emerald-700">{b.opportunity_level}</span>
                    </div>
                  </div>
                ))}
              </div>

              {/* Sweet spot banner */}
              {priceAnalytics?.sweet_spot && (
                <div className="bg-amber-50 border border-amber-300 rounded-lg p-3 text-xs text-amber-950 space-y-1">
                  <div className="font-bold flex items-center gap-1.5">
                    <Sparkles className="w-3.5 h-3.5 text-[#ff9900]" />
                    Target Sweet Spot: {priceAnalytics.sweet_spot.band} (Launch at {priceAnalytics.sweet_spot.recommended_launch_price})
                  </div>
                  <p className="text-[11px] text-gray-700 leading-relaxed">
                    {priceAnalytics.sweet_spot.rationale}
                  </p>
                </div>
              )}
            </div>
          </div>
        )}

        {/* PAGE 6: PRODUCT DETAIL WORKSPACE */}
        {activeTab === 'product' && selectedProduct && (
          <div className="space-y-4 max-w-4xl">
            <button
              onClick={() => setActiveTab('results')}
              className="text-xs font-bold text-[#007185] hover:underline flex items-center gap-1"
            >
              ← Back to Market Results
            </button>

            <div className="bg-white rounded-xl border border-gray-200 p-6 shadow-sm space-y-5">
              <div className="flex flex-col sm:flex-row gap-5">
                {/* Visual */}
                <div className="w-full sm:w-44 h-56 rounded-lg bg-slate-100 border border-gray-200 flex flex-col items-center justify-center shrink-0">
                  <span className="text-6xl">
                    {selectedProduct.color === 'Blue' ? '👗' : selectedProduct.color === 'Maroon' ? '👘' : selectedProduct.color === 'Black' ? '🖤' : '🥻'}
                  </span>
                  <span className="text-xs text-gray-500 mt-3 font-semibold">{selectedProduct.material}</span>
                </div>

                {/* Info */}
                <div className="flex-1 space-y-2">
                  <span className={`text-[10px] font-bold px-2 py-0.5 rounded ${selectedProduct.badge_type || 'badge-opportunity'} inline-block`}>
                    ★ AVA Signal: {selectedProduct.badge || 'High Opportunity'}
                  </span>
                  <h2 className="text-base font-extrabold text-gray-900 leading-snug">
                    {selectedProduct.product_name}
                  </h2>

                  <div className="flex items-center gap-2 text-xs">
                    <span className="font-extrabold text-amber-600">{selectedProduct.rating} ★</span>
                    <span className="text-gray-500">({selectedProduct.review_count.toLocaleString()} customer reviews)</span>
                    <span className="text-gray-300">·</span>
                    <span className="font-mono text-gray-400">{selectedProduct.asin}</span>
                  </div>

                  <div className="flex items-baseline gap-2 pt-1">
                    <span className="text-2xl font-black text-[#131921]">₹{selectedProduct.price_inr}</span>
                    <span className="text-sm text-gray-400 line-through">₹{selectedProduct.mrp_inr}</span>
                    <span className="text-sm font-bold text-[#b12704]">{selectedProduct.discount_pct}% off</span>
                  </div>

                  <div className="text-xs text-gray-600 pt-1">
                    Sold by: <strong className="text-gray-900">{selectedProduct.seller}</strong> ({selectedProduct.availability})
                  </div>
                </div>
              </div>

              {/* Specifications */}
              <div className="bg-gray-50 p-3.5 rounded-lg border border-gray-200 grid grid-cols-2 sm:grid-cols-3 gap-3 text-xs">
                <div><span className="text-gray-500">Fabric Material:</span> <strong className="block text-gray-900">{selectedProduct.material}</strong></div>
                <div><span className="text-gray-500">Primary Colour:</span> <strong className="block text-gray-900">{selectedProduct.color}</strong></div>
                <div><span className="text-gray-500">Pattern Style:</span> <strong className="block text-gray-900">{selectedProduct.pattern}</strong></div>
                <div><span className="text-gray-500">Brand:</span> <strong className="block text-gray-900">{selectedProduct.brand}</strong></div>
                <div><span className="text-gray-500">Available Sizes:</span> <strong className="block text-gray-900">{selectedProduct.available_sizes.join(', ')}</strong></div>
                <div><span className="text-gray-500">Category:</span> <strong className="block text-gray-900">{selectedProduct.subcategory}</strong></div>
              </div>

              {/* AVA Product Intelligence Box */}
              <div className="bg-amber-50/80 border-2 border-[#ff9900] rounded-xl p-4 space-y-3">
                <div className="flex items-center justify-between">
                  <span className="font-black text-xs text-[#131921] flex items-center gap-1.5">
                    <Sparkles className="w-4 h-4 text-[#ff9900]" /> AVA PRODUCT INTELLIGENCE
                  </span>
                  <span className="text-[10px] bg-amber-200 text-amber-950 font-black px-2 py-0.5 rounded">
                    Confidence: 92%
                  </span>
                </div>

                <div className="grid grid-cols-2 sm:grid-cols-4 gap-2 text-xs">
                  <div className="bg-white p-2 rounded border border-amber-200">
                    <span className="text-gray-500 text-[10px] block">Price Position</span>
                    <strong className="text-gray-900 text-xs">{selectedProduct.price_position}</strong>
                  </div>
                  <div className="bg-white p-2 rounded border border-amber-200">
                    <span className="text-gray-500 text-[10px] block">Rating Benchmark</span>
                    <strong className="text-emerald-700 text-xs">{selectedProduct.rating_position}</strong>
                  </div>
                  <div className="bg-white p-2 rounded border border-amber-200">
                    <span className="text-gray-500 text-[10px] block">Competition Density</span>
                    <strong className="text-gray-900 text-xs">{selectedProduct.competition}</strong>
                  </div>
                  <div className="bg-white p-2 rounded border border-amber-200">
                    <span className="text-gray-500 text-[10px] block">Customer Sentiment</span>
                    <strong className="text-emerald-700 text-xs">{selectedProduct.sentiment}</strong>
                  </div>
                </div>

                <button
                  onClick={() => {
                    setIsChatOpen(true);
                    handleSendMessage(`Tell me how to compete with this product "${selectedProduct.product_name}" at ₹${selectedProduct.price_inr}`);
                  }}
                  className="w-full py-2.5 bg-[#ff9900] hover:bg-[#f08800] text-[#131921] font-black text-xs rounded-lg shadow flex items-center justify-center gap-1.5 transition active:scale-95"
                >
                  <Sparkles className="w-3.5 h-3.5" /> Ask AVA How to Outperform This Product
                </button>
              </div>
            </div>
          </div>
        )}

        {/* PAGE 7: REVIEWS & VOICE OF CUSTOMER */}
        {activeTab === 'reviews' && (
          <div className="space-y-6">
            <div>
              <span className="text-xs font-bold text-[#ff9900] uppercase tracking-wider">Voice of Customer</span>
              <h2 className="text-xl font-black text-gray-900">Reviews &amp; Sentiment Insights</h2>
              <p className="text-xs text-gray-500">Extracted from customer reviews across Kurtas &amp; Kurtis in Eastern India.</p>
            </div>

            {/* Drivers vs Complaints */}
            <div className="grid grid-cols-1 md:grid-cols-2 gap-4">
              {/* Positive Drivers */}
              <div className="bg-white rounded-xl border border-gray-200 p-5 shadow-sm space-y-3">
                <div className="flex items-center gap-2 text-emerald-700 font-extrabold text-sm">
                  <CheckCircle2 className="w-4 h-4" /> What Customers Love (Conversion Drivers)
                </div>
                <div className="space-y-2">
                  {reviewsData?.positive_drivers.map((d, i) => (
                    <div key={i} className="p-2.5 rounded-lg bg-emerald-50/70 border border-emerald-100 text-xs text-emerald-950 font-medium">
                      ✓ {d}
                    </div>
                  ))}
                </div>
              </div>

              {/* Recurring Complaints */}
              <div className="bg-white rounded-xl border border-gray-200 p-5 shadow-sm space-y-3">
                <div className="flex items-center gap-2 text-[#b12704] font-extrabold text-sm">
                  <AlertCircle className="w-4 h-4" /> Recurring Complaints (Vendor Pitfalls)
                </div>
                <div className="space-y-2">
                  {reviewsData?.recurring_complaints.map((c, i) => (
                    <div key={i} className="p-2.5 rounded-lg bg-red-50/70 border border-red-100 text-xs text-red-950 font-medium">
                      ⚠ {c}
                    </div>
                  ))}
                </div>
              </div>
            </div>

            {/* Sample Customer Reviews */}
            <div className="bg-white rounded-xl border border-gray-200 p-5 shadow-sm space-y-4">
              <h3 className="font-extrabold text-sm text-gray-900">Recent Customer Review Samples</h3>
              <div className="space-y-3">
                {reviewsData?.samples.map(r => (
                  <div key={r.review_id} className="p-3.5 rounded-lg bg-gray-50/70 border border-gray-200 text-xs space-y-1">
                    <div className="flex items-center justify-between">
                      <span className="font-bold text-gray-900">{r.title}</span>
                      <span className="font-bold text-amber-600">{r.rating} ★ ({r.sentiment})</span>
                    </div>
                    <p className="text-gray-600 leading-relaxed">{r.text}</p>
                    <div className="text-[10px] text-gray-400">Date: {r.date} · Product ASIN: {r.product_id}</div>
                  </div>
                ))}
              </div>
            </div>
          </div>
        )}

        {/* PAGE 8: RECOMMENDATIONS */}
        {activeTab === 'recommendations' && (
          <div className="space-y-6">
            <div>
              <span className="text-xs font-bold text-[#ff9900] uppercase tracking-wider">AVA Actionable Blueprint</span>
              <h2 className="text-xl font-black text-gray-900">Sourcing &amp; Pricing Recommendations</h2>
              <p className="text-xs text-gray-500">Data-driven decisions for inventory procurement, margin targets, and launch timing.</p>
            </div>

            <div className="space-y-4">
              {recommendations.map(rec => (
                <div
                  key={rec.id}
                  className="bg-white rounded-xl border-2 border-[#ff9900] p-5 shadow-sm space-y-3"
                >
                  <div className="flex items-center justify-between">
                    <span className="px-2.5 py-0.5 rounded bg-amber-100 text-amber-900 font-extrabold text-[10px] uppercase border border-amber-300">
                      {rec.badge}
                    </span>
                    <span className="text-xs font-extrabold text-emerald-700 bg-emerald-50 px-2 py-0.5 rounded border border-emerald-200">
                      Confidence: {rec.confidence_pct}%
                    </span>
                  </div>

                  <h3 className="font-black text-base text-gray-900">{rec.title}</h3>

                  <div className="space-y-2 text-xs">
                    <div className="p-2.5 rounded-lg bg-blue-50/70 border border-blue-100 text-blue-950">
                      <strong className="block text-[11px] uppercase tracking-wide text-blue-900 mb-0.5">What was observed:</strong>
                      {rec.what_observed}
                    </div>
                    <div className="p-2.5 rounded-lg bg-amber-50/70 border border-amber-100 text-amber-950">
                      <strong className="block text-[11px] uppercase tracking-wide text-amber-900 mb-0.5">Recommended Action:</strong>
                      {rec.what_to_do}
                    </div>
                  </div>

                  {rec.sourcing_specs && (
                    <div className="bg-gray-50 p-3 rounded-lg border border-gray-200 text-xs">
                      <div className="font-bold text-gray-800 text-[11px] uppercase tracking-wide mb-1.5">Actionable Sourcing Specs:</div>
                      <div className="grid grid-cols-2 sm:grid-cols-4 gap-2 text-[11px]">
                        <div><span className="text-gray-500">Fabric:</span> <strong>{rec.sourcing_specs.fabric}</strong></div>
                        <div><span className="text-gray-500">Test Range:</span> <strong>{rec.sourcing_specs.test_range}</strong></div>
                        <div><span className="text-gray-500">Colours:</span> <strong>{rec.sourcing_specs.colors}</strong></div>
                        <div><span className="text-gray-500">Priority Sizes:</span> <strong>{rec.sourcing_specs.priority_sizes}</strong></div>
                      </div>
                    </div>
                  )}

                  <div className="flex flex-col sm:flex-row sm:items-center justify-between gap-2 pt-1">
                    <span className="text-xs text-gray-500">
                      {rec.estimated_margin && <span>Estimated profit margin: <strong>{rec.estimated_margin}</strong> · </span>}
                      <span className="italic">{rec.evidence_sample_size}</span>
                    </span>
                    <button
                      onClick={() => {
                        setIsChatOpen(true);
                        handleSendMessage(`Explain the recommendation "${rec.title}" and how I can execute it.`);
                      }}
                      className="px-3.5 py-1.5 bg-[#131921] hover:bg-slate-800 text-white font-bold text-xs rounded-lg flex items-center gap-1.5 transition"
                    >
                      <Sparkles className="w-3.5 h-3.5 text-amber-400" /> Ask AVA How
                    </button>
                  </div>
                </div>
              ))}
            </div>
          </div>
        )}
      </main>

      {/* ============================================================== */}
      {/* PERSISTENT FLOATING / DOCKED ASK AVA ASSISTANT DRAWER         */}
      {/* ============================================================== */}
      {isChatOpen && (
        <div className="fixed inset-y-0 right-0 z-50 w-full sm:w-96 bg-white shadow-2xl flex flex-col border-l border-gray-200 animate-in slide-in-from-right duration-200">
          {/* Drawer Header */}
          <div className="bg-[#131921] text-white p-3.5 flex items-center justify-between border-b border-gray-800">
            <div className="flex items-center gap-2">
              <div className="w-7 h-7 rounded bg-[#ff9900] text-[#131921] font-black flex items-center justify-center text-xs">
                AVA
              </div>
              <div>
                <h3 className="font-bold text-xs leading-none">Ask AVA Assistant</h3>
                <span className="text-[10px] text-amber-400 font-medium">Grounded Marketplace AI</span>
              </div>
            </div>
            <button
              onClick={() => setIsChatOpen(false)}
              className="text-gray-400 hover:text-white p-1 rounded transition"
            >
              <X className="w-4 h-4" />
            </button>
          </div>

          {/* Context Tag */}
          <div className="bg-amber-50 px-3 py-1.5 border-b border-amber-200 text-[11px] text-amber-950 font-medium flex items-center justify-between">
            <span className="truncate">Context: {currentScopeSummary}</span>
            <span className="text-emerald-700 font-bold shrink-0">Live Grounded</span>
          </div>

          {/* Message History */}
          <div className="flex-1 p-3 overflow-y-auto space-y-3">
            {chatMessages.map(msg => (
              <div
                key={msg.id}
                className={`flex flex-col ${msg.sender === 'user' ? 'items-end' : 'items-start'}`}
              >
                <div
                  className={`max-w-[85%] rounded-lg p-3 text-xs leading-relaxed ${msg.sender === 'user' ? 'bg-[#ff9900] text-[#131921] font-semibold' : 'bg-gray-100 text-gray-900 border border-gray-200'}`}
                >
                  <p className="whitespace-pre-line">{msg.text}</p>
                </div>

                {/* Evidence & Actions for Assistant */}
                {msg.evidence && msg.evidence.length > 0 && (
                  <div className="mt-1.5 flex flex-wrap gap-1 max-w-[85%]">
                    {msg.evidence.map((ev, i) => (
                      <span key={i} className="text-[9px] bg-slate-100 text-slate-600 px-1.5 py-0.5 rounded border border-slate-200">
                        {ev}
                      </span>
                    ))}
                  </div>
                )}

                {msg.actions && msg.actions.length > 0 && (
                  <div className="mt-2 flex flex-col gap-1 max-w-[85%]">
                    {msg.actions.map((act, i) => (
                      <button
                        key={i}
                        onClick={() => handleSendMessage(act)}
                        className="text-left text-[10px] bg-amber-50 hover:bg-amber-100 text-[#131921] font-semibold px-2 py-1 rounded border border-amber-200 transition"
                      >
                        → {act}
                      </button>
                    ))}
                  </div>
                )}
              </div>
            ))}
            {isTyping && (
              <div className="text-[11px] text-gray-400 italic flex items-center gap-1.5">
                <span className="w-1.5 h-1.5 rounded-full bg-amber-500 animate-bounce"></span>
                <span>AVA is analyzing marketplace signals...</span>
              </div>
            )}
          </div>

          {/* Chat Input Bar */}
          <div className="p-3 border-t border-gray-200 bg-white">
            <div className="relative flex items-center">
              <input
                type="text"
                value={chatInput}
                onChange={e => setChatInput(e.target.value)}
                onKeyDown={e => {
                  if (e.key === 'Enter') handleSendMessage();
                }}
                placeholder="Ask about pricing, colors, fabrics..."
                className="w-full text-xs p-2.5 pr-10 rounded-lg border border-gray-300 focus:outline-none focus:ring-2 focus:ring-[#ff9900]"
              />
              <button
                onClick={() => handleSendMessage()}
                className="absolute right-1.5 p-1.5 bg-[#ff9900] hover:bg-[#f08800] text-[#131921] rounded-md transition"
              >
                <Send className="w-3.5 h-3.5" />
              </button>
            </div>
          </div>
        </div>
      )}

      {/* ============================================================== */}
      {/* MOBILE BOTTOM NAVIGATION BAR                                  */}
      {/* ============================================================== */}
      <footer className="fixed bottom-0 inset-x-0 z-30 bg-white border-t border-gray-200 py-1.5 px-3 flex items-center justify-around md:hidden">
        <button
          onClick={() => setActiveTab('landing')}
          className={`flex flex-col items-center text-[10px] font-semibold ${activeTab === 'landing' ? 'text-[#ff9900]' : 'text-gray-500'}`}
        >
          <Home className="w-4 h-4" />
          <span>Home</span>
        </button>
        <button
          onClick={() => setActiveTab('niche')}
          className={`flex flex-col items-center text-[10px] font-semibold ${activeTab === 'niche' ? 'text-[#ff9900]' : 'text-gray-500'}`}
        >
          <Sliders className="w-4 h-4" />
          <span>Niche</span>
        </button>
        <button
          onClick={() => setActiveTab('results')}
          className={`flex flex-col items-center text-[10px] font-semibold ${activeTab === 'results' ? 'text-[#ff9900]' : 'text-gray-500'}`}
        >
          <ShoppingBag className="w-4 h-4" />
          <span>Market</span>
        </button>
        <button
          onClick={() => setActiveTab('analytics')}
          className={`flex flex-col items-center text-[10px] font-semibold ${activeTab === 'analytics' ? 'text-[#ff9900]' : 'text-gray-500'}`}
        >
          <BarChart2 className="w-4 h-4" />
          <span>Analytics</span>
        </button>
        <button
          onClick={() => setActiveTab('recommendations')}
          className={`flex flex-col items-center text-[10px] font-semibold ${activeTab === 'recommendations' ? 'text-[#ff9900]' : 'text-gray-500'}`}
        >
          <Lightbulb className="w-4 h-4 text-amber-500" />
          <span>Actions</span>
        </button>
      </footer>
    </div>
  );
}

export default App;
