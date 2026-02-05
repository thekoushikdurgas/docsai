# Page Usage by User Type - Implementation Complete ✅

## Summary

Successfully implemented comprehensive endpoint usage tracking by user type with interactive graph visualization in the DocsAI contact360 project.

## What Was Built

### 1. **Backend Infrastructure** 🔧
- Extended API tracking storage to record per-user-type statistics
- Modified middleware to extract user_type from requests (header/session/user object)
- Created new API endpoint `/api/v1/docs/endpoint-stats-by-user-type/`
- Maintained backward compatibility with existing global tracking

### 2. **Frontend Visualization** 📊
- Created D3.js graph component with three view modes:
  - **Grouped Bar Chart**: Side-by-side comparison
  - **Stacked Bar Chart**: Proportional view
  - **Heatmap**: Compact matrix view
- Interactive features: tooltips, legend toggle, view switching
- Fully responsive with dark mode support

### 3. **Integration** 🔗
- Updated `/api/docs/` page to display usage graph
- Added summary cards showing requests per user type
- Redirected old `/docs/docs/endpoint-stats/` to new page
- Updated view to fetch and pass user_type statistics

## Files Modified

### Backend
1. `apps/documentation/utils/api_tracking_storage.py` - Extended tracking
2. `apps/documentation/middleware/api_tracking_middleware.py` - User type extraction
3. `apps/documentation/api/v1/docs_meta.py` - New endpoint
4. `apps/documentation/api/v1/urls.py` - Route registration
5. `apps/documentation/views/api_docs.py` - Stats integration
6. `apps/documentation/urls.py` - Redirect update

### Frontend
7. `static/js/components/endpoint-stats-graph.js` - **NEW** Graph component
8. `templates/documentation/api_docs/index.html` - Graph integration

## Key Features

✅ **Multiple User Types**: super_admin, admin, pro_user, free_user, guest  
✅ **Flexible Detection**: Header > Session > User Object > Inferred > Default  
✅ **Three Chart Types**: Grouped bars, stacked bars, heatmap  
✅ **Interactive**: Click legend to toggle, hover for details  
✅ **Responsive**: Works on mobile, tablet, desktop  
✅ **Dark Mode**: Adapts to theme changes  
✅ **Performance**: Redis-based, 30-day TTL  
✅ **Backward Compatible**: Old tracking continues to work  

## How to Use

### For Developers

1. **Track user type in requests**:
   ```javascript
   fetch('/api/v1/pages/', {
       headers: {
           'X-User-Type': 'admin'  // or super_admin, pro_user, free_user, guest
       }
   });
   ```

2. **View statistics**:
   - Navigate to `http://localhost:8000/api/docs/`
   - See "Page Usage by User Type" graph
   - Switch between Grouped/Stacked/Heatmap views
   - Click legend items to show/hide user types

3. **Access API directly**:
   ```bash
   curl http://localhost:8000/api/v1/docs/endpoint-stats-by-user-type/
   
   # With filters
   curl http://localhost:8000/api/v1/docs/endpoint-stats-by-user-type/?user_type=admin&limit=10
   
   # Graph-optimized format
   curl http://localhost:8000/api/v1/docs/endpoint-stats-by-user-type/?format=graph
   ```

### For System Administrators

**Settings** (in `config/settings/base.py`):
```python
API_TRACKING_ENABLED = True  # Enable/disable all tracking
API_TRACKING_USER_TYPE_ENABLED = True  # Enable/disable user type tracking
API_TRACKING_PATH_PREFIX = '/api/v1/'  # Which paths to track
```

**Redis Keys**:
- Global: `api_tracking:count:{endpoint_key}`
- Per user: `api_tracking:count:{endpoint_key}:{user_type}`
- TTL: 30 days (configurable via `DEFAULT_TTL`)

## User Type Detection Priority

The middleware extracts user_type in this order:

1. **X-User-Type header** (explicit from frontend) - Highest priority
2. **Session data** (`request.session['user_type']`)
3. **User object** (`request.user.user_type`)
4. **Inferred from Django user**:
   - `is_superuser=True` → super_admin
   - `is_staff=True` → admin
   - Authenticated → pro_user
5. **Default to 'guest'** - Lowest priority

## Data Structure

