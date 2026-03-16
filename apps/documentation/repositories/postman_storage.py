"""Postman-specific storage logic for UnifiedStorage.

UnifiedStorage does not have get_configuration/list_configurations - PostmanService
uses its own repository and cache. This module exists for consistency with the 4-resource
split; clear_cache('postman', ...) is handled by the base class.
"""


class PostmanStorageMixin:
    """Mixin for postman. No postman-specific methods in UnifiedStorage - PostmanService uses repository directly."""

    pass
