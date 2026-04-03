from django.urls import NoReverseMatch, reverse

from apps.core.navigation import SIDEBAR_MENU


def _iter_nav_items():
    for group in SIDEBAR_MENU:
        for item in group.get("items", []):
            yield item
            for child in item.get("children", []):
                yield child


def test_sidebar_navigation_named_routes_resolve():
    unresolved = []
    for item in _iter_nav_items():
        app_name = item.get("app_name")
        url_name = item.get("url_name")
        if not (app_name and url_name):
            continue
        try:
            reverse(f"{app_name}:{url_name}")
        except NoReverseMatch:
            unresolved.append(f"{app_name}:{url_name}")
    assert unresolved == []

