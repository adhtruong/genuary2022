from typing import Iterator

import pytest

from pycairo_util.core import register, registry_context, run


@pytest.fixture(autouse=True)
def registry_fixture() -> Iterator[None]:
    with registry_context():
        yield


def test_core() -> None:
    def inner() -> int:
        return 5

    register(inner)

    def run_function(inner: int) -> int:
        return inner

    assert run(run_function) == 5
    assert run(run_function, inner=4) == 4


def test_nested_fixture() -> None:
    def nested_inner() -> int:
        return 4

    def inner(nested_inner: int) -> int:
        return nested_inner + 1

    register(nested_inner)
    register(inner)

    def run_function(inner: int) -> int:
        return inner

    assert run(run_function) == 5
    assert run(run_function, nested_inner=3) == 4


def test_with_default() -> None:
    def run_function(default_param: int = 5) -> int:
        return default_param

    assert run(run_function) == 5
    assert run(run_function, default_param=4) == 4


def test_registry_context() -> None:
    def entrypoint(scoped_function: int) -> int:
        return scoped_function

    with registry_context():

        @register
        def scoped_function() -> int:
            return 5

        assert run(entrypoint) == 5

    with pytest.raises(RuntimeError):
        run(entrypoint)


def test_iterable() -> None:
    has_teardown = False

    def inner() -> Iterator[int]:
        yield 5
        nonlocal has_teardown
        has_teardown = True

    register(inner)

    def run_function(inner: int) -> int:
        return inner

    assert run(run_function) == 5
    assert has_teardown
    assert run(run_function, inner=4) == 4


def test_named_register() -> None:
    def inner() -> int:
        return 5

    register(name="named_inner")(inner)

    def run_function(named_inner: int) -> int:
        return named_inner

    assert run(run_function) == 5


def test_missing_named() -> None:
    def run_function(missing: int) -> int:
        return missing

    with pytest.raises(RuntimeError):
        run(run_function)
