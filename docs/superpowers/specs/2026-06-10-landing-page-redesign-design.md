# Landing Page Redesign — Design Spec

**Date:** 2026-06-10
**Status:** Approved
**Scope:** Landing page only (`/` route → `epi_creator/templates/index.html`)

## Summary

Redesign the existing landing/hero page of the ePI Creator webapp into a modern, full-bleed gradient hero with a floating glass CTA. The page is currently the *only* entry to the app — there is no real login page — so this redesign is the user's first impression of the tool. Scope is intentionally limited to the landing page: no view changes, no new routes, no JS, no images, no Python changes. Bootstrap remains in use for the wizard pages.

## Goals

- Make the landing page feel modern, bold, and visually distinctive.
- Preserve all existing content and the "Start Wizard" call to action.
- Keep the change isolated: zero impact on the wizard flow, server, or other pages.
- No new assets, no JS, no external font, no CDN dependency.
- Respect accessibility and `prefers-reduced-motion`.

## Non-Goals

- Not building a real login/auth flow.
- Not redesigning the wizard pages.
- Not upgrading Bootstrap (which remains at 5.0.0-beta2 for the rest of the app).
- Not adding new routes, new endpoints, or new Python.
- Not adding any image, illustration, or icon.

## Affected Files

| File | Change |
|---|---|
| `epi_creator/templates/index.html` | Rewritten. Drops Bootstrap CDN. Adds semantic markup, link to new CSS, `aria-hidden` decorative layers. Form action and CSRF token preserved. |
| `epi_creator/static/css/landing.css` | **New.** All visuals: gradient/orb background, glass CTA, gradient text, link styles, reduced-motion + `backdrop-filter` fallbacks, print rules. |

No other files are touched. `epi_creator/static/css/main.css` is **not** loaded by the landing page (it only contains spinner/htmx styles used by wizard pages).

## Design Direction: "Aurora mesh"

Full-bleed dark background built from:
- A base linear gradient: deep navy → indigo → violet (`#0b1020` → `#1a1140` → `#2a0e4a`).
- A slowly rotating conic gradient masked by a soft radial, animated via `@property --angle` over 30s.
- Three large, blurred, drifting orbs (cyan, magenta, violet) with `mix-blend-mode: screen`, each on a different desynchronized animation duration (18s/26s/34s).
- A radial vignette to keep centered text high-contrast.

Centered content (no card; the CTA itself is the glass element):
1. Eyebrow — "HL7 · Gravitate Health", uppercase, letter-spaced, translucent.
2. Title — "ePI Creator", display weight, gradient text fill (white → soft cyan → violet).
3. Lead — one-sentence value prop.
4. Sub — the 11-step expectation line.
5. CTA — pill-shaped glass button "Start Wizard →".
6. Links — FAQ, FHIR Profiles, Gravitate Health IG, separated by `·`.

## DOM Structure

```html
<body class="landing">
  <div class="bg-layer" aria-hidden="true">
    <span class="orb orb--1"></span>
    <span class="orb orb--2"></span>
    <span class="orb orb--3"></span>
    <span class="vignette"></span>
  </div>

  <main class="hero">
    <p class="eyebrow">HL7 · Gravitate Health</p>
    <h1 class="title">ePI Creator</h1>
    <p class="lead">Create FHIR ePI resources using a guided step-by-step wizard. No Excel required.</p>
    <p class="sub">Fill in the forms across 11 steps to generate a complete FHIR package with FSH and JSON resources.</p>

    <form method="post" action="{{ url_for('gh_epi_creator.wizard_new') }}" class="cta-form">
      <input type="hidden" name="csrf_token" value="{{ csrf_token() }}">
      <button type="submit" class="cta">Start Wizard <span class="cta__arrow" aria-hidden="true">→</span></button>
    </form>

    <nav class="links" aria-label="Related resources">
      <a href="{{ url_for('gh_epi_creator.faq') }}">FAQ &amp; Resource Relationships</a>
      <span class="dot" aria-hidden="true">·</span>
      <a href="http://build.fhir.org/ig/HL7/emedicinal-product-info/artifacts.html">FHIR Profiles</a>
      <span class="dot" aria-hidden="true">·</span>
      <a href="http://build.fhir.org/ig/hl7-eu/gravitate-health/">Gravitate Health IG</a>
    </nav>
  </main>
</body>
```

The `<body>` gets a `landing` class so all rules are scoped and cannot leak into wizard pages.

## CSS Tokens

Defined on `:root`:

- `--bg-base: #0b1020;`
- `--bg-stop-1: #0b1020;` `--bg-stop-2: #1a1140;` `--bg-stop-3: #2a0e4a;`
- `--ink: #f4f6ff;` `--ink-dim: rgba(244, 246, 255, 0.78);` `--ink-faint: rgba(244, 246, 255, 0.55);`
- `--glass: rgba(255, 255, 255, 0.08);` `--glass-border: rgba(255, 255, 255, 0.18);`
- `--accent-cyan: #7dd3fc;` `--accent-violet: #c4b5fd;`
- `--grad-text: linear-gradient(120deg, #ffffff 0%, #bae6fd 45%, #c4b5fd 100%);`
- `--grad-cta: linear-gradient(135deg, #ffffff 0%, #bae6fd 100%);`
- `--radius-pill: 999px;`
- `--shadow-glow: 0 10px 30px rgba(124, 58, 237, 0.35), 0 2px 8px rgba(0, 0, 0, 0.25);`
- `--ease: cubic-bezier(0.22, 1, 0.36, 1);`

