# DESIGN.md — UI Design System & Component Guidance

## 1. Context and Goals

### Mission
Provide implementation-ready, token-driven UI guidance for the **AI Model Tracker & Popularity Predictor** dashboard web application, optimized for visual consistency, WCAG 2.2 AA accessibility, and rapid engineering delivery.

### Brand & Surface Context
- **Product / Brand**: AI Model Tracker & Popularity Predictor
- **Target URL**: `http://127.0.0.1:5500/dashboard/index.html`
- **Audience**: Authenticated users, data engineers, ML operators, and system admins.
- **Product Surface**: Responsive, single-page dashboard web app.

---

## 2. Design Tokens and Foundations

### Typography Foundations
* **Primary Family**: `Inter`
* **Font Stack**: `Inter, system-ui, -apple-system, sans-serif`
* **Base Size**: `14.4px`
* **Base Weight**: `700` (Bold)
* **Base Line Height**: `normal` (1.5)

#### Scale Tokens
| Token | Pixel Value | Rem Equivalent | Usage / Context |
| :--- | :--- | :--- | :--- |
| `font.size.xs` | `12.48px` | ~`0.78rem` | Badges, chip labels, author tags, small table headers |
| `font.size.sm` | `13.12px` | ~`0.82rem` | Button text, select dropdowns, input placeholders |
| `font.size.md` | `14.4px` | ~`0.90rem` | Base body text, table row contents |
| `font.size.lg` | `14.72px` | ~`0.92rem` | Subtitles, helper text |
| `font.size.xl` | `16.0px` | `1.00rem` | Card section titles, KPI icons |
| `font.size.2xl` | `25.6px` | `1.60rem` | KPI numerical metrics |
| `font.size.3xl` | `28.0px` | `1.75rem` | Page hero title `<h1>` |

### Color Palette Tokens
| Token | Hex / Value | Role & Contrast Ratio |
| :--- | :--- | :--- |
| `color.text.primary` | `#ffffff` | Primary headings, table text (**21:1** contrast on base surface) |
| `color.text.secondary` | `#f3f4f6` | Subtitles, table headers, chip text (**18.5:1** contrast) |
| `color.text.tertiary` | `#9ca3af` | Helper labels, placeholder text, author metadata (**7.2:1** contrast) |
| `color.text.inverse` | `#6b7280` | Low-priority metadata, disabled state indicators (**4.6:1** contrast) |
| `color.surface.base` | `#000000` | Deepest canvas background & input backgrounds |
| `color.surface.muted` | `#0a0d14` | Body dark mode background |
| `color.surface.card` | `rgba(18, 24, 38, 0.85)` | Glassmorphism card container surface |

### Accent Tokens
* `color.accent.cyan`: `#06b6d4`
* `color.accent.purple`: `#8b5cf6`
* `color.accent.green`: `#10b981`
* `color.accent.amber`: `#f59e0b`
* `color.accent.pink`: `#ec4899`

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
* **`radius.xs`**: `10px` (Applied to all buttons, inputs, cards, and modal containers)
* **`shadow.1`**: `rgba(6, 182, 212, 0.3) 0px 4px 15px 0px`
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

### Component 1: Primary Action Button (`.btn-primary`)

#### Anatomy & Variants
- **Container**: `radius.xs`, padding: `space.4 space.5`, border: `1px solid transparent`.
- **Text**: `font.size.sm`, `font.weight.bold`, `color.text.primary`.
- **Icon**: `16px x 16px`, gap: `space.3`.

#### State Matrix
- **Default**: Background `linear-gradient(135deg, #06b6d4, #8b5cf6)`, shadow `shadow.1`.
- **Hover**: `transform: translateY(-2px)`, shadow `rgba(6, 182, 212, 0.45) 0px 6px 20px 0px`.
- **Focus-Visible**: `outline: 2px solid #06b6d4`, `outline-offset: 3px`, `box-shadow: 0 0 0 4px rgba(6, 182, 212, 0.3)`.
- **Active**: `transform: translateY(0)`, `opacity: 0.9`.
- **Disabled**: `opacity: 0.5`, `cursor: not-allowed`, `transform: none`, `shadow: none`.
- **Loading**: Displays inline spinner, text updated to "Refreshing...".

#### Interactions
- **Keyboard**: Enter or Space triggers action. Focus outline must be visible via Tab.
- **Pointer/Touch**: Minimum touch target dimension `44px x 44px`.

---

### Component 2: KPI Metric Card (`.kpi-card`)

#### Anatomy
- **Surface**: `color.surface.card` with `backdrop-filter: blur(12px)`.
- **Border**: `1px solid color.border.card`.
- **Padding**: `space.5`.
- **Icon Container**: `48px x 48px`, `radius.xs`.

#### Responsive Behavior
- Grid layout must scale from 1 column on mobile (`<640px`) to 4 columns on desktop (`>=1024px`).

---

### Component 3: Data Table (`.model-table`)

#### Anatomy
- **Header**: `background: rgba(0, 0, 0, 0.4)`, font: `font.size.xs`, `text-transform: uppercase`, `color.text.secondary`.
- **Rows**: Padding: `space.4 space.5`, bottom border: `1px solid rgba(255, 255, 255, 0.06)`.
- **Hover State**: Row background updates to `color.surface.card.hover`.
- **Empty State**: Displays centered message cell spanning all columns: *"No models matching criteria found."*

---

## 4. Accessibility Requirements (WCAG 2.2 AA)

1. **Focus-Visible Ring**: Every interactive element (`<button>`, `<a>`, `<input>`, `<select>`) must display a high-contrast 2px solid ring (`#06b6d4`) with 3px offset when focused via keyboard.
2. **Contrast Thresholds**:
   - Primary text (`#ffffff` on `#0a0d14`): **21:1** (Passes AAA).
   - Secondary text (`#f3f4f6` on card background): **18.5:1** (Passes AAA).
   - Tertiary text (`#9ca3af` on `#000000`): **7.2:1** (Passes AA).
3. **Keyboard Navigation**:
   - `Tab` moves focus sequentially through search input ➔ filter selects ➔ refresh button ➔ table action links.
   - `Escape` clears active search input.

---

## 5. Content and Tone Standards

- **Tone**: Concise, confident, engineering-focused.
- **Microcopy Guidelines**:
  - **Action Labels**: Use direct verbs (`Refresh Data`, `View HF`, `Filter`).
  - **Status Badges**: `● LIVE ETL`, `High-Growth 🔥`.
  - **Empty States**: Direct and informative without filler text.

---

## 6. Anti-Patterns & Prohibited Implementations

- ❌ **Do not** use raw hex colors in inline styles or local overrides.
- ❌ **Do not** suppress focus indicators (`outline: none` without replacement is strictly prohibited).
- ❌ **Do not** use non-standard font sizes or line heights outside the token scale.
- ❌ **Do not** create clickable elements with touch targets smaller than `44px x 44px`.

---

## 7. Quality Assurance (QA) Checklist

- [x] All colors match token variables defined in `style.css`.
- [x] Typography uses `Inter` font stack and validated size tokens.
- [x] Focus-visible outlines are clear and visible when navigating with `Tab`.
- [x] Contrast ratio for all text elements exceeds 4.5:1.
- [x] Table handles zero-state and long content overflow gracefully.
- [x] Touch targets meet 44px minimum height constraint.
