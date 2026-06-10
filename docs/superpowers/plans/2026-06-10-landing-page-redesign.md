# Landing Page Redesign Implementation Plan

> **For agentic workers:** REQUIRED SUB-SKILL: Use superpowers:subagent-driven-development (recommended) or superpowers:executing-plans to implement this plan task-by-task. Steps use checkbox (`- [ ]`) syntax for tracking.

**Goal:** Replace the existing Bootstrap-based landing page (`epi_creator/templates/index.html`) with a modern, full-bleed gradient/glass hero, by rewriting the template and adding a single new self-contained CSS file. No server-side, JS, or wizard changes.

**Architecture:** Standalone landing page (no template inheritance). The `<body>` gets a `landing` scope class so all CSS is isolated and cannot leak into wizard pages. Background is pure CSS (linear gradient + animated conic mesh + drifting blurred orbs + vignette). The CTA is the glass element. Bootstrap CDN is removed from this page only; wizard pages continue to use it unchanged.

**Tech Stack:** Flask 2.x templates (Jinja2), plain CSS3 (custom properties, `@property`, `backdrop-filter`, `mix-blend-mode`, `prefers-reduced-motion`, `@supports` fallbacks). No JS, no fonts, no images, no new Python.

**Reference spec:** `docs/superpowers/specs/2026-06-10-landing-page-redesign-design.md`

**Project conventions:**
- Run the dev server with `python run.py` (or `flask run` if `FLASK_APP` is set). The app is mounted at `/gh-epi-creator`, so the landing page is at `http://127.0.0.1:5000/gh-epi-creator/`.
- Existing static asset layout: `epi_creator/static/css/` and `epi_creator/static/js/`. New CSS goes in `epi_creator/static/css/landing.css`.
- Commit style: short, lowercase, conventional (`feat:`, `fix:`, `chore:`, `docs:`). Atomic commits per task.

**Out of scope:** Anything in `epi_creator/templates/wizard/`, `epi_creator/views.py`, `epi_creator/__init__.py`, `epi_creator/static/css/main.css`, `epi_creator/static/js/`, Python dependencies, Bootstrap version, login/auth.

---

## File Structure

| File | Status | Responsibility |
|---|---|---|
| `epi_creator/templates/index.html` | Rewrite | Markup for the hero, single hidden CSRF input, form to `wizard_new`, links, decorative `aria-hidden` background layer. |
| `epi_creator/static/css/landing.css` | Create | All visuals. Scoped to `body.landing`. Includes tokens, background layers, hero, CTA, links, reduced-motion, `backdrop-filter` fallback, print rules. |

No other files are modified.

---

## Task 1: Create the landing CSS file with tokens and base reset

**Files:**
- Create: `epi_creator/static/css/landing.css`

- [ ] **Step 1: Create the file with tokens, scoped reset, and base typography**

Write the following to `epi_creator/static/css/landing.css`:

```css
:root {
  --bg-base: #0b1020;
  --bg-stop-1: #0b1020;
  --bg-stop-2: #1a1140;
  --bg-stop-3: #2a0e4a;
  --ink: #f4f6ff;
  --ink-dim: rgba(244, 246, 255, 0.78);
  --ink-faint: rgba(244, 246, 255, 0.55);
  --glass: rgba(255, 255, 255, 0.08);
  --glass-strong: rgba(255, 255, 255, 0.18);
  --glass-border: rgba(255, 255, 255, 0.18);
  --accent-cyan: #7dd3fc;
  --accent-violet: #c4b5fd;
  --grad-text: linear-gradient(120deg, #ffffff 0%, #bae6fd 45%, #c4b5fd 100%);
  --radius-pill: 999px;
  --shadow-glow: 0 10px 30px rgba(124, 58, 237, 0.35), 0 2px 8px rgba(0, 0, 0, 0.25);
  --shadow-glow-hover: 0 14px 40px rgba(124, 58, 237, 0.5), 0 4px 14px rgba(0, 0, 0, 0.3);
  --ease: cubic-bezier(0.22, 1, 0.36, 1);
}

@property --angle {
  syntax: "<angle>";
  inherits: false;
  initial-value: 0deg;
}

body.landing {
  margin: 0;
  min-height: 100dvh;
  color: var(--ink);
  background-color: var(--bg-base);
  color-scheme: dark;
  font-family: -apple-system, BlinkMacSystemFont, "Segoe UI", Roboto, "Helvetica Neue", Arial, sans-serif;
  -webkit-font-smoothing: antialiased;
  -moz-osx-font-smoothing: grayscale;
  box-sizing: border-box;
}

body.landing *,
body.landing *::before,
body.landing *::after {
  box-sizing: border-box;
}
```

