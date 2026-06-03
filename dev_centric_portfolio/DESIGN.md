---
name: Dev-Centric Portfolio
colors:
  surface: '#131314'
  surface-dim: '#131314'
  surface-bright: '#3a393a'
  surface-container-lowest: '#0e0e0f'
  surface-container-low: '#1c1b1c'
  surface-container: '#201f20'
  surface-container-high: '#2a2a2b'
  surface-container-highest: '#353436'
  on-surface: '#e5e2e3'
  on-surface-variant: '#c3c9b0'
  inverse-surface: '#e5e2e3'
  inverse-on-surface: '#313031'
  outline: '#8d937c'
  outline-variant: '#434935'
  surface-tint: '#a3d728'
  primary: '#ffffff'
  on-primary: '#253600'
  primary-container: '#bef446'
  on-primary-container: '#506e00'
  inverse-primary: '#4b6700'
  secondary: '#c8c5cb'
  on-secondary: '#303034'
  secondary-container: '#47464b'
  on-secondary-container: '#b6b4ba'
  tertiary: '#ffffff'
  on-tertiary: '#30302e'
  tertiary-container: '#e5e2df'
  on-tertiary-container: '#656462'
  error: '#ffb4ab'
  on-error: '#690005'
  error-container: '#93000a'
  on-error-container: '#ffdad6'
  primary-fixed: '#bef446'
  primary-fixed-dim: '#a3d728'
  on-primary-fixed: '#141f00'
  on-primary-fixed-variant: '#374e00'
  secondary-fixed: '#e4e1e7'
  secondary-fixed-dim: '#c8c5cb'
  on-secondary-fixed: '#1b1b1f'
  on-secondary-fixed-variant: '#47464b'
  tertiary-fixed: '#e5e2df'
  tertiary-fixed-dim: '#c8c6c3'
  on-tertiary-fixed: '#1b1c1a'
  on-tertiary-fixed-variant: '#474744'
  background: '#131314'
  on-background: '#e5e2e3'
  surface-variant: '#353436'
  text-primary: '#F4F3EE'
  text-muted: '#A1A1AA'
  border-hairline: rgba(255, 255, 255, 0.08)
  terminal-cursor: '#C2F94A'
typography:
  display-xl:
    fontFamily: Epilogue
    fontSize: 92px
    fontWeight: '800'
    lineHeight: '1.0'
    letterSpacing: -0.04em
  display-xl-mobile:
    fontFamily: Epilogue
    fontSize: 48px
    fontWeight: '800'
    lineHeight: '1.1'
    letterSpacing: -0.02em
  headline-lg:
    fontFamily: Epilogue
    fontSize: 48px
    fontWeight: '700'
    lineHeight: '1.2'
    letterSpacing: -0.02em
  body-md:
    fontFamily: Hanken Grotesk
    fontSize: 16px
    fontWeight: '400'
    lineHeight: '1.6'
  body-sm:
    fontFamily: Hanken Grotesk
    fontSize: 14px
    fontWeight: '400'
    lineHeight: '1.5'
  label-mono:
    fontFamily: JetBrains Mono
    fontSize: 12px
    fontWeight: '500'
    lineHeight: '1.0'
    letterSpacing: 0.05em
  label-code:
    fontFamily: JetBrains Mono
    fontSize: 13px
    fontWeight: '400'
    lineHeight: '1.4'
rounded:
  sm: 0.25rem
  DEFAULT: 0.5rem
  md: 0.75rem
  lg: 1rem
  xl: 1.5rem
  full: 9999px
spacing:
  max-width: 1180px
  section-gap: 8rem
  component-gap: 2rem
  grid-gutter: 1.5rem
  card-padding: 2rem
---

## Brand & Style

The brand personality is authoritative, technical, and hyper-transparent, designed to evoke the feeling of a high-performance terminal or an IDE. It balances the "developer-y" aesthetic of code-inspired interfaces with the professional polish of a premium digital agency. The target audience—startup founders and technical leads—should perceive a developer who is methodical, reliable, and deeply embedded in their craft.

The design style is a hybrid of **Modern Minimalism** and **Technical Brutalism**. It utilizes a "Utility-First" visual language characterized by:
- **Hairline Precision:** Using 1px borders at low opacity to define structure instead of shadows.
- **Data Density:** High information density balanced by generous section margins.
- **Monospace Accents:** Using code-inspired markers (`//`, `01`, `const`) to signpost information.
- **Atmospheric Depth:** A "Lights Out" theme using charcoal and deep slate to create a focused, low-strain environment.
- **Documentary Realism:** Avoiding the "uncanny valley" of AI by using photography with natural grain, soft light, and realistic UI mockups.

