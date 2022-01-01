__all__ = (
    "register",
    "run",
    "registry_context",
)

from contextlib import contextmanager, suppress
from contextvars import ContextVar
from inspect import signature
from logging import getLogger
from typing import Any, Callable, Iterator, Optional, TypeVar, overload

logger = getLogger(__name__)

_F = TypeVar("_F", bound=Callable)
_RType = TypeVar("_RType")


_RegistryType = dict[str, _F]
_registry_context: ContextVar[_RegistryType] = ContextVar("registry", default={})


def _get_registry() -> _RegistryType:
    return _registry_context.get().copy()


def _set_registry(registry: _RegistryType) -> None:
    _registry_context.set(registry)


@contextmanager
def registry_context() -> Iterator[None]:
    registry = _get_registry()
    yield
    _set_registry(registry)


@overload
def register(func: _F) -> _F:
    ...


@overload
def register(*, name: str) -> Callable[[_F], _F]:
    ...


def register(func: Optional[_F] = None, *, name: Optional[str] = None) -> Callable[[_F], _F]:
    wrapper = _register_inner(name)

    if func is not None:
        return wrapper(func)

    return wrapper


def _register_inner(name: Optional[str]) -> Callable[[_F], _F]:
    def inner(f: _F) -> _F:
        nonlocal name
        if name is None:
            name = f.__name__
        registry = _get_registry()
        registry[name] = f
        _set_registry(registry)
        return f

    return inner


def run(f: Callable[..., _RType], **kwargs: Any) -> _RType:
    result, teardowns = _run_inner(f, kwargs)
    for teardown in reversed(teardowns):
        with suppress(StopIteration):
            next(teardown)

    return result


def _run_inner(f: Callable[..., _RType], kwargs: dict[str, Any]) -> tuple[_RType, list]:
    teardowns = []

    function_signature = signature(f)
    parameters = {}
    for parameter, v in function_signature.parameters.items():
        logger.debug(f"For {f.__name__}, resolving {parameter}")
        if parameter in kwargs:
            parameters[parameter] = kwargs[parameter]
            continue

        registry = _get_registry()
        if parameter in registry:
            logger.info(f"Recalculating {parameter}...")
            func = registry[parameter]
            result_generator, new_teardowns = _run_inner(func, kwargs)
            teardowns.extend(new_teardowns)
            if isinstance(result_generator, Iterator):
                result = next(result_generator)
                teardowns.append(result_generator)
            else:
                result = result_generator
            kwargs[parameter] = result
            parameters[parameter] = result
            continue

        if v.default is not v.empty:
            continue

        raise RuntimeError(f"Unable to resolve parameter '{parameter}'")

    result = f(**parameters)

    return result, teardowns
