import React, { useEffect, useState } from "react";
import { Link } from "react-router-dom";
import { api, Bottle, PaginatedResponse } from "../services/api";

export default function Collection() {
  const [bottles, setBottles] = useState<Bottle[]>([]);
  const [search, setSearch] = useState("");
  const [region, setRegion] = useState("");
  const [statusFilter, setStatusFilter] = useState("");
  const [sort, setSort] = useState("created_at");
  const [order, setOrder] = useState("desc");
  const [loading, setLoading] = useState(true);
  const [viewMode, setViewMode] = useState<"grid" | "list">("grid");

  useEffect(() => {
    void fetchBottles();
  }, [search, region, statusFilter, sort, order]);

  const fetchBottles = async () => {
    setLoading(true);
    try {
      const params = new URLSearchParams();
      if (search) params.set("search", search);
      if (region) params.set("region", region);
      if (statusFilter) params.set("status", statusFilter);
      params.set("sort", sort);
      params.set("order", order);
      params.set("limit", "100");
      const data = await api.get<PaginatedResponse<Bottle>>(`/bottles?${params.toString()}`);
      setBottles(data.items);
    } catch (e) {
      console.error("Failed to fetch bottles", e);
    } finally {
      setLoading(false);
    }
  };

  const handleDelete = async (id: string) => {
    if (!confirm("Delete this bottle?")) return;
    try {
      await api.delete(`/bottles/${id}`);
      setBottles((prev) => prev.filter((b) => b.id !== id));
    } catch (e) {
      console.error("Delete failed", e);
    }
  };

  return (
    <div>
      <div style={{ display: "flex", justifyContent: "space-between", alignItems: "center", marginBottom: "1rem" }}>
        <h1>My Collection ({bottles.length})</h1>
        <Link to="/bottles/add" className="btn btn-primary">Add Bottle</Link>
      </div>

      <div style={{ display: "flex", gap: "0.5rem", flexWrap: "wrap", marginBottom: "1rem" }}>
        <input placeholder="Search..." value={search} onChange={(e) => setSearch(e.target.value)} style={{ flex: 1, minWidth: 200 }} />
        <select value={region} onChange={(e) => setRegion(e.target.value)}>
          <option value="">All Regions</option>
          {["Speyside","Highland","Lowland","Islay","Campbeltown","Islands","Kentucky","Tennessee"].map(r => (
            <option key={r} value={r}>{r}</option>
          ))}
        </select>
        <select value={statusFilter} onChange={(e) => setStatusFilter(e.target.value)}>
          <option value="">All Status</option>
          <option value="sealed">Sealed</option>
          <option value="opened">Opened</option>
          <option value="finished">Finished</option>
        </select>
        <select value={`${sort}-${order}`} onChange={(e) => { const [s, o] = e.target.value.split("-"); setSort(s); setOrder(o); }}>
          <option value="created_at-desc">Newest First</option>
          <option value="created_at-asc">Oldest First</option>
          <option value="name-asc">Name A-Z</option>
          <option value="name-desc">Name Z-A</option>
          <option value="rating-desc">Highest Rated</option>
        </select>
        <button className="btn btn-secondary" onClick={() => setViewMode(viewMode === "grid" ? "list" : "grid")}>
          {viewMode === "grid" ? "List" : "Grid"}
        </button>
      </div>

      {loading ? (
        <p>Loading...</p>
      ) : bottles.length === 0 ? (
        <div className="card" style={{ textAlign: "center", padding: "3rem" }}>
          <p>No bottles in your collection yet.</p>
          <Link to="/bottles/add" className="btn btn-primary" style={{ marginTop: "1rem" }}>Add Your First Bottle</Link>
        </div>
      ) : (
        <div className={viewMode === "grid" ? "grid grid-3" : ""}>
          {bottles.map((bottle) => (
            <div key={bottle.id} className="card" style={viewMode === "list" ? { marginBottom: "0.5rem" } : undefined}>
              <Link to={`/bottles/${bottle.id}`} style={{ fontWeight: 600 }}>{bottle.name}</Link>
              <p style={{ color: "var(--color-text-muted)", fontSize: "0.875rem" }}>
                {bottle.distillery_name} &bull; {bottle.region} &bull; {bottle.status}
                {bottle.rating && ` &bull; ${"★".repeat(bottle.rating)}`}
              </p>
              <div style={{ marginTop: "0.5rem", display: "flex", gap: "0.5rem" }}>
                <Link to={`/bottles/${bottle.id}/edit`} className="btn btn-secondary" style={{ fontSize: "0.75rem", padding: "0.25rem 0.5rem" }}>Edit</Link>
                <button onClick={() => handleDelete(bottle.id)} className="btn btn-danger" style={{ fontSize: "0.75rem", padding: "0.25rem 0.5rem" }}>Delete</button>
              </div>
            </div>
          ))}
        </div>
      )}
    </div>
  );
}
