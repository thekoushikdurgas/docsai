# Sidebar Navigation UI Design Document

**Date:** 2026-01-28  
**Purpose:** Document UI design decisions for nested sidebar navigation

---

## Design Principles

1. **Visual Hierarchy:** Clear parent-child relationships through indentation
2. **Consistency:** Uniform styling across all navigation levels
3. **Accessibility:** Keyboard navigation and ARIA labels
4. **Responsiveness:** Mobile-friendly collapsible design
5. **Feedback:** Clear active states and hover effects

---

## Component Structure

### 1. Sidebar Container (`sidebar.html`)

```
<aside id="app-sidebar">
  ├── Header (Logo + Title)
  ├── Navigation (Groups)
  │   └── Group Items
  │       └── Link Items
  │           └── Nested Items (children)
  └── Footer (User info)
</aside>
```

**Styling:**

- Fixed position: `fixed left-0 top-0`
- Width: `260px` (w-[260px])
- Height: Full viewport height
- Background: White/Dark gray
- Border: Right border for separation
- Z-index: 30 (above content, below modals)

---

### 2. Group Item (`group_item.html`)

**Structure:**

```
<div class="sidebar-group">
  <button class="group-header">
    <icon> + <label> + <chevron>
  </button>
  <div class="group-items">
    <!-- Link items -->
  </div>
</div>
```

**Styling:**

- Header: Uppercase, bold, small text
- Chevron: Rotates 180deg when expanded
- Items: Spaced vertically (space-y-1)
- Auto-expand: When group has active items

**States:**

- **Collapsed:** Items hidden, chevron down
- **Expanded:** Items visible, chevron rotated
- **Active:** Group has active item (auto-expanded)

**JavaScript:**

- Toggle on header click
- Persist state in localStorage
- ARIA expanded attribute

---

### 3. Link Item (`link_item.html`)

**Structure:**

```
<div class="sidebar-link-item-wrapper">
  <div class="flex">
    <a href="...">
      <icon> + <label> + <badge> + <active-indicator>
    </a>
    <button class="chevron-button"> <!-- if has children -->
      <chevron-icon>
    </button>
  </div>
  <div class="nested-children"> <!-- if has children -->
    <!-- Nested items -->
  </div>
</div>
```

**Styling:**

- Padding: `px-4 py-3`
- Border radius: `rounded-xl`
- Gap: `gap-3` between icon and label
- Icon size: `w-5 h-5`
- Text size: `text-sm`

**States:**

- **Default:** Gray text, gray icon
- **Hover:** Darker text, background highlight
- **Active:** Blue background, blue text, blue dot indicator
- **With Children:** Chevron button on right

**Page Type Colors:**

- **Dynamic:** Blue (default)
- **Static Forms:** Green (`text-green-500`)
- **Info Pages:** Purple (`text-purple-500`)

**Badges:**

- Small rounded badge
- Green background for "New"
- Positioned after label

---

### 4. Nested Item (`nested_item.html`)

**Structure:**

```
<a href="..." class="nested-item">
  <icon> + <label> + <badge> + <active-indicator>
</a>
```

**Styling:**

- Indentation: `ml-8` (left margin)
- Padding: `px-4 py-2.5` (smaller than parent)
- Border radius: `rounded-lg` (smaller than parent)
- Icon size: `w-4 h-4` (smaller than parent)
- Text size: `text-xs` (smaller than parent)

**Active State:**

- Blue background: `bg-blue-50 dark:bg-blue-900/30`
- Blue text: `text-blue-600 dark:text-blue-400`
- Left border: `border-l-2 border-blue-600` (visual indicator)

**Page Type Colors:**

- Same as parent link items
- Green for static forms
- Purple for info pages

---

## Visual Hierarchy

### Level 1: Groups

- **Font:** Uppercase, bold, `text-xs`
- **Color:** Gray-400/500
- **Spacing:** `py-2` vertical padding

### Level 2: Link Items (Parent)

- **Font:** Medium, `text-sm`
- **Padding:** `px-4 py-3`
- **Icon:** `w-5 h-5`
- **Indentation:** None (base level)

### Level 3: Nested Items (Children)

