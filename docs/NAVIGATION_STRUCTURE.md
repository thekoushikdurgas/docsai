# Navigation Structure Documentation

**Date:** 2026-01-28  
**Version:** 2.0  
**Status:** Complete

---

## Overview

The sidebar navigation system provides a hierarchical, nested structure for organizing both dynamic and static pages. It supports parent-child relationships, active state detection, and return URL preservation.

---

## Architecture

### Components

1. **Navigation Configuration** (`apps/core/navigation.py`)
   - Defines menu structure
   - Contains all navigation items
   - Supports nested children

2. **Context Processor** (`apps/core/context_processors.py`)
   - Processes menu for templates
   - Detects active states
   - Generates return URLs

3. **Templates:**
   - `templates/layouts/sidebar.html` - Main sidebar container
   - `templates/components/sidebar/group_item.html` - Group rendering
   - `templates/components/sidebar/link_item.html` - Link item rendering
   - `templates/components/sidebar/nested_item.html` - Nested item rendering

4. **Styles:**
   - `static/css/components/sidebar.css` - Visual hierarchy styling

5. **JavaScript:**
   - `static/js/components/sidebar-keyboard.js` - Keyboard navigation

---

## Navigation Structure

### Data Model

```python
{
    "label": "GROUP_LABEL",           # Uppercase group name
    "icon": "<svg_path>",              # SVG icon path
    "items": [
        {
            "label": "Item Label",     # Display name
            "app_name": "app_name",    # Django app name
            "url_name": "url_name",    # URL name for reverse()
            "page_type": "dynamic",    # dynamic | static | info
            "access_via": "direct",    # direct | via_detail | via_list
            "icon": "<svg_path>",      # SVG icon path
            "children": [               # Optional nested items
                {
                    "label": "Child Label",
                    "app_name": "app_name",
                    "url_name": "url_name",
                    "page_type": "static",
                    "access_via": "via_list",
                    "redirect_target": "detail",
                    "badge": "New",     # Optional badge
                    "icon": "<svg_path>"
                }
            ]
        }
    ]
}
```

---

## Navigation Groups

### 1. DOCUMENTATION
**Purpose:** Documentation management and API reference

**Items:**
- Documentation (dashboard)
- Pages (list) → Create Page (form)
- Endpoints (list) → Create Endpoint (form)
- Relationships (list) → Create Relationship (form)
- Knowledge Base (list) → Create Knowledge Entry (form)
- API Documentation (info page)

---

### 2. ANALYSIS
**Purpose:** Code analysis and analytics

**Items:**
- Codebase (dashboard)
- Analytics (dashboard)

---

### 3. AI
**Purpose:** AI assistant features

**Items:**
- AI Assistant (chat interface)
- Sessions (list)

---

### 4. AUTOMATION
**Purpose:** Workflow automation

**Items:**
- Workflows (list) → Create Workflow (form), New Editor (editor)
- Executions (list)
- Credentials (list) → Create Credential (form)

---

### 5. MANAGEMENT
**Purpose:** Task and API management

**Items:**
- Tasks (list) → Create Task (form)
- Postman (dashboard) → Create Postman Config (form)

---

### 6. TOOLS & INFO
**Purpose:** System tools and information

**Items:**
- Architecture (info)
- Database Schema (info)
- Roadmap (info)
- Accessibility (info)
- Test Runner (dashboard)
- Swagger UI (info)
- ReDoc (info)

---

## Page Types

### Dynamic Pages
- **Definition:** Data-driven pages that load content from services
- **Examples:** Dashboards, lists, detail pages
- **Color:** Blue
- **Icon Size:** 20px (w-5 h-5)

### Static Pages
- **Definition:** Static structure pages (forms, confirmations)
- **Examples:** Create forms, edit forms, delete confirmations
- **Color:** Green
- **Icon Size:** 16px (w-4 h-4)
- **Note:** Only create forms are in sidebar

