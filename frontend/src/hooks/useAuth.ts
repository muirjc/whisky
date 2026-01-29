import { createContext, useContext, useState, useCallback } from "react";
import { api, AuthResponse, setToken, clearToken, isAuthenticated } from "../services/api";

export interface AuthContextType {
  user: AuthResponse["user"] | null;
  isLoggedIn: boolean;
  login: (email: string, password: string) => Promise<void>;
  register: (email: string, password: string) => Promise<void>;
  logout: () => void;
  error: string | null;
}

export const AuthContext = createContext<AuthContextType | null>(null);

export function useAuth(): AuthContextType {
  const ctx = useContext(AuthContext);
  if (!ctx) throw new Error("useAuth must be used within AuthProvider");
  return ctx;
}

export function useAuthState(): AuthContextType {
  const [user, setUser] = useState<AuthResponse["user"] | null>(() => {
    const stored = localStorage.getItem("auth_user");
    return stored ? JSON.parse(stored) as AuthResponse["user"] : null;
  });
  const [error, setError] = useState<string | null>(null);

  const login = useCallback(async (email: string, password: string) => {
    setError(null);
    try {
      const resp = await api.post<AuthResponse>("/auth/login", { email, password });
      setToken(resp.access_token);
      localStorage.setItem("auth_user", JSON.stringify(resp.user));
      setUser(resp.user);
    } catch (e) {
      setError(e instanceof Error ? e.message : "Login failed");
      throw e;
    }
  }, []);

  const register = useCallback(async (email: string, password: string) => {
    setError(null);
    try {
      const resp = await api.post<AuthResponse>("/auth/register", { email, password });
      setToken(resp.access_token);
      localStorage.setItem("auth_user", JSON.stringify(resp.user));
      setUser(resp.user);
    } catch (e) {
      setError(e instanceof Error ? e.message : "Registration failed");
      throw e;
    }
  }, []);

  const logout = useCallback(() => {
    clearToken();
    localStorage.removeItem("auth_user");
    setUser(null);
  }, []);

  return {
    user,
    isLoggedIn: isAuthenticated() && !!user,
    login,
    register,
    logout,
    error,
  };
}
