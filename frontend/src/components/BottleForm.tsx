import React, { useState } from "react";
import FlavorProfileInput from "./FlavorProfileInput";
import { emptyFlavorProfile, FlavorProfile } from "../services/api";

export interface BottleFormData {
  name: string;
  distillery_name: string;
  age_statement: number | null;
  region: string;
  country: string;
  size_ml: number | null;
  abv: number | null;
  flavor_profile: FlavorProfile | null;
  tasting_notes: string;
  rating: number | null;
  status: "sealed" | "opened" | "finished";
  purchase_price: number | null;
  purchase_date: string;
  purchase_location: string;
}

interface BottleFormProps {
  initialData?: Partial<BottleFormData>;
  onSubmit: (data: BottleFormData) => Promise<void>;
  submitLabel: string;
}

const REGIONS = ["Speyside", "Highland", "Lowland", "Islay", "Campbeltown", "Islands",
  "Single Pot Still", "Single Malt", "Blended", "Kentucky", "Tennessee", "Other US",
  "Japanese", "Canadian", "Indian", "Taiwanese", "Australian", "Other"];

const COUNTRIES = ["Scotland", "Ireland", "USA", "Japan", "Canada", "India", "Taiwan", "Australia", "Other"];

export default function BottleForm({ initialData, onSubmit, submitLabel }: BottleFormProps) {
  const [data, setData] = useState<BottleFormData>({
    name: initialData?.name || "",
    distillery_name: initialData?.distillery_name || "",
    age_statement: initialData?.age_statement ?? null,
    region: initialData?.region || "",
    country: initialData?.country || "",
    size_ml: initialData?.size_ml ?? null,
    abv: initialData?.abv ?? null,
    flavor_profile: initialData?.flavor_profile ?? null,
    tasting_notes: initialData?.tasting_notes || "",
    rating: initialData?.rating ?? null,
    status: initialData?.status || "sealed",
    purchase_price: initialData?.purchase_price ?? null,
    purchase_date: initialData?.purchase_date || "",
    purchase_location: initialData?.purchase_location || "",
  });
  const [showProfile, setShowProfile] = useState(!!initialData?.flavor_profile);
  const [error, setError] = useState<string | null>(null);
  const [submitting, setSubmitting] = useState(false);

  const handleSubmit = async (e: React.FormEvent) => {
    e.preventDefault();
    setError(null);
    setSubmitting(true);
    try {
      await onSubmit(data);
    } catch (err) {
      setError(err instanceof Error ? err.message : "Failed to save");
    } finally {
      setSubmitting(false);
    }
  };

  const set = (field: keyof BottleFormData, value: unknown) =>
    setData((prev) => ({ ...prev, [field]: value }));

  return (
    <form onSubmit={handleSubmit}>
      <div className="grid grid-2">
        <div className="form-group">
          <label>Name *</label>
          <input value={data.name} onChange={(e) => set("name", e.target.value)} required />
        </div>
        <div className="form-group">
          <label>Distillery *</label>
          <input value={data.distillery_name} onChange={(e) => set("distillery_name", e.target.value)} required />
        </div>
        <div className="form-group">
          <label>Country *</label>
          <select value={data.country} onChange={(e) => set("country", e.target.value)} required>
            <option value="">Select...</option>
            {COUNTRIES.map(c => <option key={c} value={c}>{c}</option>)}
          </select>
        </div>
        <div className="form-group">
          <label>Region *</label>
          <select value={data.region} onChange={(e) => set("region", e.target.value)} required>
            <option value="">Select...</option>
            {REGIONS.map(r => <option key={r} value={r}>{r}</option>)}
          </select>
        </div>
        <div className="form-group">
          <label>Age Statement</label>
          <input type="number" min={0} value={data.age_statement ?? ""} onChange={(e) => set("age_statement", e.target.value ? parseInt(e.target.value) : null)} placeholder="NAS" />
        </div>
        <div className="form-group">
          <label>ABV (%)</label>
          <input type="number" min={0} max={100} step={0.1} value={data.abv ?? ""} onChange={(e) => set("abv", e.target.value ? parseFloat(e.target.value) : null)} />
        </div>
        <div className="form-group">
          <label>Size (ml)</label>
          <input type="number" min={1} value={data.size_ml ?? ""} onChange={(e) => set("size_ml", e.target.value ? parseInt(e.target.value) : null)} />
        </div>
        <div className="form-group">
          <label>Rating</label>
          <select value={data.rating ?? ""} onChange={(e) => set("rating", e.target.value ? parseInt(e.target.value) : null)}>
            <option value="">No rating</option>
            {[1,2,3,4,5].map(n => <option key={n} value={n}>{"★".repeat(n)}</option>)}
          </select>
        </div>
        <div className="form-group">
          <label>Status</label>
          <select value={data.status} onChange={(e) => set("status", e.target.value)}>
            <option value="sealed">Sealed</option>
            <option value="opened">Opened</option>
            <option value="finished">Finished</option>
          </select>
        </div>
        <div className="form-group">
          <label>Purchase Price</label>
          <input type="number" min={0} step={0.01} value={data.purchase_price ?? ""} onChange={(e) => set("purchase_price", e.target.value ? parseFloat(e.target.value) : null)} />
        </div>
        <div className="form-group">
          <label>Purchase Date</label>
          <input type="date" value={data.purchase_date} onChange={(e) => set("purchase_date", e.target.value)} />
        </div>
        <div className="form-group">
          <label>Purchase Location</label>
          <input value={data.purchase_location} onChange={(e) => set("purchase_location", e.target.value)} />
        </div>
      </div>
      <div className="form-group">
        <label>Tasting Notes</label>
        <textarea rows={3} value={data.tasting_notes} onChange={(e) => set("tasting_notes", e.target.value)} />
      </div>
      <div className="form-group">
        <button type="button" className="btn btn-secondary" onClick={() => {
          setShowProfile(!showProfile);
          if (!showProfile && !data.flavor_profile) set("flavor_profile", { ...emptyFlavorProfile });
        }}>
          {showProfile ? "Hide" : "Add"} Flavor Profile
        </button>
      </div>
      {showProfile && data.flavor_profile && (
        <div className="card" style={{ marginBottom: "1rem" }}>
          <FlavorProfileInput value={data.flavor_profile} onChange={(fp) => set("flavor_profile", fp)} />
        </div>
      )}
      {error && <p className="error-message">{error}</p>}
      <button type="submit" className="btn btn-primary" disabled={submitting}>
        {submitting ? "Saving..." : submitLabel}
      </button>
    </form>
  );
}
