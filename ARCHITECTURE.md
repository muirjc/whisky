# Whisky Collection Tracker — Architecture Guide

## Overview

A full-stack web application for managing a personal whisky collection, discovering new whiskies through flavor profile matching, and browsing a curated database of distilleries and expressions.

**Stack**: FastAPI (Python) + React (TypeScript) + PostgreSQL

---

## Backend (`backend/`)

### API Routes (`src/api/`)

| Module | Prefix | Description |
|--------|--------|-------------|
| `health.py` | `/health`, `/ready` | Liveness probe and database connectivity check. |
| `auth.py` | `/auth` | User registration, login, logout, token refresh, password change, and password reset request. Rate-limited by client IP. |
| `bottles.py` | `/bottles` | CRUD for the user's personal bottle collection. Supports search, region/status filtering, sorting, cursor-based pagination, and a `/similar` sub-endpoint that finds reference whiskies with matching flavor profiles. |
| `distilleries.py` | `/distilleries` | Read-only browsing of reference distilleries with search, region/country filtering, and listing each distillery's expressions. |
| `whiskies.py` | `/whiskies` | Read-only search and filtering of the reference whisky catalogue by name, region, or dominant flavor. |
| `wishlist.py` | `/wishlist` | Add, list, and remove reference whiskies from a personal wishlist. Prevents duplicates with a unique constraint. |
| `profile.py` | `/profile/taste` | Analyzes the user's collection to produce an averaged flavor profile, dominant flavors, region distribution, and personalized recommendations. |
| `deps.py` | — | FastAPI dependencies for JWT authentication. Extracts and validates the bearer token, fetches the user from the database. |
| `pagination.py` | — | Cursor-based pagination utilities. Encodes/decodes offset cursors as base64 JSON and provides a generic `PaginatedResponse` model. |

### Services (`src/services/`)

| Module | Description |
|--------|-------------|
| `auth.py` | Password hashing (bcrypt via passlib), password strength validation (min 8 chars, letter + digit), user creation, and credential verification. |
| `jwt.py` | Creates and decodes JWT access and refresh tokens with configurable expiration. Validates token type to prevent misuse. |
| `bottle.py` | Bottle CRUD with user-scoped queries. `list_bottles` supports text search across name/distillery, region and status filters, multi-field sorting, and offset-based cursor pagination. |
| `distillery.py` | Distillery lookups by slug and paginated listing with search and region/country filters. |
| `reference_whisky.py` | Reference whisky lookups by slug and paginated listing with search, region, distillery, and dominant flavor filters. |
| `matching.py` | Flavor similarity engine. Uses weighted Euclidean distance across 12 flavor dimensions — distinctive flavors like `smoky_peaty` and `medicinal_iodine` carry higher weight. Scores are normalized to a 0–1 scale. |
| `wishlist.py` | Wishlist add/remove/list with duplicate checking and user-scoped queries. |
| `profile.py` | Aggregates flavor profiles across a user's collection, computes averages, identifies dominant flavors, counts region distribution, and generates recommendations using the matching engine. |

### Models (`src/models/`)

| Model | Table | Description |
|-------|-------|-------------|
| `User` | `users` | Registered user with email (unique), bcrypt password hash, and timestamps. |
| `Bottle` | `bottles` | A whisky in the user's collection. Stores name, distillery info, age, ABV, size, JSONB flavor profile, rating (1–5), status (sealed/opened/finished), purchase details, and tasting notes. Scoped to a user via `user_id` FK. |
| `Distillery` | `distilleries` | Reference distillery with slug, name, region, country, coordinates, founding year, owner, history, and production notes. |
| `ReferenceWhisky` | `reference_whiskies` | Pre-seeded whisky expression with slug, name, age statement, JSONB flavor profile, and description. Linked to a distillery via `distillery_id` FK. |
| `WishlistItem` | `wishlist_items` | Join between a user and a reference whisky with optional notes. Unique constraint on `(user_id, reference_whisky_id)`. |

### Schemas (`src/schemas/`)

Pydantic models for request validation and response serialization.

| Module | Description |
|--------|-------------|
| `auth.py` | Register/login/password-change request bodies and `AuthResponse` (token + user). |
| `bottle.py` | `BottleCreate`, `BottleUpdate` (partial), and `BottleResponse` with all fields. |
| `flavor_profile.py` | 12 flavor intensity fields (0–5 scale) with a `to_vector()` method for similarity calculations. |
| `distillery.py` | `DistilleryListItem` (summary) and `DistilleryDetail` (full info). |
| `reference_whisky.py` | `ReferenceWhiskyResponse` and `SimilarWhiskyResponse` (whisky + similarity score). |
| `wishlist.py` | `WishlistItemCreate` and `WishlistItemResponse`. |
| `enums.py` | `BottleStatus` enum: `sealed`, `opened`, `finished`. |
| `constants.py` | Region/country reference data and bottle size constants. |

