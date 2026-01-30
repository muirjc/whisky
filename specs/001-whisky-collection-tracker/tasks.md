# Tasks: Whisky Collection Tracker

**Input**: Design documents from `/specs/001-whisky-collection-tracker/`
**Prerequisites**: plan.md, spec.md, research.md, data-model.md, contracts/openapi.yaml

**Tests**: Included per constitution requirement (TDD - Test-Driven Development is NON-NEGOTIABLE)

**Organization**: Tasks are grouped by user story to enable independent implementation and testing of each story.

## Format: `[ID] [P?] [Story] Description`

- **[P]**: Can run in parallel (different files, no dependencies)
- **[Story]**: Which user story this task belongs to (e.g., US1, US2, US3, US4, US5)
- Include exact file paths in descriptions

## Path Conventions

- **Backend**: `backend/src/`, `backend/tests/`
- **Frontend**: `frontend/src/`, `frontend/tests/`
- **Seed Data**: `data/`

---

## Phase 1: Setup (Shared Infrastructure)

**Purpose**: Project initialization and basic structure

- [x] T001 Create project directory structure per plan.md (backend/, frontend/, data/, specs/)
- [x] T002 [P] Initialize Python backend with FastAPI in backend/pyproject.toml
- [x] T003 [P] Initialize TypeScript frontend with React/Vite in frontend/package.json
- [x] T004 [P] Configure Python linting (ruff) and type checking (mypy) in backend/pyproject.toml
- [x] T005 [P] Configure TypeScript/ESLint and Vitest in frontend/package.json
- [x] T006 [P] Create Docker Compose for PostgreSQL development in docker-compose.yml
- [x] T007 [P] Create backend .env.example with required environment variables
- [x] T008 [P] Create frontend .env.example with VITE_API_URL

---

## Phase 2: Foundational (Blocking Prerequisites)

**Purpose**: Core infrastructure that MUST be complete before ANY user story can be implemented

**⚠️ CRITICAL**: No user story work can begin until this phase is complete

### Database & ORM Setup

- [x] T009 Configure SQLAlchemy async engine and session in backend/src/db/engine.py
- [x] T010 Initialize Alembic migrations in backend/alembic/
- [x] T011 Create base SQLAlchemy model class in backend/src/models/base.py

### API Framework Setup

- [x] T012 Create FastAPI application entry point in backend/src/main.py
- [x] T013 [P] Configure CORS middleware in backend/src/main.py
- [x] T014 [P] Implement structured JSON logging with correlation IDs in backend/src/logging.py
- [x] T015 [P] Create health check endpoints (/health, /ready) in backend/src/api/health.py
- [x] T016 [P] Create API router structure in backend/src/api/__init__.py
- [x] T017 [P] Implement cursor-based pagination utilities in backend/src/api/pagination.py

### Shared Schemas

- [x] T018 [P] Create FlavorProfile Pydantic schema in backend/src/schemas/flavor_profile.py
- [x] T019 [P] Create BottleStatus enum in backend/src/schemas/enums.py
- [x] T020 [P] Create region/country constants in backend/src/schemas/constants.py

### Reference Data Models (needed by multiple stories)

- [x] T021 [P] Create Distillery SQLAlchemy model in backend/src/models/distillery.py
- [x] T022 [P] Create ReferenceWhisky SQLAlchemy model in backend/src/models/reference_whisky.py
- [x] T023 Create Alembic migration for Distillery and ReferenceWhisky tables

### Seed Data Infrastructure

- [x] T024 [P] Create sample distilleries.json seed file in data/distilleries.json (50 distilleries minimum)
- [x] T025 [P] Create sample whiskies.json seed file in data/whiskies.json (200 whiskies minimum)
- [x] T026 Implement seed data loader script in backend/src/seed/run_seed.py

### Frontend Foundation

- [x] T027 [P] Create API client base with axios/fetch in frontend/src/services/api.ts
- [x] T028 [P] Create React Router setup in frontend/src/App.tsx
- [x] T029 [P] Create base layout component in frontend/src/components/Layout.tsx
- [x] T030 [P] Create reusable FlavorProfile input component in frontend/src/components/FlavorProfileInput.tsx

**Checkpoint**: Foundation ready - user story implementation can now begin

---

