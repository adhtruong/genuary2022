from math import pi, sin
from random import random, seed, uniform

from pycairo_util.cairo_context import Context, export


def draw_segment(context: Context, size: int, y_baseline: float, background: float) -> None:
    def get_y_offset(x: float) -> float:
        return sin(2 * pi * x / size) * size / 25

    context.line_to(size, size)
    context.line_to(0, size)
    for x in range(size):
        y_offset = get_y_offset(x)
        context.line_to(x, y_offset + y_baseline)
    context.close_path()
    context.set_grey(background)
    context.fill()

    for _ in range(10_000):
        xc, yc, radius = uniform(0, size), uniform(0, size), size / 500
        if get_y_offset(xc) + y_baseline > yc:
            continue

        context.circle(xc, yc, radius)
        context.set_grey(random())
        context.fill()


def draw(context: Context, size: int) -> None:
    seed(0)

    context.set_white()
    context.square(0, 0, size)
    context.fill()

    segments = 9
    for i in range(segments):
        draw_segment(
            context,
            size,
            size / (segments - 1) * (i - 1 / 2),
            1 - i / (segments - 1),
        )


def main() -> None:
    export(output="run/sand.png", width=8_000)


if __name__ == "__main__":
    main()