### Info Pages
- **Definition:** Information/documentation pages
- **Examples:** Architecture, database schema, API docs
- **Color:** Purple
- **Icon Size:** 20px (w-5 h-5)

---

## Access Patterns

### Direct Access
- **Definition:** Accessible directly from sidebar
- **Examples:** All list pages, dashboards, info pages
- **Usage:** Click sidebar link → Navigate directly

### Via List
- **Definition:** Accessed from list page (create forms)
- **Examples:** Create Page, Create Endpoint, Create Task
- **Usage:** List page → "Create" button → Form (also in sidebar)
- **Return URL:** Points back to list page

### Via Detail
- **Definition:** Accessed from detail page (edit/delete)
- **Examples:** Edit Page, Delete Page, Edit Endpoint
- **Usage:** Detail page → "Edit"/"Delete" button → Form/Confirmation
- **Return URL:** Points back to detail page
- **Note:** NOT in sidebar (accessed via detail page buttons)

---

## Active State Detection

### Rules

1. **Exact Match:**
   - `current_app == item.app_name AND current_url == item.url_name`
   - Item is marked active

2. **Pattern Match:**
   - `current_app == item.app_name AND url_name in current_url`
   - Used for parameterized routes (e.g., `page_edit` in `/pages/<id>/edit/`)

3. **Parent-Child:**
   - If child is active → parent is also active
   - Parent group auto-expands

4. **URL Match:**
   - For items with direct `url` field
   - `request.path_info == item.url`

### Active State Indicators

- **Background:** Blue (`bg-blue-50 dark:bg-blue-900/30`)
- **Text:** Blue (`text-blue-600 dark:text-blue-400`)
- **Dot:** Blue dot indicator on right
- **Border:** Left border for nested items (`border-l-2`)

---

## Return URL Handling

### Generation

Return URLs are generated in the context processor:

```python
# For create forms
return_url = reverse(f"{current_app}:{current_url}")
url_with_return = f"{form_url}?return_url={return_url}"
```

### Usage

1. **Create Forms:**
   - Return URL points to list page
   - After creation → Redirects to detail page
   - Cancel → Uses return URL to go back

2. **Edit Forms:**
   - Return URL preserved from detail page
   - After update → Redirects back to detail page
   - Cancel → Uses return URL to go back

---

## Adding New Pages

### Step 1: Add to Navigation Config

Edit `apps/core/navigation.py`:

```python
{
    "label": "New Section",
    "app_name": "app_name",
    "url_name": "url_name",
    "page_type": "dynamic",  # or "static" or "info"
    "access_via": "direct",
    "icon": '<path ... />',
    "children": [  # Optional
        {
            "label": "Create New Item",
            "app_name": "app_name",
            "url_name": "create",
            "page_type": "static",
            "access_via": "via_list",
            "redirect_target": "detail",
            "badge": "New",
            "icon": '<path ... />'
        }
    ]
}
```

### Step 2: Ensure URL Pattern Exists

Make sure the URL is defined in the app's `urls.py`:

```python
path('new-section/', views.new_section_view, name='url_name'),
```

### Step 3: Test Active State

- Navigate to the page
- Check if sidebar item is highlighted
- Verify parent is active if it's a nested item

---

## Troubleshooting

### Issue: Item Not Showing in Sidebar

**Possible Causes:**
1. Not added to `SIDEBAR_MENU` in `navigation.py`
2. Syntax error in navigation config
3. Missing `app_name` or `url_name`

**Solution:**
- Check `apps/core/navigation.py` for syntax errors
- Verify `app_name` and `url_name` match URL configuration
- Check browser console for JavaScript errors

---

### Issue: Active State Not Working

**Possible Causes:**
1. URL name mismatch
2. App name mismatch
3. Context processor not processing correctly

**Solution:**
- Verify `current_app` and `current_url` in context
- Check URL resolution in Django
- Add debug logging to context processor

---

### Issue: Nested Items Not Expanding

