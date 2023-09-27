from typing import Type, get_origin


def get_exact_type(_type: Type) -> Type:
    """Just a helper function for validating fields types.
    """
    if _type is None:
        return type(None)
    else:
        return get_origin(_type) or _type
