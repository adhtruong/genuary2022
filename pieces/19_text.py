from random import random, seed

from cairo import LineCap

from pycairo_util.cairo_context import Context, export


def draw_row(context: Context, gap: float, tiles: int) -> None:
    context.translate(-gap, 0)

    position = 0
    max_position = tiles * 3.2
    while position < max_position:
        if position != max_position - 5 and (position >= max_position - 3 or random() < 0.5):
            context.circle(0, 0, gap / 3)
            context.fill()
            context.translate(gap, 0)
            position += 3
        else:
            context.set_line_width(gap * 2 / 3)
            context.set_line_cap(LineCap.ROUND)
            context.line_to(0, 0)
            context.line_to(gap * 2 / 3, 0)
            context.stroke()
            context.translate(gap * 5 / 3, 0)
            position += 5


def draw(context: Context, size: int) -> None:
    seed(0)

    context.set_white()
    context.square(0, 0, size)
    context.fill()

    context.set_black()

    tiles = 35
    gap = size / tiles
    for _ in range(tiles - 1):
        context.translate(0, gap)
        context.save()
        draw_row(context, gap, tiles)
        context.restore()


def main() -> None:
    export(output="run/19_text.py", width=8_000)


if __name__ == "__main__":
    main()
