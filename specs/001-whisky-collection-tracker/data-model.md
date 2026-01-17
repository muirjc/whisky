# Data Model: Whisky Collection Tracker

**Date**: 2026-01-17
**Feature**: 001-whisky-collection-tracker

## Entity Relationship Diagram

```
┌─────────────┐       ┌─────────────┐       ┌─────────────────┐
│    User     │       │   Bottle    │       │ ReferenceWhisky │
├─────────────┤       ├─────────────┤       ├─────────────────┤
│ id (PK)     │──┐    │ id (PK)     │       │ id (PK)         │
│ email       │  │    │ user_id(FK) │───────│ distillery_id   │──┐
│ password    │  └───>│ name        │       │ name            │  │
│ created_at  │       │ distillery  │       │ age_statement   │  │
│ updated_at  │       │ age_stmt    │       │ region          │  │
└─────────────┘       │ region      │       │ country         │  │
       │              │ country     │       │ flavor_profile  │  │
       │              │ size_ml     │       └─────────────────┘  │
       │              │ abv         │                            │
       │              │ flavor_prof │       ┌─────────────────┐  │
       │              │ tasting_note│       │   Distillery    │  │
       │              │ rating      │       ├─────────────────┤  │
       │              │ status      │       │ id (PK)         │<─┘
       │              │ purchase_*  │       │ name            │
       │              │ created_at  │       │ region          │
       │              │ updated_at  │       │ country         │
       │              └─────────────┘       │ location        │
       │                                    │ founded         │
       │              ┌─────────────┐       │ owner           │
       │              │ WishlistItem│       │ history         │
       │              ├─────────────┤       │ production_note │
       └─────────────>│ id (PK)     │       │ website         │
                      │ user_id(FK) │       └─────────────────┘
                      │ whisky_id   │
                      │ notes       │
                      │ created_at  │
                      └─────────────┘
```

## Entity Definitions

### User

Represents a registered collector with authentication credentials.

| Field | Type | Constraints | Description |
|-------|------|-------------|-------------|
| id | UUID | PK | Unique identifier |
| email | VARCHAR(255) | UNIQUE, NOT NULL | Login email address |
| password_hash | VARCHAR(255) | NOT NULL | bcrypt hashed password |
| created_at | TIMESTAMP | NOT NULL, DEFAULT NOW | Account creation time |
| updated_at | TIMESTAMP | NOT NULL | Last profile update |

**Indexes**:
- `idx_user_email` on `email` (for login lookup)

**Validation Rules**:
- Email must be valid format (RFC 5322)
- Password minimum 8 characters, requires letter and number

---

### Bottle

An individual whisky in the user's collection.

| Field | Type | Constraints | Description |
|-------|------|-------------|-------------|
| id | UUID | PK | Unique identifier |
| user_id | UUID | FK(User), NOT NULL | Owning user |
| name | VARCHAR(255) | NOT NULL | Bottle/expression name |
| distillery_name | VARCHAR(255) | NOT NULL | Distillery name (free text) |
| distillery_id | UUID | FK(Distillery), NULL | Link to reference distillery |
| age_statement | INT | NULL, CHECK >=0 | Age in years (NULL for NAS) |
| region | VARCHAR(100) | NOT NULL | Whisky region |
| country | VARCHAR(100) | NOT NULL | Country of origin |
| size_ml | INT | NULL, CHECK >0 | Bottle size in milliliters |
| abv | DECIMAL(4,1) | NULL, CHECK 0-100 | Alcohol by volume percentage |
| flavor_profile | JSONB | NULL | Flavor intensity ratings |
| tasting_notes | TEXT | NULL | User's personal tasting notes |
| rating | INT | NULL, CHECK 1-5 | User's rating (1-5 stars) |
| status | ENUM | NOT NULL, DEFAULT 'sealed' | sealed/opened/finished |
| purchase_price | DECIMAL(10,2) | NULL | Purchase price |
| purchase_date | DATE | NULL | Date of purchase |
| purchase_location | VARCHAR(255) | NULL | Where purchased |
| created_at | TIMESTAMP | NOT NULL, DEFAULT NOW | When added to collection |
| updated_at | TIMESTAMP | NOT NULL | Last modification |

**Indexes**:
- `idx_bottle_user_id` on `user_id` (for collection queries)
- `idx_bottle_distillery` on `distillery_name` (for filtering)
- `idx_bottle_region` on `region` (for filtering)
- `idx_bottle_status` on `status` (for filtering)
- `idx_bottle_created` on `created_at` (for sorting)

**Validation Rules**:
- Name required, max 255 characters
- Distillery name required
- Region must be from predefined list or "Other"
- Country must be from predefined list
- ABV between 0 and 100 if provided
- Rating between 1 and 5 if provided

**State Transitions**:
```
sealed → opened → finished
         ↑
         └── (can revert if corrected)
```

