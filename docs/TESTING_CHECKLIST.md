# Sidebar Navigation - Manual Testing Checklist

**Date:** 2026-01-28  
**Purpose:** Comprehensive manual testing checklist for sidebar navigation implementation

---

## Pre-Testing Setup

- [ ] Django server is running
- [ ] Database migrations are applied
- [ ] User is logged in
- [ ] Browser cache is cleared
- [ ] Developer tools are open (for debugging)

---

## 1. Basic Navigation Structure

### 1.1 Sidebar Visibility

- [ ] Sidebar is visible on desktop (>= 768px)
- [ ] Sidebar is hidden by default on mobile (< 768px)
- [ ] Sidebar can be toggled on mobile via menu button
- [ ] Overlay appears when sidebar is open on mobile
- [ ] Sidebar closes when clicking overlay on mobile

### 1.2 Group Structure

- [ ] All 6 groups are visible: DOCUMENTATION, ANALYSIS, AI, AUTOMATION, MANAGEMENT, TOOLS & INFO
- [ ] Groups can be expanded/collapsed by clicking header
- [ ] Chevron rotates when group expands/collapses
- [ ] Group state persists after page refresh (localStorage)

### 1.3 Nested Items

- [ ] Items with children show chevron button
- [ ] Clicking chevron expands/collapses nested children
- [ ] Nested items are indented (ml-8)
- [ ] Nested items have smaller font size (text-xs)
- [ ] Nested items have smaller icons (w-4 h-4)

---

## 2. Static Pages in Sidebar

### 2.1 Documentation App

#### Pages Section

- [ ] "Pages" item is visible
- [ ] "Create Page" nested item is visible under Pages
- [ ] "Create Page" has "New" badge
- [ ] Clicking "Create Page" navigates to `/docs/pages/create/`
- [ ] Return URL is included in create form link

#### Endpoints Section

- [ ] "Endpoints" item is visible
- [ ] "Create Endpoint" nested item is visible under Endpoints
- [ ] "Create Endpoint" has "New" badge
- [ ] Clicking "Create Endpoint" navigates to `/docs/endpoints/create/`

#### Relationships Section

- [ ] "Relationships" item is visible
- [ ] "Create Relationship" nested item is visible under Relationships
- [ ] "Create Relationship" has "New" badge
- [ ] Clicking "Create Relationship" navigates to `/docs/relationships/create/`

### 2.2 Knowledge Base

- [ ] "Knowledge Base" item is visible
- [ ] "Create Knowledge Entry" nested item is visible
- [ ] "Create Knowledge Entry" has "New" badge
- [ ] Clicking navigates to `/knowledge/create/`

### 2.3 Tasks

- [ ] "Tasks" item is visible
- [ ] "Create Task" nested item is visible
- [ ] "Create Task" has "New" badge
- [ ] Clicking navigates to `/tasks/create/`

### 2.4 Postman

- [ ] "Postman" item is visible
- [ ] "Create Postman Config" nested item is visible
- [ ] "Create Postman Config" has "New" badge
- [ ] Clicking navigates to `/docs/postman/create/`

### 2.5 Automation

#### Workflows

- [ ] "Workflows" item is visible
- [ ] "Create Workflow" nested item is visible
- [ ] "New Editor" nested item is visible
- [ ] Both have appropriate badges/icons
- [ ] Clicking navigates to correct URLs

#### Credentials

- [ ] "Credentials" item is visible
- [ ] "Create Credential" nested item is visible
- [ ] "Create Credential" has "New" badge
- [ ] Clicking navigates to `/durgasflow/credential/create/`

### 2.6 Tools & Info Group

- [ ] "TOOLS & INFO" group is visible
- [ ] All 7 items are visible:
  - [ ] Architecture
  - [ ] Database Schema
  - [ ] Roadmap
  - [ ] Accessibility
  - [ ] Test Runner
  - [ ] Swagger UI
  - [ ] ReDoc
- [ ] All items navigate to correct URLs

---

## 3. Active State Detection

### 3.1 Dynamic Pages

- [ ] When on `/docs/` → "Documentation" is active
- [ ] When on `/docs/pages/list/` → "Pages" is active
- [ ] When on `/docs/endpoints/list/` → "Endpoints" is active
- [ ] When on `/tasks/` → "Tasks" is active
- [ ] When on `/knowledge/` → "Knowledge Base" is active
- [ ] When on `/durgasflow/workflows/` → "Workflows" is active

