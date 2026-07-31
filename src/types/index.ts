export type RiskLevel = 'low' | 'medium' | 'high' | 'critical';
export type TxStatus = 'approved' | 'pending' | 'blocked' | 'review';

export interface User {
  id: string;
  name: string;
  email: string;
  riskScore: number;
  status: 'active' | 'frozen' | 'review';
  device: string;
  country: string;
  lastLogin: string;
}

export interface Transaction {
  id: string;
  user: string;
  amount: number;
  country: string;
  device: string;
  vpn: boolean;
  riskScore: number;
  status: TxStatus;
  riskLevel: RiskLevel;
  timestamp: string;
}

export interface Incident {
  id: string;
  type: string;
  timestamp: string;
  severity: RiskLevel;
  affectedUser: string;
  recommendedResponse: string;
  resolved: boolean;
}

export interface ThreatLocation {
  id: string;
  name: string;
  lat: number;
  lng: number;
  severity: RiskLevel;
}

export interface AttackLine {
  from: { x: number; y: number };
  to: { x: number; y: number };
  severity: RiskLevel;
}

export interface ToastNotification {
  id: string;
  title: string;
  message: string;
  type: 'danger' | 'warning' | 'success' | 'info';
  timestamp: string;
}

export interface KpiCard {
  id: string;
  label: string;
  value: number;
  trend: number;
  icon: string;
  accent: string;
}
