"""Utilities for Evil Genius Labs."""
from collections.abc import Callable
from functools import wraps
from typing import Any, TypeVar, cast

from . import EvilGeniusEntity

CALLABLE_T = TypeVar("CALLABLE_T", bound=Callable)  # pylint: disable=invalid-name


def update_when_done(func: CALLABLE_T) -> CALLABLE_T:
    """Decorate function to trigger update when function is done."""

    @wraps(func)
    async def wrapper(self: EvilGeniusEntity, *args: Any, **kwargs: Any) -> Any:
        """Wrap function."""
        result = await func(self, *args, **kwargs)
        await self.coordinator.async_request_refresh()
        return result

    return cast(CALLABLE_T, wrapper)
