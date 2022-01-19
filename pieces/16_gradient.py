from itertools import product
from typing import Callable

from cairo import FORMAT_ARGB32, ImageSurface, Surface
from opensimplex import noise2, seed  # type: ignore

from pycairo_util.cairo_context import Context, export


def apply_gradient(context: Context, size: int, inverted: bool) -> Context:
    max_radius = int(size * 3 / 4)
    for radius in reversed(range(max_radius)):
        grey = radius / max_radius
        if inverted:
            grey = 1 - grey
        context.set_grey(grey)
        context.circle(size / 2, size / 2, radius)
        context.fill()

    return context


def apply_perlin_noise(context: Context, size: int, comparison) -> Context:

    for x, y in product(range(size), repeat=2):
        if not comparison(get_noise(size, x, y)):
            continue
        context.square(x, y, 1.0)
        context.fill()

    return context


def get_noise(size: int, x: float, y: float) -> float:
    return noise2(
        float(x) / size * 10,
        float(y) / size * 10,
    )


def get_comparison(inverted: bool) -> Callable[[float], bool]:
    return lambda value: value > 0 if inverted else lambda value: value <= 0  # type: ignore


def draw(surface: Surface, size: int) -> None:
    seed(1)

    for inverted in (False, True):
        gradient_surface = ImageSurface(FORMAT_ARGB32, size, size)
        apply_gradient(Context(gradient_surface), size, inverted)

        context = Context(surface)
        context.set_source_surface(gradient_surface)
        comparison = get_comparison(inverted)
        apply_perlin_noise(context, size, comparison)


def main() -> None:
    export(width=2_000)


if __name__ == "__main__":
    main()