- **Font:** Medium, `text-xs`
- **Padding:** `px-4 py-2.5`
- **Icon:** `w-4 h-4`
- **Indentation:** `ml-8` (32px left margin)

---

## Color Scheme

### Text Colors

**Default State:**

- Text: `text-gray-500 dark:text-gray-400`
- Icon: `text-gray-400 dark:text-gray-400`

**Hover State:**

- Text: `hover:text-gray-900 dark:hover:text-gray-100`
- Background: `hover:bg-gray-50 dark:hover:bg-gray-800`

**Active State:**

- Text: `text-blue-600 dark:text-blue-400`
- Background: `bg-blue-50 dark:bg-blue-900/30`
- Icon: `text-blue-600 dark:text-blue-400`

**Page Type Colors:**

- Static Forms: `text-green-500 dark:text-green-400`
- Info Pages: `text-purple-500 dark:text-purple-400`

### Background Colors

**Default:**

- Sidebar: `bg-white dark:bg-gray-900`
- Items: Transparent

**Hover:**

- Items: `bg-gray-50 dark:bg-gray-800`

**Active:**

- Items: `bg-blue-50 dark:bg-blue-900/30`

---

## Icons

### Icon Sizes

- Group icons: `w-4 h-4`
- Link item icons: `w-5 h-5`
- Nested item icons: `w-4 h-4`
- Chevron icons: `w-3 h-3` or `w-4 h-4`

### Icon Colors

- Default: Gray-400
- Hover: Gray-600
- Active: Blue-600
- Page type: Green-500 (static) or Purple-500 (info)

### Chevron Behavior

- **Collapsed:** Points down (0deg)
- **Expanded:** Points right (90deg) or down rotated (180deg)
- **Transition:** `transition-transform duration-200`

---

## Badges

### "New" Badge

- **Text:** "New"
- **Size:** `text-[10px]`
- **Padding:** `px-1.5 py-0.5`
- **Background:** `bg-green-100 dark:bg-green-900/30`
- **Text Color:** `text-green-700 dark:text-green-400`
- **Shape:** `rounded-full`
- **Position:** After label, before active indicator

---

## Active State Indicators

### Dot Indicator

- **Size:** `w-1.5 h-1.5`
- **Color:** `bg-blue-600 dark:bg-blue-400`
- **Shape:** `rounded-full`
- **Position:** Right side (`ml-auto`)

### Border Indicator (Nested Items)

- **Width:** `border-l-2`
- **Color:** `border-blue-600 dark:border-blue-400`
- **Position:** Left side
- **Only on:** Active nested items

---

## Spacing & Layout

### Vertical Spacing

- Between groups: `space-y-1` (4px)
- Between items: `space-y-1` (4px)
- Between nested items: `space-y-0.5` (2px)
- Group margin bottom: `mb-4` (16px)

### Horizontal Spacing

- Sidebar padding: `px-3` (12px)
- Item padding: `px-4` (16px)
- Nested item indentation: `ml-8` (32px)
- Icon-label gap: `gap-3` (12px)

### Container Spacing

- Sidebar top margin: `mt-6` (24px)
- Navigation max height: `max-h-[calc(100vh-200px)]`
- Footer position: `absolute bottom-0`

---

## Responsive Behavior

### Desktop (md and up)

- Sidebar: Always visible (`md:translate-x-0`)
- Width: Fixed 260px
- Position: Fixed left

### Mobile (below md)

- Sidebar: Hidden by default (`-translate-x-full`)
- Overlay: Dark overlay when open
- Toggle: Menu button in header
- Position: Fixed, slides in from left

### Breakpoints

- Mobile: `< 768px` (default)
- Desktop: `>= 768px` (md breakpoint)

---

## Animations & Transitions

### Transitions

- **Duration:** `duration-200` (200ms)
- **Easing:** `ease-out` or default
- **Properties:** All color, transform, opacity changes

### Transform Animations

- **Chevron rotation:** `rotate-90` or `rotate-180`
- **Sidebar slide:** `translate-x-full` to `translate-x-0`
- **Hover lift:** `hover:-translate-y-1` (optional)

### Fade Animations

- **Group items:** Fade in when expanded
- **Nested children:** Fade in when expanded

