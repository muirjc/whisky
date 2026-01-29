const API_BASE_URL = import.meta.env.VITE_API_URL || "http://localhost:8000/api/v1";

function getToken(): string | null {
  return localStorage.getItem("auth_token");
}

export function setToken(token: string): void {
  localStorage.setItem("auth_token", token);
}

export function clearToken(): void {
  localStorage.removeItem("auth_token");
}

export function isAuthenticated(): boolean {
  return !!getToken();
}

async function request<T>(
  path: string,
  options: RequestInit = {}
): Promise<T> {
  const token = getToken();
  const headers: Record<string, string> = {
    "Content-Type": "application/json",
    ...(options.headers as Record<string, string>),
  };
  if (token) {
    headers["Authorization"] = `Bearer ${token}`;
  }

  const response = await fetch(`${API_BASE_URL}${path}`, {
    ...options,
    headers,
  });

  if (response.status === 401) {
    clearToken();
    window.location.href = "/login";
    throw new Error("Unauthorized");
  }

  if (response.status === 204) {
    return undefined as T;
  }

  if (!response.ok) {
    const error = (await response.json().catch(() => ({ detail: "Request failed" }))) as { detail?: string };
    throw new Error(error.detail ?? `HTTP ${response.status}`);
  }

  return response.json() as Promise<T>;
}

export const api = {
  get: <T>(path: string) => request<T>(path),

  post: <T>(path: string, body?: unknown) =>
    request<T>(path, {
      method: "POST",
      body: body ? JSON.stringify(body) : undefined,
    }),

  put: <T>(path: string, body?: unknown) =>
    request<T>(path, {
      method: "PUT",
      body: body ? JSON.stringify(body) : undefined,
    }),

  delete: <T>(path: string) =>
    request<T>(path, { method: "DELETE" }),
};

// Types
export interface FlavorProfile {
  smoky_peaty: number;
  fruity: number;
  sherried: number;
  spicy: number;
  floral_grassy: number;
  maritime: number;
  honey_sweet: number;
  vanilla_caramel: number;
  oak_woody: number;
  nutty: number;
  malty_biscuity: number;
  medicinal_iodine: number;
}

export interface Bottle {
  id: string;
  name: string;
  distillery_name: string;
  distillery: { id: string; slug: string; name: string; region: string; country: string } | null;
  age_statement: number | null;
  region: string;
  country: string;
  size_ml: number | null;
  abv: number | null;
  flavor_profile: FlavorProfile | null;
  tasting_notes: string | null;
  rating: number | null;
  status: "sealed" | "opened" | "finished";
  purchase_price: number | null;
  purchase_date: string | null;
  purchase_location: string | null;
  created_at: string;
  updated_at: string;
}

export interface PaginatedResponse<T> {
  items: T[];
  next_cursor: string | null;
  has_more: boolean;
}

export interface AuthResponse {
  access_token: string;
  token_type: string;
  expires_in: number;
  user: { id: string; email: string; created_at: string };
}

export interface DistillerySummary {
  id: string;
  slug: string;
  name: string;
  region: string;
  country: string;
}

export interface DistilleryDetail extends DistillerySummary {
  latitude: number | null;
  longitude: number | null;
  founded: number | null;
  owner: string | null;
  history: string | null;
  production_notes: string | null;
  website: string | null;
}

export interface ReferenceWhisky {
  id: string;
  slug: string;
  name: string;
  distillery: DistillerySummary | null;
  age_statement: number | null;
  region: string;
  country: string;
  flavor_profile: FlavorProfile;
  description: string | null;
}

export interface WishlistItem {
  id: string;
  whisky: ReferenceWhisky;
  notes: string | null;
  created_at: string;
}

export const emptyFlavorProfile: FlavorProfile = {
  smoky_peaty: 0,
  fruity: 0,
  sherried: 0,
  spicy: 0,
  floral_grassy: 0,
  maritime: 0,
  honey_sweet: 0,
  vanilla_caramel: 0,
  oak_woody: 0,
  nutty: 0,
  malty_biscuity: 0,
  medicinal_iodine: 0,
};
