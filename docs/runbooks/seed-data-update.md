# Runbook: Seed Data Update

## Overview

Reference data (distilleries and whiskies) is stored in `data/distilleries.json` and `data/whiskies.json`. The seed script loads this data into PostgreSQL.

## Running the Seed Script

```bash
cd backend
python -m src.seed.run_seed
```

This is idempotent — it upserts based on slug, so re-running is safe.

## Adding New Distilleries

1. Edit `data/distilleries.json`
2. Add a new entry with required fields: `slug`, `name`, `region`, `country`, `description`
3. Optional fields: `year_founded`, `website`, `notable_expressions`
4. Run the seed script

## Adding New Whiskies

1. Edit `data/whiskies.json`
2. Add a new entry with required fields: `slug`, `name`, `distillery_slug`, `region`, `country`
3. Include `flavor_profile` with integer values (0-5) for each descriptor
4. Ensure `distillery_slug` matches an existing distillery entry
5. Run the seed script

## Validation

After seeding, verify counts:

```sql
SELECT COUNT(*) FROM distilleries;  -- Expected: 51+
SELECT COUNT(*) FROM reference_whiskies;  -- Expected: 203+
```
