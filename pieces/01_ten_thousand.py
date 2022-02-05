from itertools import product

from pycairo_util.cairo_context import Context, export


def render_tile(
    context: Context,
    tile_size: float,
    row: int,
    column: int,
    nesting: int,
) -> None:
    context.save()
    context.translate(row * tile_size, column * tile_size)
    context.translate(tile_size / 2, tile_size / 2)
    context.set_black()

    scale = 1 / nesting
    current_size = 1.0
    for _ in range(nesting):
        colour = current_size if (row + column) % 2 == 0 else 1 - current_size
        context.set_grey(colour)
        context.square(
            -current_size * tile_size / 2,
            -current_size * tile_size / 2,
            current_size * tile_size,
        )
        context.stroke()
        current_size -= scale
    context.restore()


def draw(context: Context, size: int) -> None:
    context.set_white()
    context.square(0, 0, size)
    context.fill()

    total = 10_000
    iterations = 10
    nesting = int(total / (iterations**2))
    tile_size = size / iterations
    for row, column in product(range(iterations), repeat=2):
        render_tile(context, tile_size, row, column, nesting)


def main() -> None:
    export(
        output="run/01_ten_thousand.png",
        width=5_000,
        height=5_000,
    )


if __name__ == "__main__":
    main()
