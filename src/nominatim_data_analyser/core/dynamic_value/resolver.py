from typing import Any, Dict, Iterable

from . import DynamicValue

def resolve_all(data_to_resolve: Any, resolver_data: dict[str, Any]) -> Any:
    """
        Resolves the given data_to_resolve by resolving all data inside which are
        of type DynamicValue. The resolved data are resolved again if they also contain
        DynamicValue.

        Parameter resolver_data is the data dictionnary used to resolve the dynamic values.
    """
    while(is_resolvable(data_to_resolve)):
        data_to_resolve = resolve_one(data_to_resolve, resolver_data)
    return data_to_resolve

def resolve_one(data_to_resolve: Any, resolver_data: dict[str, Any]) -> Any:
    """
        Resolves every DynamicValue of the given data_to_resolve.
        If the given data is an Iterable all values of type DynamicValue
        are resolved. If the given data is a Dictionnary every keys and values
        are resolved if of type DynamicValue.
    """
    if isinstance(data_to_resolve, Iterable):
        #Resolve dictionnary by trying to resolve each key and each value.
        if isinstance(data_to_resolve, Dict):
            new_dict = dict()
            for k, v in data_to_resolve.items():
                k = _resolve_if_resolvable(resolver_data, k)
                v = _resolve_if_resolvable(resolver_data, v)
                new_dict[k] = v
            data_to_resolve = new_dict
        #Resolve all others classic iterables.
        else:
            data_to_resolve = type(data_to_resolve)(map(lambda x: _resolve_if_resolvable(resolver_data, x), data_to_resolve)) # type: ignore[call-arg]
    else:
        data_to_resolve = _resolve_if_resolvable(resolver_data, data_to_resolve)

    return data_to_resolve

def is_resolvable(data: Any) -> bool:
    """
        Checks if the given data contains any DynamicValue which
        is resolvable. If the data is an Iterable every value are checked.
        Also, if the data is a Dictionnary every keys and every values are checked.
    """
    if isinstance(data, Iterable):
        if isinstance(data, dict):
            #Checks all the keys and values of the dictionnary.
            return _contains_dynamic_value(data.keys()) \
                or _contains_dynamic_value(data.values())
        else:
            return _contains_dynamic_value(data)
    else:
        return _is_dynamic_value(data)

def _contains_dynamic_value(data: Iterable[Any]) -> bool:
    """
        Checks if the given Iterable contains any instance
        of the DynamicValue type.
    """
    return any([_is_dynamic_value(x) for x in data])

def _is_dynamic_value(data: Any) -> bool:
    """
        Checks if the given value is an instance of the DynamicValue type.
    """
    return isinstance(data, DynamicValue)

def _resolve_if_resolvable(resolver_data: dict[str, Any], data: Any) -> Any:
    """
        If the given data is of type DynamicValue it gets resolved.
        Otherwise it gets returned as it is.
    """
    return data.resolve(resolver_data) if _is_dynamic_value(data) else data