---

### FlavorProfile (embedded in Bottle as JSONB)

Represents flavor intensity ratings for a bottle.

```json
{
  "smoky_peaty": 0-5,
  "fruity": 0-5,
  "sherried": 0-5,
  "spicy": 0-5,
  "floral_grassy": 0-5,
  "maritime": 0-5,
  "honey_sweet": 0-5,
  "vanilla_caramel": 0-5,
  "oak_woody": 0-5,
  "nutty": 0-5,
  "malty_biscuity": 0-5,
  "medicinal_iodine": 0-5
}
```

**Validation Rules**:
- All values must be integers 0-5
- Unknown keys are ignored
- Empty object is valid (no profile defined)

---

### WishlistItem

A reference whisky the user wants to acquire.

| Field | Type | Constraints | Description |
|-------|------|-------------|-------------|
| id | UUID | PK | Unique identifier |
| user_id | UUID | FK(User), NOT NULL | Owning user |
| reference_whisky_id | UUID | FK(ReferenceWhisky), NOT NULL | Desired whisky |
| notes | TEXT | NULL | User's notes about this item |
| created_at | TIMESTAMP | NOT NULL, DEFAULT NOW | When added to wishlist |

**Indexes**:
- `idx_wishlist_user` on `user_id` (for user's wishlist)
- `idx_wishlist_unique` on `(user_id, reference_whisky_id)` UNIQUE (prevent duplicates)

**Validation Rules**:
- Cannot add same whisky twice to wishlist

---

### ReferenceWhisky (Read-only reference data)

Pre-seeded whisky from the reference database.

| Field | Type | Constraints | Description |
|-------|------|-------------|-------------|
| id | UUID | PK | Unique identifier |
| slug | VARCHAR(100) | UNIQUE, NOT NULL | URL-friendly identifier |
| name | VARCHAR(255) | NOT NULL | Full whisky name |
| distillery_id | UUID | FK(Distillery), NOT NULL | Producing distillery |
| age_statement | INT | NULL | Age in years |
| region | VARCHAR(100) | NOT NULL | Whisky region |
| country | VARCHAR(100) | NOT NULL | Country of origin |
| flavor_profile | JSONB | NOT NULL | Flavor intensity ratings |
| description | TEXT | NULL | Brief description |

**Indexes**:
- `idx_ref_whisky_distillery` on `distillery_id`
- `idx_ref_whisky_region` on `region`
- `idx_ref_whisky_name` on `name` (for search)
- GIN index on `flavor_profile` (for similarity queries)

---

### Distillery (Read-only reference data)

Pre-seeded distillery information.

| Field | Type | Constraints | Description |
|-------|------|-------------|-------------|
| id | UUID | PK | Unique identifier |
| slug | VARCHAR(100) | UNIQUE, NOT NULL | URL-friendly identifier |
| name | VARCHAR(255) | NOT NULL | Distillery name |
| region | VARCHAR(100) | NOT NULL | Region (Speyside, Islay, etc.) |
| country | VARCHAR(100) | NOT NULL | Country |
| latitude | DECIMAL(9,6) | NULL | GPS latitude |
| longitude | DECIMAL(9,6) | NULL | GPS longitude |
| founded | INT | NULL | Year founded |
| owner | VARCHAR(255) | NULL | Current owner/parent company |
| history | TEXT | NULL | Historical description |
| production_notes | TEXT | NULL | Production method notes |
| website | VARCHAR(500) | NULL | Official website URL |

**Indexes**:
- `idx_distillery_region` on `region`
- `idx_distillery_country` on `country`
- `idx_distillery_name` on `name` (for search)

## Enumeration Values

### BottleStatus
- `sealed` - Bottle unopened
- `opened` - Bottle opened, in use
- `finished` - Bottle empty/finished

### WhiskyRegion (predefined list)
**Scotland**: Speyside, Highland, Lowland, Islay, Campbeltown, Islands
**Ireland**: Single Pot Still, Single Malt, Blended
**USA**: Kentucky, Tennessee, Other US
**Japan**: Japanese
**Other**: Canadian, Indian, Taiwanese, Australian, Other

## Data Isolation

All user-owned entities (Bottle, WishlistItem) include `user_id` foreign key:
- All queries MUST filter by authenticated `user_id`
- Database-level row security policies enforce isolation
- API layer validates ownership before any operation

## Seed Data Requirements

### Initial Reference Data
- ~500 distilleries with complete profiles
- ~5000 reference whiskies with flavor profiles
- Focus on Scotch, Irish, American, Japanese distilleries
- Data stored in `/data/distilleries.json` and `/data/whiskies.json`
- Seeded on initial deployment via migration script

### Flavor Profile Coverage
- All reference whiskies must have complete flavor profiles
- Profiles curated from expert tasting notes and official descriptions
- Enables meaningful similarity matching from day one
