from math import pi, sin
from typing import Iterable

from pycairo_util.cairo_context import Context, export


def get_sine_path(size: int, curves: float, magnitude: float) -> Iterable[tuple[float, float]]:
    for y in range(size):
        yield sin(curves * 2 * pi * y / size) * magnitude, y


def draw_pattern(context: Context, size: int, colour: float, gap) -> None:
    width = size / 25
    for _ in range(40):
        context.set_grey(colour)
        for x, y in get_sine_path(size, 3, width):
            context.line_to(x, y)
        context.translate(gap, 0)
        for x, y in reversed(list(get_sine_path(size, 3, width))):
            context.line_to(x, y)
        context.close_path()
        context.fill()

        colour = 1 - colour
        gap *= 0.9


def draw(context: Context, size: int) -> None:
    context.set_white()
    context.rectangle(0, 0, size, size)
    context.fill()

    context.translate(size / 2, 0)
    context.save()
    draw_pattern(context, size, 1, int(size / 18))
    context.restore()
    draw_pattern(context, size, 0, -int(size / 18))


def main() -> None:
    export(output="run/31_negative_space.png", width=8_000)


if __name__ == "__main__":
    main()
