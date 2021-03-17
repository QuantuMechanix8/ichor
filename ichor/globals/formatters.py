from functools import wraps
from typing import Any, cast

from ichor.typing import F


def formatter(func: F) -> F:
    @wraps(func)
    def wrapper(val: Any) -> Any:
        if func.__annotations__:
            # If the type doesn't match the type expected by the annotations
            # don't run formatter
            if type(val) != next(iter(func.__annotations__.values())):
                return val
        return func(val)

    return cast(F, wrapper)


@formatter
def cleanup_str(str_in: str) -> str:
    return str_in.replace('"', "").replace("'", "").strip()


@formatter
def to_upper(s: str) -> str:
    return s.upper()


@formatter
def to_lower(s: str) -> str:
    return s.lower()