**Possible Causes:**
1. JavaScript not loaded
2. `expanded` state not set
3. CSS hiding children

**Solution:**
- Check browser console for JavaScript errors
- Verify `expanded` attribute in context
- Check CSS for `.hidden` class

---

### Issue: Return URL Not Working

**Possible Causes:**
1. Return URL not generated
2. Form not using return URL
3. Redirect logic incorrect

**Solution:**
- Check context processor return URL generation
- Verify form view uses `return_url` parameter
- Check redirect logic in form submission

---

## Best Practices

### 1. Organization
- Group related items together
- Use clear, descriptive labels
- Maintain consistent icon style

### 2. Nested Items
- Only nest when there's a clear parent-child relationship
- Limit nesting depth (max 2 levels)
- Use badges sparingly

### 3. Active States
- Ensure parent is active when child is active
- Auto-expand groups with active items
- Provide clear visual feedback

### 4. Performance
- Keep navigation config simple
- Avoid deep nesting
- Cache processed menu if needed

### 5. Accessibility
- Use proper ARIA labels
- Support keyboard navigation
- Provide focus indicators

---

## API Reference

### Context Processor: `navigation(request)`

**Returns:**
```python
{
    'current_view': str,        # Current URL name
    'current_app': str,         # Current app name
    'sidebar_menu': list,       # Processed menu with active states
    'user': User,               # Current user
}
```

**Sidebar Menu Structure:**
```python
[
    {
        'label': str,
        'icon': str,
        'active': bool,
        'expanded': bool,
        'items': [
            {
                'label': str,
                'app_name': str,
                'url_name': str,
                'page_type': str,
                'access_via': str,
                'active': bool,
                'expanded': bool,
                'children': [...],
                'url_with_return': str,  # Optional
            }
        ]
    }
]
```

---

## Migration Guide

### From Flat to Nested Structure

**Before:**
```python
{
    "label": "Pages",
    "app_name": "documentation",
    "url_name": "pages_list",
    "icon": "..."
}
```

**After:**
```python
{
    "label": "Pages",
    "app_name": "documentation",
    "url_name": "pages_list",
    "page_type": "dynamic",
    "access_via": "direct",
    "icon": "...",
    "children": [
        {
            "label": "Create Page",
            "app_name": "documentation",
            "url_name": "page_create",
            "page_type": "static",
            "access_via": "via_list",
            "redirect_target": "page_detail",
            "badge": "New",
            "icon": "..."
        }
    ]
}
```

---

## Examples

### Example 1: Simple Dynamic Page

```python
{
    "label": "Analytics",
    "app_name": "analytics",
    "url_name": "dashboard",
    "page_type": "dynamic",
    "access_via": "direct",
    "icon": '<path ... />'
}
```

### Example 2: Dynamic Page with Create Form

```python
{
    "label": "Tasks",
    "app_name": "tasks",
    "url_name": "list",
    "page_type": "dynamic",
    "access_via": "direct",
    "icon": '<path ... />',
    "children": [
        {
            "label": "Create Task",
            "app_name": "tasks",
            "url_name": "create",
            "page_type": "static",
            "access_via": "via_list",
            "redirect_target": "detail",
            "badge": "New",
            "icon": '<path d="M12 4v16m8-8H4" />'
        }
    ]
}
```

### Example 3: Info Page with Direct URL

```python
{
    "label": "Swagger UI",
    "url": "/api/swagger/",
    "page_type": "info",
    "access_via": "direct",
    "icon": '<path ... />',
    "external": False
}
```

---

## Related Documentation

- [Sidebar Implementation Summary](SIDEBAR_IMPLEMENTATION_SUMMARY.md)
- [Static Pages Mapping](SIDEBAR_STATIC_PAGES_MAPPING.md)
- [UI Design Document](SIDEBAR_UI_DESIGN.md)
- [Testing Checklist](TESTING_CHECKLIST.md)

---

**Last Updated:** 2026-01-28  
**Maintainer:** Development Team
