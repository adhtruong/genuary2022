from itertools import product
from math import sqrt
from random import randint, seed, uniform

from pycairo_util.cairo_context import Context, export


def get_level_height_from_width(width: float) -> float:
    return 1 / sqrt(2) * width


def draw_building(context: Context, height: float, width: float) -> None:
    steps = randint(20, 60)
    height = uniform(height / 3, height)
    spacing = height / steps
    level_height = get_level_height_from_width(width)
    for offset_index in range(steps):
        context.save()
        context.translate(0, -offset_index * spacing)

        context.line_to(0, 0)
        context.line_to(width / 2, -level_height / 2)
        context.line_to(0, -level_height)
        context.line_to(-width / 2, -level_height / 2)
        context.close_path()

        context.set_white()
        context.fill_preserve()
        context.set_black()
        context.stroke()

        context.restore()


def draw(context: Context, size: int, seed_: int = 4) -> None:
    seed(seed_)

    context.set_white()
    context.square(0, 0, size)
    context.fill()

    context.set_line_width(size / 500)

    width = size / 8
    height = get_level_height_from_width(width)
    for j, i in product(range(20), range(10)):
        context.save()
        x_offset = i * width if j % 2 == 0 else (i + 1 / 2) * width
        context.translate(x_offset, j * height)
        draw_building(context, size / 4, width)
        context.restore()


def main() -> None:
    export(output="run/09_architecture.png", width=8_000)


if __name__ == "__main__":
    main()