- [ ] **Step 2: Verify the file is syntactically valid CSS**

Run: `python -c "import re,sys; css=open('epi_creator/static/css/landing.css').read(); print('chars:', len(css)); print('braces balanced:', css.count('{')==css.count('}'))"`
Expected: prints `chars: <n>` and `braces balanced: True`.

- [ ] **Step 3: Commit**

```bash
git add epi_creator/static/css/landing.css
git commit -m "feat(landing): add landing.css base tokens and reset"
```

---

## Task 2: Add the background layer (gradient + conic mesh + orbs + vignette)

**Files:**
- Modify: `epi_creator/static/css/landing.css` (append)

- [ ] **Step 1: Append the background layer rules**

Append to `epi_creator/static/css/landing.css`:

```css
.bg-layer {
  position: fixed;
  inset: 0;
  z-index: -1;
  overflow: hidden;
  pointer-events: none;
  background:
    linear-gradient(135deg, var(--bg-stop-1) 0%, var(--bg-stop-2) 50%, var(--bg-stop-3) 100%);
}

.bg-layer::before {
  content: "";
  position: absolute;
  top: 50%;
  left: 50%;
  width: 140vmax;
  height: 140vmax;
  transform: translate(-50%, -50%) rotate(-12deg);
  background: conic-gradient(
    from var(--angle),
    rgba(125, 211, 252, 0.18) 0deg,
    rgba(196, 181, 253, 0.18) 90deg,
    rgba(244, 114, 182, 0.16) 180deg,
    rgba(125, 211, 252, 0.18) 270deg,
    rgba(125, 211, 252, 0.18) 360deg
  );
  -webkit-mask-image: radial-gradient(circle at center, black 0%, black 35%, transparent 70%);
          mask-image: radial-gradient(circle at center, black 0%, black 35%, transparent 70%);
  filter: blur(40px);
  opacity: 0.85;
  animation: mesh-rotate 30s linear infinite;
}

.bg-layer .vignette {
  position: absolute;
  inset: 0;
  background: radial-gradient(ellipse at center, transparent 45%, rgba(0, 0, 0, 0.55) 100%);
}

.orb {
  position: absolute;
  border-radius: 50%;
  filter: blur(80px);
  opacity: 0.55;
  mix-blend-mode: screen;
  will-change: transform;
}

.orb--1 {
  top: 10%;
  left: 8%;
  width: 420px;
  height: 420px;
  background: radial-gradient(circle, #7dd3fc 0%, transparent 70%);
  animation: drift-1 26s var(--ease) infinite;
}

.orb--2 {
  top: 55%;
  right: 6%;
  width: 500px;
  height: 500px;
  background: radial-gradient(circle, #c4b5fd 0%, transparent 70%);
  animation: drift-2 34s var(--ease) infinite;
}

.orb--3 {
  bottom: 5%;
  left: 30%;
  width: 360px;
  height: 360px;
  background: radial-gradient(circle, #f472b6 0%, transparent 70%);
  animation: drift-3 18s var(--ease) infinite;
}

@keyframes mesh-rotate {
  to { --angle: 360deg; }
}

@keyframes drift-1 {
  0%, 100% { transform: translate(0, 0); }
  50%      { transform: translate(60px, 40px); }
}

@keyframes drift-2 {
  0%, 100% { transform: translate(0, 0); }
  50%      { transform: translate(-50px, -60px); }
}

@keyframes drift-3 {
  0%, 100% { transform: translate(0, 0); }
  50%      { transform: translate(40px, -50px); }
}
```

