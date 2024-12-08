from typing import Any, Dict, List, TypeVar

T = TypeVar("T")


def set_attrs_from_dict(src_dict: Dict[str, Any], dist_obj: Any, /):
    for key, value in src_dict.items():
        if hasattr(dist_obj, key):
            setattr(dist_obj, key, value)


def flatten_list(l: List[T | List[T]]) -> List[T]:
    ret: List[T] = []
    for item in l:
        if isinstance(item, List):
            ret += item
        else:
            ret.append(item)
    return ret
