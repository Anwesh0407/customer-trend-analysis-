import { useState } from 'react';
import type { Category } from '../types';
import {
  Tag,
  ArrowRight,
  Sparkles,
  Info,
  CheckCircle2,
  Clock,
  Layers,
  HeartHandshake,
} from 'lucide-react';

interface CategoriesWorkspaceProps {
  categories: Category[];
  selectedCategory: string;
  onSelectCategory: (categoryName: string) => void;
}

export function CategoriesWorkspace({
  categories: _categories,
  selectedCategory: _selectedCategory,
  onSelectCategory,
}: CategoriesWorkspaceProps) {
  const [requestedPilot, setRequestedPilot] = useState(false);

  return (
    <div className="space-y-6">
      {/* Top Breadcrumb & Status */}
      <div className="flex flex-wrap items-center justify-between gap-4 pb-2 border-b border-[#e2e8f0]">
        <div>
          <div className="flex items-center gap-1.5 text-xs text-[#75777c] uppercase font-mono tracking-wider">
            <span>Marketplace Catalog</span>
            <span>/</span>
            <span>Taxonomy Hierarchy</span>
            <span>/</span>
            <span className="text-[#8a5100] font-bold">Apparel Focus</span>
          </div>
          <h1 className="text-2xl font-bold tracking-tight text-[#131b2e] mt-1 flex items-center gap-2">
            <Tag className="text-[#ff9900]" size={24} />
            Marketplace Categories & Sub-Categories
          </h1>
          <p className="text-xs text-gray-500 mt-1">
            Browse structured product taxonomies. Select active MVP retail category to inspect live marketplace data.
          </p>
        </div>

        <div className="flex items-center gap-2">
          <span className="inline-flex items-center gap-1.5 px-3 py-1 rounded-full bg-[#ecfdf5] text-[#065f46] border border-[#a7f3d0] font-bold text-xs font-mono">
            <span className="w-2 h-2 rounded-full bg-emerald-500 animate-pulse" />
            1 Active Pilot Category
          </span>
        </div>
      </div>

      {/* FEATURED CATEGORY: Women's Clothing -> Kurtas & Kurtis (Exact Stitch Hero Design) */}
      <div className="bg-white rounded-xl border border-[#e2e8f0] shadow-sm overflow-hidden">
        {/* Banner Header */}
        <div className="p-4 bg-[#f2f3ff] border-b border-[#dae2fd] flex flex-wrap items-center justify-between gap-3">
          <div className="flex items-center gap-3">
            <div className="w-10 h-10 rounded-lg bg-[#131921] text-white flex items-center justify-center font-bold">
              <Layers size={20} className="text-[#ff9900]" />
            </div>
            <div>
              <div className="flex items-center gap-2">
                <h2 className="text-base font-bold text-[#131b2e]">Women's Clothing · Apparel</h2>
                <span className="px-2 py-0.5 rounded bg-[#161c24] text-white font-mono text-[10px] font-bold uppercase">
                  Primary Scope Node
                </span>
              </div>
              <span className="text-xs text-gray-500">
                Sambalpuri Handloom, Breathable Pure Cotton, & Regional Ethnic Tops
              </span>
            </div>
          </div>

          <div className="flex items-center gap-3">
            <span className="inline-flex items-center gap-1 px-2.5 py-1 rounded bg-[#ffdcbd] text-[#693c00] font-bold text-xs">
              <Sparkles size={13} />
              Active MVP Scope
            </span>
            <span className="font-mono text-xs font-bold text-[#131b2e]">1,248 Catalog SKUs</span>
          </div>
        </div>

        {/* Featured Breakdown Content */}
        <div className="p-6 grid grid-cols-1 lg:grid-cols-12 gap-6">
          {/* Subcategory focus (7 cols) */}
          <div className="lg:col-span-7 space-y-4">
            <div className="flex items-center justify-between">
              <span className="text-[11px] font-bold uppercase tracking-wider text-[#75777c]">
                Subcategory Breakdown
              </span>
              <span className="text-xs text-[#8a5100] font-bold">Active Demonstration Scope</span>
            </div>

            <div className="bg-[#f2f3ff] rounded-xl p-4 space-y-3">
              <div className="flex items-center justify-between">
                <span className="font-bold text-sm text-[#131b2e]">Kurtas & Kurtis</span>
                <span className="font-mono text-xs font-bold text-[#8a5100]">1 Active Focus</span>
              </div>

              {/* Active Subcategory Box */}
              <div className="bg-white rounded-lg p-4 border border-[#dae2fd] shadow-sm space-y-3">
                <div className="flex items-start justify-between gap-3">
                  <div>
                    <div className="flex items-center gap-2">
                      <span className="w-2 h-2 rounded-full bg-[#fe9800] animate-pulse" />
                      <span className="font-bold text-sm text-[#131b2e]">Kurtas & Kurtis</span>
                      <span className="px-1.5 py-0.5 rounded bg-[#ffdcbd] text-[#2c1600] font-mono text-[10px] font-bold">
                        ACTIVE MVP
                      </span>
                    </div>
                    <p className="text-xs text-gray-600 mt-1">
                      Sambalpuri Handloom & Pure Breathable Cotton Demand Corridor for Eastern India vendors.
                    </p>
                  </div>
                  <div className="text-right shrink-0">
                    <span className="font-mono text-lg font-bold text-[#8a5100]">1,248</span>
                    <span className="block text-[10px] text-gray-500 uppercase font-mono">Listings</span>
                  </div>
                </div>

                {/* Sub-pills */}
                <div className="grid grid-cols-3 gap-2 pt-1 font-mono text-xs">
                  <div className="bg-[#f2f3ff] p-2 rounded text-center">
                    <span className="block text-[10px] text-gray-500">Sarees</span>
                    <span className="text-[11px] text-gray-400">Upcoming Q3</span>
                  </div>
                  <div className="bg-[#f2f3ff] p-2 rounded text-center">
                    <span className="block text-[10px] text-gray-500">Ethnic Sets</span>
                    <span className="text-[11px] text-gray-400">Upcoming Q3</span>
                  </div>
                  <div className="bg-[#f2f3ff] p-2 rounded text-center">
                    <span className="block text-[10px] text-gray-500">Western Tops</span>
                    <span className="text-[11px] text-gray-400">Upcoming Q4</span>
                  </div>
                </div>
              </div>
            </div>

            {/* Action Buttons */}
            <div className="flex flex-wrap items-center gap-3 pt-2">
              <button
                type="button"
                onClick={() => onSelectCategory("Women's Kurtas & Kurtis")}
                className="px-5 py-2.5 bg-[#fe9800] hover:bg-[#ffad33] text-[#2c1600] font-bold text-xs rounded-lg shadow-sm transition flex items-center gap-1.5 cursor-pointer"
              >
                <span>Select & Open Niche Filters</span>
                <ArrowRight size={15} />
              </button>

              <button
                type="button"
                onClick={() => onSelectCategory("Women's Kurtas & Kurtis")}
                className="px-4 py-2.5 bg-[#eaedff] hover:bg-[#dae2fd] text-[#131b2e] font-semibold text-xs rounded-lg transition cursor-pointer"
              >
                <span>Explore Results</span>
              </button>
            </div>
          </div>

          {/* Category overview & studio photography (5 cols - Exact Stitch) */}
          <div className="lg:col-span-5 flex flex-col justify-between bg-[#f2f3ff] rounded-xl p-4 space-y-4">
            <div className="space-y-3">
              <div className="flex items-center justify-between text-xs">
                <span className="text-[10px] font-bold uppercase tracking-wider text-[#75777c]">
                  Category Overview
                </span>
                <span className="font-mono text-[11px] text-gray-500">1,248 ACTIVE SKUS</span>
              </div>

              <div className="bg-white p-3.5 rounded-lg border border-[#dae2fd] shadow-sm flex items-start gap-3 text-xs">
                <div className="w-8 h-8 rounded-full bg-amber-100 flex items-center justify-center text-amber-800 shrink-0">
                  <Info size={16} />
                </div>
                <div>
                  <span className="font-bold text-[#131b2e] block">Active Demonstration Scope</span>
                  <p className="text-gray-600 mt-0.5 leading-relaxed text-[11px]">
                    Kurtas & Kurtis in Odisha region is pre-indexed with live marketplace intelligence data.
                    Explore pricing brackets, fabric trends, and seller performance.
                  </p>
                </div>
              </div>

              {/* Photo Showcase */}
              <div className="grid grid-cols-2 gap-3 pt-1">
                <div className="relative rounded-lg overflow-hidden shadow-sm aspect-4/3 bg-gray-100">
                  <img
                    src="https://images.unsplash.com/photo-1610030469983-98e550d6193c?w=500&auto=format&fit=crop&q=80"
                    alt="Handloom cotton kurti"
                    className="w-full h-full object-cover"
                  />
                  <div className="absolute inset-0 bg-gradient-to-t from-black/80 via-transparent to-transparent flex items-end p-2">
                    <span className="text-white text-[10px] font-bold uppercase tracking-wider font-mono">
                      Handloom Cotton
                    </span>
                  </div>
                </div>

                <div className="relative rounded-lg overflow-hidden shadow-sm aspect-4/3 bg-gray-100">
                  <img
                    src="https://images.unsplash.com/photo-1583391733956-3750e0ff4e8b?w=500&auto=format&fit=crop&q=80"
                    alt="Indigo blue kurti"
                    className="w-full h-full object-cover"
                  />
                  <div className="absolute inset-0 bg-gradient-to-t from-black/80 via-transparent to-transparent flex items-end p-2">
                    <span className="text-white text-[10px] font-bold uppercase tracking-wider font-mono">
                      Indigo Weave
                    </span>
                  </div>
                </div>
              </div>
            </div>

            <div className="pt-3 flex items-center justify-between text-gray-500 font-mono text-[10px] border-t border-[#dae2fd]">
              <span>REGIONAL TAXONOMY: ACTIVE</span>
              <span className="text-[#8a5100] font-bold">1,248 CATALOG ASINS</span>
            </div>
          </div>
        </div>
      </div>

      {/* 6 UPCOMING CATEGORIES (Exact Stitch Grid) */}
      <div>
        <div className="flex items-center justify-between mb-3">
          <span className="text-xs font-bold uppercase tracking-wider text-[#75777c]">
            Planned Expansion Taxonomies (Future Scope)
          </span>
          <span className="text-[11px] text-gray-400 font-mono">6 Categories Scheduled</span>
        </div>

        <div className="grid grid-cols-1 sm:grid-cols-2 lg:grid-cols-3 gap-4">
          {[
            { name: 'Jewellery', desc: 'Fashion Jewellery, Silver, and Traditional Handcrafted Ornaments.', quarter: 'Q3' },
            { name: 'Home & Kitchen', desc: 'Handwoven Bed Linen, Tabletop, and Brass Artisan Ware.', quarter: 'Q3' },
            { name: 'Footwear', desc: 'Ethnic Juttis, Kolhapuris, and Handcrafted Leather Sandals.', quarter: 'Q4' },
            { name: 'Beauty & Personal Care', desc: 'Ayurvedic Botanical Formulations and Herbal Haircare.', quarter: 'Q4' },
            { name: 'Bags & Luggage', desc: 'Handbags, Handcrafted Jute Totes, and Ethnic Clutches.', quarter: 'Q4' },
            { name: 'Electronics Accessories', desc: 'Cases, Fast Charging Cables, and Wearable Straps.', quarter: '2027' },
          ].map((cat) => (
            <div
              key={cat.name}
              className="bg-white rounded-xl p-5 border border-[#e2e8f0] shadow-sm flex flex-col justify-between hover:shadow-md transition"
            >
              <div>
                <div className="flex items-center justify-between mb-2">
                  <span className="font-bold text-sm text-[#131b2e]">{cat.name}</span>
                  <span className="px-2 py-0.5 rounded bg-[#f2f3ff] text-gray-600 font-mono text-[10px] font-semibold uppercase">
                    Coming Soon · {cat.quarter}
                  </span>
                </div>
                <p className="text-xs text-gray-500 leading-relaxed">{cat.desc}</p>
              </div>

              <div className="pt-3 border-t border-gray-100 flex items-center justify-between text-xs text-gray-400 mt-3">
                <span>Planned Category</span>
                <span className="text-[#8a5100] font-semibold text-[11px] flex items-center gap-0.5">
                  <Clock size={12} /> Pre-indexing
                </span>
              </div>
            </div>
          ))}
        </div>
      </div>

      {/* Bottom Early Access Banner (Exact Stitch) */}
      <div className="bg-white rounded-xl p-6 border border-[#e2e8f0] shadow-sm flex flex-col md:flex-row items-start md:items-center justify-between gap-4">
        <div className="flex items-center gap-4">
          <div className="w-12 h-12 rounded-full bg-amber-100 flex items-center justify-center text-[#ff9900] shrink-0">
            <HeartHandshake size={24} />
          </div>
          <div>
            <h3 className="text-base font-bold text-[#131b2e]">Can't find your category?</h3>
            <p className="text-xs text-gray-600 mt-0.5">
              Request early access for regional handicrafts, GI-tagged weaves, and artisan clusters.
            </p>
          </div>
        </div>

        <button
          type="button"
          onClick={() => setRequestedPilot(true)}
          className="px-5 py-2.5 bg-[#131921] hover:bg-slate-800 text-white font-bold text-xs rounded-lg shadow-sm transition whitespace-nowrap cursor-pointer flex items-center gap-2"
        >
          {requestedPilot ? (
            <>
              <CheckCircle2 size={15} className="text-emerald-400" />
              <span>Pilot Request Registered!</span>
            </>
          ) : (
            <>
              <Sparkles size={15} className="text-[#ff9900]" />
              <span>Request Category Pilot</span>
            </>
          )}
        </button>
      </div>
    </div>
  );
}
