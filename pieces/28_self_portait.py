from itertools import product
from typing import Iterable

from PIL import Image  # type: ignore

from pycairo_util.cairo_context import Context, export

_SOURCE = "assets\\WIN_20220203_19_51_20_Pro.jpg"


def get_pixels(size: int) -> Iterable[tuple[int, int, int]]:
    image = Image.open(_SOURCE)

    width, height = image.size
    minimum = min(width, height)

    image = image.crop(
        (
            width / 2 - minimum / 2,
            height / 2 - minimum / 2,
            width / 2 + minimum / 2,
            height / 2 + minimum / 2,
        )
    )

    image_small = image.resize((size, size), resample=Image.BILINEAR)
    yield from image_small.getdata()


def bound(p: float, n: int) -> float:
    return int(p * n) / n


def draw(context: Context, size: int) -> None:
    context.set_white()
    context.square(0, 0, size)
    context.fill()

    pixels = 48
    tile_size = size / pixels
    for (y, x), pixel in zip(
        product(range(pixels), repeat=2),
        get_pixels(pixels),
    ):
        bounded_size = bound(sum(pixel) / (3 * 256), 8)

        context.circle(
            (x + 0.5) * tile_size,
            (y + 0.5) * tile_size,
            tile_size / 2 * bounded_size,
        )
        context.set_black()
        context.stroke_preserve()
        context.fill()


def main() -> None:
    export(output="run/28_self_portrait.png", width=8_000)


if __name__ == "__main__":
    main()
