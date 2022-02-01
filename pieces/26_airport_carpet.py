from itertools import cycle
from math import pi, sin
from typing import Iterable

from pycairo_util.cairo_context import Context, export


def draw_hexagon(context: Context, radius: float) -> None:
    context.save()
    context.rotate(-pi / 2)
    for _ in range(6):
        context.line_to(radius, 0)
        context.rotate(pi / 3)
    context.close_path()
    context.restore()


def get_sine_curve_points(
    size: float,
    magnitude: float,
    frequency: int,
    points: int,
) -> Iterable[tuple[float, float]]:
    for y in range(points):
        percent = y / points
        yield sin(frequency * pi * percent) * magnitude, percent * size


def draw_pattern(
    context: Context,
    size: float,
    gap: float,
    amplitude: float,
    background: float,
) -> None:
    frequency = 7
    context.save()
    for x, y in get_sine_curve_points(size, amplitude, frequency, int(size)):
        context.line_to(x, y)
    context.translate(gap, 0)
    for x, y in reversed(
        tuple(get_sine_curve_points(size, -amplitude, frequency, int(size))),
    ):
        context.line_to(x, y)
    context.set_grey(background)
    context.fill()

    if amplitude < 0:
        context.translate(-gap / 2, size / (frequency * 2))
        for _ in range(4):
            context.circle(0, 0, -amplitude)
            context.set_black()
            context.fill()
            context.translate(0, size / frequency * 2)

    context.restore()


def draw(context: Context, size: int) -> None:
    context.set_white()
    context.square(0, 0, size)
    context.fill()

    pieces = 18
    gap = size / pieces
    context.translate(-gap / 2, 0)
    for colour, _ in zip(cycle((0, 1 / 2)), range(pieces + 1)):
        amplitude = gap / 3 if not colour else -gap / 3
        draw_pattern(context, size, gap, amplitude, colour)
        context.translate(gap, 0)


def main() -> None:
    export(output="run/26_airport_carpet.png", width=8_000)


if __name__ == "__main__":
    main()
