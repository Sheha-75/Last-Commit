import axios from 'axios';
import {
  generateUsers,
  generateTransactions,
  generateIncidents,
  generateThreats,
  generateTimeline,
  generateLoginAttempts,
  generateRiskDistribution,
} from './mockData';
import type { User, Transaction, Incident, ThreatLocation } from '@/types';

const api = axios.create({
  baseURL: '/api',
  timeout: 8000,
});

function delay<T>(data: T, ms = 600): Promise<T> {
  return new Promise((resolve) => setTimeout(() => resolve(data), ms));
}

let usersCache: User[] | null = null;
let txCache: Transaction[] | null = null;

function seed() {
  if (!usersCache) usersCache = generateUsers(100);
  if (!txCache) txCache = generateTransactions(500, usersCache);
}

export const fraudService = {
  async getUsers(): Promise<User[]> {
    seed();
    return delay([...(usersCache as User[])]);
  },
  async getTransactions(): Promise<Transaction[]> {
    seed();
    return delay([...(txCache as Transaction[])]);
  },
  async getIncidents(): Promise<Incident[]> {
    seed();
    return delay(generateIncidents(txCache as Transaction[], 24));
  },
  async getThreats(): Promise<ThreatLocation[]> {
    return delay(generateThreats());
  },
  async getTimeline() {
    seed();
    return delay(generateTimeline(txCache as Transaction[]));
  },
  async getLoginAttempts() {
    return delay(generateLoginAttempts());
  },
  async getRiskDistribution() {
    seed();
    return delay(generateRiskDistribution(txCache as Transaction[]));
  },
  async getKpis() {
    seed();
    const tx = txCache as Transaction[];
    return delay({
      totalTransactions: tx.length,
      activeUsers: (usersCache as User[]).filter((u) => u.status === 'active').length,
      fraudAlerts: tx.filter((t) => t.riskScore >= 65).length,
      blockedTransactions: tx.filter((t) => t.status === 'blocked').length,
      highRiskAccounts: (usersCache as User[]).filter((u) => u.riskScore >= 65).length,
      aiRiskScore: 73,
    });
  },
};

export default api;
