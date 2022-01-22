from itertools import cycle, product
from math import cos, pi, sin
from typing import Iterable

from pycairo_util.cairo_context import Context, export


def polar_to_cart(radius: float, angle: float) -> tuple[float, float]:
    return radius * cos(angle), radius * sin(angle)


def get_arc(size: float) -> Iterable[tuple[float, float]]:
    for i in range(1000):
        yield polar_to_cart(size / 50 * i, i / 10)


def draw_arc(context: Context, size: float, reverse: bool) -> None:
    points: Iterable[tuple[float, float]] = list(get_arc(size))
    if reverse:
        points = reversed(list(points))
    for x, y in points:
        context.line_to(x, y)


def draw_circle(context: Context, size: float) -> None:
    context.circle(0, 0, size)
    context.clip()

    arcs = 8
    for color_setter, _ in zip(
        cycle((context.set_black, context.set_white)),
        range(arcs),
    ):
        draw_arc(context, size, False)
        context.rotate(2 * pi / arcs)
        draw_arc(context, size, True)
        color_setter()
        context.fill()

        # context.rotate(2 * pi / (arcs * 2))


def draw(context: Context, size: int) -> None:
    context.set_white()
    context.square(0, 0, size)
    context.fill()

    tiles = 8
    tile_size = size / tiles
    circle_radius = tile_size * 2 / 5

    for x, y in product(range(tiles), repeat=2):
        if x % 2 != 0:
            continue
        context.save()
        context.translate((x + 0.5) * tile_size, (y + 0.5) * tile_size)

        y_offset = -circle_radius + size / 200
        if (int(x / 2) + y) % 2 != 0:
            y_offset *= -1
        context.translate(0, y_offset)

        context.line_to(0, 0)
        context.line_to(tile_size, 0)
        context.set_black()
        context.set_line_width(size / 100)
        context.stroke()

        context.restore()

    for x, y in product(range(tiles), repeat=2):
        context.save()
        context.translate((x + 0.5) * tile_size, (y + 0.5) * tile_size)
        draw_circle(context, circle_radius)
        context.restore()


def main() -> None:
    export(output="run/18_vhs.png", width=8_000)


if __name__ == "__main__":
    main()
