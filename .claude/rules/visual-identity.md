# PMP Visual Identity

> **Client overlay (PMP — Peinture et Métallisation sur Plastique).** This is
> the brand contract for any PMP web/UI surface: the single source of truth for
> color, typography, and styling. Auto-read when this rule is dropped into a PMP
> project's `.claude/rules/`. The matching tokens are in
> `clients/pmp/assets/theme.css` (a Tailwind v4 `@theme`). If a design question
> isn't answered here, ask before improvising.

Brand reference: the PMP public website (homepage hero + hero section). When PMP
issues an official brand guide (Pantone refs), those values supersede the hex
below — update this file and `theme.css` together.

---

## Brand voice in one paragraph

PMP's identity is **industrial luxury**: deep teal that signals expertise and
trust, gold that signals craftsmanship and value. The brand site uses cream
backgrounds to keep the palette warm rather than corporate-sterile, and
flowing gold curves to suggest motion and refinement. The dashboard inherits
this voice. It should feel like a serious professional instrument that
happens to be beautiful — not a beige enterprise tool, not a startup
playground.

**What this means in practice:**
- Generous whitespace, not Bloomberg-terminal density
- Numbers and data prominent (the QC responsable's job is reading numbers)
- Gold appears sparingly — when it shows up, it matters
- Teal is the everyday workhorse color
- French-first copy (the plant operates in French)

---

## Color palette

### Brand colors

| Token | Hex | HSL | Use |
|---|---|---|---|
| `brand` | `#1A5560` | `190 58% 24%` | Primary buttons, navigation, logo area, page headers |
| `brand-dark` | `#134349` | `188 59% 18%` | Hover/pressed state on `brand` |
| `brand-deep` | `#0E353C` | `190 61% 14%` | Watermarks, deep backgrounds (login splash only) |

The brand teal is the **default identity color**. When in doubt, use it.

### Accents

| Token | Hex | HSL | Use |
|---|---|---|---|
| `accent` | `#D4B765` | `42 53% 62%` | Focus rings, "next" CTAs, important highlights, decorative dividers |
| `accent-light` | `#E4CD8B` | `42 61% 72%` | Hover state on accent elements |

Gold is the **scarce resource**. A page with five gold elements has used it
wrong. A page with zero gold elements may have missed an opportunity. The
sweet spot is one or two — a focus ring on the active input, a "view more"
arrow, the active step in a wizard.

### Surfaces

| Token | Hex | HSL | Use |
|---|---|---|---|
| `cream` | `#FAEEE3` | `28 80% 95%` | Page background — warm, not white |
| `cream-subtle` | `#F5E8DC` | `28 76% 91%` | Alternating table rows, subtle section separators |
| `white` | `#FFFFFF` | `0 0% 100%` | Card surfaces, modals, dropdown panels |

Cream as the page background is non-negotiable. Pure white pages break the
brand connection.

### Semantic / status

Derived to harmonize with brand teal — not pulled from the brand site, which
doesn't need status colors.

| Token | Hex | HSL | Use |
|---|---|---|---|
| `success` | `#2E7D5B` | `153 46% 33%` | Device online, save succeeded, healthy status |
| `warning` | `#C89238` | `33 57% 50%` | Queue draining, degraded service, rate-limited |
| `danger` | `#B84545` | `0 46% 50%` | Device offline >5 min, failed operations |
| `info` | `#3E7B86` | `190 37% 39%` | Neutral notifications, informational badges |

Status colors are muted relative to their stereotypical web defaults. No
fire-engine reds. No alarm-clinic yellows. Plant-floor staff see these
constantly; tone them down.

### Text

| Token | Hex | HSL | Use |
|---|---|---|---|
| `ink-heading` | `#1A5560` | `190 58% 24%` | All headings (= brand teal) |
| `ink` | `#2D2D2D` | `0 0% 18%` | Body text on cream/white |
| `ink-inverse` | `#FAEEE3` | `28 80% 95%` | Body text on teal panels |
| `ink-muted` | `#6B6B6B` | `0 0% 42%` | Captions, timestamps, secondary metadata |

Headings always use the brand teal, never black. This single rule does more
brand-anchoring work than anything else.

---

## Typography

**Sans-serif (everywhere):** [Inter](https://rsms.me/inter/)

| Weight | Use |
|---|---|
| 400 (regular) | Body text |
| 500 (medium) | Emphasized body, table column headers, small labels |
| 600 (semibold) | UI section headings (h2, h3), button text |
| 700 (bold) | Page titles (h1), dashboard stat numbers |

**Monospace (data only):** [JetBrains Mono](https://www.jetbrains.com/lp/mono/)
or IBM Plex Mono as fallback.

Monospace is reserved for content where character alignment matters:
- Timestamps in log views (`2026-05-16 14:32:07`)
- Device IDs (`qc-stm32-001a2b3c`)
- Defect IDs, MQTT topics, configuration version hashes
- Any tabular numeric data where rows should align by digit position

Do **not** use monospace for general body text, never for headings, never to
look "technical." It's for alignment, period.

**No serifs anywhere.** The brand is unambiguously sans-serif and modern.

### Type scale

| Level | Tailwind | Size | Weight | Line height |
|---|---|---|---|---|
| Page title (h1) | `text-3xl` | 30px | 700 | 1.2 |
| Section (h2) | `text-2xl` | 24px | 600 | 1.3 |
| Subsection (h3) | `text-xl` | 20px | 600 | 1.4 |
| Card header (h4) | `text-lg` | 18px | 600 | 1.4 |
| Body | `text-base` | 16px | 400 | 1.6 |
| Small / caption | `text-sm` | 14px | 400 | 1.5 |
| Micro (timestamps) | `text-xs` | 12px | 400 | 1.4 |

Stat tiles (dashboard home) use `text-4xl` (36px) `font-bold` `tabular-nums`
for the big number, `text-sm` `text-ink-muted` for the label beneath.

---

## Spacing and layout

**Whitespace is part of the brand.** The PMP site breathes; the dashboard
should too.

Standard Tailwind scale. Use generously:
- Cards: `p-6` minimum for content, `p-8` for feature cards
- Sections: `space-y-6` or `space-y-8` between major blocks
- Lists/tables: `gap-4` between rows, never sub-`gap-2`
- Page margins: `px-6 md:px-8 lg:px-12`

**Grid:** 12-column on desktop (`lg:grid-cols-12`), with content typically
spanning 8 or 12. The hero of the brand site is roughly 5/12 text + 7/12
visual — a useful proportion to borrow for split-pane pages.

---

## Shapes and elevation

**Border radius:** medium throughout.
- Default (`rounded-lg`, 8px) for cards, inputs, buttons
- Smaller (`rounded`, 4px) for badges, chips, inline elements
- Pill (`rounded-full`) only for status dots and avatars
- Never `rounded-2xl` or higher — too playful for the brand

**Borders:** minimal. Sections separate via **background-color shift**, not
1px borders. When a border is necessary (input field outlines, table cell
dividers in dense views), use `border-cream-subtle` or a translucent
`border-brand/10`.

**Shadows:** soft and brand-tinted, not generic gray.

```ts
// In tailwind.config.ts
boxShadow: {
  card:     '0 1px 3px rgba(26, 85, 96, 0.08), 0 1px 2px rgba(26, 85, 96, 0.04)',
  elevated: '0 4px 12px rgba(26, 85, 96, 0.12)',
  popover:  '0 8px 24px rgba(26, 85, 96, 0.15)',
}
```

Usage:
- `shadow-card` — resting elevation for cards
- `shadow-elevated` — hover state on cards, dropdown panels
- `shadow-popover` — modals, command palettes, autocomplete

---

## Iconography

**Library:** [Lucide React](https://lucide.dev) (already in the stack).

**Configuration:**
- Stroke width: **1.5** (not the default 2) — matches the lighter, refined
  feel of the brand
- Sizes: 16px in tables/buttons, 20px in headers, 24px in empty states and
  feature highlights
- Color: inherit from surrounding text (no fixed icon color)

```tsx
// Wrap Lucide icons to enforce stroke width project-wide
import { Settings as SettingsIcon } from 'lucide-react';
<SettingsIcon size={20} strokeWidth={1.5} />
```

Consider creating a thin wrapper in `src/components/Icon.tsx` so the
1.5 stroke is enforced without each call site repeating it.

---

## Component patterns

### Buttons

| Variant | Background | Text | Use |
|---|---|---|---|
| Primary | `bg-brand hover:bg-brand-dark` | `text-cream` | Main action per view (Save, Create, Submit) |
| Secondary | `bg-transparent border border-brand` | `text-brand hover:bg-brand/5` | Secondary actions on the same view |
| Ghost | `bg-transparent` | `text-brand hover:bg-brand/5` | Tertiary actions, inline controls |
| Accent | `bg-transparent` | `text-accent hover:text-accent-light` | "Next →" / "View more →" — the gold treatment from the brand site |
| Danger | `bg-danger hover:bg-danger/90` | `text-cream` | Destructive actions (delete, archive) — confirm dialog required |

Buttons: padding `px-4 py-2` (small `px-3 py-1.5`, large `px-6 py-3`).
Font weight 600. Border radius `rounded-lg`. Transition 150ms.

### Cards

```tsx
<div className="bg-white rounded-lg shadow-card p-6">
  <h3 className="text-lg font-semibold text-ink-heading mb-4">
    Defect Categories
  </h3>
  {/* content */}
</div>
```

Card on cream background. White surface. Title in brand teal. No border.

### Forms

- Input fields: `bg-white border border-cream-subtle rounded-lg px-3 py-2`
- Focus state: `focus:ring-2 focus:ring-accent/40 focus:border-accent`
  (gold focus ring at 40% opacity — the signature brand touch)
- Labels: `text-sm font-medium text-ink-heading mb-1`
- Helper/error text: `text-xs` below the field, `text-ink-muted` or
  `text-danger`
- Required fields: small `*` in `text-danger` after the label

### Tables

- Header row: `bg-cream-subtle` with `text-xs font-medium uppercase tracking-wide text-ink-muted`
- Body rows: alternating `bg-white` and `bg-cream/30`
- Cell padding: `px-4 py-3`
- Sortable columns: small caret icon (Lucide `ChevronUp`/`Down`) at 12px
- Empty state: centered, with a Lucide icon (24px) and a sentence —
  never just "No data"

### Status badges

```tsx
// Online (success)
<span className="inline-flex items-center gap-1.5 px-2 py-0.5 rounded text-xs font-medium bg-success/10 text-success">
  <span className="w-1.5 h-1.5 rounded-full bg-success" />
  En ligne
</span>
```

Background at 10% opacity, text at full color, optional dot at full color.
Same pattern for `warning`, `danger`, `info` variants.

---

## Interactions

**Transitions:** 150ms ease-out by default. Slower (300ms) only for layout
shifts that need to feel deliberate (sidebar open/close, modal fade-in).

**Focus rings:** gold (`accent`) at 40% opacity, 2px wide, `offset-2`.
Visible on every interactive element. Accessibility non-negotiable.

```css
focus:ring-2 focus:ring-accent/40 focus:ring-offset-2 focus:outline-none
```

**Hover states:**
- Cards: shadow rises from `shadow-card` to `shadow-elevated`
- Buttons: background darkens by one shade
- Links: underline appears, color unchanged
- Table rows: background shifts to `bg-cream-subtle`

**Loading states:**
- Skeletons in `bg-cream-subtle` with a subtle shimmer (Tailwind's
  `animate-pulse` works fine)
- Spinners in `text-brand` for primary actions, `text-accent` for the
  "doing something important" feel — never default browser spinner

---

## Page composition recipes

### Dashboard home (stat tiles + recent activity)

```
┌─ Page (bg-cream) ────────────────────────────────────┐
│  [Stat tile] [Stat tile] [Stat tile] [Stat tile]     │  ← grid-cols-4, bg-white
│                                                       │
│  ┌─ Recent defects (bg-white card) ──────────────┐   │
│  │  Table with cream-subtle alternating rows     │   │
│  │  Status badges per row                        │   │
│  │  "View all →" link in accent at the bottom    │   │
│  └────────────────────────────────────────────────┘   │
│                                                       │
│  ┌─ Devices (bg-white card) ─────────────────────┐   │
│  │  ...                                          │   │
│  └────────────────────────────────────────────────┘   │
└──────────────────────────────────────────────────────┘
```

### Login page

The one place to lean into brand vibes. Cream background. Centered card
with brand-teal header strip. Large brand watermark behind (faded at 5%
opacity, like the PMP watermark on the public hero). Gold focus ring on
the PIN/password input. Logo at top.

### Data-heavy page (logs, devices)

Less decoration, more density. Full-width table. Filter bar at top
in a thin cream-subtle strip. Pagination at bottom. Resist the
temptation to add cards everywhere — at scale, cards waste vertical space.

---

## Anti-patterns (don't do)

- ❌ Pure white page backgrounds (loses the warmth)
- ❌ Black headings (use brand teal)
- ❌ Gold buttons for primary actions (gold is an accent, not a workhorse)
- ❌ Bright red destructive buttons (use muted `danger`)
- ❌ Three or more accent colors on one screen
- ❌ Serif fonts anywhere
- ❌ Monospace for non-data content
- ❌ Sharp corners (`rounded-none`) or extreme rounds (`rounded-3xl`)
- ❌ Drop shadows that are pure gray (use brand-teal-tinted shadows)
- ❌ Generic Bootstrap-style alerts (build alerts with the semantic palette)
- ❌ Emoji as UI icons (use Lucide consistently)
- ❌ Default browser `:focus` outlines (always use the accent ring)

---

## Implementation checklist

When scaffolding the dashboard, apply these in order:

1. **Fonts loaded** in `index.html` (Inter + JetBrains Mono via Google Fonts)
2. **Tailwind config** extends theme with all tokens above
3. **CSS variables** in `src/index.css` for shadcn/ui compatibility
4. **Base body styles**: `bg-cream text-ink font-sans antialiased`
5. **Icon wrapper** (`src/components/Icon.tsx`) enforcing stroke-width 1.5
6. **Button component** with all six variants
7. **Card component** as the default container
8. **Status badge component** with semantic variants
9. **Form-field component** with the gold focus ring
10. **Page layout** with cream background and proper padding
11. **First real screen** (Login) testing the full system end to end

If something looks generic at this stage, return to this document. The
brand identity isn't decoration; it's a feature.

---

## Reference

- Brand site: PMP homepage (Peinture et Métallisation sur Plastique)
- Primary teal sampled from PMP logo + hero panel
- Accent gold sampled from PMP CTA arrows + decorative curves
- Cream sampled from PMP page background
- Semantic colors: derived to harmonize with brand teal (not from PMP)

If PMP later provides an official brand guide (PDF with Pantone refs),
those values supersede the hex values here. Update this file and the
Tailwind config together.
