"""
Retry decorator with exponential backoff for resilient API calls.
Mirrors contact360.io/2/apps/core/decorators/retry.py for S3Service and other core clients.
"""

import logging
import random
import time
from functools import wraps
from typing import Any, Callable, Optional, Tuple, TypeVar

logger = logging.getLogger(__name__)

T = TypeVar("T")


def retry(
    max_retries: int = 3,
    initial_delay: float = 1.0,
    max_delay: float = 60.0,
    exponential_base: float = 2.0,
    retryable_exceptions: Optional[Tuple[type[Exception], ...]] = None,
    jitter: bool = True,
    retry_logging: bool = True,
):
    def decorator(func: Callable[..., T]) -> Callable[..., T]:
        @wraps(func)
        def wrapper(*args: Any, **kwargs: Any) -> T:
            last_exception: Optional[Exception] = None

            for attempt in range(max_retries):
                try:
                    return func(*args, **kwargs)
                except Exception as e:
                    last_exception = e

                    if retryable_exceptions is not None:
                        if not isinstance(e, retryable_exceptions):
                            if retry_logging:
                                logger.debug(
                                    "%s: Exception %s not in retryable list, raising immediately: %s",
                                    func.__name__,
                                    type(e).__name__,
                                    e,
                                )
                            raise

                    if attempt == max_retries - 1:
                        if retry_logging:
                            logger.error(
                                "%s failed after %d attempts: %s",
                                func.__name__,
                                max_retries,
                                e,
                                exc_info=True,
                            )
                        raise

                    delay = min(
                        initial_delay * (exponential_base**attempt),
                        max_delay,
                    )
                    if jitter:
                        delay += delay * 0.1 * random.random()

                    if retry_logging:
                        logger.warning(
                            "%s failed (attempt %d/%d): %s: %s. Retrying in %.2fs...",
                            func.__name__,
                            attempt + 1,
                            max_retries,
                            type(e).__name__,
                            e,
                            delay,
                        )

                    time.sleep(delay)

            if last_exception:
                raise last_exception

            raise RuntimeError(
                f"{func.__name__} failed after {max_retries} attempts with no exception captured"
            )

        return wrapper

    return decorator


def retry_on_network_error(
    max_retries: int = 3,
    initial_delay: float = 1.0,
    max_delay: float = 60.0,
):
    try:
        import httpx
        import requests

        network_exceptions: Tuple[type[Exception], ...] = (
            httpx.TimeoutException,
            httpx.NetworkError,
            httpx.ConnectError,
            httpx.ConnectTimeout,
            requests.exceptions.Timeout,
            requests.exceptions.ConnectionError,
            requests.exceptions.RequestException,
            ConnectionError,
            TimeoutError,
            OSError,
        )
    except ImportError:
        network_exceptions = (
            ConnectionError,
            TimeoutError,
            OSError,
        )

    return retry(
        max_retries=max_retries,
        initial_delay=initial_delay,
        max_delay=max_delay,
        retryable_exceptions=network_exceptions,
    )


def retry_on_server_error(
    max_retries: int = 3,
    initial_delay: float = 1.0,
    max_delay: float = 60.0,
):
    try:
        import httpx

        server_error_exceptions: Tuple[type[Exception], ...] = (httpx.HTTPStatusError,)
    except ImportError:
        server_error_exceptions = (Exception,)

    def decorator(func: Callable[..., T]) -> Callable[..., T]:
        @wraps(func)
        def wrapper(*args: Any, **kwargs: Any) -> T:
            last_exception: Optional[Exception] = None

            for attempt in range(max_retries):
                try:
                    result = func(*args, **kwargs)
                    if hasattr(result, "status_code"):
                        status_code = getattr(result, "status_code")
                        if 500 <= status_code < 600:
                            raise RuntimeError(
                                f"Server error {status_code} returned from {func.__name__}"
                            )
                    return result
                except Exception as e:
                    last_exception = e
                    should_retry = False
                    if isinstance(e, server_error_exceptions):
                        should_retry = True
                    elif hasattr(e, "response") and hasattr(e.response, "status_code"):
                        status_code = e.response.status_code
                        if 500 <= status_code < 600:
                            should_retry = True

                    if not should_retry:
                        logger.debug(
                            "%s: Exception %s is not a server error, raising immediately: %s",
                            func.__name__,
                            type(e).__name__,
                            e,
                        )
                        raise

                    if attempt == max_retries - 1:
                        logger.error(
                            "%s failed after %d attempts: %s",
                            func.__name__,
                            max_retries,
                            e,
                            exc_info=True,
                        )
                        raise

                    delay = min(initial_delay * (2.0**attempt), max_delay)
                    delay += delay * 0.1 * random.random()
                    logger.warning(
                        "%s failed (attempt %d/%d): %s: %s. Retrying in %.2fs...",
                        func.__name__,
                        attempt + 1,
                        max_retries,
                        type(e).__name__,
                        e,
                        delay,
                    )
                    time.sleep(delay)

            if last_exception:
                raise last_exception

            raise RuntimeError(
                f"{func.__name__} failed after {max_retries} attempts with no exception captured"
            )

        return wrapper

    return decorator
