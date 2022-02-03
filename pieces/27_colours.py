from itertools import cycle, product

from pycairo_util.cairo_context import Context, export

HEX_COLOURS = [
    "#2E294E",
    "#541388",
    "#F1E9DA",
    "#FFD400",
    "#D90368",
]


def get_rgb(hex_colour: str) -> tuple[float, float, float]:
    colours = (int(hex_colour[i + 1 : i + 3], 16) for i in (0, 2, 4))  # noqa
    return tuple(colours)  # type: ignore


def get_normalised_black_and_white(hex_colour: str) -> float:
    rgb = get_rgb(hex_colour)
    return sum(rgb) / (len(rgb) * 256)


def draw(context: Context, size: int, tiles: int = 7) -> None:
    context.set_white()
    context.square(0, 0, size)
    context.fill()

    colours = tuple(map(get_normalised_black_and_white, HEX_COLOURS))
    tile_size = size / tiles
    for (x, y), colour in zip(
        product(range(tiles), repeat=2),
        cycle(colours),
    ):
        context.square(x * tile_size, y * tile_size, tile_size)
        context.set_grey(colour)
        context.fill()


def main() -> None:
    for tiles in (7, 11, 13, 17, 19):
        export(
            output=f"run/27_colours_{tiles}.png",
            tiles=tiles,
            width=8_000,
        )


if __name__ == "__main__":
    main()