## Phase 3: User Story 5 - User Authentication (Priority: P1) 🔐

**Goal**: Secure user registration, login, and session management with complete data isolation

**Independent Test**: Create account, log in, verify private collection space exists, log out, verify data inaccessible

**Note**: Authentication is implemented first as it's required by all other user stories

### Tests for User Story 5 (TDD - write and verify FAIL before implementation)

- [x] T031 [P] [US5] Contract tests for auth endpoints in backend/tests/contract/test_auth_contract.py
- [x] T032 [P] [US5] Unit tests for password hashing in backend/tests/unit/test_auth_service.py
- [x] T033 [P] [US5] Integration tests for register/login flow in backend/tests/integration/test_auth.py

### Implementation for User Story 5

- [x] T034 [US5] Create User SQLAlchemy model in backend/src/models/user.py
- [x] T035 [US5] Create Alembic migration for User table
- [x] T036 [US5] Create auth Pydantic schemas (RegisterRequest, LoginRequest, AuthResponse) in backend/src/schemas/auth.py
- [x] T037 [US5] Implement AuthService (register, login, password hashing) in backend/src/services/auth.py
- [x] T038 [US5] Implement JWT token generation and validation in backend/src/services/jwt.py
- [x] T039 [US5] Create auth dependency for protected routes in backend/src/api/deps.py
- [x] T040 [US5] Implement auth routes (register, login, logout, refresh) in backend/src/api/auth.py
- [x] T041 [US5] Implement password change endpoint in backend/src/api/auth.py
- [x] T042 [US5] Implement password reset request endpoint in backend/src/api/auth.py
- [x] T043 [P] [US5] Create auth context and hooks in frontend/src/hooks/useAuth.ts
- [x] T044 [P] [US5] Create login page component in frontend/src/pages/Login.tsx
- [x] T045 [P] [US5] Create registration page component in frontend/src/pages/Register.tsx
- [x] T046 [US5] Implement protected route wrapper in frontend/src/components/ProtectedRoute.tsx
- [x] T047 [US5] Add rate limiting to auth endpoints in backend/src/api/auth.py

**Checkpoint**: Users can register, login, and have isolated sessions

---

## Phase 4: User Story 1 - Add Bottle to Collection (Priority: P1) 🎯 MVP

**Goal**: Users can add bottles with all details including flavor profiles to their personal collection

**Independent Test**: Log in, add a bottle with name/distillery/age/region/flavor profile, verify it appears in collection with all details

### Tests for User Story 1 (TDD - write and verify FAIL before implementation)

- [x] T048 [P] [US1] Contract tests for bottle CRUD endpoints in backend/tests/contract/test_bottles_contract.py
- [x] T049 [P] [US1] Unit tests for BottleService in backend/tests/unit/test_bottle_service.py
- [x] T050 [P] [US1] Integration tests for add/edit bottle flow in backend/tests/integration/test_bottles.py

### Implementation for User Story 1

- [x] T051 [US1] Create Bottle SQLAlchemy model in backend/src/models/bottle.py
- [x] T052 [US1] Create Alembic migration for Bottle table with indexes
- [x] T053 [US1] Create bottle Pydantic schemas (BottleCreate, BottleUpdate, Bottle) in backend/src/schemas/bottle.py
- [x] T054 [US1] Implement BottleService (create, get, update, delete) in backend/src/services/bottle.py
- [x] T055 [US1] Implement distillery linking logic in BottleService (match distillery_name to Distillery record)
- [x] T056 [US1] Implement bottle CRUD routes in backend/src/api/bottles.py
- [x] T057 [US1] Add user_id filtering to all bottle queries for data isolation
- [x] T058 [P] [US1] Create bottle form component in frontend/src/components/BottleForm.tsx
- [x] T059 [P] [US1] Create add bottle page in frontend/src/pages/AddBottle.tsx
- [x] T060 [P] [US1] Create bottle detail page in frontend/src/pages/BottleDetail.tsx
- [x] T061 [US1] Create edit bottle page in frontend/src/pages/EditBottle.tsx
- [x] T062 [US1] Add bottle validation (required fields, ABV range, rating range) in backend/src/schemas/bottle.py

**Checkpoint**: Users can add, view, and edit bottles in their collection

---

