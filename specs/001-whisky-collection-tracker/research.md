# Research: Whisky Collection Tracker

**Date**: 2026-01-17
**Feature**: 001-whisky-collection-tracker

## Technology Stack Decisions

### Backend Framework: FastAPI

**Decision**: Use FastAPI as the backend framework

**Rationale**:
- Native async support for efficient I/O handling
- Automatic OpenAPI/Swagger documentation generation (aligns with API-First principle)
- Built-in request validation via Pydantic (aligns with Type Safety principle)
- Excellent performance characteristics for API workloads
- Strong typing support with Python type hints

**Alternatives Considered**:
- Django REST Framework: More batteries-included but heavier; async support less mature
- Flask: Simpler but lacks built-in validation and OpenAPI generation
- Starlette: Lower-level; would require more boilerplate

### Database: PostgreSQL with SQLAlchemy

**Decision**: Use PostgreSQL as the primary database with SQLAlchemy ORM

**Rationale**:
- ACID compliance for data integrity (user collections must be reliable)
- Rich querying capabilities for filtering/sorting bottles
- JSON/JSONB support for flexible flavor profile storage
- Mature ecosystem with excellent Python support
- SQLAlchemy provides type-safe ORM with good async support (via asyncpg)

**Alternatives Considered**:
- SQLite: Simpler but limited concurrent write support; not suitable for multi-user web app
- MongoDB: Flexible schema but overkill for well-defined entities; weaker data integrity
- MySQL: Viable but PostgreSQL has better JSON support and richer feature set

### Frontend Framework: React with TypeScript

**Decision**: Use React with TypeScript for the frontend

**Rationale**:
- Component-based architecture suits the feature-organized structure
- TypeScript provides compile-time type safety (aligns with Type Safety principle)
- Large ecosystem for UI components (tables, forms, filters)
- Good tooling support (Vite, Vitest, Playwright)
- React Server Components not needed for this app's complexity level

**Alternatives Considered**:
- Vue.js: Excellent but smaller ecosystem; team familiarity assumed with React
- Svelte: Newer, smaller bundle size but less mature testing tooling
- HTMX + Jinja: Simpler but less interactive; harder to build rich filtering/search UX

### Authentication: JWT with httpOnly Cookies

**Decision**: Use JWT tokens stored in httpOnly cookies for session management

**Rationale**:
- Stateless authentication reduces server-side complexity
- httpOnly cookies prevent XSS token theft (aligns with Security by Default)
- Refresh token rotation for extended sessions
- Works well with SPA architecture
- No external auth provider needed for single-user focus

**Alternatives Considered**:
- Session-based with Redis: More server state to manage; unnecessary for this scale
- OAuth2/OIDC: Overkill for single-user app without social features
- Auth0/Firebase Auth: External dependency unnecessary for simple email/password auth

## Flavor Profile Matching Algorithm

### Decision: Vector Similarity with Weighted Euclidean Distance

**Decision**: Represent flavor profiles as numeric vectors and use weighted Euclidean distance for similarity matching

**Rationale**:
- Flavor descriptors map naturally to numeric scales (intensity 0-5 for each descriptor)
- Euclidean distance provides intuitive similarity measure
- Weights allow prioritizing dominant flavors (e.g., smoke/peat for Islay malts)
- Simple to implement and explain to users
- Can be computed efficiently in SQL or Python

**Algorithm**:
```
similarity_score = 1 / (1 + sqrt(sum(weight_i * (a_i - b_i)^2)))
```

Where:
- `a_i`, `b_i` are intensity values for flavor descriptor `i`
- `weight_i` prioritizes key distinguishing flavors
- Score normalized to 0-1 range (1 = identical profile)

**Alternatives Considered**:
- Cosine similarity: Works but less intuitive for comparing absolute intensity levels
- Machine learning embeddings: Overkill for predefined descriptor set; requires training data
- Rule-based matching: Less nuanced; would miss subtle flavor relationships

### Flavor Descriptor Set

**Decision**: Use a curated set of 12 core flavor descriptors

**Descriptors** (each rated 0-5 intensity):
1. Smoky/Peaty
2. Fruity (citrus, orchard, tropical)
3. Sherried (dried fruit, rich)
4. Spicy (pepper, cinnamon)
5. Floral/Grassy
6. Maritime (brine, seaweed)
7. Honey/Sweet
8. Vanilla/Caramel
9. Oak/Woody
10. Nutty
11. Malty/Biscuity
12. Medicinal/Iodine

**Rationale**:
- Covers major whisky flavor categories recognized by experts
- 12 descriptors balance detail with usability (users can rate quickly)
- Aligns with common whisky tasting wheel categories
- Sufficient granularity for meaningful similarity matching

## Reference Data Strategy