### Middleware (`src/middleware/`)

| Module | Description |
|--------|-------------|
| `logging.py` | Wraps every request with structured JSON logging — method, path, status code, duration, and correlation ID. |
| `error_handler.py` | Global exception handlers mapping `IntegrityError` → 409, `ValueError` → 400, and unhandled exceptions → 500. |
| `rate_limit.py` | In-memory token-bucket rate limiter keyed by client IP. Applied to auth endpoints (10 requests per 60 seconds by default). |

### Configuration & Infrastructure

| File | Description |
|------|-------------|
| `src/config.py` | Pydantic Settings loading from environment or `.env` file. Database URLs, JWT secrets, CORS origins, rate limits. |
| `src/logging.py` | Structured JSON logging via structlog with correlation ID context variables. |
| `src/db/engine.py` | Async SQLAlchemy engine and session factory using asyncpg. |
| `src/main.py` | FastAPI app initialization — lifespan events, CORS, middleware registration, router mounting under `/api/v1`. |

---

## Frontend (`frontend/`)

### Pages (`src/pages/`)

| Page | Route | Description |
|------|-------|-------------|
| `Login.tsx` | `/login` | Email/password login form. Redirects to collection on success. |
| `Register.tsx` | `/register` | Registration form with password confirmation. |
| `Collection.tsx` | `/collection` | Main dashboard showing the user's bottles in a grid/list view. Supports search, region/status filters, and sort controls. |
| `AddBottle.tsx` | `/bottles/add` | Form to add a new bottle to the collection. |
| `EditBottle.tsx` | `/bottles/:id/edit` | Pre-filled form to update an existing bottle. |
| `BottleDetail.tsx` | `/bottles/:id` | Full bottle details with flavor profile visualization, tasting notes, and a list of similar reference whiskies. |
| `Wishlist.tsx` | `/wishlist` | Grid of wishlisted reference whiskies with notes and remove buttons. |
| `Distilleries.tsx` | `/distilleries` | Searchable grid of all distilleries. |
| `DistilleryDetail.tsx` | `/distilleries/:slug` | Distillery info (history, owner, founded) and its notable expressions. |

### Components (`src/components/`)

| Component | Description |
|-----------|-------------|
| `Layout.tsx` | App shell with navigation header. Shows different links for authenticated vs. public users. |
| `BottleForm.tsx` | Reusable form for bottle create/edit with all fields including an embedded flavor profile editor. |
| `FlavorProfileInput.tsx` | 12 range sliders (0–5) for editing or viewing a flavor profile. Supports a read-only display mode. |
| `ProtectedRoute.tsx` | Route guard that redirects unauthenticated users to `/login`. |
| `ErrorBoundary.tsx` | Catches rendering errors and displays a recovery UI. |
| `LoadingSpinner.tsx` | CSS-animated loading indicator. |

### Services & Hooks

| File | Description |
|------|-------------|
| `src/services/api.ts` | Centralized HTTP client wrapping `fetch`. Attaches JWT bearer tokens, handles 401 redirects, and provides typed `get`/`post`/`put`/`delete` methods. Base URL configurable via `VITE_API_URL`. |
| `src/hooks/useAuth.ts` | Auth context and hook providing `login`, `register`, `logout`, `user`, and `isLoggedIn`. Persists auth state in localStorage. |

---

## Data Layer

### Reference Data (`data/`)

| File | Records | Description |
|------|---------|-------------|
| `distilleries.json` | ~51 | Curated distillery data — Scottish (Islay, Speyside, Highland, Islands, Lowland, Campbeltown), plus Japanese, American, Irish, Indian, and Taiwanese distilleries. |
| `whiskies.json` | ~203 | Reference whisky expressions with full 12-dimension flavor profiles, age statements, and descriptions. |

### Database Migrations (`alembic/`)

Four sequential migrations building the schema:

1. `000001` — `distilleries` and `reference_whiskies` tables
2. `000002` — `users` table
3. `000003` — `bottles` table with check constraints
4. `000004` — `wishlist_items` table with unique constraint

---

## Key Design Decisions

**Flavor matching** uses weighted Euclidean distance across 12 dimensions. Distinctive flavors (smoky/peaty, medicinal/iodine, maritime) are weighted higher than common ones (fruity, vanilla), so a peaty Islay malt won't be matched to a smooth Speyside just because both score high on "fruity."

**Cursor-based pagination** uses base64-encoded JSON offsets rather than keyset pagination. Simple to implement and sufficient for the dataset size (~200 whiskies, ~50 distilleries).

**Authentication** uses stateless JWT tokens with bcrypt password hashing. No refresh token rotation — the `/refresh` endpoint issues a new access token using the current valid token.

**User data isolation** is enforced at the service layer. Every bottle and wishlist query is scoped by `user_id`, preventing cross-user data access.