- [ ] **Step 2: Verify braces still balance**

Run: `python -c "css=open('epi_creator/static/css/landing.css').read(); print('braces balanced:', css.count('{')==css.count('}'))"`
Expected: `braces balanced: True`.

- [ ] **Step 3: Commit**

```bash
git add epi_creator/static/css/landing.css
git commit -m "feat(landing): add animated background layer and orbs"
```

---

## Task 3: Add the hero, typography, and eyebrow

**Files:**
- Modify: `epi_creator/static/css/landing.css` (append)

- [ ] **Step 1: Append hero and typography rules**

Append to `epi_creator/static/css/landing.css`:

```css
.hero {
  position: relative;
  min-height: 100dvh;
  display: grid;
  place-items: center;
  padding: clamp(24px, 5vw, 64px);
}

.hero__inner {
  width: 100%;
  max-width: 56ch;
  text-align: center;
}

.eyebrow {
  margin: 0 0 1rem;
  font-size: 0.78rem;
  font-weight: 600;
  letter-spacing: 0.18em;
  text-transform: uppercase;
  color: var(--ink-dim);
}

.title {
  margin: 0;
  font-size: clamp(2.5rem, 7vw, 4.5rem);
  font-weight: 800;
  line-height: 1.02;
  letter-spacing: -0.03em;
  background: var(--grad-text);
  -webkit-background-clip: text;
          background-clip: text;
  color: transparent;
  text-shadow: 0 2px 30px rgba(186, 230, 253, 0.15);
}

.lead {
  margin: 1.25rem auto 0.5rem;
  max-width: 38ch;
  font-size: clamp(1.05rem, 1.6vw, 1.2rem);
  line-height: 1.55;
  color: var(--ink);
}

.sub {
  margin: 0 auto;
  max-width: 46ch;
  font-size: 0.95rem;
  line-height: 1.55;
  color: var(--ink-dim);
}
```

- [ ] **Step 2: Verify braces still balance**

Run: `python -c "css=open('epi_creator/static/css/landing.css').read(); print('braces balanced:', css.count('{')==css.count('}'))"`
Expected: `braces balanced: True`.

- [ ] **Step 3: Commit**

```bash
git add epi_creator/static/css/landing.css
git commit -m "feat(landing): add hero layout and typography"
```

---

## Task 4: Add the glass CTA button and its hover/focus states

**Files:**
- Modify: `epi_creator/static/css/landing.css` (append)

- [ ] **Step 1: Append CTA rules**

Append to `epi_creator/static/css/landing.css`:

```css
.cta-form {
  margin: 2.25rem 0 1.5rem;
}

.cta {
  display: inline-flex;
  align-items: center;
  gap: 0.5em;
  padding: 0.95em 1.6em;
  font: inherit;
  font-size: 1.05rem;
  font-weight: 600;
  color: var(--ink);
  background: var(--glass);
  border: 1px solid var(--glass-border);
  border-radius: var(--radius-pill);
  cursor: pointer;
  box-shadow: var(--shadow-glow);
  -webkit-backdrop-filter: blur(14px) saturate(140%);
          backdrop-filter: blur(14px) saturate(140%);
  transition:
    transform 200ms var(--ease),
    background-color 200ms var(--ease),
    box-shadow 200ms var(--ease);
}

.cta__arrow {
  display: inline-block;
  transition: transform 200ms var(--ease);
}

.cta:hover {
  background: var(--glass-strong);
  transform: translateY(-2px);
  box-shadow: var(--shadow-glow-hover);
}

.cta:hover .cta__arrow {
  transform: translateX(4px);
}

.cta:active {
  transform: translateY(0);
}

.cta:focus-visible {
  outline: 2px solid var(--accent-cyan);
  outline-offset: 4px;
}

@media (max-width: 480px) {
  .cta {
    width: 100%;
    max-width: 320px;
    justify-content: center;
  }
}
```

