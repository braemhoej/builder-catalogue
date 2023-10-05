import asyncio
from typing import Any, Coroutine, TypeVar

T = TypeVar("T")


def run_async(coroutine: Coroutine[Any, Any, T]) -> T:
    loop = asyncio.get_event_loop()
    return loop.run_until_complete(coroutine)
