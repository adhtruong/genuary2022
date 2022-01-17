from math import cos, pi, sin, sqrt
from typing import Callable

from cairo import LineJoin

from pycairo_util.cairo_context import Context, export


def draw_relative_points(context: Context, *points: tuple[float, float]) -> None:
    context.save()
    for point in points:
        context.translate(*point)
        context.line_to(0, 0)
    context.restore()


def draw_segment(context: Context, radius: float, width: float) -> None:
    draw_relative_points(
        context,
        (
            -radius * cos(pi / 3),
            radius * cos(pi / 3) / sqrt(3),
        ),
        (-width, 0),
        (
            (radius + 3 * width) * cos(pi / 3),
            -(radius + 3 * width) * sin(pi / 3),
        ),
        (
            (radius + 4 * width) * sin(pi / 6),
            (radius + 4 * width) * cos(pi / 6),
        ),
        (
            -width * cos(pi / 3),
            width * sin(pi / 3),
        ),
        (
            -(radius + 3 * width) * cos(pi / 3),
            -(radius + 3 * width) * sin(pi / 3),
        ),
    )


def draw_penrose_triangle(context: Context, radius: float, width: float) -> None:
    for i in range(3):
        context.rotate(-pi * 2 / 3)
        draw_segment(context, radius, width)
        context.close_path()
        context.set_line_width(radius / 10)
        context.set_black()
        context.stroke_preserve()
        context.set_grey(i * 1 / 2)
        context.fill()


def render_grid(context: Context, radius: float, renderer: Callable[[], None]) -> None:
    for j in range(10):
        context.save()
        for i in range(11):
            context.save()
            if (i + j) % 2:
                context.translate(0, -radius / 2)
                context.rotate(pi)
                context.rotate(pi * 2 / 3)
            renderer()
            context.restore()
            context.translate(radius * sqrt(3) / 2, 0)
        context.restore()
        context.translate(0, radius * 1.5)


def draw(context: Context, size: int) -> None:
    context.set_white()
    context.square(0, 0, size)
    context.fill()

    context.translate(0, 0)
    context.set_line_join(LineJoin.ROUND)

    inner_radius = size / 30
    width = inner_radius
    # FIXME wrong formula when not equal
    radius = inner_radius * (2 * sqrt(2)) + width * (1 + sqrt(2)) / 2
    render_grid(
        context,
        radius,
        lambda: draw_penrose_triangle(context, inner_radius, width),
    )


def main() -> None:
    export(
        output="run/14_something_you_would_never_make.png",
        width=8_000,
    )


if __name__ == "__main__":
    main()
