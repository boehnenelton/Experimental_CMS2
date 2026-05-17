# Component Architecture Plan: BECSS Architecture 2026

This document outlines the architectural strategy for refactoring individual body components using **Modern CSS (2026 BECSSs)**.

## 1. Core Architectural Pillars

### 1.1 Encapsulation via BEM and Cascade Layers
To prevent style leakage, every component will be wrapped in a unique BEM block name matching its filename (e.g., .c-auth-login).
- All internal styles will be nested under this block or grouped into a CSS Cascade Layer.
- Naming BECSS: .c-[component-name]

### 1.2 Atomic Integration
Components are categorized by complexity:
- Atoms: Shared standard buttons/inputs via CSS variables.
- Molecules: Composed units like search-bar.
- Organisms: The final body components.

### 1.3 Adaptive Design: Container Queries
Instead of @media (viewport), components will use @container to adapt to column width.

### 1.4 Theming: OKLCH
- Use oklch() for uniform perceptual brightness.
- Brand Primary: oklch(65% 0.2 25) (Red emphasis).

---

## 2. Individual Component Strategy

### 2.1 Authentication
- Modern Features: :user-invalid validation; accent-color for inputs.
- BEM: .c-auth-login, .c-auth-login__form.

### 2.2 Communication (Chat)
- Modern Features: field-sizing: content; Scroll-Driven Animations.
- BEM: .c-chat, .c-chat__messages.

### 2.3 Data and Tables
- Modern Features: subgrid for alignment; color-mix() for highlights.
- BEM: .c-data-table.

### 2.4 Administrative (Log/Health)
- Modern Features: animation-timeline: scroll(); oklch() semantic colors.
- BEM: .c-admin-log.

### 2.5 Feeds and Cards
- Modern Features: CSS Grid with masonry; View Transitions.
- BEM: .c-feed-gallery.

---

## 3. Implementation Checklist

1. Wrap every component in a <div class="c-[name]">.
2. Move internal styles into @layer components.[name].
3. Convert hex codes to oklch().
4. Replace @media with @container.
5. Audit for clashing.

---
**Status:** Planning Phase Complete.

---

## Part 2: Unified External Stylesheet (Core Architecture)

This phase focuses on externalizing the redundant layout logic into a single, high-performance central file: becss-core.css.

### 2.1 The Layered Hierarchy (@layer)
To ensure the central stylesheet remains robust and non-conflicting, we will use CSS Cascade Layers:
1. @layer reset: BECSS browser normalization.
2. @layer base: Root variables (OKLCH palette), typography.
3. @layer layout: The 3-column grid system, header branding, sidebars.
4. @layer interactive: Global transitions and mobile drawer logic.

### 2.2 Global Variable Tokenization
Extract hardcoded values into a centralized :root block using 2026 naming conventions:
- --color-brand-primary: oklch(65% 0.2 25)
- --font-sans: Inter, system-ui, sans-serif
- --sidebar-width: 250px

### 2.3 Responsive Scaffolding
Move layout-level media queries into this file. The Shell of every page is managed centrally.

### 2.4 Implementation Strategy
1. Core Extraction: Pull common layout CSS into becss-core.css.
2. Refactor: Replace internal style blocks in all 47 templates with a link to the external CSS.
3. Isolation: Central file manages Page Scaffolding; components manage internal content.

**Goal:** Reduce file size and allow for system-wide layout updates with a single edit.
