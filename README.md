# ROUTEZERO Web Platform

Official website for **ROUTEZERO (루트제로)** — Applied Intelligence, Systems & Digital Ventures.

Built with a high-craft **White Editorial 2-Column Split System** (inspired by `hand-axe.com`), zero-bloat vanilla frontend architecture, Google Analytics (GA4) telemetry, and edge-ready Vercel configuration.

---

## Features

- **White Editorial Design System**: Crisp white typography grid (`#FFFFFF` / `#FAFAFB`), obsidian text, electric cobalt accents, and ultra-fine hairline borders.
- **Hand-Axe 2-Column Architecture**:
  - **Left Panel (40%)**: Sticky brand lockup, active section indicator lines, direct social links, and quick-copy contact badge.
  - **Right Panel (60%)**: Smooth-scrolling sections including Thesis, Ventures & Products, Capabilities Matrix, Architecture Table, Insights, and Contact.
- **Comprehensive Studio Footer**: Live Seoul (KST) real-time clock, system status indicator, quick links, business & legal metadata placeholder, and smooth back-to-top trigger.
- **Google Analytics 4 (GA4)**: Built-in `gtag.js` script with section scroll-spy tracking, venture outbound link tracking, and email copy event telemetry.
- **Vercel Edge Ready**: `vercel.json` pre-configured with clean URLs, immutable asset caching, and security headers.

---

## File Structure

```
Routezero/
├── index.html          # Main HTML document with SEO & GA4 tags
├── styles/
│   └── main.css        # Design tokens, grid layout, responsive breakpoints
├── scripts/
│   └── app.js          # Scroll-spy, KST live clock, clipboard toast, GA4 events
├── assets/
│   ├── logo.svg        # Routezero vector logo & wordmark
│   └── favicon.svg     # Modern SVG favicon
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

## Google Analytics (GA4) Configuration

In [index.html](file:///Users/daeyounglee/Projects/Routezero/index.html), locate the `G-XXXXXXXXXX` placeholder and replace it with your actual Google Analytics Measurement ID:

```html
<!-- Google Analytics 4 (GA4) -->
<script async src="https://www.googletagmanager.com/gtag/js?id=G-TTVJZ0V80C"></script>
<script>
  window.dataLayer = window.dataLayer || [];
  function gtag(){dataLayer.push(arguments);}
  gtag('js', new Date());
  gtag('config', 'G-TTVJZ0V80C');
</script>
```

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
