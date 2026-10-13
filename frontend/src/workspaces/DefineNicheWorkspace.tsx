import { useState, useEffect } from 'react';
import type { Niche, NicheFilter } from '../types';
import { SampleSizeBadge } from '../components/Badges';
import { Sliders, BookmarkPlus, AlertTriangle, Check, RefreshCw } from 'lucide-react';

interface DefineNicheWorkspaceProps {
  category: string;
  currentFilter: NicheFilter;
  onFilterChange: (filter: NicheFilter) => void;
  savedNiches: Niche[];
  activeNicheId?: string;
  onSelectNiche: (niche: Niche) => void;
  onSaveNiche: (name: string, description: string, filter: NicheFilter) => Promise<void>;
  onPreviewNiche: (filter: NicheFilter) => Promise<number>;
}

export function DefineNicheWorkspace({
  category,
  currentFilter,
  onFilterChange,
  savedNiches,
  activeNicheId,
  onSelectNiche,
  onSaveNiche,
  onPreviewNiche,
}: DefineNicheWorkspaceProps) {
  const [filterState, setFilterState] = useState<NicheFilter>(currentFilter);
  const [previewCount, setPreviewCount] = useState<number | null>(null);
  const [isPreviewLoading, setIsPreviewLoading] = useState(false);
  const [nicheName, setNicheName] = useState('');
  const [nicheDesc, setNicheDesc] = useState('');
  const [saveSuccess, setSaveSuccess] = useState(false);

  // Update preview on filter changes
  useEffect(() => {
    let isCancelled = false;
    async function updatePreview() {
      setIsPreviewLoading(true);
      try {
        const count = await onPreviewNiche(filterState);
        if (!isCancelled) setPreviewCount(count);
      } catch {
        if (!isCancelled) setPreviewCount(null);
      } finally {
        if (!isCancelled) setIsPreviewLoading(false);
      }
    }
    const timer = setTimeout(updatePreview, 300);
    return () => {
      isCancelled = true;
      clearTimeout(timer);
    };
  }, [filterState]);

  const handleApplyFilter = () => {
    onFilterChange(filterState);
  };

  const handleSave = async (e: React.FormEvent) => {
    e.preventDefault();
    if (!nicheName.trim()) return;
    await onSaveNiche(nicheName.trim(), nicheDesc.trim(), filterState);
    setSaveSuccess(true);
    setNicheName('');
    setNicheDesc('');
    setTimeout(() => setSaveSuccess(false), 3000);
  };

  const isThinSample = previewCount !== null && previewCount < 30;

  return (
    <div className="grid grid-cols-1 lg:grid-cols-3 gap-6">
      {/* Filter Builder (2 cols) */}
      <div className="lg:col-span-2 space-y-6">
        <div className="border-b border-gray-200 pb-4">
          <h2 className="text-xl font-bold text-gray-900 flex items-center gap-2">
            <Sliders className="text-amber-500" size={22} />
            Define & Customize Niche
          </h2>
          <p className="text-sm text-gray-600 mt-1">
            Build custom target segments for <span className="font-semibold text-gray-800">{category}</span>. All
            analytics, product tables, and AI insights update live.
          </p>
        </div>

        {/* Live Preview Box */}
        <div
          className={`p-4 rounded-lg border flex flex-wrap items-center justify-between gap-4 transition-colors ${
            isThinSample
              ? 'bg-amber-50/70 border-amber-300'
              : 'bg-emerald-50/60 border-emerald-300'
          }`}
        >
          <div className="flex items-center gap-3">
            <div className="flex flex-col">
              <span className="text-xs uppercase font-bold text-gray-500 tracking-wider">
                Live Sample Size Preview
              </span>
              <div className="flex items-center gap-2 mt-0.5">
                <span className="text-2xl font-bold font-mono text-gray-900">
                  {isPreviewLoading ? (
                    <RefreshCw size={20} className="animate-spin text-gray-400" />
                  ) : (
                    previewCount ?? '—'
                  )}
                </span>
                <SampleSizeBadge n={previewCount} minThreshold={30} label="Marketplace Listings" />
              </div>
            </div>
          </div>

          {isThinSample && (
            <div className="flex items-center gap-2 text-xs text-amber-800 bg-amber-100/70 px-3 py-1.5 rounded-md border border-amber-300">
              <AlertTriangle size={15} className="text-amber-600 flex-shrink-0" />
              <span>
                <strong>Warning:</strong> Sample size &lt; 30. Statistical insights will be suppressed to avoid false conclusions.
              </span>
            </div>
          )}

          <button
            type="button"
            onClick={handleApplyFilter}
            className="px-4 py-2 bg-slate-900 hover:bg-slate-800 text-white text-xs font-semibold rounded-md shadow-sm transition-colors"
          >
            Apply Niche to All Workspaces
          </button>
        </div>

        {/* Filter Controls */}
        <div className="bg-white p-5 rounded-lg border border-gray-200 shadow-sm space-y-5">
          <h3 className="text-sm font-bold uppercase tracking-wider text-gray-700">Filter Parameters</h3>

          <div className="grid grid-cols-1 sm:grid-cols-2 gap-4">
            {/* Price Min / Max */}
            <div>
              <label className="block text-xs font-medium text-gray-700 mb-1">Min Price (₹)</label>
              <input
                type="number"
                placeholder="e.g. 400"
                value={filterState.price_min ?? ''}
                onChange={(e) =>
                  setFilterState({
                    ...filterState,
                    price_min: e.target.value ? Number(e.target.value) : undefined,
                  })
                }
                className="w-full text-xs p-2 rounded border border-gray-300 focus:outline-none focus:border-amber-500"
              />
            </div>
            <div>
              <label className="block text-xs font-medium text-gray-700 mb-1">Max Price (₹)</label>
              <input
                type="number"
                placeholder="e.g. 1200"
                value={filterState.price_max ?? ''}
                onChange={(e) =>
                  setFilterState({
                    ...filterState,
                    price_max: e.target.value ? Number(e.target.value) : undefined,
                  })
                }
                className="w-full text-xs p-2 rounded border border-gray-300 focus:outline-none focus:border-amber-500"
              />
            </div>

            {/* Material */}
            <div>
              <label className="block text-xs font-medium text-gray-700 mb-1">Fabric / Material</label>
              <select
                value={filterState.materials?.[0] || ''}
                onChange={(e) =>
                  setFilterState({
                    ...filterState,
                    materials: e.target.value ? [e.target.value] : undefined,
                  })
                }
                className="w-full text-xs p-2 rounded border border-gray-300 focus:outline-none focus:border-amber-500"
              >
                <option value="">All Fabrics</option>
                <option value="Cotton">Pure Cotton</option>
                <option value="Rayon">Rayon</option>
                <option value="Silk Blend">Silk Blend</option>
                <option value="Georgette">Georgette</option>
                <option value="Chanderi">Chanderi</option>
                <option value="Mulmul">Mulmul</option>
              </select>
            </div>

            {/* Pattern */}
            <div>
              <label className="block text-xs font-medium text-gray-700 mb-1">Pattern</label>
              <select
                value={filterState.patterns?.[0] || ''}
                onChange={(e) =>
                  setFilterState({
                    ...filterState,
                    patterns: e.target.value ? [e.target.value] : undefined,
                  })
                }
                className="w-full text-xs p-2 rounded border border-gray-300 focus:outline-none focus:border-amber-500"
              >
                <option value="">All Patterns</option>
                <option value="Printed">Printed</option>
                <option value="Solid">Solid</option>
                <option value="Floral">Floral</option>
                <option value="Embroidered">Embroidered</option>
                <option value="Ikat">Ikat</option>
                <option value="Bandhani">Bandhani</option>
                <option value="Anarkali">Anarkali</option>
              </select>
            </div>

            {/* Sizes */}
            <div>
              <label className="block text-xs font-medium text-gray-700 mb-1">Must Offer Size</label>
              <select
                value={filterState.sizes?.[0] || ''}
                onChange={(e) =>
                  setFilterState({
                    ...filterState,
                    sizes: e.target.value ? [e.target.value] : undefined,
                  })
                }
                className="w-full text-xs p-2 rounded border border-gray-300 focus:outline-none focus:border-amber-500"
              >
                <option value="">Any Size</option>
                <option value="S">S</option>
                <option value="M">M</option>
                <option value="L">L</option>
                <option value="XL">XL</option>
                <option value="XXL">XXL</option>
                <option value="3XL">3XL</option>
                <option value="4XL">4XL</option>
              </select>
            </div>

            {/* Min Rating */}
            <div>
              <label className="block text-xs font-medium text-gray-700 mb-1">Min Rating (Stars)</label>
              <select
                value={filterState.min_rating ?? ''}
                onChange={(e) =>
                  setFilterState({
                    ...filterState,
                    min_rating: e.target.value ? Number(e.target.value) : undefined,
                  })
                }
                className="w-full text-xs p-2 rounded border border-gray-300 focus:outline-none focus:border-amber-500"
              >
                <option value="">Any Rating</option>
                <option value="3.5">3.5★ and above</option>
                <option value="4.0">4.0★ and above</option>
                <option value="4.2">4.2★ and above</option>
                <option value="4.5">4.5★ and above</option>
              </select>
            </div>
          </div>

          {/* Keyword Search */}
          <div>
            <label className="block text-xs font-medium text-gray-700 mb-1">Keyword in Title</label>
            <input
              type="text"
              placeholder="e.g. straight, a-line, festive, daily wear"
              value={filterState.keyword ?? ''}
              onChange={(e) =>
                setFilterState({
                  ...filterState,
                  keyword: e.target.value || undefined,
                })
              }
              className="w-full text-xs p-2 rounded border border-gray-300 focus:outline-none focus:border-amber-500"
            />
          </div>

          <div className="pt-2 flex items-center justify-between">
            <button
              type="button"
              onClick={() => {
                const cleared: NicheFilter = { category };
                setFilterState(cleared);
                onFilterChange(cleared);
              }}
              className="text-xs text-gray-500 hover:text-gray-800 underline"
            >
              Reset to Category Default
            </button>
            <button
              type="button"
              onClick={handleApplyFilter}
              className="px-4 py-2 bg-amber-500 hover:bg-amber-600 text-slate-900 font-bold text-xs rounded shadow-sm transition-colors"
            >
              Apply Filter
            </button>
          </div>
        </div>
      </div>

      {/* Saved Niches & Save Box (1 col) */}
      <div className="space-y-6">
        {/* Save Current Niche */}
        <div className="bg-white p-5 rounded-lg border border-gray-200 shadow-sm space-y-4">
          <h3 className="text-sm font-bold uppercase tracking-wider text-gray-700 flex items-center gap-1.5">
            <BookmarkPlus size={16} className="text-amber-500" />
            Save this Niche
          </h3>
          <p className="text-xs text-gray-500">
            Bookmark these filter criteria for fast access across sessions.
          </p>

          <form onSubmit={handleSave} className="space-y-3">
            <div>
              <label className="block text-xs font-medium text-gray-700 mb-1">Niche Name *</label>
              <input
                type="text"
                required
                placeholder="e.g. Budget Daily Cotton Kurtis"
                value={nicheName}
                onChange={(e) => setNicheName(e.target.value)}
                className="w-full text-xs p-2 rounded border border-gray-300 focus:outline-none focus:border-amber-500"
              />
            </div>
            <div>
              <label className="block text-xs font-medium text-gray-700 mb-1">Description (optional)</label>
              <input
                type="text"
                placeholder="Targeting ₹500–₹999 high-volume cotton segment"
                value={nicheDesc}
                onChange={(e) => setNicheDesc(e.target.value)}
                className="w-full text-xs p-2 rounded border border-gray-300 focus:outline-none focus:border-amber-500"
              />
            </div>

            <button
              type="submit"
              className="w-full py-2 bg-slate-900 hover:bg-slate-800 text-white text-xs font-semibold rounded shadow-sm flex items-center justify-center gap-1.5 transition-colors"
            >
              <BookmarkPlus size={14} />
              Save Niche
            </button>

            {saveSuccess && (
              <div className="text-xs font-semibold text-emerald-700 flex items-center gap-1 mt-1 justify-center">
                <Check size={14} /> Niche saved successfully!
              </div>
            )}
          </form>
        </div>

        {/* Saved Niches List */}
        <div className="bg-white p-5 rounded-lg border border-gray-200 shadow-sm space-y-3">
          <h3 className="text-sm font-bold uppercase tracking-wider text-gray-700">Saved Niches</h3>

          {savedNiches.length === 0 ? (
            <p className="text-xs text-gray-400 italic">No saved niches yet.</p>
          ) : (
            <div className="space-y-2.5">
              {savedNiches.map((niche) => {
                const isSelected = activeNicheId === niche.id;
                return (
                  <div
                    key={niche.id}
                    onClick={() => onSelectNiche(niche)}
                    className={`p-3 rounded border text-left cursor-pointer transition-all ${
                      isSelected
                        ? 'border-amber-500 bg-amber-50/40 ring-1 ring-amber-400'
                        : 'border-gray-200 hover:border-amber-300 hover:bg-gray-50'
                    }`}
                  >
                    <div className="flex items-center justify-between">
                      <span className="text-xs font-bold text-gray-900">{niche.name}</span>
                      <SampleSizeBadge n={niche.sample_size} minThreshold={30} />
                    </div>
                    {niche.description && (
                      <p className="text-[11px] text-gray-500 mt-1 line-clamp-1">{niche.description}</p>
                    )}
                  </div>
                );
              })}
            </div>
          )}
        </div>
      </div>
    </div>
  );
}