- [ ] **Step 2: Verify braces still balance**

Run: `python -c "css=open('epi_creator/static/css/landing.css').read(); print('braces balanced:', css.count('{')==css.count('}'))"`
Expected: `braces balanced: True`.

- [ ] **Step 3: Commit**

```bash
git add epi_creator/static/css/landing.css
git commit -m "feat(landing): add glass CTA with hover and focus states"
```

---

## Task 5: Add the footer links (FAQ / FHIR / Gravitate)

**Files:**
- Modify: `epi_creator/static/css/landing.css` (append)

- [ ] **Step 1: Append link rules**

Append to `epi_creator/static/css/landing.css`:

```css
.links {
  display: flex;
  flex-wrap: wrap;
  justify-content: center;
  align-items: center;
  gap: 0.25rem 0.4rem;
  margin-top: 0.5rem;
}

.links a {
  color: var(--ink-faint);
  text-decoration: none;
  font-size: 0.9rem;
  padding: 0.25rem 0.4rem;
  border-radius: 6px;
  transition: color 200ms var(--ease);
}

.links a:hover,
.links a:focus-visible {
  color: var(--ink);
  text-decoration: underline;
  text-underline-offset: 4px;
}

.links a:focus-visible {
  outline: 2px solid var(--accent-cyan);
  outline-offset: 2px;
}

.dot {
  color: var(--ink-faint);
  user-select: none;
}
```

- [ ] **Step 2: Verify braces still balance**

Run: `python -c "css=open('epi_creator/static/css/landing.css').read(); print('braces balanced:', css.count('{')==css.count('}'))"`
Expected: `braces balanced: True`.

- [ ] **Step 3: Commit**

```bash
git add epi_creator/static/css/landing.css
git commit -m "feat(landing): add footer link styles"
```

---

## Task 6: Add reduced-motion, `backdrop-filter` fallback, and print rules

**Files:**
- Modify: `epi_creator/static/css/landing.css` (append)

- [ ] **Step 1: Append a11y/print/feature-query rules**

Append to `epi_creator/static/css/landing.css`:

```css
@supports not ((backdrop-filter: blur(1px)) or (-webkit-backdrop-filter: blur(1px))) {
  .cta {
    background: var(--glass-strong);
  }
}

@media (prefers-reduced-motion: reduce) {
  .bg-layer::before,
  .orb--1,
  .orb--2,
  .orb--3,
  .cta,
  .cta__arrow {
    animation: none !important;
    transition: none !important;
  }

  .cta:hover {
    transform: none;
  }

  .cta:hover .cta__arrow {
    transform: none;
  }
}

@media print {
  body.landing {
    background: #ffffff;
    color: #000000;
  }

  .bg-layer,
  .cta {
    display: none;
  }
}
```

- [ ] **Step 2: Verify braces still balance**

Run: `python -c "css=open('epi_creator/static/css/landing.css').read(); print('braces balanced:', css.count('{')==css.count('}'))"`
Expected: `braces balanced: True`.

- [ ] **Step 3: Commit**

```bash
git add epi_creator/static/css/landing.css
git commit -m "feat(landing): add a11y, print, and backdrop-filter fallbacks"
```

---

## Task 7: Rewrite `index.html` to use the new design

**Files:**
- Modify: `epi_creator/templates/index.html` (full rewrite)

- [ ] **Step 1: Replace the file contents**

Write the following to `epi_creator/templates/index.html`:

