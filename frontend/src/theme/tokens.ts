/**
 * Stitch Design System Theme Tokens
 * Direct extraction from Stitch project "Amazon Vendor Assist (AVA) Prototype"
 * Project ID: 8542281932053266715
 */

export const colors = {
  // Stitch Surfaces & Canvas
  surface: {
    canvas: '#faf8ff',
    dim: '#d2d9f4',
    bright: '#faf8ff',
    containerLowest: '#ffffff',
    containerLow: '#f2f3ff',
    container: '#eaedff',
    containerHigh: '#e2e7ff',
    containerHighest: '#dae2fd',
    onSurface: '#131b2e',
    onSurfaceVariant: '#45474b',
    outline: '#75777c',
    outlineVariant: '#c5c6cb',
  },

  // Amazon Brand Palettes
  brand: {
    navyDark: '#131921',         // Primary top bar & console navy
    navyMedium: '#232f3e',       // Secondary navigation menu bar
    navySurface: '#161c24',      // Primary container
    orange: '#ff9900',           // Amazon action orange (primary CTA)
    orangeHover: '#f08800',      // Action hover
    orangeContainer: '#fe9800',  // Secondary container
    amber: '#febd69',            // Accent highlight
    linkTeal: '#007185',         // Amazon link teal
    linkTealHover: '#004b57',
  },

  // Status & Semantic Feedback
  semantic: {
    success: '#067d62',
    successBg: '#f0fdf4',
    warning: '#f59e0b',
    warningBg: '#fffbeb',
    error: '#b12704',
    errorBg: '#fef2f2',
    info: '#0284c7',
    infoBg: '#f0f9ff',
  },

  // Confidence Tiers (Section 8: very_low, low, moderate - NEVER "high")
  confidence: {
    moderate: { text: '#065f46', bg: '#d1fae5', border: '#a7f3d0' },
    low: { text: '#92400e', bg: '#fef3c7', border: '#fde68a' },
    very_low: { text: '#991b1b', bg: '#fee2e2', border: '#fecaca' },
  },

  // Badges & Labels
  badge: {
    observation: { text: '#1e40af', bg: '#dbeafe', border: '#bfdbfe' },
    estimate: { text: '#6b21a8', bg: '#f3e8ff', border: '#e9d5ff' },
    demoData: { text: '#991b1b', bg: '#fef2f2', border: '#f87171' },
    planned: { text: '#4b5563', bg: '#f3f4f6', border: '#e5e7eb' },
  },
} as const;

export const typography = {
  fontFamily: {
    sans: '"Hanken Grotesk", -apple-system, BlinkMacSystemFont, "Segoe UI", Roboto, sans-serif',
    mono: '"JetBrains Mono", monospace',
  },
  fontSize: {
    xs: '0.6875rem',  // 11px
    sm: '0.75rem',    // 12px
    base: '0.8125rem',// 13px (Stitch body-md)
    md: '0.875rem',   // 14px
    lg: '1rem',       // 16px (Stitch headline-sm)
    xl: '1.25rem',    // 20px (Stitch headline-lg)
    xxl: '1.75rem',   // 28px (Stitch headline-xl)
  },
} as const;
