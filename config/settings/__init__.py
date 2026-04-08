"""
Load settings from DJANGO_ENV.

``manage.py check --deploy`` always uses production so deploy checks match prod.
"""

import os
import sys

if "check" in sys.argv and "--deploy" in sys.argv:
    _env = "production"
else:
    _env = os.getenv("DJANGO_ENV", "development").lower()

DJANGO_ENV = _env

if DJANGO_ENV == "production":
    from .production import *  # noqa: F403
elif DJANGO_ENV == "staging":
    from .staging import *  # noqa: F403
elif DJANGO_ENV in ("testing", "test"):
    from .testing import *  # noqa: F403
else:
    from .development import *  # noqa: F403
