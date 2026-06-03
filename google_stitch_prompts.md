# Google Stitch — Prompt Pack
### Full-stack developer portfolio · dark, developer-y, bold + clean

> **How to use this:** Stitch produces its best work *one screen at a time*, not from a single mega-prompt.
> 1. Open Stitch → choose **Web** medium → pick the **Thinking / Gemini Pro** model for quality.
> 2. Paste **PROMPT 0 (Style System)** first to set the project direction.
> 3. Then paste each screen prompt (1–6) one at a time. Generate the **desktop** version, then add the mobile line at the bottom of each to get the responsive variant.
> 4. Refine with small, single-change follow-ups (e.g. *"make the hero headline 1.5× larger"*) — never "make it better."

---

## PROMPT 0 — Style System (paste first)

```
Design a personal portfolio website for a freelance full-stack web developer. The brand is confident, modern and "developer-y" — a blend of bold-and-creative with clean-and-corporate.

GLOBAL STYLE (apply to every screen):
- Theme: dark by default. Background near-black charcoal (#0A0A0B), elevated surfaces #16161A, hairline borders at 8% white.
- Single bold accent: electric lime-green (#C2F94A). Use it sparingly — for the primary CTA, active states, links, and one highlighted word per heading. Everything else is warm off-white text (#F4F3EE) on dark.
- Typography: a characterful geometric display font for headings (heavy, tight letter-spacing) paired with a clean grotesque for body text. Use a monospace font (JetBrains Mono style) for labels, nav items, numbers, tags and small captions to give a subtle "code" feel.
- Code-aesthetic accents: numbered nav items (01, 02…), monospace section labels like "// about", a faint background grid, a small blinking terminal cursor in the hero headline, "available" status dot.
- Layout: generous spacing, strong typographic hierarchy, max content width ~1180px, rounded corners ~14px, 1px hairline borders rather than heavy shadows.
- Tone of imagery: realistic and understated, NOT glossy AI render. See IMAGE RULES below.
- Include a light/dark theme toggle in the top nav.

IMAGE RULES (important — avoid the "AI-generated" look):
- Use natural, candid, documentary-style photography with realistic lighting and grain — like a real DSLR photo, not a hyper-smooth render.
- Headshot: a real-looking developer at a desk, neutral expression, soft natural window light, muted colours, slight film grain. No plastic skin, no exaggerated bokeh, no glowing neon.
- Project visuals: prefer clean UI screenshots / browser mockups over stock photos.
- Avoid: oversaturated gradients, futuristic "AI" blue glow, fake people with too-perfect faces, glossy 3D blobs.

Navigation (sticky top bar on every page): logo "jordan.dev" with a lime status dot · links Home / About / Work / Services / Blog · theme toggle · lime "Hire me" button. Mobile: collapse links into a full-screen hamburger drawer.
```

---

## PROMPT 1 — Home / Hero

```
Generate the HOME / hero screen using the established style system.

- Sticky nav as defined.
- A small pill near the top: a pulsing lime dot + monospace text "Available for new projects · 1–2 spots open".
- Huge display headline (clamp ~48–92px): "I build reliable web products" with the word "reliable" in lime, and a blinking lime terminal cursor after the last word.
- Sub-headline in muted grey, max ~560px: "Full-stack developer helping startups and small teams ship — from greenfield builds to legacy rescue. Four years delivering production-grade software across the stack."
- Two buttons side by side: lime filled "Hire me →" and outlined "View work".
- A row of 4 stats below: "4 years shipping", "30+ projects delivered", "12+ happy clients", "99% uptime shipped".
- A faint radial lime glow behind the headline and a subtle background grid.
- At the very bottom, an infinite horizontal marquee strip of monospace tech keywords: React · Next.js · TypeScript · Node.js · PostgreSQL · GraphQL · Available for hire.

Also generate the mobile version: stack everything in a single column, hamburger menu, headline ~40px, stats in a 2×2 grid.
```

---

## PROMPT 2 — About

```
Generate the ABOUT screen using the style system.

- Monospace eyebrow label "// 02 — about".
- Two-column layout. LEFT (narrower): a portrait headshot in a 4:5 rounded frame with a 1px border (follow the IMAGE RULES — realistic, natural light, film grain, not an AI render). Below it, a minimal vertical timeline: "2024→ Freelance Full-Stack Dev", "2022 Senior Frontend Engineer · Fintech startup", "2020 Full-Stack Developer · Digital agency", each year in lime monospace.
- RIGHT (wider): display heading "A developer who handles both sides of the stack." Then 2–3 short body paragraphs about 4 years of experience, working end-to-end from database schema to polished UI, and rescuing legacy codebases. Bold a few key phrases in off-white.
- A monospace label "// core stack" followed by a wrap of pill tags: React, Next.js, TypeScript, Node.js, PostgreSQL, GraphQL, Tailwind, Prisma, Docker, AWS, Vercel. Tags glow lime on hover.
- Two buttons: lime "↓ Download CV" and outlined "Get in touch".

Mobile version: single column, headshot first, then text, tags wrap naturally.
```

---

