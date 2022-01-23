from math import pi, sqrt
from random import random, seed

from pycairo_util.cairo_context import Context, export


def get_size(x: float, y: float, size: int) -> float:
    return (1 - dist(size / 2, size / 2, x, y) / (size / 2)) * size / 100


def draw_polygon(
    context: Context,
    x: float,
    y: float,
    radius: float,
    n: int = 3,
) -> None:
    context.save()
    context.translate(x, y)
    context.rotate(random() * 2 * pi)
    context.new_sub_path()
    for _ in range(n):
        context.line_to(radius, 0)
        context.rotate(2 * pi / n)
    context.close_path()
    context.restore()


def dist(x1: float, y1: float, x2: float, y2: float) -> float:
    return sqrt((x1 - x2) ** 2 + (y1 - y2) ** 2)


def draw(context: Context, size: int) -> None:
    seed(0)

    context.set_white()
    context.square(0, 0, size)
    context.fill()

    context.set_black(0.5)
    for _ in range(1_000):
        x, y = random() * size, random() * size
        context.set_line_width(get_size(x, y, size))
        draw_polygon(context, x, y, size / 20)
        context.set_black()
        context.stroke_preserve()
        context.set_white()
        context.fill()


def main() -> None:
    export(output="run/20_sea_of_shapes.png", width=8_000)


if __name__ == "__main__":
    main()
