from typing import Any


def Run(pyObject: Any, key: str) -> Any:
    """
    Confidentiality: True
    """
    return pyObject.__getattr__(key)