## PROMPT 3 — Portfolio / Work

```
Generate the WORK / portfolio screen using the style system.

- Eyebrow "// 03 — selected work", display heading "Things I've shipped", muted subline.
- A row of monospace filter chips: All (active, lime filled), Web apps, APIs & backend, Tools. Active chip is lime; others outlined.
- A 2-column grid of project cards. Each card has:
  • a top "visual" area styled as a mini browser-window mockup (traffic-light dots, a lime UI block and skeleton content lines) — NOT a stock photo;
  • a monospace category label in lime (e.g. "Web app");
  • a bold project title;
  • a 1–2 line description;
  • a row of small monospace tech tags;
  • two monospace links: "↗ Live demo" and "</> GitHub".
- Sample projects: Ledgerly (real-time finance dashboard), PayBridge (unified payments API), Roomly (co-working booking platform), envcheck (config-validation dev tool), Notifyd (multi-channel notification service), Schema Viz (Prisma schema → ER diagram tool).
- Cards lift slightly on hover.

Mobile version: single-column cards, filter chips scroll horizontally.
```

---

## PROMPT 4 — Services

```
Generate the SERVICES screen using the style system.

- Eyebrow "// 04 — services", heading "What I can build for you", subline about helping startups ship reliable web products.
- THREE service cards in a row, each with a monospace "/ 01" number, a title, a short paragraph, and a lime monospace mini stack list:
  1) Web app development — end-to-end build, database schema to polished UI. Stack: React / Next.js, Node.js, PostgreSQL, TypeScript.
  2) API & backend development — REST/GraphQL APIs, auth, integrations, background jobs. Stack: REST / GraphQL, Auth & JWT, Integrations, Serverless.
  3) Code review & audits — performance, security, tech-debt review with a prioritised plan. Stack: Security, Performance, Architecture, Debt mapping.
- Below, a "Packages" section: three pricing cards.
  • AUDIT — £750 flat fee — security & performance review, written report with priorities, 60-min debrief call, delivered in 5 working days.
  • BUILD — £3,500 per project — highlighted/featured card with a lime "★ Most popular" badge — full-stack design & development, up to 6 weeks scope, weekly progress updates, deployment + handover docs, 14 days post-launch support.
  • CUSTOM — "Let's talk" — flexible engagement, retainer or milestone billing, team collaboration welcome, NDA on request.
  Each list item uses a lime "→" bullet. Each card has a CTA button (the featured one lime-filled).
- Bottom: a "How it works" 4-step row: 01 Discovery call, 02 Scoping, 03 Build, 04 Handover, each with a short description, separated by a top hairline.

Mobile version: cards stack vertically; the featured BUILD card moves to the top; steps stack in one column.
```

---

## PROMPT 5 — Blog

```
Generate the BLOG screen using the style system.

- Eyebrow "// 05 — writing", heading "Notes from the build", muted subline "Short posts on projects, opinions, and things I learn shipping software."
- A clean list (not cards) of posts separated by hairline rules. Each row: a monospace date on the left, the post title (large) with a small lime monospace category tag beneath it, and an "↗" arrow on the right. On hover the row indents slightly and the title turns lime.
- Sample posts:
  • May 2026 · Architecture — "Why I stopped reaching for microservices"
  • Apr 2026 · TypeScript — "Type-safe APIs end to end without the ceremony"
  • Mar 2026 · Career — "What 4 years of freelancing taught me about scope"
- Also generate a single article-reading layout: a back link, large title, monospace meta line (date · tag · 4 min read), comfortable ~720px reading column, with a styled monospace code block using the lime accent.

Mobile version: date stacks above the title; comfortable single-column reading view.
```

---

## PROMPT 6 — Contact

```
Generate the CONTACT screen using the style system.

- Eyebrow "// 06 — contact". Two columns.
- LEFT: big display heading "Ready to start a project?", a short paragraph "I typically have 1–2 spots open per month. Get in touch early.", then three contact method rows, each a bordered pill that slides right on hover with a small square monospace icon:
  • "Book a call — 30-min discovery call →"
  • "LinkedIn — Connect →"
  • "Email — you@example.com"
- RIGHT: a contact form in a bordered card with monospace field labels: Name, Email, Project type, Message (textarea), and a lime "Send message →" button. Inputs have dark fields with a lime focus border. Show an inline success state ("✓ Message sent") after submit.

Mobile version: single column, form below the contact methods.
```

---

## Refinement follow-ups (use one at a time)
- "Make the hero headline larger and tighten the letter-spacing."
- "The lime is being overused — limit it to the primary button, active nav item, and one highlighted word per heading."
- "Replace the project card photos with browser-window UI mockups instead of stock imagery."
- "Make the headshot look like a natural DSLR photo with soft window light and slight grain — less polished, less AI."
- "Add more vertical spacing between sections so it breathes."

## Export
Stitch exports **HTML + Tailwind CSS** (you can't pick the stack). To match your brief's Next.js / TypeScript / Framer Motion stack, treat the Stitch output as the **visual reference**, then port the markup into your Next.js components — or hand the exported HTML to a coding agent to convert.
