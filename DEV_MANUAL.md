# 📖 DEVELOPER MANUAL: OPERATING ExpCSS v2.0
**System Identity:** Experimental CSS CMS (Template Scaffolding Edition)
**Base Standards:** BEJSON v104 | MFDB v1.3.1 | BECSS v2026
**Lead Architect:** Elton Boehnen

---

## 1. ARCHITECTURAL OVERVIEW
ExpCSS v2.0 is a block-based static site generator that leverages the **BEJSON HTML Template Library**.

### 1.1. Unified Backend (`ExpCSS_CMS.py`)
The administrative layer has been consolidated into a single high-performance Flask application (Port 5005). It integrates:
- **Relational Dashboard:** Real-time MFDB metrics.
- **Advanced Content Editor:** Specialized views for Article, Code, and Multimedia.
- **Media Orchestrator:** Secure asset registration and SHA-256 deduplication.
- **Preview Node:** Integrated HTTP server for verifying built assets.
- **Build Engine Controller:** One-click synchronization with the static scaffolding.

### 1.2. Presentation Layer
v2.0 assembles pages from discrete, re-usable fragments:
- **Headers:** Telemetry-aware functional components.
- **Sidebars:** Dynamic NavTrees generated from MFDB Category registries.
- **Bodies:** Content-specific fragments (Article, Code, Video, Feed).
- **Footers:** Modular status ribbons and system logs.

## 2. THE RECONSTRUCTION SKELETON
The new `Global_Skeleton.html` uses a **Block Injection** pattern.

### Injection Points:
- `{{ header_block }}`: Injects a server-side rendered header component.
- `{{ sidebar_block }}`: Injects a dynamic navigation sidebar.
- `{{ main_content }}`: Injects the specific page type component (e.g., Article).
- `{{ footer_block }}`: Injects the global system status footer.

## 3. COMPONENT DIRECTORY (`staging_templates/`)
All building blocks are sourced from the library and staged locally for the build process:
- `/components/headers/`: `Template-Header-Telemetry-HUD.html` (Current Default)
- `/components/sidebars/`: `Sidebar-Nav-Tree.html` (Current Default)
- `/components/footers/`: `Template-Footer-Status-Feed.html` (Current Default)
- `/css/`: Standard BECSS library files.

## 4. BUILDER LOGIC (`ExpCSS_Builder.py`)
The generator has been re-wired to perform the following sequence:
1.  **Sync CSS:** Copies all library styles into the build `css/` directory.
2.  **Initialize Context:** Fetches global configs and categories from MFDB.
3.  **Fragment Assembly:** Reads and renders the individual components into variables.
4.  **Relational Join:** Joins Page metadata with Content (HTML, Source Code, or Video URLs).
5.  **Final Stitching:** Passes all assembled blocks into the `Global_Skeleton.html` for final output.

## 5. PAGE TYPE SPECIFICATIONS

### 5.1. Standard Articles
- **Base:** `Article_Skeleton.html` (v2.0)
- **Features:** Responsive meta-bar, auto-injected author profile, and Tailwind-enhanced typography.

### 5.2. Technical Source Code
- **Base:** `SourceCode_Skeleton.html` (v2.0)
- **Features:** Multi-file support, syntax-aware labels, and one-click clipboard copying.

### 5.3. Multimedia Video
- **Base:** `Video_Skeleton.html` (v2.0)
- **Features:** 16:9 aspect ratio locking and integrated description cards.

## 6. CSS LAYERING PROTOCOL
The system adheres to **2026 BECSS Standards**:
1.  `becss-core.css`: Resets and global variables.
2.  `becss-components.css`: Fragment-specific styling.
3.  `becss-headers/sidebars/footers.css`: Positional layout rules.

---
*Status: Phase 4 Complete | Build v2.0.4*
