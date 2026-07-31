import { lazy, Suspense } from 'react';
import { BrowserRouter, Routes, Route, Navigate } from 'react-router-dom';
import { AuthProvider, useAuth } from '@/hooks/useAuth';
import { useToasts } from '@/hooks/useToasts';
import { ToastContainer } from '@/components/ui/Toast';
import { SocLayout } from '@/layouts/SocLayout';
import Login from '@/pages/Login';
import type { ToastNotification } from '@/types';
import type { ReactNode } from 'react';
import { ShieldLogo } from '@/components/ShieldLogo';

const Dashboard = lazy(() => import('@/pages/Dashboard'));
const Simulation = lazy(() => import('@/pages/Simulation'));
const RiskAnalytics = lazy(() => import('@/pages/RiskAnalytics'));
const Users = lazy(() => import('@/pages/Users'));
const Transactions = lazy(() => import('@/pages/Transactions'));
const Incidents = lazy(() => import('@/pages/Incidents'));
const AiInsights = lazy(() => import('@/pages/AiInsights'));
const ThreatDetection = lazy(() => import('@/pages/ThreatDetection'));
const Settings = lazy(() => import('@/pages/Settings'));

function PageFallback() {
  return (
    <div className="flex items-center justify-center min-h-[60vh]">
      <ShieldLogo size={56} />
    </div>
  );
}

function ProtectedRoute({ children }: { children: ReactNode }) {
  const { user } = useAuth();
  if (!user) return <Navigate to="/" replace />;
  return <>{children}</>;
}

function AppRoutes() {
  const { toasts, push, dismiss } = useToasts();
  const { user } = useAuth();

  return (
    <>
      <ToastContainer toasts={toasts} onDismiss={dismiss} />
      <Routes>
        <Route path="/" element={user ? <Navigate to="/app/dashboard" replace /> : <Login />} />
        <Route
          path="/app"
          element={
            <ProtectedRoute>
              <SocLayout notifications={toasts} onOpenNotifications={() => {}} pushToast={push} />
            </ProtectedRoute>
          }
        >
          <Route index element={<Navigate to="dashboard" replace />} />
          <Route path="dashboard" element={<Suspense fallback={<PageFallback />}><Dashboard pushToast={push} /></Suspense>} />
          <Route path="transactions" element={<Suspense fallback={<PageFallback />}><Transactions /></Suspense>} />
          <Route path="threat-detection" element={<Suspense fallback={<PageFallback />}><ThreatDetection /></Suspense>} />
          <Route path="incidents" element={<Suspense fallback={<PageFallback />}><Incidents /></Suspense>} />
          <Route path="risk-analytics" element={<Suspense fallback={<PageFallback />}><RiskAnalytics /></Suspense>} />
          <Route path="users" element={<Suspense fallback={<PageFallback />}><Users /></Suspense>} />
          <Route path="ai-insights" element={<Suspense fallback={<PageFallback />}><AiInsights /></Suspense>} />
          <Route path="simulation" element={<Suspense fallback={<PageFallback />}><Simulation pushToast={push} /></Suspense>} />
          <Route path="settings" element={<Suspense fallback={<PageFallback />}><Settings /></Suspense>} />
        </Route>
        <Route path="*" element={<Navigate to="/" replace />} />
      </Routes>
    </>
  );
}

function App() {
  return (
    <AuthProvider>
      <BrowserRouter>
        <AppRoutes />
      </BrowserRouter>
    </AuthProvider>
  );
}

export default App;
