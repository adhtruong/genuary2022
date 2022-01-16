from itertools import product
from math import pi, sin

from pycairo_util.cairo_context import Context, export


def draw(context: Context, size: int) -> None:
    context.set_white()
    context.square(0, 0, size)
    context.fill()

    context.translate(size / 400, size / 160)

    for x, y in product(range(800), range(80)):
        context.save()
        context.translate(x * size / 800, y * size / 80)
        context.circle(0, 0, size / 250)
        colour = sin(x / 800 * 4 * pi + y / 80 * 3 * pi) / 2 + 1 / 2
        context.set_grey(colour)
        context.fill()
        context.restore()


def main() -> None:
    export(output="run/800x80.png", width=8_000)


if __name__ == "__main__":
    main()
