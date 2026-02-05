"""Security middleware for adding security headers."""
from django.utils.deprecation import MiddlewareMixin
from django.conf import settings


class SecurityHeadersMiddleware(MiddlewareMixin):
    """Add security headers to all responses."""
    
    def process_response(self, request, response):
        # Security headers
        response['X-Content-Type-Options'] = 'nosniff'
        response['X-Frame-Options'] = 'DENY'
        response['X-XSS-Protection'] = '1; mode=block'
        response['Referrer-Policy'] = 'strict-origin-when-cross-origin'
        
        # Content Security Policy (only if not in admin or debug mode)
        if not request.path.startswith('/admin/') and not settings.DEBUG:
            response['Content-Security-Policy'] = (
                "default-src 'self'; "
                # Allow Tailwind CDN + d3js for current templates (login uses Tailwind CDN).
                # Prefer self-hosting in the future to tighten CSP.
                "script-src 'self' 'unsafe-inline' 'unsafe-eval' https://cdn.tailwindcss.com https://d3js.org; "
                "script-src-elem 'self' 'unsafe-inline' 'unsafe-eval' https://cdn.tailwindcss.com https://d3js.org; "
                "style-src 'self' 'unsafe-inline'; "
                "img-src 'self' data: https:; "
                # Some pages may reference external fonts; allow this specific host.
                "font-src 'self' data: https://r2cdn.perplexity.ai; "
                "connect-src 'self' https:;"
            )
        
        # Permissions Policy (Feature Policy)
        response['Permissions-Policy'] = (
            "geolocation=(), "
            "microphone=(), "
            "camera=(), "
            "payment=(), "
            "usb=()"
        )
        
        return response
