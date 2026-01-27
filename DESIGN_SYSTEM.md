# Macro Dashboard Design System v2.0

**Last Updated:** January 23, 2026  
**Philosophy:** Clean, data-first, professional. Linear's speed + Stripe's clarity + FT's authority.

---

## Table of Contents

1. [Foundation](#foundation)
2. [Typography](#typography)
3. [Color Palette](#color-palette)
4. [Spacing & Layout](#spacing--layout)
5. [Components](#components)
6. [Chart Styling](#chart-styling)
7. [Interactions](#interactions)
8. [Responsive Design](#responsive-design)
9. [Accessibility](#accessibility)
10. [Implementation Checklist](#implementation-checklist)

---

## Foundation

### Design Principles

1. **Data First**: The data is the hero. Design should clarify, not decorate.
2. **Hierarchy Matters**: Big number → Sparkline → Context. Always.
3. **Speed > Fancy**: Fast, snappy interactions. No sluggish animations.
4. **Professional**: Would you show this to investors? If not, iterate.
5. **Keyboard Accessible**: Power users demand it.

### Design References

- **Linear**: Fast UI, keyboard shortcuts, minimal animations
- **Stripe Dashboard**: Metric cards, clean hierarchy, financial data presentation
- **Financial Times**: Chart annotations, authoritative typography, red/green signals
- **Observable**: Interactive charts, "show the data" philosophy

---

## Typography

### Font Family

```css
@import url('https://fonts.googleapis.com/css2?family=Urbanist:wght@100;200;300;400;500;600;700;800;900&display=swap');

font-family: 'Urbanist', -apple-system, BlinkMacSystemFont, 'Segoe UI', sans-serif;
```

### Type Scale

```css
/* Display */
--text-display: 32px;
--text-display-weight: 700;
--text-display-tracking: -0.02em;
--text-display-line-height: 1.2;
/* Usage: Main title "Macro Dashboard" */

/* Heading 1 */
--text-h1: 24px;
--text-h1-weight: 600;
--text-h1-tracking: 0;
--text-h1-line-height: 1.3;
/* Usage: Page titles like "Dashboard Overview" */

/* Heading 2 */
--text-h2: 20px;
--text-h2-weight: 600;
--text-h2-tracking: 0;
--text-h2-line-height: 1.4;
/* Usage: Section headers like "Key Economic Indicators" */

/* Heading 3 */
--text-h3: 16px;
--text-h3-weight: 500;
--text-h3-tracking: 0;
--text-h3-line-height: 1.5;
/* Usage: Card titles, subsection headers */

/* Body */
--text-body: 14px;
--text-body-weight: 400;
--text-body-tracking: 0;
--text-body-line-height: 1.5;
/* Usage: Default text, descriptions, labels */

/* Caption */
--text-caption: 12px;
--text-caption-weight: 400;
--text-caption-tracking: 0.02em;
--text-caption-line-height: 1.5;
/* Usage: Metadata, timestamps, footnotes */

/* Metric Display Large */
--text-metric-lg: 36px;
--text-metric-lg-weight: 700;
--text-metric-lg-tracking: -0.02em;
--text-metric-lg-line-height: 1.2;
/* Usage: Big dashboard numbers in metric cards */

/* Metric Display Small */
--text-metric-sm: 24px;
--text-metric-sm-weight: 600;
--text-metric-sm-tracking: 0;
--text-metric-sm-line-height: 1.2;
/* Usage: Secondary metrics, inline numbers */
```

### Typography Rules

1. **Never mix fonts** - Urbanist for everything
2. **Use weight for hierarchy** - Not just size
3. **Tighter tracking on large text** - Improves readability
4. **Wider tracking on small caps** - Labels, metadata
5. **Numbers use tabular figures** - For alignment in tables

---

## Color Palette

### Base Colors

```css
/* Backgrounds */
--color-bg-primary: #0a0a0a;          /* Main background */
--color-bg-secondary: #141414;        /* Card backgrounds */
--color-bg-tertiary: #1e1e1e;         /* Hover states, elevated elements */
--color-bg-overlay: rgba(0, 0, 0, 0.8); /* Modals, overlays */

/* Text */
--color-text-primary: #ffffff;        /* Headings, important text */
--color-text-secondary: #a3a3a3;      /* Body text, labels */
--color-text-tertiary: #737373;       /* Muted text, captions */
--color-text-disabled: #525252;       /* Disabled state */

/* Borders */
--color-border-subtle: #262626;       /* Very subtle dividers */
--color-border-default: #404040;      /* Default borders */
--color-border-strong: #525252;       /* Emphasized borders */
```

### Accent & Brand

```css
/* Primary Accent (Teal) */
--color-accent-primary: #14b8a6;      /* Primary actions, highlights */
--color-accent-hover: #0d9488;        /* Hover state */
--color-accent-active: #0f766e;       /* Pressed state */
--color-accent-subtle: rgba(20, 184, 166, 0.1);  /* Subtle backgrounds */
--color-accent-border: rgba(20, 184, 166, 0.3);  /* Subtle borders */
```

### Status Colors

```css
/* Success (Positive) */
--color-success: #10b981;             /* Positive trends, good signals */
--color-success-bg: rgba(16, 185, 129, 0.1);

/* Warning (Caution) */
--color-warning: #f59e0b;             /* Moderate risk, caution */
--color-warning-bg: rgba(245, 158, 11, 0.1);

/* Danger (Negative) */
--color-danger: #ef4444;              /* Negative trends, high risk */
--color-danger-bg: rgba(239, 68, 68, 0.1);

/* Info (Neutral) */
--color-info: #3b82f6;                /* Neutral information */
--color-info-bg: rgba(59, 130, 246, 0.1);
```

### Chart Colors

```css
/* Multi-line chart palette - use in order */
--color-chart-1: #14b8a6;  /* Teal - primary line */
--color-chart-2: #8b5cf6;  /* Purple - secondary */
--color-chart-3: #f59e0b;  /* Amber - tertiary */
--color-chart-4: #ec4899;  /* Pink - quaternary */
--color-chart-5: #06b6d4;  /* Cyan - quinary */

/* Chart UI elements */
--color-chart-grid: rgba(255, 255, 255, 0.05);     /* Grid lines */
--color-chart-axis: #737373;                        /* Axis labels */
--color-chart-crosshair: #14b8a6;                  /* Hover crosshair */
```

### Color Usage Rules

1. **Text on dark backgrounds**: Use primary/secondary text colors for proper contrast
2. **Status colors**: Red = bad/danger, Green = good/success, Amber = caution
3. **Accent sparingly**: Teal for primary actions and highlights only
4. **Chart colors**: Use the 5-color palette in order, don't add random colors
5. **Hover states**: Move from secondary → tertiary background
6. **Active states**: Use accent-primary background with white text

---

## Spacing & Layout

### Spacing Scale

```css
--space-xs: 4px;
--space-sm: 8px;
--space-md: 16px;
--space-lg: 24px;
--space-xl: 32px;
--space-2xl: 48px;
--space-3xl: 64px;
--space-4xl: 96px;
```

### Border Radius

```css
--radius-sm: 4px;    /* Small elements, tight corners */
--radius-md: 8px;    /* Cards, buttons, inputs */
--radius-lg: 12px;   /* Modals, large containers */
--radius-full: 9999px; /* Pills, avatars, badges */
```

### Shadows

```css
--shadow-sm: 0 1px 2px rgba(0, 0, 0, 0.3);
--shadow-md: 0 4px 8px rgba(0, 0, 0, 0.4);
--shadow-lg: 0 12px 24px rgba(0, 0, 0, 0.5);
--shadow-xl: 0 20px 40px rgba(0, 0, 0, 0.6);

/* Special: Glow effect for accent */
--shadow-accent: 0 0 16px rgba(20, 184, 166, 0.3);
```

### Layout Grid

```css
/* Container */
--container-max-width: 1400px;
--container-padding: var(--space-xl);

/* Columns */
--col-gap: var(--space-lg);
--row-gap: var(--space-2xl);

/* Sidebar */
--sidebar-width: 240px;
```

### Spacing Rules

1. **Consistent rhythm**: Use spacing scale, don't make up values
2. **Larger gaps between sections**: Use 2xl or 3xl
3. **Breathing room**: Content should never touch edges
4. **Vertical rhythm**: Maintain consistent spacing between stacked elements
5. **Responsive**: Reduce spacing on mobile (divide by 2)

---

## Components

### 1. Metric Card

**Purpose:** Display key metrics with trend indicators (Stripe-inspired)

**Specifications:**
```
Size: Flexible width, 120px min height
Padding: --space-md (16px)
Background: --color-bg-secondary
Border: 1px solid --color-border-subtle
Border-radius: --radius-md
Gap between elements: --space-sm
```

**Structure:**
```
┌─────────────────────────────┐
│ Label                       │ ← 12px, weight 400, text-secondary
│                             │
│ 1,234.56            ↑ 5.2% │ ← Value: 36px, bold | Change: 14px, medium
│                             │
│ ▁▂▃▄▅▆▇█                   │ ← Sparkline: 40px height
└─────────────────────────────┘
```

**States:**
- **Default**: Background secondary, border subtle
- **Hover**: Background → tertiary, border → accent-border (150ms transition)
- **Loading**: Show skeleton with shimmer animation

**Change Indicator:**
- Positive: Success color (#10b981), ↑ arrow
- Negative: Danger color (#ef4444), ↓ arrow
- Neutral: Text-secondary color, → arrow
- Position: Top right, aligned with value

**Code Template:**
```tsx
<div className="metric-card">
  <span className="metric-label">Unemployment Rate</span>
  <div className="metric-value-row">
    <span className="metric-value">4.2</span>
    <span className="metric-change positive">↑ 0.3%</span>
  </div>
  <Sparkline data={data} />
</div>
```

---

### 2. Section Header

**Purpose:** Divide dashboard into logical sections

**Specifications:**
```
Margin-top: --space-2xl (48px)
Margin-bottom: --space-lg (24px)
Padding-bottom: --space-sm (8px)
Border-bottom: 1px solid --color-border-subtle
```

**Structure:**
```
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
Section Title (24px, weight 600)
Optional subtitle (14px, text-secondary)
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
```

**Code Template:**
```tsx
<div className="section-header">
  <h2>Key Economic Indicators</h2>
  <p className="subtitle">Track recession signals and trends</p>
</div>
```

---

### 3. Chart Container

**Purpose:** Consistent wrapper for all charts (Observable + FT-inspired)

**Specifications:**
```
Height: 400px (adjustable via prop)
Padding: --space-lg (24px)
Background: --color-bg-secondary
Border-radius: --radius-md
No border (clean look)
```

**Structure:**
```
┌────────────────────────────────┐
│ Chart Title (16px, medium)     │
│ Subtitle (12px, text-tertiary) │
├────────────────────────────────┤
│                                │
│                                │
│     [Chart Canvas]             │
│                                │
│                                │
└────────────────────────────────┘
```

**Internal Chart Styling:**
```javascript
{
  backgroundColor: 'transparent',
  
  // Grid
  grid: {
    show: true,
    borderColor: 'var(--color-chart-grid)',
    borderDash: [4, 4]
  },
  
  // X Axis
  xAxis: {
    axisLabel: {
      color: 'var(--color-chart-axis)',
      fontSize: 12
    },
    axisLine: {
      lineStyle: { color: 'var(--color-border-default)' }
    }
  },
  
  // Y Axis
  yAxis: {
    axisLabel: {
      color: 'var(--color-chart-axis)',
      fontSize: 12
    },
    splitLine: {
      lineStyle: {
        color: 'var(--color-chart-grid)',
        type: 'dashed',
        opacity: 0.3
      }
    }
  },
  
  // Series
  series: {
    lineStyle: { width: 2 },
    smooth: false, // Keep accurate
    areaStyle: {
      opacity: 0.1 // For area charts
    }
  },
  
  // Tooltip
  tooltip: {
    backgroundColor: 'var(--color-bg-tertiary)',
    borderColor: 'var(--color-border-default)',
    textStyle: { 
      color: 'var(--color-text-primary)',
      fontSize: 12
    },
    trigger: 'axis',
    axisPointer: {
      lineStyle: {
        color: 'var(--color-chart-crosshair)',
        width: 1
      }
    }
  }
}
```

---

### 4. Sidebar Navigation

**Purpose:** Primary navigation (Linear-inspired)

**Specifications:**
```
Width: 240px
Background: --color-bg-secondary
Border-right: 1px solid --color-border-subtle
Padding: --space-lg
```

**Nav Item:**
```
Height: 40px
Padding: --space-sm --space-md
Border-radius: --radius-sm
Gap between icon and label: --space-sm
```

**States:**
- **Default**: text-secondary, no background
- **Hover**: background → accent-subtle, text → text-primary
- **Active**: background → accent-primary, text → white
- **Transition**: all 150ms ease

**Structure:**
```
┌──────────────────────┐
│ 🏠 Overview          │ ← Active state
│ 📊 Recession Watch   │ ← Hover state
│ 📈 Market Overview   │ ← Default state
│ 🔍 Custom Analysis   │
│ ❓ FAQ               │
├──────────────────────┤
│ Data Management      │ ← Section header
│ [Refresh FRED]       │ ← Button
│ [Refresh Market]     │
└──────────────────────┘
```

**Code Template:**
```tsx
<nav className="sidebar">
  <div className="nav-section">
    <NavItem icon="home" label="Overview" active />
    <NavItem icon="chart" label="Recession Watch" />
    <NavItem icon="trending" label="Market Overview" />
  </div>
  
  <div className="nav-section">
    <span className="section-title">Data Management</span>
    <Button variant="secondary">Refresh FRED</Button>
  </div>
</nav>
```

---

### 5. Button

**Purpose:** Primary, secondary, and tertiary actions

**Variants:**

**Primary:**
```css
height: 40px;
padding: 0 var(--space-md);
background: var(--color-accent-primary);
color: white;
border: none;
border-radius: var(--radius-sm);
font-size: var(--text-body);
font-weight: 500;
```

**Secondary:**
```css
background: transparent;
border: 1px solid var(--color-border-default);
color: var(--color-text-primary);
```

**Ghost:**
```css
background: transparent;
border: none;
color: var(--color-text-secondary);
```

**States:**
- **Hover**: transform: translateY(-1px), box-shadow: var(--shadow-md)
- **Active**: transform: translateY(0), box-shadow: none
- **Disabled**: opacity: 0.5, cursor: not-allowed
- **Loading**: Show spinner, disable interaction

---

### 6. Time Range Selector

**Purpose:** Filter charts by time period

**Specifications:**
```
Button height: 32px
Padding: 0 --space-md
Gap between buttons: --space-xs
Border-radius: --radius-sm
```

**Structure:**
```
[1M] [3M] [6M] [1Y] [5Y] [All]
```

**States:**
- **Default**: text-secondary, border 1px border-default
- **Hover**: text-primary, border accent-border
- **Active**: background accent-primary, text white, no border

---

### 7. Data Table

**Purpose:** Display tabular data

**Specifications:**
```
Row height: 48px
Cell padding: --space-sm horizontal, --space-xs vertical
Border between rows: 1px solid --color-border-subtle
```

**Structure:**
```
┌──────────┬──────────┬──────────┐
│ Header 1 │ Header 2 │ Header 3 │ ← 12px, medium, bg-tertiary
├──────────┼──────────┼──────────┤
│ Value 1  │ Value 2  │ Value 3  │ ← 14px
│ Value 1  │ Value 2  │ Value 3  │
└──────────┴──────────┴──────────┘
```

**Rules:**
- Header: background-tertiary, text-secondary, sticky on scroll
- Rows: Hover → background-tertiary
- Numbers: Right-aligned, tabular figures
- Alternating rows: Optional subtle background (#121212)

---

### 8. Loading Skeleton

**Purpose:** Show loading state without spinners

**Specifications:**
```
Background: Linear gradient shimmer
Animation: 1.5s infinite ease-in-out
```

**Implementation:**
```css
.skeleton {
  background: linear-gradient(
    90deg,
    var(--color-bg-secondary) 0%,
    var(--color-bg-tertiary) 50%,
    var(--color-bg-secondary) 100%
  );
  background-size: 200% 100%;
  animation: shimmer 1.5s ease-in-out infinite;
  border-radius: var(--radius-sm);
}

@keyframes shimmer {
  0% { background-position: -200% 0; }
  100% { background-position: 200% 0; }
}
```

---

## Chart Styling

### Line Chart (Time Series)

**Best for:** Showing trends over time (unemployment, rates, GDP)

**Configuration:**
```javascript
{
  type: 'line',
  lineStyle: { 
    width: 2,
    color: 'var(--color-chart-1)'
  },
  smooth: false, // Keep data accurate
  symbol: 'none', // No dots on line
  emphasis: {
    focus: 'series',
    lineStyle: { width: 3 }
  }
}
```

---

### Area Chart (Ranges/Volatility)

**Best for:** Showing magnitude (VIX, volatility ranges)

**Configuration:**
```javascript
{
  type: 'line',
  lineStyle: { width: 2 },
  areaStyle: {
    opacity: 0.1,
    color: 'var(--color-chart-1)'
  }
}
```

---

### Multi-Line Chart (Comparisons)

**Best for:** Comparing multiple indicators

**Configuration:**
```javascript
series: [
  { name: 'Indicator 1', color: 'var(--color-chart-1)' },
  { name: 'Indicator 2', color: 'var(--color-chart-2)' },
  { name: 'Indicator 3', color: 'var(--color-chart-3)' }
]
```

**Legend:**
- Position: Top right
- Font: 12px, weight 400
- Interactive: Click to show/hide series

---

### Threshold Lines (Annotations)

**Best for:** Marking critical levels (zero line, inversion)

**Configuration:**
```javascript
markLine: {
  silent: true, // Non-interactive
  data: [
    { yAxis: 0, name: 'Zero Line' }
  ],
  lineStyle: {
    type: 'dashed',
    color: 'var(--color-danger)',
    width: 1
  },
  label: {
    show: true,
    position: 'insideEndTop',
    color: 'var(--color-danger)',
    fontSize: 11,
    fontWeight: 500
  }
}
```

---

### Sparkline (Metric Card Trend)

**Best for:** Showing trend in small space

**Specifications:**
```
Width: 100% of card
Height: 40px
No axes, no labels
Line width: 1.5px
Area fill: 10% opacity
```

---

## Interactions

### Transitions

**Global timing:**
```css
/* Standard transition */
transition: all 150ms cubic-bezier(0.4, 0, 0.2, 1);

/* Fast transition (subtle changes) */
transition: all 100ms ease-out;

/* Slow transition (large movements) */
transition: all 250ms ease-in-out;
```

**What to animate:**
- ✅ Background colors
- ✅ Border colors
- ✅ Opacity
- ✅ Transform (translate, scale)
- ❌ Width/height (causes reflow)
- ❌ Position (use transform instead)

---

### Hover States

```css
/* Cards */
.card:hover {
  background: var(--color-bg-tertiary);
  border-color: var(--color-accent-border);
}

/* Buttons */
button:hover {
  transform: translateY(-1px);
  box-shadow: var(--shadow-md);
}

/* Nav items */
.nav-item:hover {
  background: var(--color-accent-subtle);
  color: var(--color-text-primary);
}

/* Table rows */
tr:hover {
  background: var(--color-bg-tertiary);
}
```

---

### Active States

```css
/* Buttons */
button:active {
  transform: translateY(0);
  box-shadow: none;
}

/* Nav items */
.nav-item.active {
  background: var(--color-accent-primary);
  color: white;
}
```

---

### Focus States (Keyboard Accessibility)

```css
*:focus {
  outline: 2px solid var(--color-accent-primary);
  outline-offset: 2px;
}

/* For elements that don't need visible focus */
button:focus:not(:focus-visible) {
  outline: none;
}
```

---

### Loading States

**Use skeletons, not spinners:**
```tsx
{loading ? (
  <div className="skeleton" style={{ width: '100%', height: '400px' }} />
) : (
  <Chart data={data} />
)}
```

---

### Page Transitions

```css
.page-enter {
  opacity: 0;
  transform: translateY(8px);
}

.page-enter-active {
  opacity: 1;
  transform: translateY(0);
  transition: all 200ms ease-out;
}

.page-exit {
  opacity: 1;
}

.page-exit-active {
  opacity: 0;
  transition: opacity 150ms ease-in;
}
```

---

## Responsive Design

### Breakpoints

```css
/* Mobile first approach */
--breakpoint-sm: 640px;   /* Mobile landscape */
--breakpoint-md: 768px;   /* Tablet */
--breakpoint-lg: 1024px;  /* Desktop */
--breakpoint-xl: 1280px;  /* Large desktop */
--breakpoint-2xl: 1536px; /* Extra large */
```

### Layout Adjustments

**Desktop (default):**
- Sidebar: Visible, 240px width
- Metric cards: 4 columns
- Charts: 2 columns
- Tables: Full width

**Tablet (< 1024px):**
- Sidebar: Collapsible, overlay on open
- Metric cards: 2 columns
- Charts: 1 column
- Tables: Horizontal scroll

**Mobile (< 768px):**
- Sidebar: Hidden, hamburger menu
- Metric cards: 1 column
- Charts: 1 column, reduced height
- Tables: Horizontal scroll, sticky first column

**Implementation:**
```css
/* Metric cards */
.metric-grid {
  display: grid;
  grid-template-columns: repeat(4, 1fr);
  gap: var(--space-lg);
}

@media (max-width: 1024px) {
  .metric-grid {
    grid-template-columns: repeat(2, 1fr);
  }
}

@media (max-width: 768px) {
  .metric-grid {
    grid-template-columns: 1fr;
    gap: var(--space-md);
  }
}
```

---

## Accessibility

### Contrast Ratios

**Text on dark backgrounds:**
- Primary text (#ffffff): 21:1 (AAA)
- Secondary text (#a3a3a3): 7.3:1 (AAA)
- Tertiary text (#737373): 4.6:1 (AA)

**Accent color (#14b8a6):**
- On dark background: 5.2:1 (AA for large text)
- On white: 3.1:1 (AA for large text)

### Minimum Touch Targets

```css
/* Interactive elements */
min-width: 44px;
min-height: 44px;
```

### Keyboard Navigation

**Tab order:**
1. Skip to main content link (hidden, shows on focus)
2. Sidebar navigation
3. Page content (metrics, charts, tables)
4. Action buttons

**Keyboard shortcuts:**
- `/` - Focus search (if implemented)
- `Esc` - Close modals/overlays
- `←/→` - Navigate time ranges
- `Tab` - Move forward
- `Shift+Tab` - Move backward
- `Enter/Space` - Activate button

### Screen Reader Support

```html
<!-- Metric cards -->
<div role="region" aria-label="Unemployment Rate Metric">
  <span aria-label="Indicator name">Unemployment Rate</span>
  <span aria-label="Current value">4.2%</span>
  <span aria-label="Change">up 0.3%</span>
</div>

<!-- Charts -->
<div role="img" aria-label="Unemployment Rate trend chart from 2020 to 2025">
  <!-- Chart content -->
</div>

<!-- Loading states -->
<div role="status" aria-live="polite" aria-label="Loading data">
  <!-- Skeleton or spinner -->
</div>
```

---

## Implementation Checklist

### Phase 1: Foundation (Do First)

- [ ] Set up CSS custom properties for all design tokens
- [ ] Import Urbanist font family
- [ ] Apply base typography scale
- [ ] Set up color palette variables
- [ ] Define spacing scale
- [ ] Define border radius scale

### Phase 2: Component Updates

- [ ] Update metric cards to match spec (sparkline, change indicator)
- [ ] Standardize chart styling (grid, axes, tooltips)
- [ ] Fix sidebar navigation states (hover, active)
- [ ] Add section headers with proper spacing
- [ ] Update button styles (primary, secondary, ghost)
- [ ] Standardize data tables (row height, borders, hover)

### Phase 3: Interactions

- [ ] Add 150ms transitions to all interactive elements
- [ ] Implement proper hover states (background, border, transform)
- [ ] Add keyboard focus outlines
- [ ] Replace spinners with skeleton screens
- [ ] Add page transition animations

### Phase 4: Responsive

- [ ] Test on mobile (< 768px)
- [ ] Test on tablet (768px - 1024px)
- [ ] Make sidebar collapsible on small screens
- [ ] Stack charts vertically on mobile
- [ ] Add horizontal scroll to tables on mobile

### Phase 5: Polish

- [ ] Add loading skeletons for all async content
- [ ] Implement keyboard shortcuts
- [ ] Add chart annotations for key events
- [ ] Add export/share functionality
- [ ] Optimize for accessibility (ARIA labels, focus management)

---

## Known Issues & Fixes

### Issue 1: Phantom Text in Sidebar

**Problem:** "keyb" and "key[Name]_right" text appearing on hover

**Root Cause:** React key props leaking into DOM as visible text nodes

**Fix:**
```tsx
// WRONG - key prop spreads into DOM
const props = { key: "keyb", ...otherProps };
return <div {...props}>Content</div>;

// CORRECT - key isolated
return <div key="keyb" {...otherProps}>Content</div>;
```

**Action:**
- Search codebase for `{...props}` patterns on DOM elements
- Ensure `key` prop is never spread
- Check animation library configuration (Framer Motion)

---

### Issue 2: Yahoo Finance API Failures

**Problem:** Market data (S&P 500, VIX) fails to load

**Root Cause:** yfinance library is a scraper that breaks when Yahoo changes their site

**Fix Options:**
1. Try with shorter time periods (1 year instead of 10)
2. Add error handling and continue without market data
3. Switch to alternative APIs (Alpha Vantage, Polygon.io)

**Recommendation:** Market data is nice-to-have. FRED economic data is the core value. Don't block on this.

---

### Issue 3: Health Check SQL Error

**Problem:** `/health` endpoint throws SQL syntax error

**Root Cause:** SQLAlchemy requires explicit `text()` wrapper

**Fix:**
```python
# WRONG
db.execute("SELECT 1")

# CORRECT
from sqlalchemy import text
db.execute(text("SELECT 1"))
```

---

## Version History

**v2.0** (January 23, 2026)
- Complete design system overhaul
- Added Urbanist typography
- Defined comprehensive color palette
- Created component library
- Added chart styling guidelines

**v1.0** (January 13, 2026)
- Initial dashboard with basic styling
- Dark theme with teal accents
- Basic Streamlit UI

---

## Contact & Feedback

**Maintained by:** Tony (tonyl@...)
**Last Review:** January 23, 2026
**Next Review:** As needed when adding new features

**To propose changes:**
1. Update this document
2. Get approval from Tony
3. Send updated file to Claude Code for implementation
4. Test on localhost
5. Deploy to production

---

## Quick Reference

### Most Common Tokens

```css
/* Spacing */
--space-sm: 8px;
--space-md: 16px;
--space-lg: 24px;

/* Colors */
--color-bg-secondary: #141414;
--color-text-primary: #ffffff;
--color-accent-primary: #14b8a6;

/* Typography */
--text-body: 14px;
--text-h2: 20px;
--text-metric-lg: 36px;

/* Transitions */
transition: all 150ms cubic-bezier(0.4, 0, 0.2, 1);
```

### Component Sizes

```
Metric Card: 120px min height
Sidebar: 240px width
Button: 40px height
Nav Item: 40px height
Table Row: 48px height
Chart: 400px height
```

---

**End of Design System Documentation**
