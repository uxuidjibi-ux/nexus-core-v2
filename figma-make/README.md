# AutoCommerce Figma Make MVP

This folder contains a complete responsive React/Vite prototype prepared for Figma Make.

## Open locally

```bash
npm install
npm run dev
```

Then open the local URL shown by Vite.

## Use in Figma Make

1. Create a new Figma Make project.
2. Upload every file and folder in this directory, preserving the structure.
3. Paste the full content of `FIGMA_MAKE_PROMPT.md` into Figma Make.
4. Ask Figma Make to run the project without replacing the existing React implementation.
5. Verify search, filters, quick view, comparison and the seller listing flow.

## Core demonstration path

1. Hide and reopen Filters.
2. Search for `Honda`, filter by SUV and adjust the maximum price.
3. Select a vehicle to open Quick view.
4. Add or remove vehicles from Compare.
5. Select `Sell your vehicle`.
6. Enter a VIN, continue with demo photos and generate the AI listing.

No API key is required for the prototype. VIN decoding, image validation and AI generation are simulated locally and are ready to be replaced with production endpoints.
