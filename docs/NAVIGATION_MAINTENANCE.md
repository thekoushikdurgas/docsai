# Navigation Maintenance Guide

**Date:** 2026-01-28  
**Purpose:** Guide for maintaining and updating sidebar navigation

---

## Quick Reference

### Files to Modify

1. **Navigation Config:** `apps/core/navigation.py`
2. **Context Processor:** `apps/core/context_processors.py` (rarely)
3. **Templates:** `templates/components/sidebar/*.html` (rarely)
4. **Styles:** `static/css/components/sidebar.css` (rarely)
5. **JavaScript:** `static/js/components/sidebar-keyboard.js` (rarely)

---

## Common Tasks

### Task 1: Add a New Page to Sidebar

#### Step 1: Determine Page Type

- **Dynamic:** List, dashboard, detail page → Add as main item
- **Static:** Create form → Add as child of parent list
- **Info:** Documentation, info page → Add to appropriate group

#### Step 2: Add to Navigation Config

**For Dynamic Page:**
```python
# In apps/core/navigation.py, find appropriate group
{
    "label": "New Page",
    "app_name": "app_name",
    "url_name": "url_name",
    "page_type": "dynamic",
    "access_via": "direct",
    "icon": '<path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="..." />'
}
```

**For Static Form (Create):**
```python
# Add as child of parent list item
{
    "label": "Parent List",
    "app_name": "app_name",
    "url_name": "list",
    "page_type": "dynamic",
    "access_via": "direct",
    "icon": "...",
    "children": [
        {
            "label": "Create New Item",
            "app_name": "app_name",
            "url_name": "create",
            "page_type": "static",
            "access_via": "via_list",
            "redirect_target": "detail",
            "badge": "New",
            "icon": '<path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M12 4v16m8-8H4" />'
        }
    ]
}
```

#### Step 3: Verify URL Exists

```python
# In app's urls.py
path('new-page/', views.new_page_view, name='url_name'),
```

#### Step 4: Test

- Navigate to the page
- Check sidebar item appears
- Verify active state works
- Test navigation

---

### Task 2: Add a New Group

#### Step 1: Add Group to Navigation Config

```python
# In apps/core/navigation.py, add new group to SIDEBAR_MENU
{
    "label": "NEW_GROUP",
    "icon": '<path ... />',
    "items": [
        # Add items here
    ]
}
```

#### Step 2: Choose Icon

- Use Heroicons or similar icon set
- SVG path format
- Consistent style with other groups

#### Step 3: Test

- Verify group appears in sidebar
- Test expand/collapse
- Verify styling

---

### Task 3: Remove a Page from Sidebar

#### Step 1: Remove from Navigation Config

```python
# In apps/core/navigation.py
# Remove the item from appropriate group's items array
```

#### Step 2: Check Dependencies

- Ensure no other code references the removed item
- Check if it's a parent of nested items (remove children too)

#### Step 3: Test

- Verify item no longer appears
- Check for broken links
- Test navigation flow

---

### Task 4: Reorder Navigation Items

#### Step 1: Reorder in Navigation Config

```python
# In apps/core/navigation.py
# Reorder items in the items array
# Reorder groups in SIDEBAR_MENU array
```

#### Step 2: Test

- Verify new order appears correctly
- Test all navigation still works

---

### Task 5: Change Page Icon

#### Step 1: Update Icon in Navigation Config

```python
{
    "label": "Page Name",
    "icon": '<path ... NEW_ICON_PATH ... />',  # Update here
    # ... rest of config
}
```

#### Step 2: Test

- Verify new icon appears
- Check icon size and color
- Verify dark mode compatibility

---

### Task 6: Add/Remove Badge

#### Step 1: Update Badge Field

```python
{
    "label": "Create Page",
    "badge": "New",  # Add or remove this field
    # ... rest of config
}
```

#### Step 2: Test

- Verify badge appears/disappears
- Check badge styling
- Verify positioning

---

## Advanced Tasks

### Task 7: Custom Active State Logic

#### When Needed

- Custom route matching
- Complex parameterized routes
- Special cases

#### Implementation

Edit `apps/core/context_processors.py`:

```python
def _is_item_active(item, current_app, current_url, request_path):
    # Add custom logic here
    if item.get('custom_match'):
        # Custom matching logic
        return custom_match_function(item, current_app, current_url)
    
    # Default logic
    return default_match_logic(item, current_app, current_url, request_path)
```

---

### Task 8: Custom Return URL Logic

#### When Needed

- Complex redirect flows
- Conditional redirects
- Multiple return paths

#### Implementation

Edit `apps/core/context_processors.py`:

```python
def _process_item_children(...):
    # Custom return URL generation
    if child_copy.get('custom_return_url'):
        child_copy['url_with_return'] = generate_custom_return_url(...)
    else:
        # Default logic
        child_copy['url_with_return'] = generate_default_return_url(...)
```

---

### Task 9: Add Conditional Items

#### When Needed

- Role-based navigation
- Feature flags
- User permissions

#### Implementation

Edit `apps/core/context_processors.py`:

```python
def navigation(request):
    # Filter items based on conditions
    processed_menu = []
    for group in SIDEBAR_MENU:
        filtered_items = [
            item for item in group['items']
            if should_show_item(item, request.user)
        ]
        # Process filtered items
        ...
```

---

## Troubleshooting

### Problem: Item Not Appearing

**Checklist:**

