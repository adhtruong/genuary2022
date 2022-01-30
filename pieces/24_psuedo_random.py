# flake8: noqa
from itertools import product

from pycairo_util.cairo_context import Context, export


class RandomNumberGenerator:
    """RNG using middle square method"""

    def __init__(self, seed: int) -> None:
        self._length = len(str(seed))
        self._current = seed

    def get(self) -> float:
        half_length = int(self._length / 2)
        self._current = int(
            str(self._current * self._current).zfill(
                2 * self._length,
            )[half_length : 3 * half_length]
        )
        return self._current / (10 ** self._length)


def draw(context: Context, size: int) -> None:
    context.set_black()
    context.square(0, 0, size)
    context.fill()

    rng = RandomNumberGenerator(2347)

    tiles = 10
    tile_size = size / tiles
    for i, j in product(range(tiles), repeat=2):
        context.save()
        height = rng.get() * tile_size * 2 / 5
        context.translate(
            (i + 1 / 2) * tile_size,
            (j + 1 / 2) * tile_size,
        )
        context.circle(0, 0, height)

        context.set_line_width(tile_size / 8)
        context.set_white()
        context.stroke_preserve()

        context.set_line_width(tile_size / 24)
        context.set_black()
        context.stroke()

        context.restore()


def main() -> None:
    export(output="run/24_rng.png", width=8_000)


if __name__ == "__main__":
    main()
