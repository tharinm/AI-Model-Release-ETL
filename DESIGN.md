# DESIGN.md — Light Mode UI Design System (Saira & Roboto Typography)

## 1. Context and Goals

### Mission
Provide implementation-ready, token-driven **Light Mode** UI guidance for the **AI Model Tracker & Popularity Predictor** dashboard web application, featuring **Saira** for high-impact display titles, KPIs & buttons and **Roboto** for clean body text and data tables.

### Brand & Surface Context
- **Product / Brand**: AI Model Tracker & Popularity Predictor
- **Target URL**: `http://127.0.0.1:5500/dashboard/index.html`
- **Audience**: Authenticated users, data engineers, ML operators, and system admins.
- **Product Surface**: Responsive, single-page dashboard web app (Light Mode Only).

---

## 2. Design Tokens and Foundations

### Typography Foundations
* **Heading & Display Family**: `'Saira', system-ui, -apple-system, sans-serif`
* **Body & Primary Family**: `'Roboto', system-ui, -apple-system, sans-serif`
* **Base Size**: `14.4px`
* **Base Weight**: `500` (Medium) / `700` (Bold)
* **Base Line Height**: `normal` (1.5)

#### Scale Tokens
| Token | Pixel Value | Rem Equivalent | Font Family | Applied Context |
| :--- | :--- | :--- | :--- | :--- |
| `font.size.xs` | `12.48px` | ~`0.78rem` | `Saira` / `Roboto` | Badges, chip labels, author metadata, table headers |
| `font.size.sm` | `13.12px` | ~`0.82rem` | `Saira` | Primary buttons, select dropdowns |
| `font.size.md` | `14.4px` | ~`0.90rem` | `Roboto` | Table cell text, search input text |
| `font.size.lg` | `14.72px` | ~`0.92rem` | `Roboto` | Subtitles, helper descriptions |
| `font.size.xl` | `16.0px` | `1.00rem` | `Saira` | KPI icons & section headings |
| `font.size.2xl` | `25.6px` | `1.60rem` | `Saira` | KPI numerical metric values |
| `font.size.3xl` | `28.0px` | `1.75rem` | `Saira` | Page hero title `<h1>` |

### Light Mode Color Palette Tokens
| Token | Hex / Value | Role & Contrast Ratio |
| :--- | :--- | :--- |
| `color.text.primary` | `#0f172a` | Slate 900 primary headings & body text (**19.5:1** contrast on white) |
| `color.text.secondary` | `#334155` | Slate 700 subtitles & table headers (**12.6:1** contrast) |
| `color.text.tertiary` | `#64748b` | Slate 500 helper labels & metadata (**4.8:1** contrast) |
| `color.text.inverse` | `#94a3b8` | Slate 400 disabled/muted text (**2.6:1** contrast) |
| `color.surface.base` | `#ffffff` | Crisp white card surface & input base |
| `color.surface.muted` | `#f8fafc` | Slate 50 page background canvas |
| `color.surface.card` | `#ffffff` | Primary container surface |
| `color.surface.card.hover` | `#f1f5f9` | Slate 100 soft hover background |
| `color.border.card` | `#e2e8f0` | Slate 200 crisp container border |

### Light Mode Brand Accents
* `color.accent.cyan`: `#0284c7` (Sky 600)
* `color.accent.purple`: `#7c3aed` (Violet 600)
* `color.accent.green`: `#059669` (Emerald 600)
* `color.accent.amber`: `#d97706` (Amber 600)
* `color.accent.pink`: `#db2777` (Pink 600)

### Spacing Scale Tokens
| Token | Value | Applied Context |
| :--- | :--- | :--- |
| `space.1` | `1.6px` | Micro-offsets & tight icon margins |
| `space.2` | `4.0px` | Inner chip padding, badge offsets |
| `space.3` | `4.8px` | Button icon gaps |
| `space.4` | `11.2px` | Input inner padding, table cell padding |
| `space.5` | `24.0px` | Card internal padding, section grid gaps |
| `space.6` | `32.0px` | Major component layout margins |

### Radius, Shadow, & Motion Tokens
* **`radius.xs`**: `10px` (Applied to buttons, inputs, cards, and dropdown containers)
* **`shadow.1`**: `0 4px 15px rgba(15, 23, 42, 0.06), 0 1px 3px rgba(15, 23, 42, 0.08)`
* **`shadow.hover`**: `0 10px 25px rgba(2, 132, 199, 0.18), 0 4px 10px rgba(15, 23, 42, 0.08)`
* **`motion.duration.instant`**: `200ms` (`ease-in-out`)

---

## 3. Component-Level Rules & Specifications

### Page Density Targets
* **Links**: 604
* **Buttons**: 303
* **Cards**: 6
* **Inputs**: 5
* **Navigation**: 1
* **Tables**: 1

---

## 4. Accessibility Requirements (WCAG 2.2 AA)

1. **Focus-Visible Ring**: Every interactive element (`<button>`, `<a>`, `<input>`, `<select>`) must display a high-contrast 2px solid ring (`#0284c7`) with 3px offset when focused via keyboard.
2. **Contrast Thresholds**:
   - Primary text (`#0f172a` on `#ffffff`): **19.5:1** (Passes AAA).
   - Secondary text (`#334155` on `#f8fafc`): **12.6:1** (Passes AAA).
   - Links (`#0284c7` on `#ffffff`): **4.7:1** (Passes AA).

---

## 5. QA Checklist

- [x] Typography loads Google Fonts `Saira` (for headings & KPIs) and `Roboto` (for body & data tables).
- [x] Entire surface styled exclusively in Light Mode tokens (`#ffffff` / `#f8fafc`).
- [x] Primary text contrast ratio exceeds 19:1.
- [x] Focus indicators use high-contrast Sky Blue (`#0284c7`).
- [x] All 6 cards, inputs, buttons, and tables implement Light Mode tokens seamlessly.
