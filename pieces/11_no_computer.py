from itertools import cycle
from math import sqrt

from more_itertools import pairwise

from pycairo_util.cairo_context import Context, export


def draw(context: Context, size: int) -> None:
    context.set_white()
    context.square(0, 0, size)
    context.fill()

    context.set_black()
    context.square(0, 0, size)
    context.set_line_width(size / 200)
    context.stroke()

    base_radius = size * 2 / 5
    context.translate(size / 2 + base_radius, size / 2 + base_radius)
    center = (1 - 1 / sqrt(2)) * base_radius
    radii = (base_radius * (9 / 10) ** i for i in range(5))
    for sign, (previous, radius) in zip(
        cycle((1,)),
        pairwise((0, *radii)),
    ):
        center += sign * (radius - previous) / sqrt(2)
        context.circle(-center, -center, radius)
        context.stroke()


def main() -> None:
    export(output="run/11_no_computers.png", width=8_000)


if __name__ == "__main__":
    main()
