from itertools import product
from math import pi

from pycairo_util.cairo_context import Context, export


def draw_pattern(context: Context, square_size: float, iterations: int, power: float) -> None:
    context.save()
    square_size *= power**iterations
    for _ in range(iterations, -1, -1):
        context.square(-square_size / 2, -square_size / 2, square_size)
        context.set_white()
        context.fill_preserve()
        context.set_black()
        context.stroke()

        square_size /= power
        context.rotate(pi / 36)
    context.restore()


def draw_rose(context: Context, size: float) -> None:
    size *= 2 / 3
    draw_pattern(context, size / 6, 36, 1.02)
    context.rotate(pi / 2)
    draw_pattern(context, size / 12, 36, 1.03)
    context.rotate(pi / 2)
    draw_pattern(context, size / 36, 36, 1.05)


def draw(context: Context, size: int) -> None:
    context.set_white()
    context.square(0, 0, size)
    context.fill()

    context.set_line_width(size / 900)

    for x, y in product(range(3), repeat=2):
        context.save()
        context.translate((x + 0.5) * size / 3, (y + 0.5) * size / 3)
        draw_rose(context, size)
        context.restore()


def main() -> None:
    export(output="run/30_organic.png", width=8_000)


if __name__ == "__main__":
    main()
