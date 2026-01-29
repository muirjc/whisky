import React, { useEffect, useState } from "react";
import { api, PaginatedResponse, WishlistItem } from "../services/api";

export default function Wishlist() {
  const [items, setItems] = useState<WishlistItem[]>([]);
  const [loading, setLoading] = useState(true);

  useEffect(() => {
    api.get<PaginatedResponse<WishlistItem>>("/wishlist?limit=100")
      .then((data) => setItems(data.items))
      .catch(console.error)
      .finally(() => setLoading(false));
  }, []);

  const handleRemove = async (id: string) => {
    await api.delete(`/wishlist/${id}`);
    setItems((prev) => prev.filter((i) => i.id !== id));
  };

  if (loading) return <p>Loading...</p>;

  return (
    <div>
      <h1>Wishlist ({items.length})</h1>
      {items.length === 0 ? (
        <div className="card" style={{ textAlign: "center", padding: "3rem" }}>
          <p>Your wishlist is empty. Browse similar whiskies from your bottle details to add items.</p>
        </div>
      ) : (
        <div className="grid grid-3">
          {items.map((item) => (
            <div key={item.id} className="card">
              <strong>{item.whisky.name}</strong>
              <p style={{ color: "var(--color-text-muted)", fontSize: "0.875rem" }}>
                {item.whisky.distillery?.name} &bull; {item.whisky.region}
              </p>
              {item.notes && <p style={{ fontSize: "0.875rem", marginTop: "0.5rem" }}>{item.notes}</p>}
              <button onClick={() => handleRemove(item.id)} className="btn btn-danger" style={{ marginTop: "0.5rem", fontSize: "0.75rem" }}>Remove</button>
            </div>
          ))}
        </div>
      )}
    </div>
  );
}