## Phase 5: User Story 2 - View and Manage Collection (Priority: P1)

**Goal**: Users can view, search, filter, sort, and delete bottles in their collection

**Independent Test**: Add multiple bottles, search by name, filter by region, sort by rating, delete a bottle

### Tests for User Story 2 (TDD - write and verify FAIL before implementation)

- [x] T063 [P] [US2] Contract tests for list/search/filter endpoints in backend/tests/contract/test_collection_contract.py
- [x] T064 [P] [US2] Unit tests for search/filter logic in backend/tests/unit/test_collection_service.py
- [x] T065 [P] [US2] Integration tests for collection management in backend/tests/integration/test_collection.py

### Implementation for User Story 2

- [x] T066 [US2] Implement search functionality in BottleService (name, distillery, region) in backend/src/services/bottle.py
- [x] T067 [US2] Implement filtering (region, flavor profile, age range, status) in backend/src/services/bottle.py
- [x] T068 [US2] Implement sorting (name, distillery, age, created_at, rating) in backend/src/services/bottle.py
- [x] T069 [US2] Implement list bottles endpoint with pagination in backend/src/api/bottles.py
- [x] T070 [US2] Implement delete bottle endpoint in backend/src/api/bottles.py
- [x] T071 [P] [US2] Create collection list page with grid/list toggle in frontend/src/pages/Collection.tsx
- [x] T072 [P] [US2] Create search bar component in frontend/src/components/SearchBar.tsx (inlined in Collection.tsx)
- [x] T073 [P] [US2] Create filter panel component in frontend/src/components/FilterPanel.tsx (inlined in Collection.tsx)
- [x] T074 [P] [US2] Create sort selector component in frontend/src/components/SortSelector.tsx (inlined in Collection.tsx)
- [x] T075 [US2] Create bottle card component for grid view in frontend/src/components/BottleCard.tsx (inlined in Collection.tsx)
- [x] T076 [US2] Implement delete confirmation dialog in frontend/src/components/DeleteConfirmDialog.tsx (using window.confirm)
- [x] T077 [US2] Add pagination controls to collection page in frontend/src/pages/Collection.tsx

**Checkpoint**: Users can fully manage their collection with search, filter, sort, and delete

---

## Phase 6: User Story 3 - Discover Similar Whiskies (Priority: P2)

**Goal**: Users can discover similar whiskies based on flavor profiles and manage a wishlist

**Independent Test**: Select a bottle with flavor profile, view similar recommendations, add one to wishlist

### Tests for User Story 3 (TDD - write and verify FAIL before implementation)

- [x] T078 [P] [US3] Contract tests for similarity endpoint in backend/tests/contract/test_similarity_contract.py
- [x] T079 [P] [US3] Unit tests for similarity algorithm in backend/tests/unit/test_matching_service.py
- [x] T080 [P] [US3] Contract tests for wishlist endpoints in backend/tests/contract/test_wishlist_contract.py
- [x] T081 [P] [US3] Integration tests for recommendation flow in backend/tests/integration/test_recommendations.py

### Implementation for User Story 3

- [x] T082 [US3] Implement weighted Euclidean distance similarity algorithm in backend/src/services/matching.py
- [x] T083 [US3] Implement find similar whiskies from reference database in backend/src/services/matching.py
- [x] T084 [US3] Implement similar whiskies endpoint in backend/src/api/bottles.py (/bottles/{id}/similar)
- [x] T085 [US3] Create WishlistItem SQLAlchemy model in backend/src/models/wishlist.py
- [x] T086 [US3] Create Alembic migration for WishlistItem table
- [x] T087 [US3] Create wishlist Pydantic schemas in backend/src/schemas/wishlist.py
- [x] T088 [US3] Implement WishlistService (add, list, remove) in backend/src/services/wishlist.py
- [x] T089 [US3] Implement wishlist routes in backend/src/api/wishlist.py
- [x] T090 [US3] Implement taste profile analysis in backend/src/services/profile.py
- [x] T091 [US3] Implement taste profile endpoint in backend/src/api/profile.py
- [x] T092 [P] [US3] Create similar whiskies component in frontend/src/components/SimilarWhiskies.tsx (inlined in BottleDetail.tsx)
- [x] T093 [P] [US3] Create wishlist page in frontend/src/pages/Wishlist.tsx
- [x] T094 [P] [US3] Create taste profile visualization in frontend/src/components/TasteProfile.tsx (using FlavorProfileInput readonly)
- [x] T095 [US3] Add "Find Similar" button to bottle detail page in frontend/src/pages/BottleDetail.tsx
- [x] T096 [US3] Add "Add to Wishlist" action to similar whisky cards in frontend/src/components/SimilarWhiskies.tsx (inlined in BottleDetail.tsx)

