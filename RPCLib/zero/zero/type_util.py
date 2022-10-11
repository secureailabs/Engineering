import inspect
import typing

from zero.customtypes import SecretObject
from zero.errors import ZeroException

# from pydantic import BaseModel

basic_types = [
    int,
    float,
    str,
    bool,
    list,
    dict,
    tuple,
    set,
]
typing_types = [
    typing.List,
    typing.Tuple,
    typing.Dict,
]
special_types = [
    typing.Union,
    typing.Optional,
]
pydantic_types = [
    # BaseModel,  TODO: next feature
]


allowed_types = basic_types + typing_types + special_types + pydantic_types


def verify_function_args(func: typing.Callable):
    """
    Verify function argument types

    :param func: rpc function
    :type func: typing.Callable
    :raises ZeroException: raise if no type hint is given in the safe function
    """
    arg_count = func.__code__.co_argcount
    # if arg_count > 1:
    #     raise ZeroException(
    #         f"`{func.__name__}` has more than 1 args; RPC functions can have only one arg - msg, or no arg"
    #     )

    if arg_count > 1:
        arg_name = inspect.signature(func).parameters
        func_arg_type = typing.get_type_hints(func)
        for arg in arg_name:
            if arg not in func_arg_type:
                raise ZeroException(f"`{func.__name__}` has no type hinting; RPC functions must have type hints")


def verify_function_return(func: typing.Callable):
    """
    verify function return types

    :param func: rpc function
    :type func: typing.Callable
    :raises ZeroException: raise if no return type hint given in the safe function
    """
    types = typing.get_type_hints(func)
    if not types.get("return"):
        raise ZeroException(f"`{func.__name__}` has no return type hinting; RPC functions must have type hints")


def get_function_input_class(func: typing.Callable):
    """
    get function argument types

    :param func: rpc function
    :type func: typing.Callable
    :return: a dict containing function arg types
    :rtype: dict
    """
    arg_count = func.__code__.co_argcount
    if arg_count == 0:
        return None
    # if arg_count == 1:
    #    arg_name = func.__code__.co_varnames[0]
    #    func_arg_type = typing.get_type_hints(func)
    elif arg_count > 0:
        func_arg_type = typing.get_type_hints(func)
        func_arg_type.pop("return")
        return func_arg_type


def get_function_return_class(func: typing.Callable):
    """
    get function return types

    :param func: rpc function
    :type func: typing.Callable
    :return: dict containing function return types
    :rtype: dict
    """
    types = typing.get_type_hints(func)
    return types.get("return")


def verify_function_input_type(func: typing.Callable):
    """
    verify if function input parameter types are basic python types

    :param func: rpc function
    :type func: typing.Callable
    :raises TypeError: if the types given is not basic python types(can not processed by msgpack)
    """
    input_type = get_function_input_class(func)
    if input_type is None:
        return

    for key in input_type:
        if input_type[key] in basic_types:
            continue
        elif input_type[key] is typing.Type[SecretObject]:
            continue
        elif typing.get_origin(input_type[key]) in basic_types:
            continue
        elif typing.get_origin(input_type[key]) in special_types:
            continue
        elif issubclass(input_type, tuple(pydantic_types)):
            continue
        else:
            raise TypeError(
                f"{func.__name__} has type {input_type} which is not allowed; "
                "allowed types are: \n" + "\n".join([str(t) for t in allowed_types])
            )


def verify_allowed_type(msg, rpc_method: str = None):
    """
    verify if the input parameter types are allowed types

    :param msg: incoming parameters
    :type msg: Any
    :param rpc_method: callable, defaults to None
    :type rpc_method: str, optional
    :raises TypeError: raise if the input parameters have not allowed types
    """
    if not isinstance(msg, tuple(allowed_types)):
        method_name = f"for method `{rpc_method}`" if rpc_method else ""
        raise TypeError(
            f"{msg} is not allowed {method_name}; allowed types are: \n" + "\n".join([str(t) for t in allowed_types])
        )


def verify_incoming_rpc_call_input_type(msg, rpc_method: str, rpc_input_type_map: dict):  # pragma: no cover
    """
    verify if the incoming rpc call input types matches the given ones

    :param msg: input parameters
    :type msg: Any
    :param rpc_method: rpc method
    :type rpc_method: str
    :param rpc_input_type_map: input types defined
    :type rpc_input_type_map: dict
    :raises TypeError: if the input parameter have type does not match the given ones
    """
    it = rpc_input_type_map[rpc_method]
    if it is None:
        return

    if it in basic_types:
        if it != type(msg):
            raise TypeError(f"{msg} is not allowed for method `{rpc_method}`; allowed type: {it}")

    if (origin_type := typing.get_origin(it)) in basic_types:
        if origin_type != type(msg):
            raise TypeError(f"{msg} is not allowed for method `{rpc_method}`; allowed type: {it}")


def is_pydantic(cls):  # pragma: no cover
    """
    _summary_

    :return: _description_
    :rtype: _type_
    """
    if cls not in basic_types:
        if not typing.get_origin(cls) in basic_types:
            if not typing.get_origin(cls) in special_types:
                if issubclass(cls, tuple(pydantic_types)):
                    return True
