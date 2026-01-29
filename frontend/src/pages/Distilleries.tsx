import React, { useEffect, useState } from "react";
import { Link } from "react-router-dom";
import { api, DistillerySummary, PaginatedResponse } from "../services/api";

export default function Distilleries() {
  const [distilleries, setDistilleries] = useState<DistillerySummary[]>([]);
  const [search, setSearch] = useState("");
  const [loading, setLoading] = useState(true);

  useEffect(() => {
    const params = new URLSearchParams();
    if (search) params.set("search", search);
    params.set("limit", "100");
    api.get<PaginatedResponse<DistillerySummary>>(`/distilleries?${params.toString()}`)
      .then((data) => setDistilleries(data.items))
      .catch(console.error)
      .finally(() => setLoading(false));
  }, [search]);

  return (
    <div>
      <h1>Distilleries</h1>
      <div style={{ marginBottom: "1rem" }}>
        <input placeholder="Search distilleries..." value={search} onChange={(e) => setSearch(e.target.value)} style={{ width: "100%", maxWidth: 400 }} />
      </div>
      {loading ? (
        <p>Loading...</p>
      ) : (
        <div className="grid grid-3">
          {distilleries.map((d) => (
            <Link to={`/distilleries/${d.slug}`} key={d.id} className="card" style={{ textDecoration: "none", color: "inherit" }}>
              <strong>{d.name}</strong>
              <p style={{ color: "var(--color-text-muted)", fontSize: "0.875rem" }}>{d.region}, {d.country}</p>
            </Link>
          ))}
        </div>
      )}
    </div>
  );
}
