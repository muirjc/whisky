import React, { useEffect, useState } from "react";
import { Link, useParams, useNavigate } from "react-router-dom";
import FlavorProfileInput from "../components/FlavorProfileInput";
import { api, Bottle, ReferenceWhisky } from "../services/api";

interface SimilarItem {
  whisky: ReferenceWhisky;
  similarity_score: number;
}

export default function BottleDetail() {
  const { id } = useParams<{ id: string }>();
  const navigate = useNavigate();
  const [bottle, setBottle] = useState<Bottle | null>(null);
  const [similar, setSimilar] = useState<SimilarItem[]>([]);
  const [loading, setLoading] = useState(true);

  useEffect(() => {
    if (!id) return;
    const load = async () => {
      try {
        const b = await api.get<Bottle>(`/bottles/${id}`);
        setBottle(b);
        if (b.flavor_profile && Object.values(b.flavor_profile).some(v => v > 0)) {
          const sim = await api.get<{ items: SimilarItem[] }>(`/bottles/${id}/similar?limit=5`);
          setSimilar(sim.items);
        }
      } catch {
        navigate("/collection");
      } finally {
        setLoading(false);
      }
    };
    void load();
  }, [id, navigate]);

  const handleDelete = async () => {
    if (!confirm("Delete this bottle?")) return;
    await api.delete(`/bottles/${id}`);
    navigate("/collection");
  };

  if (loading) return <p>Loading...</p>;
  if (!bottle) return <p>Bottle not found</p>;

  return (
    <div>
      <div style={{ display: "flex", justifyContent: "space-between", alignItems: "center" }}>
        <h1>{bottle.name}</h1>
        <div style={{ display: "flex", gap: "0.5rem" }}>
          <Link to={`/bottles/${id}/edit`} className="btn btn-secondary">Edit</Link>
          <button onClick={handleDelete} className="btn btn-danger">Delete</button>
        </div>
      </div>

      <div className="grid grid-2" style={{ marginTop: "1rem" }}>
        <div className="card">
          <h3>Details</h3>
          <p><strong>Distillery:</strong> {bottle.distillery_name}
            {bottle.distillery && (
              <> (<Link to={`/distilleries/${bottle.distillery.slug}`}>{bottle.distillery.name}</Link>)</>
            )}
          </p>
          <p><strong>Region:</strong> {bottle.region}, {bottle.country}</p>
          <p><strong>Age:</strong> {bottle.age_statement ? `${bottle.age_statement} years` : "NAS"}</p>
          {bottle.abv && <p><strong>ABV:</strong> {bottle.abv}%</p>}
          {bottle.size_ml && <p><strong>Size:</strong> {bottle.size_ml}ml</p>}
          <p><strong>Status:</strong> {bottle.status}</p>
          {bottle.rating && <p><strong>Rating:</strong> {"★".repeat(bottle.rating)}{"☆".repeat(5 - bottle.rating)}</p>}
          {bottle.purchase_price && <p><strong>Price:</strong> ${bottle.purchase_price}</p>}
          {bottle.purchase_date && <p><strong>Purchased:</strong> {bottle.purchase_date}</p>}
          {bottle.purchase_location && <p><strong>Location:</strong> {bottle.purchase_location}</p>}
        </div>

        {bottle.tasting_notes && (
          <div className="card">
            <h3>Tasting Notes</h3>
            <p>{bottle.tasting_notes}</p>
          </div>
        )}
      </div>

      {bottle.flavor_profile && (
        <div className="card" style={{ marginTop: "1rem" }}>
          <h3>Flavor Profile</h3>
          <FlavorProfileInput value={bottle.flavor_profile} readonly />
        </div>
      )}

      {similar.length > 0 && (
        <div style={{ marginTop: "1.5rem" }}>
          <h3>Similar Whiskies</h3>
          <div className="grid grid-3" style={{ marginTop: "0.5rem" }}>
            {similar.map((item) => (
              <div key={item.whisky.id} className="card">
                <strong>{item.whisky.name}</strong>
                <p style={{ color: "var(--color-text-muted)", fontSize: "0.875rem" }}>
                  {item.whisky.distillery?.name} &bull; {item.whisky.region}
                </p>
                <p style={{ fontSize: "0.875rem" }}>
                  Match: {Math.round(item.similarity_score * 100)}%
                </p>
              </div>
            ))}
          </div>
        </div>
      )}
    </div>
  );
}
