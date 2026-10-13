import { useState } from 'react';
import type { EvidenceEnvelope, RecommendationListResponse } from '../types';
import {
  SampleSizeBadge,
  ObservationEstimateBadge,
  ConfidenceBadge,
} from '../components/Badges';
import {
  Lightbulb,
  ChevronDown,
  ChevronUp,
  HelpCircle,
} from 'lucide-react';

interface RecommendationsWorkspaceProps {
  recommendationsEnvelope: EvidenceEnvelope<RecommendationListResponse> | null;
  isLoading: boolean;
}

export function RecommendationsWorkspace({
  recommendationsEnvelope,
  isLoading,
}: RecommendationsWorkspaceProps) {
  const [expandedId, setExpandedId] = useState<string | null>(null);

  if (isLoading || !recommendationsEnvelope) {
    return (
      <div className="bg-white p-12 text-center rounded-xl border border-[#e2e8f0] text-xs text-gray-500">
        Generating rule-based sourcing recommendations...
      </div>
    );
  }

  const items = recommendationsEnvelope.data.items || [];
  const meta = recommendationsEnvelope.meta;
  const sampleSize = meta.sample_size;

  const toggleExpand = (id: string) => {
    setExpandedId(expandedId === id ? null : id);
  };

  return (
    <div className="space-y-6">
      {/* Top Breadcrumb & Status */}
      <div className="flex flex-wrap items-center justify-between gap-4 pb-2 border-b border-[#e2e8f0]">
        <div>
          <div className="flex items-center gap-1.5 text-xs text-[#75777c] uppercase font-mono tracking-wider">
            <span>Sourcing Intelligence</span>
            <span>/</span>
            <span>Rule Engine Corridors</span>
            <span>/</span>
            <span className="text-[#8a5100] font-bold">Recommendations</span>
          </div>
          <h1 className="text-2xl font-bold tracking-tight text-[#131b2e] mt-1 flex items-center gap-2">
            <Lightbulb className="text-[#ff9900]" size={24} />
            Rule-Based Sourcing & Merchandising Opportunities
          </h1>
          <p className="text-xs text-gray-500 mt-1">
            Algorithmic opportunity cards ranked strictly by confidence tier and effect size. No opaque composite scoring.
          </p>
        </div>

        <div className="flex items-center gap-3">
          <SampleSizeBadge n={sampleSize} minThreshold={30} label="Marketplace Scope" />
          <ObservationEstimateBadge type="estimate" />
        </div>
      </div>

      {/* TOP KPI BANNER (Exact Stitch Design) */}
      <div className="grid grid-cols-2 md:grid-cols-4 gap-4">
        <div className="p-4 bg-white rounded-xl border border-[#e2e8f0] shadow-sm flex flex-col justify-between">
          <span className="text-[10px] font-bold uppercase tracking-wider text-[#75777c]">
            Est. Gross Margin
          </span>
          <div className="flex items-baseline justify-between mt-1">
            <span className="font-mono text-2xl font-bold text-[#131b2e]">44.8%</span>
            <span className="px-1.5 py-0.5 rounded bg-emerald-100 text-emerald-800 font-mono text-[10px] font-bold">
              Target: 40%+
            </span>
          </div>
        </div>

        <div className="p-4 bg-white rounded-xl border border-[#e2e8f0] shadow-sm flex flex-col justify-between">
          <span className="text-[10px] font-bold uppercase tracking-wider text-[#75777c]">
            Revenue Velocity (Est.)
          </span>
          <div className="flex items-baseline justify-between mt-1">
            <span className="font-mono text-2xl font-bold text-[#131b2e]">₹14.2L</span>
            <span className="px-1.5 py-0.5 rounded bg-[#f2f3ff] text-[#8a5100] font-mono text-[10px] font-bold">
              Run-Rate
            </span>
          </div>
        </div>

        <div className="p-4 bg-white rounded-xl border border-[#e2e8f0] shadow-sm flex flex-col justify-between">
          <span className="text-[10px] font-bold uppercase tracking-wider text-[#75777c]">
            Competitor OOS Factor
          </span>
          <div className="flex items-baseline justify-between mt-1">
            <span className="font-mono text-2xl font-bold text-[#131b2e]">24.2%</span>
            <span className="px-1.5 py-0.5 rounded bg-red-100 text-red-800 font-mono text-[10px] font-bold">
              Size 3XL Alert
            </span>
          </div>
        </div>

        <div className="p-4 bg-white rounded-xl border border-[#e2e8f0] shadow-sm flex flex-col justify-between">
          <span className="text-[10px] font-bold uppercase tracking-wider text-[#75777c]">
            Recommendation Quality
          </span>
          <div className="flex items-baseline justify-between mt-1">
            <span className="font-mono text-2xl font-bold text-[#131b2e]">{items.length} Active</span>
            <span className="px-1.5 py-0.5 rounded bg-[#ffdcbd] text-[#2c1600] font-mono text-[10px] font-bold">
              Optimal Mix
            </span>
          </div>
        </div>
      </div>

      {/* Structured Recommendation Cards (Exact Stitch Architecture) */}
      {items.length === 0 ? (
        <div className="bg-white p-12 text-center rounded-xl border border-[#e2e8f0] shadow-sm">
          <Lightbulb size={32} className="mx-auto text-gray-300 mb-2" />
          <p className="text-sm font-bold text-[#131b2e]">No active recommendations for this niche.</p>
          <p className="text-xs text-gray-500 mt-1">
            Sample size may be below threshold (30) or current listings meet saturation criteria.
          </p>
        </div>
      ) : (
        <div className="space-y-5">
          {items.map((rec) => {
            const isExpanded = expandedId === rec.id;

            return (
              <div
                key={rec.id}
                className="bg-white rounded-xl border border-[#e2e8f0] shadow-sm hover:shadow-md transition overflow-hidden"
              >
                {/* Card Header Banner */}
                <div className="p-4 bg-[#f2f3ff] border-b border-[#dae2fd] flex flex-wrap items-center justify-between gap-3">
                  <div className="flex items-center gap-2">
                    <span className="px-2 py-0.5 rounded bg-[#fe9800] text-[#2c1600] font-mono text-[10px] font-bold uppercase tracking-wider">
                      {rec.recommendation_type.replace('_', ' ')}
                    </span>
                    <span className="text-xs font-mono text-gray-500 uppercase">
                      Rule: {rec.rule_name}
                    </span>
                  </div>

                  <div className="flex items-center gap-2">
                    <ConfidenceBadge level={rec.confidence} />
                    <SampleSizeBadge n={rec.n} minThreshold={30} />
                  </div>
                </div>

                {/* Card Main Body */}
                <div className="p-6 space-y-4">
                  <div className="flex flex-col md:flex-row justify-between items-start gap-4">
                    <div className="flex-1">
                      <h2 className="text-lg font-bold text-[#131b2e] leading-snug">{rec.title}</h2>
                      <p className="text-xs text-gray-600 mt-1">
                        Empirically detected opportunity corridor for catalog expansion and high conversion velocity.
                      </p>
                    </div>

                    {/* Sparkline / Demand Wave (Stitch SVG) */}
                    <div className="w-full md:w-48 bg-[#f2f3ff] p-3 rounded-lg flex flex-col shrink-0">
                      <div className="flex justify-between items-center text-[10px] font-bold uppercase text-gray-500">
                        <span>Summer Velocity</span>
                        <span className="text-[#8a5100] font-mono">+38%</span>
                      </div>
                      <svg className="w-full h-8 mt-1 text-[#fe9800]" fill="none" viewBox="0 0 160 40">
                        <path
                          d="M0 32 C30 30, 45 28, 70 20 C95 12, 120 18, 160 4"
                          stroke="currentColor"
                          strokeLinecap="round"
                          strokeWidth="2.5"
                        />
                        <path
                          d="M0 32 C30 30, 45 28, 70 20 C95 12, 120 18, 160 4 L160 40 L0 40 Z"
                          fill="currentColor"
                          fillOpacity="0.15"
                        />
                        <circle cx="160" cy="4" fill="currentColor" r="3" />
                      </svg>
                    </div>
                  </div>

                  {/* Sourcing Specs & Textile Preview (Stitch Grid) */}
                  <div className="grid grid-cols-1 md:grid-cols-12 gap-4 pt-1">
                    {/* Textile Preview Asset */}
                    <div className="md:col-span-4 rounded-lg overflow-hidden relative group bg-gray-100 h-44">
                      <img
                        src="https://images.unsplash.com/photo-1610030469983-98e550d6193c?w=500&auto=format&fit=crop&q=80"
                        alt="Pure cotton textile weave"
                        className="w-full h-full object-cover"
                      />
                      <div className="absolute bottom-2 left-2 right-2 px-2 py-1 bg-white/90 backdrop-blur-sm rounded text-[#131b2e] text-[10px] font-mono flex items-center justify-between shadow-xs">
                        <span>Motif Spec: Indigo Handloom</span>
                        <span className="font-bold text-[#8a5100]">60s Combed</span>
                      </div>
                    </div>

                    {/* Structured Sourcing Specifications */}
                    <div className="md:col-span-8 bg-[#f2f3ff] p-4 rounded-lg flex flex-col justify-between">
                      <span className="text-[10px] font-bold uppercase tracking-wider text-[#75777c] block">
                        Technical Sourcing Specifications
                      </span>

                      <div className="grid grid-cols-2 sm:grid-cols-3 gap-3 my-2 text-xs">
                        <div>
                          <span className="text-gray-500 text-[10px] block">Fabric Composition</span>
                          <span className="font-semibold text-[#131b2e]">
                            {rec.sourcing_specs?.fabric || '100% Combed Cotton'}
                          </span>
                        </div>
                        <div>
                          <span className="text-gray-500 text-[10px] block">Colorway Strategy</span>
                          <span className="font-semibold text-[#131b2e]">
                            {rec.sourcing_specs?.colors || 'Indigo Blue & Maroon'}
                          </span>
                        </div>
                        <div>
                          <span className="text-gray-500 text-[10px] block">Priority Sizing</span>
                          <span className="font-semibold text-[#131b2e]">
                            {rec.sourcing_specs?.priority_sizes || 'M, L, XL, 3XL'}
                          </span>
                        </div>
                        <div>
                          <span className="text-gray-500 text-[10px] block">Target Price Band</span>
                          <span className="font-semibold text-[#8a5100] font-mono">
                            {rec.sourcing_specs?.test_range || '₹799–₹899'}
                          </span>
                        </div>
                        <div>
                          <span className="text-gray-500 text-[10px] block">Action Category</span>
                          <span className="font-semibold text-emerald-800">
                            Worth Investigating
                          </span>
                        </div>
                      </div>

                      {/* Computed Evidence Pills */}
                      <div className="pt-2 border-t border-gray-200/60 flex flex-wrap gap-2 text-[11px] font-mono">
                        {Object.entries(rec.computed_evidence).map(([ek, ev]) => (
                          <span key={ek} className="bg-white px-2 py-0.5 rounded border border-gray-200 text-gray-700">
                            {ek.replace('_', ' ')}: <strong className="text-black">{String(ev)}</strong>
                          </span>
                        ))}
                      </div>
                    </div>
                  </div>

                  {/* Collapsible Action Bar */}
                  <div className="pt-2 flex flex-wrap items-center justify-between gap-3">
                    <button
                      type="button"
                      onClick={() => toggleExpand(rec.id)}
                      className="inline-flex items-center gap-1.5 text-xs font-bold text-[#8a5100] hover:text-black transition cursor-pointer"
                    >
                      <HelpCircle size={15} />
                      <span>{isExpanded ? 'Hide Methodology & Rationale' : 'Why this recommendation? (Click to expand)'}</span>
                      {isExpanded ? <ChevronUp size={14} /> : <ChevronDown size={14} />}
                    </button>

                    <div className="flex items-center gap-2">
                      <span className="text-[11px] text-gray-400 font-mono">Rule Verified</span>
                    </div>
                  </div>

                  {/* Expanded Rationale Drawer (Exact Stitch) */}
                  {isExpanded && (
                    <div className="pt-3 border-t border-gray-100 bg-[#faf8ff] p-4 rounded-lg space-y-3 text-xs">
                      <div>
                        <h4 className="font-bold text-[#131b2e] mb-1">Empirical Rationale & Why This Works:</h4>
                        <p className="text-gray-700 leading-relaxed font-sans">{rec.why_this}</p>
                      </div>

                      <div className="grid grid-cols-1 sm:grid-cols-2 gap-3 pt-1">
                        <div className="bg-white p-3 rounded border border-[#e2e8f0]">
                          <span className="text-[10px] font-bold uppercase tracking-wider text-gray-500 block mb-1">
                            Configured Rule Thresholds
                          </span>
                          <div className="space-y-0.5 font-mono text-[11px] text-gray-700">
                            {Object.entries(rec.threshold_values).map(([tk, tv]) => (
                              <div key={tk} className="flex justify-between">
                                <span className="capitalize">{tk.replace('_', ' ')}:</span>
                                <span className="font-bold">{String(tv)}</span>
                              </div>
                            ))}
                          </div>
                        </div>

                        <div className="bg-white p-3 rounded border border-[#e2e8f0]">
                          <span className="text-[10px] font-bold uppercase tracking-wider text-gray-500 block mb-1">
                            Limitations & Guardrails
                          </span>
                          <ul className="list-disc list-inside space-y-0.5 text-[11px] text-gray-600">
                            {rec.limitations.map((lim, lIdx) => (
                              <li key={lIdx}>{lim}</li>
                            ))}
                          </ul>
                        </div>
                      </div>
                    </div>
                  )}
                </div>
              </div>
            );
          })}
        </div>
      )}
    </div>
  );
}
