import React from "react";
import type { FlavorProfile } from "../services/api";

const FLAVOR_LABELS: Record<keyof FlavorProfile, string> = {
  smoky_peaty: "Smoky / Peaty",
  fruity: "Fruity",
  sherried: "Sherried",
  spicy: "Spicy",
  floral_grassy: "Floral / Grassy",
  maritime: "Maritime",
  honey_sweet: "Honey / Sweet",
  vanilla_caramel: "Vanilla / Caramel",
  oak_woody: "Oak / Woody",
  nutty: "Nutty",
  malty_biscuity: "Malty / Biscuity",
  medicinal_iodine: "Medicinal / Iodine",
};

interface FlavorProfileInputProps {
  value: FlavorProfile;
  onChange?: (profile: FlavorProfile) => void;
  readonly?: boolean;
}

export default function FlavorProfileInput({
  value,
  onChange,
  readonly = false,
}: FlavorProfileInputProps) {
  const handleChange = (key: keyof FlavorProfile, val: number) => {
    if (onChange) {
      onChange({ ...value, [key]: val });
    }
  };

  return (
    <div style={{ display: "grid", gap: "0.5rem" }}>
      {(Object.keys(FLAVOR_LABELS) as (keyof FlavorProfile)[]).map((key) => (
        <div key={key} style={{ display: "flex", alignItems: "center", gap: "0.75rem" }}>
          <label
            style={{
              width: "140px",
              fontSize: "0.875rem",
              color: "var(--color-text-muted)",
              flexShrink: 0,
            }}
          >
            {FLAVOR_LABELS[key]}
          </label>
          <input
            type="range"
            min={0}
            max={5}
            step={1}
            value={value[key]}
            onChange={(e) => handleChange(key, parseInt(e.target.value, 10))}
            disabled={readonly}
            style={{ flex: 1 }}
          />
          <span style={{ width: "20px", textAlign: "center", fontWeight: 600 }}>
            {value[key]}
          </span>
        </div>
      ))}
    </div>
  );
}
