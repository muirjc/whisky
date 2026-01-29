import { useEffect, useState } from "react";
import { useParams } from "react-router-dom";
import { api, DistilleryDetail as DistilleryType, ReferenceWhisky, PaginatedResponse } from "../services/api";

export default function DistilleryDetail() {
  const { slug } = useParams<{ slug: string }>();
  const [distillery, setDistillery] = useState<DistilleryType | null>(null);
  const [whiskies, setWhiskies] = useState<ReferenceWhisky[]>([]);
  const [loading, setLoading] = useState(true);

  useEffect(() => {
    if (!slug) return;
    Promise.all([
      api.get<DistilleryType>(`/distilleries/${slug}`),
      api.get<PaginatedResponse<ReferenceWhisky>>(`/distilleries/${slug}/whiskies?limit=100`),
    ])
      .then(([d, w]) => {
        setDistillery(d);
        setWhiskies(w.items);
      })
      .catch(console.error)
      .finally(() => setLoading(false));
  }, [slug]);

  if (loading) return <p>Loading...</p>;
  if (!distillery) return <p>Distillery not found</p>;

  return (
    <div>
      <h1>{distillery.name}</h1>
      <p style={{ color: "var(--color-text-muted)" }}>{distillery.region}, {distillery.country}</p>

      <div className="grid grid-2" style={{ marginTop: "1rem" }}>
        <div className="card">
          <h3>Information</h3>
          {distillery.founded && <p><strong>Founded:</strong> {distillery.founded}</p>}
          {distillery.owner && <p><strong>Owner:</strong> {distillery.owner}</p>}
          {distillery.website && <p><strong>Website:</strong> <a href={distillery.website} target="_blank" rel="noopener noreferrer">{distillery.website}</a></p>}
          {distillery.history && <><h4 style={{ marginTop: "1rem" }}>History</h4><p>{distillery.history}</p></>}
          {distillery.production_notes && <><h4 style={{ marginTop: "1rem" }}>Production</h4><p>{distillery.production_notes}</p></>}
        </div>
        <div>
          <h3>Notable Expressions ({whiskies.length})</h3>
          <div className="grid" style={{ marginTop: "0.5rem" }}>
            {whiskies.map((w) => (
              <div key={w.id} className="card">
                <strong>{w.name}</strong>
                {w.age_statement && <span> ({w.age_statement} yr)</span>}
                {w.description && <p style={{ fontSize: "0.875rem", color: "var(--color-text-muted)" }}>{w.description}</p>}
              </div>
            ))}
          </div>
        </div>
      </div>
    </div>
  );
}
