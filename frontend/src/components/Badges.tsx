import { colors } from '../theme/tokens';
import { AlertTriangle, CheckCircle2 } from 'lucide-react';

export interface SampleSizeBadgeProps {
  n: number | undefined | null;
  minThreshold?: number; // default 30
  label?: string;
}

export function SampleSizeBadge({ n, minThreshold = 30, label }: SampleSizeBadgeProps) {
  const count = typeof n === 'number' ? n : 0;
  const isThin = count < minThreshold;

  return (
    <span
      className="inline-flex items-center gap-1 px-2 py-0.5 rounded text-xs font-medium font-mono"
      style={{
        backgroundColor: isThin ? '#fef3c7' : '#f0fdf4',
        color: isThin ? '#92400e' : '#166534',
        border: `1px solid ${isThin ? '#fde68a' : '#bbf7d0'}`,
      }}
      title={isThin ? `Sample size n=${count} is below recommended threshold (${minThreshold}). Interpret with caution.` : `Sample size: ${count} verified listings`}
    >
      {isThin && <AlertTriangle size={11} className="text-amber-600" />}
      <span>{label ? `${label} (n=${count})` : `n=${count}`}</span>
      {isThin && <span className="text-[10px] font-semibold text-amber-700 uppercase tracking-wider ml-0.5">Thin</span>}
    </span>
  );
}

export interface ObservationEstimateBadgeProps {
  type: 'observation' | 'estimate' | 'hypothesis';
}

export function ObservationEstimateBadge({ type }: ObservationEstimateBadgeProps) {
  const isObs = type === 'observation';
  const label = isObs ? 'Observed Fact' : type === 'hypothesis' ? 'Hypothesis' : 'Estimate';

  return (
    <span
      className="inline-flex items-center gap-1 px-2 py-0.5 rounded text-xs font-semibold uppercase tracking-wider"
      style={{
        backgroundColor: isObs ? colors.badge.observation.bg : colors.badge.estimate.bg,
        color: isObs ? colors.badge.observation.text : colors.badge.estimate.text,
        border: `1px solid ${isObs ? colors.badge.observation.border : colors.badge.estimate.border}`,
      }}
      title={isObs ? 'Direct observation from collected marketplace records' : 'Model hypothesis or estimate based on heuristic rules'}
    >
      <span className="w-1.5 h-1.5 rounded-full" style={{ backgroundColor: isObs ? '#2563eb' : '#9333ea' }} />
      {label}
    </span>
  );
}

export interface ConfidenceBadgeProps {
  level: 'very_low' | 'low' | 'moderate' | string;
}

export function ConfidenceBadge({ level }: ConfidenceBadgeProps) {
  const normalized = level?.toLowerCase().replace('-', '_');
  const config =
    normalized === 'moderate'
      ? colors.confidence.moderate
      : normalized === 'low'
      ? colors.confidence.low
      : colors.confidence.very_low;

  const display =
    normalized === 'moderate'
      ? 'Moderate Confidence'
      : normalized === 'low'
      ? 'Low Confidence'
      : 'Very Low Confidence';

  return (
    <span
      className="inline-flex items-center gap-1 px-2 py-0.5 rounded text-xs font-semibold"
      style={{
        backgroundColor: config.bg,
        color: config.text,
        border: `1px solid ${config.border}`,
      }}
    >
      {normalized === 'moderate' ? (
        <CheckCircle2 size={12} />
      ) : (
        <AlertTriangle size={12} />
      )}
      {display}
    </span>
  );
}

export interface DemoDataBannerProps {
  dataMode?: 'demo' | 'synthetic' | 'real' | 'mixed' | string;
  sources?: string[];
  asOf?: string;
}

export function DemoDataBanner({ dataMode = 'demo', sources, asOf }: DemoDataBannerProps) {
  const isSynthetic =
    dataMode === 'demo' ||
    dataMode === 'synthetic' ||
    dataMode === 'mixed' ||
    sources?.some(s => s.toLowerCase().includes('synthetic') || s.toLowerCase().includes('demo'));

  if (!isSynthetic) return null;

  return (
    <div
      role="banner"
      className="w-full bg-amber-500 text-slate-900 border-b border-amber-600 px-4 py-2 flex flex-wrap items-center justify-between text-xs font-medium shadow-sm"
      style={{ backgroundColor: '#ff9900', color: '#111827' }}
    >
      <div className="flex items-center gap-2">
        <span className="bg-slate-900 text-white font-bold px-1.5 py-0.5 rounded text-[11px] tracking-wider uppercase">
          DEMO DATA
        </span>
        <span className="font-semibold">
          Notice: Market data shown is synthetic & illustrative for college MVP demonstration.
        </span>
        <span className="hidden md:inline text-slate-800">
          No live scraping of Amazon web pages is ever performed.
        </span>
      </div>
      <div className="flex items-center gap-3 text-[11px] font-mono text-slate-900">
        {asOf && <span>As of: {new Date(asOf).toLocaleDateString()}</span>}
        <span className="bg-white/40 px-2 py-0.5 rounded font-sans font-medium">Compliance Guard Active</span>
      </div>
    </div>
  );
}