### API Response Format
```json
{
    "success": true,
    "data": {
        "by_endpoint": {
            "pages/list": {
                "super_admin": {"request_count": 45, "last_called_at": 1738368000.0},
                "admin": {"request_count": 32, "last_called_at": 1738367500.0},
                "pro_user": {"request_count": 18},
                "free_user": {"request_count": 12},
                "guest": {"request_count": 5}
            }
        },
        "by_user_type": {
            "super_admin": {
                "total_requests": 150,
                "unique_endpoints": 25,
                "avg_duration_ms": 45.2
            }
        },
        "summary": {
            "total_requests": 500,
            "total_endpoints": 50,
            "user_types_active": 5
        }
    }
}
```

## Testing

### Manual Testing Checklist

- [x] Backend tracking records user_type correctly
- [x] Middleware extracts user_type from various sources
- [x] API endpoint returns correct data structure
- [x] Graph renders in all three views
- [x] View switching works (grouped/stacked/heatmap)
- [x] Legend toggle shows/hides user types
- [x] Tooltips display correct information
- [x] Dark mode renders correctly
- [x] Responsive on mobile/tablet/desktop
- [x] Old URL redirects to new page
- [x] Summary cards display aggregated stats

### Test Commands

```bash
# Test API with user_type header
curl -H "X-User-Type: admin" http://localhost:8000/api/v1/pages/

# Check Redis keys
redis-cli KEYS "api_tracking:count:*:admin"

# Test new endpoint
curl http://localhost:8000/api/v1/docs/endpoint-stats-by-user-type/

# Test redirect
curl -I http://localhost:8000/docs/docs/endpoint-stats/
# Should return: 301 Permanent Redirect to /api/docs/
```

## Future Enhancements

Potential features for future iterations:

1. **Time-Series Tracking**
   - Store hourly/daily buckets
   - Add date range picker
   - Show trends over time

2. **Advanced Analytics**
   - User journey visualization
   - Conversion funnel analysis
   - Anomaly detection

3. **Export & Reporting**
   - Export as CSV/PNG
   - Generate PDF reports
   - Scheduled email reports

4. **Real-Time Updates**
   - WebSocket integration
   - Live graph updates
   - Real-time notifications

## Architecture Decisions

### Why Redis for Storage?
- **Performance**: In-memory, extremely fast
- **Scalability**: Handles millions of keys easily
- **TTL Support**: Automatic expiration after 30 days
- **Atomic Operations**: `INCR` for concurrent updates

### Why D3.js for Visualization?
- **Flexibility**: Custom chart types
- **Performance**: Handles large datasets
- **Interactivity**: Rich event handling
- **Already Available**: Loaded in base template

### Why Multiple View Types?
- **Grouped**: Best for comparing user types
- **Stacked**: Best for seeing totals
- **Heatmap**: Best for large datasets (many endpoints)

### Why Top 20 Default?
- **Performance**: Faster rendering
- **Clarity**: Less visual clutter
- **Customizable**: Can be changed via options

## Troubleshooting

### Graph Not Showing?
1. Check browser console for JavaScript errors
2. Verify `user_type_stats_json` is populated in view context
3. Ensure D3.js is loaded (`<script src="https://d3js.org/d3.v7.min.js">`)
4. Check that endpoint-stats-graph.js is loaded

### No Data in Graph?
1. Make some API requests first to generate data
2. Check Redis for keys: `redis-cli KEYS "api_tracking:*"`
3. Verify middleware is enabled: `API_TRACKING_USER_TYPE_ENABLED = True`
4. Check that requests include user_type (or middleware can infer it)

### User Type Not Being Tracked?
1. Verify `X-User-Type` header is sent from frontend
2. Check middleware logs (DEBUG level)
3. Ensure middleware is in `MIDDLEWARE` list in settings
4. Verify user is authenticated (if relying on inference)

### Dark Mode Issues?
1. Graph observes `dark` class on `<html>` or `<body>`
2. Check theme.js is working
3. Verify graph re-renders on theme change

## Performance Considerations

- **Redis Memory**: ~250 keys for 50 endpoints × 5 user types
- **Graph Rendering**: Optimized for up to 50 endpoints
- **API Response**: Typically < 100KB
- **Page Load**: Minimal impact (D3.js already loaded)

## Security Considerations

- **User Type Validation**: Middleware validates against `VALID_USER_TYPES`
- **No Sensitive Data**: Only counts and timestamps stored
- **Redis TTL**: Automatic cleanup after 30 days
- **No User Identification**: User_type only, no user IDs stored

## Browser Support

- Chrome/Edge: ✅ Fully supported
- Firefox: ✅ Fully supported
- Safari: ✅ Fully supported
- Mobile browsers: ✅ Responsive design

## Implementation Date

**January 31, 2026**

---

## Contact

For questions or issues related to this implementation, refer to this document or the code comments in the modified files.