```html
<!DOCTYPE html>
<html lang="en">
<head>
  <meta charset="utf-8">
  <meta name="viewport" content="width=device-width, initial-scale=1">
  <title>ePI Creator</title>
  <link rel="stylesheet" href="{{ url_for('static', filename='css/landing.css') }}">
</head>
<body class="landing">
  <div class="bg-layer" aria-hidden="true">
    <span class="orb orb--1"></span>
    <span class="orb orb--2"></span>
    <span class="orb orb--3"></span>
    <span class="vignette"></span>
  </div>

  <main class="hero">
    <div class="hero__inner">
      <p class="eyebrow">HL7 &middot; Gravitate Health</p>
      <h1 class="title">ePI Creator</h1>
      <p class="lead">Create FHIR ePI resources using a guided step-by-step wizard. No Excel required.</p>
      <p class="sub">Fill in the forms across 11 steps to generate a complete FHIR package with FSH and JSON resources.</p>

      <form method="post" action="{{ url_for('gh_epi_creator.wizard_new') }}" class="cta-form">
        <input type="hidden" name="csrf_token" value="{{ csrf_token() }}">
        <button type="submit" class="cta">Start Wizard <span class="cta__arrow" aria-hidden="true">&rarr;</span></button>
      </form>

      <nav class="links" aria-label="Related resources">
        <a href="{{ url_for('gh_epi_creator.faq') }}">FAQ &amp; Resource Relationships</a>
        <span class="dot" aria-hidden="true">&middot;</span>
        <a href="http://build.fhir.org/ig/HL7/emedicinal-product-info/artifacts.html">FHIR Profiles</a>
        <span class="dot" aria-hidden="true">&middot;</span>
        <a href="http://build.fhir.org/ig/hl7-eu/gravitate-health/">Gravitate Health IG</a>
      </nav>
    </div>
  </main>
</body>
</html>
```

- [ ] **Step 2: Verify no Bootstrap references remain**

Run: `grep -c "bootstrap" epi_creator/templates/index.html || true`
Expected: `0`.

Run: `grep -c "main.css" epi_creator/templates/index.html || true`
Expected: `0`.

- [ ] **Step 3: Verify Jinja tags are well-formed**

