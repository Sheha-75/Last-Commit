import { createContext, useContext, useState, type ReactNode } from 'react';

interface AuthState {
  user: { email: string; name: string } | null;
  login: (email: string, password: string) => Promise<void>;
  logout: () => void;
}

const AuthContext = createContext<AuthState | undefined>(undefined);

export function AuthProvider({ children }: { children: ReactNode }) {
  const [user, setUser] = useState<AuthState['user']>(null);

  async function login(email: string, _password: string) {
    await new Promise((r) => setTimeout(r, 700));
    setUser({ email, name: email.split('@')[0].replace(/^\w/, (c) => c.toUpperCase()) });
  }

  function logout() {
    setUser(null);
  }

  return <AuthContext.Provider value={{ user, login, logout }}>{children}</AuthContext.Provider>;
}

export function useAuth() {
  const ctx = useContext(AuthContext);
  if (!ctx) throw new Error('useAuth must be used within AuthProvider');
  return ctx;
}
