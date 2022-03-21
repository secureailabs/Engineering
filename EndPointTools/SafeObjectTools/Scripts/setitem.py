from typing import Any


def Run(pyObject: Any,
        key: str,
        value: Any) -> (Any, [True]):
    pyObject.__setitem__(key, value)
    return pyObject
