from itertools import cycle, product

from pycairo_util.cairo_context import Context, export, export_video


def draw_pattern(context: Context, size: float, percent: float, extra: int) -> None:
    delta = size / 25
    current_size = size + percent * extra * delta
    for colour_setter, _ in zip(
        cycle((context.set_black, context.set_white)),
        range(25 + extra),
    ):
        if current_size < 0:
            break
        margin = (size - current_size) / 2
        colour_setter()
        context.square(margin, margin, current_size)
        context.fill()

        current_size -= delta


def draw(
    context: Context,
    size: int,
    percent: float = 0,
    frames: int = 120,
    frate_rate: int = 30,
) -> None:
    context.set_white()
    context.square(0, 0, size)
    context.fill()

    tiles = 3
    tile_size = size / tiles

    raw_length = frames / frate_rate
    length = int(raw_length)
    if raw_length != length:
        raise RuntimeError(f"Unable to parse {raw_length}")

    for i, j in product(range(tiles), repeat=2):
        context.save()
        context.translate(i * tile_size, j * tile_size)
        context.square(0, 0, tile_size)
        context.clip()
        draw_pattern(context, tile_size, percent, length * 2)
        context.restore()


def main() -> None:
    export(output="run/25_perspective.png", width=6_000)
    export_video(output="run/25_perspective.mp4", frames=120, width=1_080)


if __name__ == "__main__":
    main()
