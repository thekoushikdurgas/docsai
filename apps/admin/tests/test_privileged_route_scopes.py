from django.urls import resolve, reverse


CRITICAL_SUPER_ADMIN_ROUTES = [
    ("operations:dashboard", {}),
    ("page_builder:editor", {}),
    ("roadmap:dashboard", {}),
    ("architecture:blueprint", {}),
    ("ai_agent:chat", {}),
    ("ai_agent:sessions", {}),
    ("ai_agent:session_detail", {"session_id": "session-1"}),
    ("ai_agent:chat_completion_api", {}),
]


def test_critical_super_admin_routes_require_super_admin_scope():
    for route_name, kwargs in CRITICAL_SUPER_ADMIN_ROUTES:
        url = reverse(route_name, kwargs=kwargs)
        callback = resolve(url).func
        assert getattr(callback, "required_role_scope", None) == "super_admin"
