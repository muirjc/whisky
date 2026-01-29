import React from "react";
import { useNavigate } from "react-router-dom";
import BottleForm, { BottleFormData } from "../components/BottleForm";
import { api, Bottle } from "../services/api";

export default function AddBottle() {
  const navigate = useNavigate();

  const handleSubmit = async (data: BottleFormData) => {
    const payload = {
      ...data,
      tasting_notes: data.tasting_notes || null,
      purchase_date: data.purchase_date || null,
      purchase_location: data.purchase_location || null,
    };
    const bottle = await api.post<Bottle>("/bottles", payload);
    navigate(`/bottles/${bottle.id}`);
  };

  return (
    <div>
      <h1>Add Bottle</h1>
      <BottleForm onSubmit={handleSubmit} submitLabel="Add to Collection" />
    </div>
  );
}