### 3.2 Static Pages (Forms)

- [ ] When on `/docs/pages/create/` → "Pages" parent is active, "Create Page" child is active
- [ ] When on `/docs/endpoints/create/` → "Endpoints" parent is active, "Create Endpoint" child is active
- [ ] When on `/docs/relationships/create/` → "Relationships" parent is active, "Create Relationship" child is active
- [ ] When on `/tasks/create/` → "Tasks" parent is active, "Create Task" child is active
- [ ] When on `/knowledge/create/` → "Knowledge Base" parent is active, "Create Knowledge Entry" child is active

### 3.3 Parameterized Routes

- [ ] When on `/docs/pages/<id>/edit/` → "Pages" parent is active (edit forms not in sidebar)
- [ ] When on `/docs/endpoints/<id>/edit/` → "Endpoints" parent is active
- [ ] When on `/docs/pages/<id>/delete/` → "Pages" parent is active (delete confirmations not in sidebar)

### 3.4 Info Pages

- [ ] When on `/architecture/` → "Architecture" is active
- [ ] When on `/database/` → "Database Schema" is active
- [ ] When on `/api/swagger/` → "Swagger UI" is active
- [ ] When on `/api/redoc/` → "ReDoc" is active

### 3.5 Active State Visual Indicators

- [ ] Active items have blue background (`bg-blue-50`)
- [ ] Active items have blue text (`text-blue-600`)
- [ ] Active items show blue dot indicator
- [ ] Active nested items have left border (`border-l-2`)
- [ ] Parent groups auto-expand when child is active

---

## 4. Return URL Functionality

### 4.1 Create Forms

- [ ] Clicking "Create Page" from sidebar includes return URL
- [ ] Return URL points back to list page
- [ ] After form submission, redirects to detail page
- [ ] Cancel button uses return URL to go back

### 4.2 Edit Forms (via detail pages)

- [ ] Edit forms accessed from detail pages preserve return URL
- [ ] Return URL points back to detail page
- [ ] After form submission, redirects back to detail page

---

## 5. Visual Hierarchy

### 5.1 Indentation

- [ ] Nested items are indented (32px / ml-8)
- [ ] Visual hierarchy is clear
- [ ] Parent-child relationship is obvious

### 5.2 Icons

- [ ] Icons are properly sized:
  - [ ] Group icons: 16px (w-4 h-4)
  - [ ] Link item icons: 20px (w-5 h-5)
  - [ ] Nested item icons: 16px (w-4 h-4)
- [ ] Icons change color based on state:
  - [ ] Default: Gray
  - [ ] Active: Blue
  - [ ] Static forms: Green
  - [ ] Info pages: Purple

### 5.3 Badges

- [ ] "New" badges are visible on create forms
- [ ] Badges are properly styled (green, rounded)
- [ ] Badges are positioned correctly (after label)

### 5.4 Colors

- [ ] Page type colors are applied:
  - [ ] Dynamic pages: Blue
  - [ ] Static forms: Green
  - [ ] Info pages: Purple

---

## 6. Expand/Collapse Functionality

### 6.1 Groups

- [ ] Groups can be expanded by clicking header
- [ ] Groups can be collapsed by clicking header again
- [ ] Chevron rotates smoothly (180deg)
- [ ] State persists in localStorage
- [ ] Groups auto-expand when they have active items

### 6.2 Nested Items