## Colors

The palette is anchored in a "Deep Charcoal" ecosystem to provide maximum contrast for the Electric Lime-Green accent. 

- **Primary (#C2F94A):** Reserved strictly for action-oriented elements: CTAs, active navigation states, terminal cursors, and single-word typographic highlights. 
- **Neutral/Background (#0A0A0B):** The base canvas.
- **Elevated Surfaces (#16161A):** Used for cards and input fields to create subtle separation from the background without relying on shadows.
- **Text Strategy:** High-contrast off-white (#F4F3EE) for primary reading, and a muted slate (#A1A1AA) for metadata, labels, and secondary descriptions.

## Typography

The typographic system is a three-tiered hierarchy designed for technical storytelling:

1.  **Display (Epilogue):** Used for large impact headlines. It should be set with tight tracking and heavy weights to feel architectural and bold.
2.  **Interface/Body (Hanken Grotesk):** A clean, modern grotesque that ensures high readability for long-form service descriptions and blog content.
3.  **Utility (JetBrains Mono):** The "Code Layer." Used for all navigational markers, category tags, numbers, and technical specs. It should feel like it was pulled directly from a text editor.

Always prefix section headers with `//` and use numeric prefixes for list items (e.g., `01`, `02`) in the monospace face to reinforce the developer-centric theme.

## Layout & Spacing

The layout follows a **Fixed Grid** model with a maximum content width of 1180px. 

- **The Grid:** A 12-column system is used for desktop. A faint, low-opacity background grid (1px lines every 40px) can be used in hero sections to reinforce the "blueprint" aesthetic.
- **Sectioning:** Large vertical gaps (8rem / 128px) separate major content blocks to provide "breathing room" and allow the bold typography to stand out.
- **Responsive Behavior:** 
    - **Desktop:** Multi-column layouts (e.g., 2-column About, 2-column Work cards).
    - **Tablet:** Reduction to 1-column for text-heavy sections; 2-column for project grids.
    - **Mobile:** 1-column stack. Margins reduce to 1.25rem. Section gaps reduce to 4rem.

## Elevation & Depth

This system avoids traditional shadows in favor of **Tonal Layering** and **Hairline Outlines**.

- **Surface Levels:** 
    - Base: `#0A0A0B` (Canvas)
    - Surface: `#16161A` (Cards, Modals, Inputs)
- **Dividers:** Use 1px hairline borders (`border-hairline`). For cards, use a solid 1px border. For section dividers, use a horizontal rule that spans the grid width.
- **Interactive Depth:** On hover, cards should not lift with shadows. Instead, use a subtle border color shift (e.g., from 8% white to 20% white) or a slight translation (Y-axis -4px).
- **Glassmorphism:** Reserved only for the sticky navigation bar, using a high-blur (20px) backdrop filter with a semi-transparent background to maintain legibility over scrolling content.

## Shapes

The shape language is "Soft-Tech"—predominantly geometric but with enough radius to feel modern and accessible.

- **Cards & Primary Blocks:** 14px (`rounded-lg`) is the standard for containers.
- **Tags & Pills:** Use 99px (full pill) for category tags and tech-stack labels.
- **Inputs:** Match the card radius (14px) for consistency.
- **Buttons:** 12px-14px radius. Avoid sharp corners to contrast against the rigid grid layout.

## Components

### Buttons
- **Primary:** Filled Electric Lime (#C2F94A) with Black text (#000000). Bold weight. No shadow.
- **Secondary/Ghost:** 1px hairline border in White (15% opacity). Transitions to a solid border on hover.
- **Iconography:** Use a monospace arrow (→) or chevron.

### Cards (Project/Service)
- **Background:** `#16161A`.
- **Border:** 1px `border-hairline`.
- **Structure:** Top area features a "Browser Mockup" (grey bar with three window control dots) containing the project visual.
- **Hover:** The border color brightens, and any primary links inside transition to the accent color.

### Form Fields
- **Background:** Same as elevated surfaces (#16161A).
- **Labels:** Monospace, uppercase, small font size.
- **Focus State:** 1px solid border in Electric Lime. No glow.

### Status Indicator
- A small, pulsing circle in Electric Lime, paired with monospace text (e.g., "• AVAILABLE FOR HIRE").

### Tags/Chips
- Small, uppercase monospace text.
- Outlined with 1px hairline for neutral tags.
- Solid background for active/featured tags.