1. ✅ Added to `SIDEBAR_MENU` in `navigation.py`
2. ✅ Syntax is correct (no missing commas, brackets)
3. ✅ `app_name` and `url_name` exist in URL config
4. ✅ No JavaScript errors in console
5. ✅ Template is rendering correctly

**Debug Steps:**
```python
# Add debug logging to context processor
logger.debug(f"Processing menu: {SIDEBAR_MENU}")
logger.debug(f"Current app: {current_app}, URL: {current_url}")
```

---

### Problem: Active State Not Working

**Checklist:**

1. ✅ URL name matches exactly
2. ✅ App name matches exactly
3. ✅ Context processor is processing item
4. ✅ Template is checking `item.active`

**Debug Steps:**
```python
# In context processor, add logging
logger.debug(f"Checking item: {item['label']}")
logger.debug(f"Current: app={current_app}, url={current_url}")
logger.debug(f"Item: app={item.get('app_name')}, url={item.get('url_name')}")
logger.debug(f"Is active: {is_active}")
```

---

### Problem: Nested Items Not Showing

**Checklist:**

1. ✅ `children` array exists and is not empty
2. ✅ Template is checking for `item.children`
3. ✅ JavaScript is not hiding children
4. ✅ CSS is not hiding children

**Debug Steps:**
```html
<!-- In template, add debug -->
{% if item.children %}
    <!-- Children exist: {{ item.children|length }} -->
{% endif %}
```

---

### Problem: Return URL Not Working

**Checklist:**

1. ✅ Return URL is generated in context processor
2. ✅ Form view accepts `return_url` parameter
3. ✅ Form redirects using return URL
4. ✅ URL is properly encoded

**Debug Steps:**
```python
# In form view
return_url = request.GET.get('return_url')
logger.debug(f"Return URL: {return_url}")
```

---

## Code Examples

### Example 1: Adding a New App Section

```python
# In apps/core/navigation.py

SIDEBAR_MENU = [
    # ... existing groups ...
    {
        "label": "NEW_APP",
        "icon": '<path ... />',
        "items": [
            {
                "label": "Dashboard",
                "app_name": "new_app",
                "url_name": "dashboard",
                "page_type": "dynamic",
                "access_via": "direct",
                "icon": '<path ... />'
            },
            {
                "label": "Items",
                "app_name": "new_app",
                "url_name": "list",
                "page_type": "dynamic",
                "access_via": "direct",
                "icon": '<path ... />',
                "children": [
                    {
                        "label": "Create Item",
                        "app_name": "new_app",
                        "url_name": "create",
                        "page_type": "static",
                        "access_via": "via_list",
                        "redirect_target": "detail",
                        "badge": "New",
                        "icon": '<path d="M12 4v16m8-8H4" />'
                    }
                ]
            }
        ]
    }
]
```

---

### Example 2: Modifying Existing Item

```python
# Find the item in navigation.py
{
    "label": "Pages",
    "app_name": "documentation",
    "url_name": "pages_list",
    "page_type": "dynamic",
    "access_via": "direct",
    "icon": '<path ... />',
    "children": [
        {
            "label": "Create Page",
            # ... existing config ...
            "badge": None,  # Remove badge
            # Or add new child:
        },
        {
            "label": "Import Pages",  # New child
            "app_name": "documentation",
            "url_name": "pages_import",
            "page_type": "static",
            "access_via": "via_list",
            "icon": '<path d="M7 16a4 4 0 01-.88-7.903A5 5 0 1115.9 6L16 6a5 5 0 011 9.9M15 13l-3-3m0 0l-3 3m3-3v12" />'
        }
    ]
}
```

---

### Example 3: Conditional Item Display

```python
# In apps/core/context_processors.py

def should_show_item(item, user):
    """Determine if item should be shown based on user permissions."""
    # Check for permission requirement
    if item.get('requires_permission'):
        return user.has_perm(item['requires_permission'])
    
    # Check for feature flag
    if item.get('feature_flag'):
        return getattr(settings, item['feature_flag'], False)
    
    # Check for role requirement
    if item.get('requires_role'):
        return user.role == item['requires_role']
    
    return True

def navigation(request):
    # ... existing code ...
    for group in SIDEBAR_MENU:
        filtered_items = [
            item for item in group['items']
            if should_show_item(item, request.user)
        ]
        # Process filtered_items instead of group['items']
        ...
```

---

## Testing Checklist

After making changes, test:

- [ ] Item appears in sidebar
- [ ] Item navigates correctly
- [ ] Active state works
- [ ] Nested items expand/collapse
- [ ] Return URLs work (for forms)
- [ ] Keyboard navigation works
- [ ] Responsive behavior works
- [ ] Dark mode works
- [ ] No console errors
- [ ] No broken links

---

## Version History

### v2.0 (2026-01-28)

- Added nested item support
- Added static pages to sidebar
- Enhanced active state detection
- Added return URL support
- Added keyboard navigation
- Added visual hierarchy styling

### v1.0 (Previous)

- Flat navigation structure
- Basic active state detection
- No nested items

---

## Support

### Getting Help

1. Check this guide first
2. Review [Navigation Structure](NAVIGATION_STRUCTURE.md)
3. Check [Testing Checklist](TESTING_CHECKLIST.md)
4. Review code examples above
5. Check Django URL configuration

### Common Issues

See [Troubleshooting](#troubleshooting) section above.

---

**Last Updated:** 2026-01-28  
**Maintainer:** Development Team
