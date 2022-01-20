from itertools import product

from pycairo_util.cairo_context import Context, export


def draw(context: Context, size: int) -> None:
    context.set_white()
    context.square(0, 0, size)
    context.fill()

    margin = size / 20
    tiles = 9
    tile_size = (size - margin * 2) / tiles

    context.translate(margin, margin)

    for x, y in product(range(tiles), repeat=2):
        context.save()
        context.translate(tile_size * (x + 0.5), tile_size * (y + 0.5))
        context.circle(0, 0, tile_size * 3 / 5)
        context.set_black(0.5)
        context.fill()
        context.restore()


def main() -> None:
    export(output="run/17_3_colours.png", width=8_000)


if __name__ == "__main__":
    main()