- [ ] Items with children can expand/collapse
- [ ] Chevron button is clickable
- [ ] Parent link still navigates (doesn't toggle)
- [ ] Nested children fade in smoothly
- [ ] State persists during session

---

## 7. Keyboard Navigation

### 7.1 Basic Navigation

- [ ] Tab key navigates through items
- [ ] Shift+Tab navigates backwards
- [ ] Enter/Space activates links
- [ ] Focus is visible (outline)

### 7.2 Arrow Keys

- [ ] Arrow Down moves to next item
- [ ] Arrow Up moves to previous item
- [ ] Arrow Right expands groups/children
- [ ] Arrow Left collapses groups/children
- [ ] Navigation wraps at ends

### 7.3 Special Keys

- [ ] Home key goes to first item
- [ ] End key goes to last item
- [ ] Escape closes sidebar on mobile

### 7.4 ARIA Support

- [ ] ARIA labels are present
- [ ] aria-expanded updates correctly
- [ ] aria-haspopup is set for items with children
- [ ] Screen reader announces state changes

---

## 8. Responsive Behavior

### 8.1 Desktop (>= 768px)

- [ ] Sidebar is always visible
- [ ] Sidebar width is 260px
- [ ] Sidebar is fixed position
- [ ] Content margin adjusts (ml-[260px])

### 8.2 Mobile (< 768px)

- [ ] Sidebar is hidden by default
- [ ] Menu button toggles sidebar
- [ ] Sidebar slides in from left
- [ ] Dark overlay appears
- [ ] Clicking overlay closes sidebar
- [ ] Escape key closes sidebar

### 8.3 Tablet (768px - 1023px)

- [ ] Sidebar behaves like desktop
- [ ] Layout is responsive
- [ ] Touch targets are adequate

---

## 9. Dark Mode

### 9.1 Colors

- [ ] Dark mode colors are applied
- [ ] Text is readable in dark mode
- [ ] Backgrounds are appropriate
- [ ] Active states are visible

### 9.2 Icons

- [ ] Icons are visible in dark mode
- [ ] Icon colors adapt to dark mode

### 9.3 Borders

- [ ] Borders are visible in dark mode
- [ ] Active borders are clear

---

## 10. Performance

### 10.1 Loading

- [ ] Sidebar loads quickly
- [ ] No layout shift
- [ ] Animations are smooth

### 10.2 Interactions

- [ ] Clicks respond immediately
- [ ] Hover effects are instant
- [ ] Transitions are smooth (200ms)

### 10.3 localStorage

- [ ] Expanded state persists
- [ ] No performance impact
- [ ] Works across tabs

---

## 11. Edge Cases

### 11.1 Missing Data

- [ ] Handles missing children gracefully
- [ ] Handles missing icons gracefully
- [ ] Handles missing URLs gracefully

### 11.2 Invalid Routes

- [ ] Handles 404 routes gracefully
- [ ] Handles invalid app_name gracefully
- [ ] Handles invalid url_name gracefully

### 11.3 Parameterized Routes

- [ ] Handles edit routes correctly
- [ ] Handles delete routes correctly
- [ ] Handles detail routes correctly

---

## 12. Integration Testing

### 12.1 Navigation Flow

- [ ] List → Create → Detail flow works
- [ ] Detail → Edit → Detail flow works
- [ ] Detail → Delete → List flow works
- [ ] Return URLs are preserved

### 12.2 Form Submission

- [ ] Create forms redirect correctly
- [ ] Edit forms redirect correctly
- [ ] Cancel buttons work correctly

### 12.3 Breadcrumb Integration

- [ ] Breadcrumbs match sidebar navigation
- [ ] Navigation context is preserved

---

## 13. Browser Compatibility

### 13.1 Chrome/Edge

- [ ] All features work
- [ ] Animations are smooth
- [ ] localStorage works

### 13.2 Firefox

- [ ] All features work
- [ ] Animations are smooth
- [ ] localStorage works

### 13.3 Safari

- [ ] All features work
- [ ] Animations are smooth
- [ ] localStorage works

---

## 14. Accessibility

### 14.1 Screen Readers

- [ ] Navigation is announced correctly
- [ ] State changes are announced
- [ ] Links are properly labeled

### 14.2 Keyboard Only

- [ ] All functionality accessible via keyboard
- [ ] Focus order is logical
- [ ] No keyboard traps

### 14.3 Visual

- [ ] Contrast ratios meet WCAG AA
- [ ] Focus indicators are visible
- [ ] Text is readable

---

## 15. Documentation

### 15.1 Code Documentation

- [ ] Navigation structure is documented
- [ ] Context processor is documented
- [ ] Templates are documented

### 15.2 User Documentation

- [ ] Navigation structure is clear
- [ ] How to add pages is documented
- [ ] Troubleshooting guide exists

---

## Test Results Summary

**Date Tested:** _______________  
**Tester:** _______________  
**Browser:** _______________  
**OS:** _______________  

### Summary

- **Total Tests:** 150+
- **Passed:** _____
- **Failed:** _____
- **Skipped:** _____

### Critical Issues

1. _________________________________
2. _________________________________
3. _________________________________

### Minor Issues

1. _________________________________
2. _________________________________
3. _________________________________

### Notes

_________________________________
_________________________________
_________________________________

---

**Last Updated:** 2026-01-28  
**Status:** Ready for Testing
