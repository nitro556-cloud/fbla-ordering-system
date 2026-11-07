# Rendezvous interface refinement

Implemented November 7, 2026 in the existing Flask / Jinja / vanilla CSS application.

## Audit and direction

The original pages gave six navigation destinations equal weight, used a generic coffee headline, repeated rounded product cards, and presented checkout and reports as technical forms and paragraphs. Available inventory was treated like marketing scarcity even when plentiful. Cart feedback did not identify what was added or preserve the browsing context.

The new visual system treats Rendezvous as a café menu book: deep green ink, warm paper, restrained brown accents, distinctive lowercase typography, aligned prices, open product rows, and rules instead of nested cards. Offline display typography uses Iowan Old Style / Palatino-family fallbacks; body text uses Avenir Next / Avenir / Segoe UI. The homepage uses the existing coffee photograph and a single arched crop, with copy tied to the meaning of rendezvous: making time to meet. No business claims, products, or photography were invented.

## Implemented changes

- Shared shell: Menu and Your Order take priority. A native disclosure and footer expose story, help, and reporting. Added session item count, skip link, categorized feedback, visible focus styles, and shared semantic color and typography tokens.
- Home: new wordmark, focused headline and menu action, and photographic links to the existing Drinks and Food categories.
- Menu: open two-column product rows on desktop and one column on mobile; category sections, visible prices, truthful availability, sold-out controls, searchable category filtering, and enhanced quantity controls. Additions name the item and quantity and preserve search/category context.
- Cart: distinct item list and checkout panel; inline quantity update/removal, selectable fulfillment options, instructions, discount and spending-limit help, server-rendered total preview, and an explicit stale-preview notice when settings change. Empty carts offer a direct menu path. Stock conflicts are visible beside affected items.
- Receipt: reassurance separated from a readable saved receipt, itemized totals, fulfillment, instructions, and order-history link.
- Report: grouped filters, calculated summary figures, accessible sales table, separate low-stock inventory, newest-first receipt links, and purposeful empty states. Labels explain the difference between gross item revenue and full-order totals.
- Help: offline keyword assistance, native expandable common questions, ordering guide, and accurate demonstration/contact context.
- Story: editorial layout using existing product photography, with an honest account of the FBLA project.

All existing routes, data structures, money calculations, stock checks, discount rules, budget enforcement, persistence, report filtering, and offline functionality are retained. JavaScript only enhances controls and feedback; the server remains authoritative. No dependencies were added.

## Verification performed

- `PYTHONDONTWRITEBYTECODE=1 .venv/bin/python -m unittest -v`: **15 tests passed**. This includes all 12 original regression tests and 3 new tests for combined category/search filtering, specific add feedback with context and count, and inline removal / empty checkout behavior.
- `node --check static/ordering.js`: passed.
- `git diff --check`: passed.
- Headless Chrome: all seven page types checked at 320, 390, 768, 1024, and 1440 pixels with no horizontal document overflow. Desktop and mobile screenshots captured; homepage, menu, cart, confirmation, help, story, and reports reviewed.
- Browser ordering flow: quantity stepper incremented a latte quantity to two; add preserved search and category and showed the correct count; checkout choices marked the preview stale; CAFE10 with simulated delivery produced $12.83; a $1 limit blocked checkout; a $20 limit saved the receipt, cleared the cart, and populated reports.
- Keyboard Space opened secondary navigation; Escape closed it; keyboard focus had a visible solid outline. Native menu quantity fields and POST forms remained available with JavaScript disabled. Offline FAQ form submission returned the expected budget answer. No browser JavaScript exceptions were recorded during the completed accessibility/responsive pass.
- Calculated contrast ratios: primary text 10.51:1, muted text 5.29:1, muted text on checkout 4.93:1, brown accent 5.55:1, primary button 11.46:1, error text 6.81:1.
- Tests used temporary storage. Browser QA used a separate `/private/tmp/rendezvous-visual-qa.json`; the project's saved orders and inventory were not consumed.

## Limits

Browser verification used Chrome with responsive viewport emulation, not physical touch devices, Safari, or Firefox. Font appearance depends on installed offline fonts. This remains the existing student demonstration, with no real payments, pickup address, or delivery dispatch. No deployment was performed.
