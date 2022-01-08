from enum import Enum
from itertools import product
from math import pi

from pycairo_util.cairo_context import Context, export


def draw_lines(context: Context, tile_size: float, lines: int) -> None:
    line_size = tile_size / lines
    for i in range(lines):
        context.save()
        if i % 2 == 0:
            context.set_black()
        else:
            context.set_white()

        context.translate(i * line_size, 0)
        context.rectangle(0, 0, line_size, tile_size)
        context.fill()
        context.restore()


class Symbol(str, Enum):
    SQUARE = "square"
    CIRCLE = "circle"


def draw_tile(context: Context, tile_size: float, lines: int, symbol: Symbol = Symbol.CIRCLE) -> None:
    draw_lines(context, tile_size, lines)
    context.save()
    if symbol == Symbol.CIRCLE:
        context.circle(tile_size / 2, tile_size / 2, tile_size * 2 / 5)
    elif symbol == Symbol.SQUARE:
        offset = tile_size / 5
        context.square(offset, offset, tile_size - 2 * offset)
    context.clip()
    rotate_about(context, tile_size / 2, tile_size / 2, pi / 2)
    draw_lines(context, tile_size, lines)
    context.restore()


def rotate_about(context: Context, x: float, y: float, angle: float) -> None:
    context.translate(x, y)
    context.rotate(angle)
    context.translate(-x, -y)


def draw(context: Context, size: int) -> None:
    context.set_white()
    context.square(0, 0, size)
    context.fill()

    tile_size = size / 3
    lines = 15
    for x, y in product(range(3), repeat=2):
        context.save()
        context.translate(x * tile_size, y * tile_size)
        if (x + y) % 2 == 1:
            rotate_about(context, tile_size / 2, tile_size / 2, pi / 2)
        symbol = Symbol.SQUARE if (x + y) % 2 == 1 else Symbol.CIRCLE
        draw_tile(context, tile_size, lines, symbol)
        context.restore()


def main() -> None:
    export(output="run/07_sol_lewitt.png", width=8100)


if __name__ == "__main__":
    main()