### Whisky Reference Database

**Decision**: Create a pre-seeded JSON database of ~5000 common whiskies with flavor profiles

**Data Structure**:
```json
{
  "id": "lagavulin-16",
  "name": "Lagavulin 16 Year Old",
  "distillery_id": "lagavulin",
  "age_statement": 16,
  "region": "Islay",
  "country": "Scotland",
  "flavor_profile": {
    "smoky_peaty": 5,
    "maritime": 4,
    "sherried": 3,
    ...
  }
}
```

**Data Sources** (for initial population):
- Publicly available whisky databases
- Community-contributed tasting notes
- Distillery official descriptions

**Rationale**:
- Static JSON allows version control of reference data
- Easy to update periodically without code changes
- Seeded into PostgreSQL at deployment for efficient querying
- No runtime dependency on external APIs

### Distillery Database

**Decision**: Create a curated JSON database of ~500 distilleries

**Data Structure**:
```json
{
  "id": "lagavulin",
  "name": "Lagavulin",
  "region": "Islay",
  "country": "Scotland",
  "location": {
    "latitude": 55.6358,
    "longitude": -6.1264
  },
  "founded": 1816,
  "owner": "Diageo",
  "history": "Founded in 1816...",
  "production_notes": "Known for heavily peated...",
  "website": "https://www.malts.com/lagavulin"
}
```

**Rationale**:
- Curated data ensures quality and consistency
- No web scraping avoids legal/reliability issues
- Can be updated by app owner on release cycle
- Links to official website for users wanting more detail

## API Design Patterns

### REST Resource Structure

**Decision**: Use standard REST patterns with nested resources where appropriate

**Endpoints** (summary):
- `/api/v1/auth/*` - Authentication (register, login, refresh, logout)
- `/api/v1/bottles/*` - User's bottle collection (CRUD)
- `/api/v1/bottles/{id}/similar` - Similar whisky recommendations
- `/api/v1/wishlist/*` - User's wishlist (CRUD)
- `/api/v1/distilleries/*` - Reference distillery data (read-only)
- `/api/v1/whiskies/*` - Reference whisky data (read-only, search)
- `/api/v1/profile/*` - User taste profile analysis

**Rationale**:
- RESTful patterns well-understood and documented
- Versioned API (`/v1/`) allows future evolution
- Nested resources (`/bottles/{id}/similar`) express relationships clearly

### Pagination Strategy

**Decision**: Use cursor-based pagination for list endpoints

**Rationale**:
- Stable results when data changes during pagination
- Efficient for large collections (up to 500 bottles)
- Works well with sorted/filtered queries

**Format**:
```json
{
  "items": [...],
  "next_cursor": "eyJpZCI6MTAwfQ==",
  "has_more": true
}
```

## Security Considerations

### Password Storage

**Decision**: Use bcrypt with cost factor 12 for password hashing

**Rationale**:
- Industry standard for password hashing
- Cost factor 12 provides good balance of security and performance
- Built-in salt prevents rainbow table attacks

### Input Validation

**Decision**: Validate all input at API boundary using Pydantic models

**Rationale**:
- Centralized validation prevents injection attacks
- Type coercion handles common input issues
- Error messages automatically generated
- Aligns with Type Safety principle

### Rate Limiting

**Decision**: Implement rate limiting on authentication endpoints

**Limits**:
- Login: 5 attempts per minute per IP
- Registration: 3 per hour per IP
- Password reset: 3 per hour per email

**Rationale**:
- Prevents brute force attacks
- Protects against credential stuffing
- Standard security practice

## Observability Strategy

### Logging

**Decision**: Use structlog for structured JSON logging

**Log Fields**:
- `timestamp`: ISO 8601 format
- `level`: DEBUG/INFO/WARNING/ERROR
- `correlation_id`: Request-scoped UUID
- `user_id`: Authenticated user (if applicable)
- `endpoint`: API route
- `duration_ms`: Request duration
- `message`: Human-readable message

**Rationale**:
- JSON format enables log aggregation and search
- Correlation IDs enable request tracing
- Aligns with Observability principle

### Health Checks

**Decision**: Implement `/health` and `/ready` endpoints

- `/health`: Basic liveness check (always returns 200 if app running)
- `/ready`: Readiness check (verifies database connectivity)

**Rationale**:
- Standard pattern for container orchestration
- Enables automated health monitoring
- Supports graceful deployment strategies

## Open Questions Resolved

All technical clarifications from the specification phase have been addressed:

1. **Reference database source**: Pre-seeded static JSON, loaded into PostgreSQL
2. **Distillery information**: Curated static database, no live web fetching
3. **Social/sharing scope**: Single-user only, no sharing features

No remaining NEEDS CLARIFICATION items.
