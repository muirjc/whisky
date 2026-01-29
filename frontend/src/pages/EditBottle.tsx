import React, { useEffect, useState } from "react";
import { useParams, useNavigate } from "react-router-dom";
import BottleForm, { BottleFormData } from "../components/BottleForm";
import { api, Bottle } from "../services/api";

export default function EditBottle() {
  const { id } = useParams<{ id: string }>();
  const navigate = useNavigate();
  const [bottle, setBottle] = useState<Bottle | null>(null);
  const [loading, setLoading] = useState(true);

  useEffect(() => {
    if (!id) return;
    api.get<Bottle>(`/bottles/${id}`)
      .then(setBottle)
      .catch(() => navigate("/collection"))
      .finally(() => setLoading(false));
  }, [id, navigate]);

  const handleSubmit = async (data: BottleFormData) => {
    const payload = {
      ...data,
      tasting_notes: data.tasting_notes || null,
      purchase_date: data.purchase_date || null,
      purchase_location: data.purchase_location || null,
    };
    await api.put(`/bottles/${id}`, payload);
    navigate(`/bottles/${id}`);
  };

  if (loading) return <p>Loading...</p>;
  if (!bottle) return <p>Bottle not found</p>;

  return (
    <div>
      <h1>Edit: {bottle.name}</h1>
      <BottleForm
        initialData={{
          ...bottle,
          tasting_notes: bottle.tasting_notes || "",
          purchase_date: bottle.purchase_date || "",
          purchase_location: bottle.purchase_location || "",
        }}
        onSubmit={handleSubmit}
        submitLabel="Save Changes"
      />
    </div>
  );
}