Run: `python -c "import jinja2; jinja2.Environment().parse(open('epi_creator/templates/index.html').read()); print('jinja ok')"`
Expected: `jinja ok`. (If `jinja2` is unavailable in the project venv, run with the project venv's Python: `.venv/bin/python -c "import jinja2; ..."`.)

- [ ] **Step 4: Commit**

```bash
git add epi_creator/templates/index.html
git commit -m "feat(landing): rewrite index.html with gradient hero and glass CTA"
```

---

## Task 8: Manual smoke test — render and verify the page

**Files:** none (verification only)

- [ ] **Step 1: Start the dev server in the background**

Run: `.venv/bin/python run.py` (or `python run.py` if venv is active).
Expected: server logs "Starting GH EPI Creator app" and listens on `http://127.0.0.1:5000`. Keep the process running for the next steps.

- [ ] **Step 2: Fetch the landing page and verify HTTP 200**

Run: `curl -sS -o /tmp/landing.html -w "%{http_code}\n" http://127.0.0.1:5000/gh-epi-creator/`
Expected: `200`.

- [ ] **Step 3: Verify expected markup is present**

Run:
```bash
grep -c 'class="landing"' /tmp/landing.html
grep -c 'bg-layer' /tmp/landing.html
grep -c 'class="cta"' /tmp/landing.html
grep -c 'csrf_token' /tmp/landing.html
grep -c 'wizard_new' /tmp/landing.html
grep -c 'landing.css' /tmp/landing.html
```
Expected: `1` for each.

Run: `grep -c -i "bootstrap" /tmp/landing.html || true`
Expected: `0`.

- [ ] **Step 4: Verify the wizard flow still works (CSRF + redirect)**

Run: `curl -sS -c /tmp/cookies.txt -o /dev/null http://127.0.0.1:5000/gh-epi-creator/`
Then extract the CSRF token from the rendered page:
```bash
TOKEN=$(grep -oE 'name="csrf_token"[^>]*value="[^"]+"' /tmp/landing.html | head -1 | sed -E 's/.*value="([^"]+)".*/\1/')
echo "token length: ${#TOKEN}"
```
Expected: a non-empty token.

Then POST to start the wizard:
```bash
curl -sS -b /tmp/cookies.txt -L -o /tmp/wizard.html -w "%{http_code} %{url_effective}\n" \
  -X POST -d "csrf_token=$TOKEN" \
  http://127.0.0.1:5000/gh-epi-creator/wizard/new
```
Expected: a `200` final response and the URL ending in `/wizard/organization` (the first step).

- [ ] **Step 5: Open the page in a browser and confirm the visuals**

Open `http://127.0.0.1:5000/gh-epi-creator/` in Chrome and verify:
- Dark gradient background with soft, drifting color.
- Large gradient-text "ePI Creator" centered.
- Lead and sub text readable in white/translucent white.
- "Start Wizard →" pill button has a glass effect; hover lifts and brightens; focus ring visible when tabbed.
- Three footer links (FAQ · FHIR Profiles · Gravitate Health IG) with hover underline.
- Tab order: CTA → FAQ → FHIR Profiles → Gravitate Health IG.

- [ ] **Step 6: Verify reduced-motion behavior**

In DevTools → Rendering → "Emulate CSS media feature prefers-reduced-motion: reduce", reload the page. Expected: no orb drift, no conic rotation, no CTA hover translate (color change only). Then disable the emulation and confirm motion returns.

- [ ] **Step 7: Stop the dev server**

Stop the `run.py` process started in step 1 (Ctrl-C in its terminal, or `kill <pid>`).

- [ ] **Step 8: Final commit if any cleanup was made**

If you made any cleanup edits during smoke testing, commit them now. Otherwise, no commit is needed.

```bash
git status
```

---

## Self-Review

**1. Spec coverage:**
- Goal (modern gradient/glass hero) → Tasks 1–7, 8.
- Preserve all existing content → Task 7 keeps title, lead, sub, CTA, three links.
- No JS, no images, no new Python → Tasks 1–7 only touch the two allowed files.
- Bootstrap dropped from this page → Task 7 step 2 verifies zero `bootstrap` references.
- `body.landing` scoping → Tasks 1, 7.
- Eyebrow / title / lead / sub / CTA / links DOM → Task 7.
- Tokens / background / hero / CTA / links CSS → Tasks 1, 2, 3, 4, 5.
- `prefers-reduced-motion` → Task 6.
- `backdrop-filter` fallback → Task 6.
- Print rules → Task 6.
- Responsive (`<480px` CTA) → Task 4.
- No new automated tests → documented decision in spec; Task 8 covers manual verification.
- Wizard flow unaffected → Task 8 step 4.

**2. Placeholder scan:** No TBDs, no "implement later", no "similar to". Every CSS block is included verbatim.

**3. Type / name consistency:**
- Class names used in CSS and HTML match exactly: `landing`, `bg-layer`, `orb`, `orb--1/2/3`, `vignette`, `hero`, `hero__inner`, `eyebrow`, `title`, `lead`, `sub`, `cta-form`, `cta`, `cta__arrow`, `links`, `dot`.
- Custom property names match between `:root` and consumers (`--bg-base`, `--glass`, `--glass-border`, `--ink`, `--ink-dim`, `--ink-faint`, `--grad-text`, `--radius-pill`, `--shadow-glow`, `--shadow-glow-hover`, `--ease`, `--accent-cyan`, `--glass-strong`).
- `--glass-strong` is added in Task 1 and consumed in Task 4 (hover) and Task 6 (fallback). Consistent.
- The `--angle` custom property is registered via `@property` in Task 1 and animated in Task 2. Consistent.

No issues found.