## Key CSS Rules (intent, not literal)

- `body.landing` — dark `color-scheme`, system font stack, full viewport height, fallback `background-color: var(--bg-base)` so the page is readable even if the layered background fails to render.
- `.bg-layer` — `position: fixed; inset: 0; z-index: -1; overflow: hidden;` carries the base linear gradient, the conic mesh, the orbs, and the vignette.
- `.orb` — absolute, `border-radius: 50%`, `filter: blur(80px)`, `opacity: 0.55`, `mix-blend-mode: screen`, `pointer-events: none`. Each orb has a unique `@keyframes drift` translating in a loop, with distinct durations/delays.
- `.hero` — `min-height: 100dvh; display: grid; place-items: center; padding: clamp(24px, 5vw, 64px);` with an inner wrapper `max-width: 56ch; text-align: center;`.
- `.title` — `clamp(2.5rem, 7vw, 4.5rem); font-weight: 800; letter-spacing: -0.03em;` with `background: var(--grad-text); -webkit-background-clip: text; color: transparent;` and a soft cyan `text-shadow` glow.
- `.lead` / `.sub` — clamped sizes, `--ink` and `--ink-dim` respectively, with `max-width: 38ch` / `46ch` for readability.
- `.cta` — pill, glass background, `backdrop-filter: blur(14px) saturate(140%)` (with `-webkit-` prefix), `border: 1px solid var(--glass-border)`, soft glow shadow, white text. Hover: `translateY(-2px)`, brighter background, deeper shadow, 200ms `var(--ease)`. The arrow inside the button slides `translateX(4px)` on hover. Focus-visible: 2px cyan outline with 4px offset.
- `.links a` — `--ink-faint`, no underline; hover `--ink` + underline with `text-underline-offset: 4px`. Focus-visible ring.
- `.dot` — `var(--ink-faint)`, decorative (`aria-hidden`).
- `@media (prefers-reduced-motion: reduce)` — disables all animations and the hover transform; CTA hover becomes a plain color change.
- `@supports not ((backdrop-filter: blur(1px)) or (-webkit-backdrop-filter: blur(1px)))` — bumps glass background to `rgba(255,255,255,0.18)` so contrast holds on browsers without `backdrop-filter`.
- `@media print` — hides `.bg-layer` and `.cta`, switches to white background with black text so the page is sensible if printed.

## Accessibility

- Real semantic structure: `<main>`, `<h1>`, `<p>`, `<nav aria-label="Related resources">`.
- Decorative layers (`bg-layer`, orbs, vignette, dot separators, CTA arrow) are `aria-hidden="true"`.
- Color contrast: title uses gradient over a dark vignette — white stop keeps it ≥ 7:1. Lead (`--ink` on dark) ≥ 7:1. Sub (`--ink-dim`) ≥ 4.5:1. Links (`--ink-faint`) ≥ 4.5:1.
- Focus order: CTA → FAQ → FHIR Profiles → Gravitate Health IG. All have visible focus rings.
- Tabbable: CTA button and the three links. No other focusable elements.
- Respects `prefers-reduced-motion` (see above).
- Respects `prefers-color-scheme` by **not** overriding it — the landing is intentionally dark regardless of system theme, as a deliberate design decision distinct from the wizard.
- No information is conveyed by color or motion alone.

## Error Handling & Edge Cases

- The page is GET-only with a single POST form. The form target (`wizard_new`) and CSRF token are unchanged from the current template, so Flask-WTF continues to protect it. No new failure modes introduced.
- External links (FHIR Profiles, Gravitate Health IG) open in the same window, identical to current behavior.
- If `landing.css` fails to load, the body fallback `background-color: var(--bg-base)` and the unstyled text remain readable; the form still submits (no JS dependency).
- `<480px` viewports: CTA becomes `width: 100%; max-width: 320px;` and the title scales down via `clamp()`.
- `>1600px` viewports: content stays capped at `56ch`, orbs scale visually but `pointer-events: none` ensures they never block interaction.
- No JS means there is nothing to break on script-disabled clients.

## Testing Strategy

- **No new Python tests** — no server-side code is added.
- **Manual visual checks:** run the app, open `/` in Chrome, Safari, Firefox, and a mobile-sized viewport. Verify orb drift, conic gradient, gradient text, glass CTA, hover, focus ring, and reduced-motion behavior.
- **Smoke test:** click "Start Wizard" — the existing wizard flow loads (CSRF works, redirect to step 1).
- **Accessibility check:** tab through the page; confirm focus order and visible focus rings; quick contrast check on lead/sub against the darkest background region (vignette).
- **Reduced motion:** toggle the OS setting (or DevTools rendering → "Emulate CSS media feature prefers-reduced-motion: reduce") and confirm animations stop and the CTA hover stays static.

## Out of Scope / Future Work

- A real login/auth flow (user explicitly chose "landing page only").
- A custom SVG hero illustration or brand mark.
- A dark mode toggle (the page is dark by design).
- Upgrading Bootstrap on the rest of the app.
