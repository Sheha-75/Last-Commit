import { clsx, type ClassValue } from 'clsx';
import { twMerge } from 'tailwind-merge';

export function cn(...inputs: ClassValue[]) {
  return twMerge(clsx(inputs));
}

export function formatCurrency(n: number) {
  return new Intl.NumberFormat('en-US', { style: 'currency', currency: 'USD', maximumFractionDigits: 0 }).format(n);
}

export function formatNumber(n: number) {
  return new Intl.NumberFormat('en-US').format(n);
}

export function timeAgo(iso: string) {
  const diff = Date.now() - new Date(iso).getTime();
  const mins = Math.floor(diff / 60000);
  if (mins < 1) return 'just now';
  if (mins < 60) return `${mins}m ago`;
  const hrs = Math.floor(mins / 60);
  if (hrs < 24) return `${hrs}h ago`;
  return `${Math.floor(hrs / 24)}d ago`;
}

export const riskColor: Record<string, { text: string; bg: string; border: string; hex: string }> = {
  low: { text: 'text-emerald-400', bg: 'bg-emerald-500/15', border: 'border-emerald-500/40', hex: '#22C55E' },
  medium: { text: 'text-amber-400', bg: 'bg-amber-500/15', border: 'border-amber-500/40', hex: '#F59E0B' },
  high: { text: 'text-orange-400', bg: 'bg-orange-500/15', border: 'border-orange-500/40', hex: '#F97316' },
  critical: { text: 'text-red-400', bg: 'bg-red-500/15', border: 'border-red-500/40', hex: '#EF4444' },
};

export const statusColor: Record<string, string> = {
  approved: 'text-emerald-400 bg-emerald-500/15 border-emerald-500/40',
  pending: 'text-amber-400 bg-amber-500/15 border-amber-500/40',
  blocked: 'text-red-400 bg-red-500/15 border-red-500/40',
  review: 'text-orange-400 bg-orange-500/15 border-orange-500/40',
};
