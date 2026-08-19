# ROUTEZERO Web Platform

Official website for **ROUTEZERO (루트제로)** — Applied Intelligence, Design Automation & Studio Engineering.

Built with a high-craft **White & Emerald Green Editorial Split System** (inspired by `hand-axe.com`), zero-bloat vanilla frontend architecture, adaptive responsive mobile navigation, Google Analytics (GA4) telemetry, and edge-ready Vercel configuration.

---

## Features

- **White & Emerald Editorial Design System**: Crisp typography grid (`#FFFFFF` / `#FAFAFB`), obsidian text (`#0F172A`), emerald green accents (`#059669` / `#10B981`), and subtle hairline borders.
- **Adaptive Responsive Architecture**:
  - **Desktop (≥ 1024px)**: 2-Column Split System with sticky brand lockup, active section indicator lines, direct social links, and quick-copy contact badge.
  - **Mobile / Tablet (< 1024px)**: Single column with a sticky blurred chip navigation track (`backdrop-filter: blur(12px)`) and synchronized scroll-spy.
- **Core Sections**:
  - **Design & Automation**: Editorial grid & layout systems, creative scripting (Adobe UXP/CLI), and automated typography pipelines.
  - **Archive**: Structured, responsive systems and project history table with live status badges.
  - **About Routezero**: Studio vision, philosophy, and engineering approach.
- **Studio Footer**: Live Seoul (KST) real-time clock, location metadata, quick links, and smooth back-to-top trigger.
- **Google Analytics 4 (GA4)**: Built-in `gtag.js` script (`G-TTVJZ0V80C`) with section scroll-spy tracking, outbound link telemetry, and email copy event tracking.
- **Vercel Edge Ready**: `vercel.json` pre-configured with clean URLs, immutable asset caching, and security headers.

---

## File Structure

```
Routezero/
├── index.html          # Main HTML document with SEO, OpenGraph & GA4 tags
├── styles/
│   └── main.css        # Design tokens, grid layout, fluid typography & media queries
├── scripts/
│   └── app.js          # Scroll-spy, KST live clock, clipboard toast, GA4 events
├── assets/
│   ├── logo.svg        # Routezero vector logo & wordmark
│   ├── favicon.svg     # Modern SVG favicon
│   └── routezero_*.png # Studio branding assets
├── vercel.json         # Vercel deployment configuration
└── README.md
```

---

## Local Development

You can run the project locally with any static web server:

```bash
# Option 1: Python 3 built-in server
python3 -m http.server 3000

# Option 2: Node.js npx serve
npx serve .
```

Open `http://localhost:3000` in your browser.

---

## Vercel Deployment

Deploy directly using the Vercel CLI:

```bash
# Preview deployment
vercel

# Production deployment
vercel --prod
```

Or connect the repository to your [Vercel Dashboard](https://vercel.com).
