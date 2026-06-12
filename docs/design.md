# Design System Documentation

## Overview

This design system is built around the color **#EDFaff**, creating a clean, modern, airy, and trustworthy visual identity suitable for SaaS platforms, AI products, dashboards, developer tools, and enterprise applications.

### Design Principles

* Minimal and uncluttered interfaces
* High readability
* Consistent spacing and typography
* Accessible color contrast
* Responsive-first design
* Modern glassmorphism-inspired aesthetics
* Smooth and subtle animations

---

# Color Palette

## Primary Colors

| Name               | Hex     | Usage                       |
| ------------------ | ------- | --------------------------- |
| Primary Background | #EDFaff | Main application background |
| Primary Blue       | #38BDF8 | Buttons, links, highlights  |
| Primary Hover      | #0284C7 | Hover states                |
| Secondary Blue     | #B8EFFF | Cards, secondary elements   |
| Accent Blue        | #7DD3FC | Notifications, badges       |

---

## Neutral Colors

| Name      | Hex     | Usage                |
| --------- | ------- | -------------------- |
| White     | #FFFFFF | Cards and surfaces   |
| Slate 900 | #0F172A | Primary text         |
| Slate 700 | #334155 | Secondary text       |
| Slate 500 | #64748B | Muted text           |
| Border    | #D6F4FF | Borders and dividers |

---

## Semantic Colors

### Success

* #22C55E

### Warning

* #F59E0B

### Error

* #EF4444

### Info

* #38BDF8

---

# Typography

## Font Family

Primary:

```css
font-family:
  Inter,
  -apple-system,
  BlinkMacSystemFont,
  "Segoe UI",
  sans-serif;
```

---

## Font Scale

### Heading 1

```css
font-size: 48px;
font-weight: 700;
line-height: 56px;
```

### Heading 2

```css
font-size: 36px;
font-weight: 700;
line-height: 44px;
```

### Heading 3

```css
font-size: 30px;
font-weight: 600;
line-height: 38px;
```

### Heading 4

```css
font-size: 24px;
font-weight: 600;
line-height: 32px;
```

### Body Large

```css
font-size: 18px;
line-height: 28px;
font-weight: 400;
```

### Body

```css
font-size: 16px;
line-height: 24px;
font-weight: 400;
```

### Small Text

```css
font-size: 14px;
line-height: 20px;
font-weight: 400;
```

---

# Spacing System

Use an 8px grid system.

| Token | Value |
| ----- | ----- |
| xs    | 4px   |
| sm    | 8px   |
| md    | 16px  |
| lg    | 24px  |
| xl    | 32px  |
| 2xl   | 48px  |
| 3xl   | 64px  |
| 4xl   | 96px  |

---

# Border Radius

| Token  | Value  |
| ------ | ------ |
| Small  | 8px    |
| Medium | 12px   |
| Large  | 16px   |
| XL     | 24px   |
| Full   | 9999px |

---

# Shadows

## Card Shadow

```css
box-shadow:
0 4px 12px rgba(15,23,42,0.05);
```

## Elevated Shadow

```css
box-shadow:
0 10px 25px rgba(15,23,42,0.08);
```

## Modal Shadow

```css
box-shadow:
0 25px 50px rgba(15,23,42,0.12);
```

---

# Components

## Primary Button

### Default

Background:

```css
#38BDF8
```

Text:

```css
#FFFFFF
```

Border Radius:

```css
12px
```

Padding:

```css
12px 24px
```

Hover:

```css
#0284C7
```

---

## Secondary Button

Background:

```css
#FFFFFF
```

Border:

```css
1px solid #D6F4FF
```

Text:

```css
#0F172A
```

---

## Cards

Background:

```css
#FFFFFF
```

Border:

```css
1px solid #D6F4FF
```

Radius:

```css
16px
```

Shadow:

```css
0 4px 12px rgba(15,23,42,0.05)
```

---

## Input Fields

Background:

```css
#FFFFFF
```

Border:

```css
1px solid #D6F4FF
```

Focus:

```css
2px solid #38BDF8
```

Height:

```css
48px
```

Radius:

```css
12px
```

---

# Glassmorphism Style

## Glass Card

```css
background: rgba(255,255,255,0.6);
backdrop-filter: blur(16px);
border: 1px solid rgba(255,255,255,0.4);
```

---

# Gradients

## Ocean Sky

```css
background:
linear-gradient(
135deg,
#EDFaff 0%,
#B8EFFF 50%,
#4FC3F7 100%
);
```

## Premium Ice

```css
background:
linear-gradient(
135deg,
#EDFaff 0%,
#D7F5FF 40%,
#7DD3FC 100%
);
```

---

# Animation Guidelines

### Transition

```css
transition:
all 0.2s ease;
```

### Hover Scale

```css
transform: scale(1.02);
```

### Card Hover

```css
transform: translateY(-2px);
```

---

# Accessibility

* Minimum contrast ratio: 4.5:1
* Keyboard navigable components
* Visible focus states
* ARIA support
* Responsive typography
* Touch targets minimum 44px

---

# CSS Variables

```css
:root {
  --background: #EDFaff;
  --surface: #FFFFFF;

  --primary: #38BDF8;
  --primary-hover: #0284C7;

  --secondary: #B8EFFF;
  --accent: #7DD3FC;

  --success: #22C55E;
  --warning: #F59E0B;
  --error: #EF4444;

  --text-primary: #0F172A;
  --text-secondary: #64748B;

  --border: #D6F4FF;
}
```

---

# Recommended Usage

Best suited for:

* AI Products
* SaaS Platforms
* Dashboards
* Admin Panels
* Developer Tools
* Productivity Applications
* Enterprise Software
* Analytics Platforms

The design system aims to provide a modern, trustworthy, lightweight, and highly scalable user experience while maintaining excellent readability and accessibility.