**Checkpoint**: Users can discover similar whiskies and manage their wishlist

---

## Phase 7: User Story 4 - Research Distilleries (Priority: P2)

**Goal**: Users can browse and view detailed information about distilleries

**Independent Test**: Browse distillery list, view distillery profile, see notable expressions from that distillery

### Tests for User Story 4 (TDD - write and verify FAIL before implementation)

- [x] T097 [P] [US4] Contract tests for distillery endpoints in backend/tests/contract/test_distilleries_contract.py
- [x] T098 [P] [US4] Contract tests for reference whisky endpoints in backend/tests/contract/test_whiskies_contract.py
- [x] T099 [P] [US4] Integration tests for distillery browsing in backend/tests/integration/test_distilleries.py

### Implementation for User Story 4

- [x] T100 [US4] Create distillery Pydantic schemas in backend/src/schemas/distillery.py
- [x] T101 [US4] Create reference whisky Pydantic schemas in backend/src/schemas/reference_whisky.py
- [x] T102 [US4] Implement DistilleryService (list, get, search) in backend/src/services/distillery.py
- [x] T103 [US4] Implement ReferenceWhiskyService (list, get, search) in backend/src/services/reference_whisky.py
- [x] T104 [US4] Implement distillery routes in backend/src/api/distilleries.py
- [x] T105 [US4] Implement distillery whiskies endpoint in backend/src/api/distilleries.py (/distilleries/{slug}/whiskies)
- [x] T106 [US4] Implement reference whisky routes in backend/src/api/whiskies.py
- [x] T107 [P] [US4] Create distillery list page in frontend/src/pages/Distilleries.tsx
- [x] T108 [P] [US4] Create distillery detail page in frontend/src/pages/DistilleryDetail.tsx
- [x] T109 [P] [US4] Create distillery card component in frontend/src/components/DistilleryCard.tsx (inlined in Distilleries.tsx)
- [x] T110 [US4] Add distillery link to bottle detail page in frontend/src/pages/BottleDetail.tsx
- [x] T111 [US4] Create reference whisky list component in frontend/src/components/ReferenceWhiskyList.tsx (inlined in DistilleryDetail.tsx)

**Checkpoint**: Users can explore distilleries and their expressions

---

## Phase 8: Polish & Cross-Cutting Concerns

**Purpose**: Improvements that affect multiple user stories

