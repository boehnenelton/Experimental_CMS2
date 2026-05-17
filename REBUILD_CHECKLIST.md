# 🛠️ ExpCSS RECONSTRUCTION: MASTER PLAN & CHECKLIST
**Project:** Experimental CSS CMS (v2.0)
**Core Mandate:** Rewire CMS to use the BEJSON HTML Template Library.
**Status:** Phase 1 - Planning & Staging

---

## 📋 PROGRESS CHECKLIST

- [x] **PHASE 1: ENVIRONMENT & CORE SKELETON**
    - [x] Stage HTML Templates to `staging_templates/`
    - [x] Create Universal `ExpCSS_Skeleton.html` (Merging Template-Blank with CMS Logic)
    - [x] Map static asset paths (CSS/JS) to new BEJSON Standard

- [x] **PHASE 2: GLOBAL COMPONENT REWIRING**
    - [x] Integrate `Template-Header-Default` (Telemetry HUD) into Skeleton
    - [x] Integrate `Template-Footer-Status-Feed` (for system metrics)
    - [x] Integrate Sidebar Discovery (Mapping MFDB NavLinks to `Sidebar-Nav-Tree`)

- [x] **PHASE 3: FEED & CATEGORY OVERHAUL**
    - [x] Rewire `Category_Feed_Skeleton` to support Blog, News, Products, and Masonry
    - [x] Implement dynamic feed type discovery in `ExpCSS_Builder.py`
    - [x] Integrate advanced feed CSS classes from library

- [x] **PHASE 4: PAGE TYPE MODERNIZATION**
    - [x] Rewire `Article_Skeleton` to `Template-Standard-Article`
    - [x] Rewire `SourceCode_Skeleton` to `Template-Standard-Code-Viewer`
    - [x] Implement `Video_Skeleton` with `Template-Standard-Video-Player`

- [x] **PHASE 5: BUILDER LOGIC UPDATE**
    - [x] Refactor `ExpCSS_Builder.py` to target new template blocks
    - [x] Update Relational Joins for advanced feed metadata

- [x] **PHASE 6: VALIDATION & MANUAL**
    - [x] Verify build output against 2026 CSS Standards
    - [x] Finalize "Developer Manual: Operating ExpCSS v2.0"

---

## 📝 TECHNICAL DESIGN NOTES

### 1. The Universal Skeleton
The new skeleton will abandon the legacy Tailwind-only approach. It will use `@layer` based CSS from the library.
- **Base:** `Template-Standard-Blank-Skeleton.html`
- **Injection Points:** `{{ header_block }}`, `{{ sidebar_block }}`, `{{ content_block }}`, `{{ footer_block }}`.

### 2. Feed Mapping
CMS Categories will now have a `template_preference` field in the MFDB to choose which feed type to render:
- `blog` -> `c-feed-blog`
- `news` -> `c-feed-news-advanced`
- `gallery` -> `c-feed-masonry`

### 3. CSS Portability
Every build will include a `css/` directory containing:
- `becss-core.css`
- `becss-components.css`
- `becss-headers.css` / `sidebars.css` / `footers.css`

---
*Last Updated: 2026-05-15 11:35:00*
