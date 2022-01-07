from itertools import product
from random import seed, shuffle

from pycairo_util.cairo_context import Context, export

_Tile = tuple[bool, bool, bool, bool, bool, bool]


def get_all_possilibities(n: int = 6) -> list[_Tile]:
    return list(*product((True, False), repeat=n))


def _render_tile(context: Context, tile: _Tile, size: float, line_points: tuple) -> None:
    if len(line_points) != len(tile):
        raise RuntimeError("Mismtach in length")

    for (start, end), tile_value in zip(line_points, tile):
        if not tile_value:
            continue

        context.line_to(*start)
        context.line_to(*end)
        context.stroke()


def render_tile_cross(context: Context, tile: _Tile, size: float) -> None:
    _render_tile(
        context,
        tile,
        size,
        (
            ((0, 0), (size, 0)),
            ((size, 0), (size, size)),
            ((size, size), (0, size)),
            ((0, size), (0, 0)),
            ((0, 0), (size, size)),
            ((0, size), (size, 0)),
        ),
    )


def render_tile_box(context: Context, tile: _Tile, size: float) -> None:
    _render_tile(
        context,
        tile,
        size,
        (
            ((0, 0), (size, 0)),
            ((size, 0), (size, size)),
            ((size, size), (0, size)),
            ((0, size), (0, 0)),
            ((size / 2, 0), (size / 2, size)),
            ((0, size / 2), (size, size / 2)),
        ),
    )


def render_tile_radial(context: Context, tile: _Tile, size: float) -> None:
    context.save()
    context.translate(size / 2, size / 2)
    context.set_line_width(size / 20)
    radius = size / 2
    radius_diff = radius / len(tile)
    for tile_value in tile:
        if tile_value:
            context.circle(0, 0, radius)
            context.stroke()
        radius -= radius_diff
    context.restore()


RENDERERS = [
    render_tile_box,
    render_tile_cross,
    render_tile_radial,
]


def draw(context: Context, size: int, render_method_index: int = 2) -> None:
    context.set_white()
    context.square(0, 0, size)
    context.fill()

    n = 6

    tiles = get_all_possilibities()
    seed(0)
    shuffle(tiles)

    render_tile = RENDERERS[render_method_index]

    squares = int(2 ** (n / 2))
    tile_size = size / squares
    tile_margin = tile_size / 6
    block_size = tile_size - 2 * tile_margin
    context.set_black()
    context.set_line_width(tile_size / 20)
    for (i, j), tile in zip(product(range(squares), repeat=2), tiles):
        context.save()
        context.translate(
            tile_size * i + tile_margin,
            tile_size * j + tile_margin,
        )
        render_tile(context, tile, block_size)
        context.restore()


def main() -> None:
    for index in range(len(RENDERERS)):
        export(
            output=f"run/06_trade_styles_{index}.png",
            render_method_index=index,
            width=8_000,
        )


if __name__ == "__main__":
    main()
