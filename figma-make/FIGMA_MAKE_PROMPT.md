# AutoCommerce — Figma Make execution prompt

Build the complete AutoCommerce Canadian automotive marketplace MVP from the attached React/Vite source files. Preserve the existing component architecture, content, design tokens, interactions, responsive behavior and accessibility.

## Product objective

Create an automotive marketplace that is simpler and more fluid than traditional classifieds. The filter system must be retractable and never dominate browsing. AutoCommerce owns the product and supports both buyers and professional sellers.

## Required screens and states

1. Vehicle search and results:
   - compact black navigation bar;
   - retractable left filter drawer;
   - search, sort and grid/list controls;
   - responsive vehicle cards;
   - saved vehicles;
   - comparison tray for up to three vehicles;
   - empty search state.
2. Vehicle quick view:
   - image;
   - price and finance estimate;
   - VIN-verified state;
   - technical specifications;
   - contact and financing actions.
3. Smart seller listing flow:
   - VIN input and decoding state;
   - intelligent photo-upload state;
   - AI listing-generation state;
   - final publish action.
4. Responsive mobile behavior:
   - full-screen filters;
   - single-column inventory;
   - full-width vehicle detail;
   - compact comparison bar.

## Visual system

- Background: true white `#FFFFFF`.
- Primary text/navigation: near black `#111111`.
- Primary action: AutoCommerce red `#D71920`.
- Verified/success: green `#198754`.
- Neutral surface: `#F6F7F8`.
- Borders: `#DFE2E5`.
- Typography: Helvetica Neue / Helvetica / Arial.
- Avoid gradients, glassmorphism, excessive cards and decorative dashboards.
- Use the provided concept image at `design-reference/autocommerce-marketplace-concept.png` as the visual reference.

## Functional requirements

- All filters, search and sorting must update local UI state.
- Save and compare controls must work.
- The quick-view panel must open and close.
- The seller modal must progress through all three steps.
- VIN decoding and AI description generation can be simulated locally.
- Use reusable components, semantic HTML, keyboard-visible focus and `prefers-reduced-motion`.
- Do not add unrelated sections, marketing claims, fake statistics or decorative badges.

## Source-file instruction

Use `src/App.jsx`, `src/data.js` and `src/styles.css` as the canonical implementation. Do not replace the interface with a static screenshot. Keep all visible controls code-native and interactive.