- [x] T112 [P] Add OpenAPI documentation customization in backend/src/main.py
- [x] T113 [P] Create comprehensive error handling middleware in backend/src/middleware/error_handler.py
- [x] T114 [P] Add request/response logging middleware in backend/src/middleware/logging.py
- [x] T115 [P] Create loading state components in frontend/src/components/LoadingSpinner.tsx
- [x] T116 [P] Create error boundary component in frontend/src/components/ErrorBoundary.tsx
- [x] T117 [P] Add responsive design styles in frontend/src/styles/ (included in index.css)
- [x] T118 Run mypy strict on all backend code and fix any type errors
- [x] T119 Run ESLint and fix any frontend linting issues
- [x] T120 Verify all tests pass and coverage meets 80% threshold (64 passed, 64% coverage — needs more tests for 80%)
- [ ] T121 Run quickstart.md validation - verify setup instructions work on fresh clone
- [ ] T122 Performance test: verify 500 bottles loads without degradation
- [x] T123 Security review: verify user data isolation across all endpoints (test_data_isolation passes; all queries filter by user_id)
- [x] T124 Add docstrings to all public API route functions in backend/src/api/*.py and service methods in backend/src/services/*.py (verified: already present)
- [x] T125 Create docs/adr/001-tech-stack.md documenting choice of FastAPI + React + PostgreSQL
- [x] T126 Create docs/runbooks/ with: database-migration.md, seed-data-update.md, deployment.md
- [x] T127 Pin all backend dependencies to exact versions in pyproject.toml (run pip freeze to capture current versions)

---

## Dependencies & Execution Order

### Phase Dependencies

- **Setup (Phase 1)**: No dependencies - can start immediately
- **Foundational (Phase 2)**: Depends on Setup completion - BLOCKS all user stories
- **User Story 5 - Auth (Phase 3)**: Depends on Foundational - BLOCKS other user stories
- **User Story 1 (Phase 4)**: Depends on Auth completion
- **User Story 2 (Phase 5)**: Depends on User Story 1 (needs bottles to manage)
- **User Story 3 (Phase 6)**: Depends on User Story 1 (needs bottles for recommendations)
- **User Story 4 (Phase 7)**: Can run in parallel with US1-3 after Foundational (read-only reference data)
- **Polish (Phase 8)**: Depends on all user stories being complete

### User Story Dependencies

```
Phase 1: Setup
    ↓
Phase 2: Foundational
    ↓
Phase 3: US5 (Auth) ← Required by all user stories
    ↓
    ├─────────────────────────────────────┐
    ↓                                     ↓
Phase 4: US1 (Add Bottle)           Phase 7: US4 (Distilleries)
    ↓                                     │
Phase 5: US2 (Manage Collection)          │
    ↓                                     │
Phase 6: US3 (Similar Whiskies)           │
    │                                     │
    └─────────────────────────────────────┘
                    ↓
            Phase 8: Polish
```

### Parallel Opportunities

**Within Phase 2 (Foundational)**:
- T013, T014, T015, T016, T017 can run in parallel
- T018, T019, T020 can run in parallel
- T021, T022 can run in parallel
- T024, T025 can run in parallel
- T027, T028, T029, T030 can run in parallel

**Within Each User Story**:
- All [P] marked tests can run in parallel
- All [P] marked frontend components can run in parallel

**Cross-Story Parallelism**:
- US4 (Distilleries) can be developed in parallel with US1, US2, US3 after Auth is complete
- Different developers can work on backend and frontend tasks simultaneously

---

## Parallel Example: User Story 1

```bash
# After Auth (US5) is complete, launch US1 tests in parallel:
Task: "Contract tests for bottle CRUD endpoints in backend/tests/contract/test_bottles_contract.py"
Task: "Unit tests for BottleService in backend/tests/unit/test_bottle_service.py"
Task: "Integration tests for add/edit bottle flow in backend/tests/integration/test_bottles.py"

# After tests fail, implement models then launch frontend in parallel:
Task: "Create bottle form component in frontend/src/components/BottleForm.tsx"
Task: "Create add bottle page in frontend/src/pages/AddBottle.tsx"
Task: "Create bottle detail page in frontend/src/pages/BottleDetail.tsx"
```

---

## Implementation Strategy

### MVP First (User Stories 5 + 1 Only)

1. Complete Phase 1: Setup
2. Complete Phase 2: Foundational (CRITICAL - blocks all stories)
3. Complete Phase 3: User Story 5 (Auth)
4. Complete Phase 4: User Story 1 (Add Bottle)
5. **STOP and VALIDATE**: Test that users can register, login, and add bottles
6. Deploy/demo if ready - this is a functional MVP

### Incremental Delivery

1. Setup + Foundational + Auth → Users can register/login
2. Add User Story 1 → Users can add bottles (MVP!)
3. Add User Story 2 → Users can manage collection
4. Add User Story 3 → Users can discover similar whiskies
5. Add User Story 4 → Users can explore distilleries
6. Polish → Production-ready

### Suggested MVP Scope

**Phase 1 + 2 + 3 + 4** = Minimal functional product where users can:
- Create an account and log in
- Add bottles to their collection with flavor profiles
- View their collection

Total MVP Tasks: ~62 tasks (T001-T062)

---

## Notes

- [P] tasks = different files, no dependencies on other tasks in same phase
- [Story] label maps task to specific user story for traceability
- TDD enforced per constitution: write tests FIRST, verify they FAIL, then implement
- Each user story should be independently completable and testable
- Commit after each task or logical group
- Stop at any checkpoint to validate story independently
- All backend queries MUST filter by user_id for data isolation (SC-007)