---

## Accessibility Features

### ARIA Attributes

- **Sidebar:** `aria-label="Main navigation"`
- **Groups:** `aria-expanded="true/false"`
- **Links:** Proper href attributes
- **Buttons:** `aria-label` for chevron buttons

### Keyboard Navigation

- **Tab:** Navigate through items
- **Enter/Space:** Activate link or toggle group
- **Arrow keys:** Navigate up/down (future enhancement)
- **Escape:** Close sidebar on mobile (future enhancement)

### Focus States

- **Visible focus:** Outline or ring on focus
- **Focus order:** Logical tab order
- **Skip links:** Skip to main content (in base template)

---

## Dark Mode Support

### Color Variants
All colors have dark mode variants:

- `dark:bg-gray-900` for backgrounds
- `dark:text-gray-100` for text
- `dark:border-gray-800` for borders
- `dark:bg-blue-900/30` for active states

### Theme Toggle

- Controlled by `data-theme` attribute on `<html>`
- Persisted in session/localStorage
- Applied via Tailwind dark mode

---

## Component States

### Group States

1. **Collapsed:** Items hidden, chevron down
2. **Expanded:** Items visible, chevron rotated
3. **Active:** Has active item (auto-expanded)

### Link Item States

1. **Default:** Gray text, transparent background
2. **Hover:** Darker text, gray background
3. **Active:** Blue text, blue background, blue dot
4. **With Children:** Chevron button visible

### Nested Item States

1. **Default:** Gray text, indented
2. **Hover:** Darker text, gray background
3. **Active:** Blue text, blue background, left border

---

## JavaScript Functionality

### Functions

#### `toggleSidebarGroup(button)`

- Toggles group expansion
- Updates chevron rotation
- Saves state to localStorage
- Updates ARIA attributes

#### `toggleNestedChildren(wrapper)`

- Toggles nested children visibility
- Updates chevron rotation
- Smooth animation

#### Auto-expand Logic

- Expands groups with active items
- Expands nested items with active children
- Runs on page load

### localStorage Keys

- Format: `sidebar_group_{GROUP_LABEL}`
- Values: `"expanded"` or `"collapsed"`
- Expires: Never (until cleared)

---

## Design Mockups

### Desktop View

```
┌─────────────────────────────┐
│  D  DocsAI                  │
├─────────────────────────────┤
│ ▼ DOCUMENTATION             │
│   📄 Documentation           │
│   📄 Pages              •    │
│     ➜ Create Page      NEW  │
│   📄 Endpoints              │
│     ➜ Create Endpoint  NEW  │
│   📄 Relationships          │
│     ➜ Create Relationship  │
│                             │
│ ▶ ANALYSIS                  │
│                             │
│ ▶ AI                        │
└─────────────────────────────┘
```

### Mobile View

```
┌─────────────────────────────┐
│ [☰] DocsAI                 │
├─────────────────────────────┤
│                             │
│  [Sidebar slides in]        │
│  [Dark overlay behind]      │
│                             │
└─────────────────────────────┘
```

---

## Implementation Notes

### CSS Classes Used

- Tailwind utility classes
- Custom classes: `custom-scrollbar`, `sidebar-group`, `sidebar-link-item-wrapper`
- Dark mode: All classes have `dark:` variants

### Template Structure

- Django template inheritance
- Component includes for reusability
- Conditional rendering for nested items

### Performance Considerations

- Minimal JavaScript (vanilla JS)
- CSS transitions (GPU accelerated)
- localStorage for state (fast access)
- No heavy libraries

---

## Future Enhancements

1. **Keyboard Navigation:**
   - Arrow keys for navigation
   - Enter to activate
   - Escape to close

2. **Search:**
   - Search box in sidebar
   - Filter navigation items
   - Highlight matches

3. **Favorites:**
   - Star items to pin to top
   - Custom ordering
   - Quick access section

4. **Tooltips:**
   - Hover tooltips for truncated labels
   - Help text for complex items

5. **Animations:**
   - Smooth slide animations
   - Stagger animations for children
   - Loading states

---

**Last Updated:** 2026-01-28  
**Status:** Design Complete, Implementation In Progress
