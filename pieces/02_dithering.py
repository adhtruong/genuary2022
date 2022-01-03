from itertools import product
from math import cos, floor, pi, sqrt
from typing import Callable, Union

from cairo import FORMAT_ARGB32, ImageSurface

from pycairo_util.cairo_context import Context, export


def get_square_surface(size: int, blocks: int = 10) -> ImageSurface:
    surface = ImageSurface(FORMAT_ARGB32, size, size)
    context = Context(surface)

    block_width = float(size) / blocks
    for x, y in product(range(10), repeat=2):
        context.set_grey(1 - (x + y) / (2 * blocks - 1))
        context.square(x * block_width, y * block_width, block_width)
        context.fill()

    return surface


def get_radial_surface(size: int) -> ImageSurface:
    surface = ImageSurface(FORMAT_ARGB32, size, size)
    context = Context(surface)

    circles = 10
    for index in range(circles, 0, -1):
        radius = float(index) / circles * size * sqrt(2) / 2
        context.set_grey(float(index) / circles)
        context.circle(size / 2, size / 2, radius)
        context.fill()

    return surface


def get_pattern(size: int) -> ImageSurface:
    surface = ImageSurface(FORMAT_ARGB32, size, size)
    context = Context(surface)

    blocks = 10
    block_width = float(size) / blocks
    for block in range(-1, blocks + 2):
        context.save()
        context.set_grey(1 - (block + 1) / (blocks))
        context.translate(block * block_width + block_width / 2, 0)
        context.line_to(0, 0)
        for y in range(size):
            context.line_to(
                block_width / 2 + cos(y / size * 2 * pi) * block_width / 2,
                y,
            )
        for y in range(size + 1, 0, -1):
            context.line_to(
                -block_width / 2 + cos(y / size * 2 * pi) * block_width / 2,
                y,
            )
        context.close_path()
        context.fill()
        context.restore()

    return surface


Colour = Union[int, float]


class _PixelWrapper:
    @classmethod
    def from_surface(cls, surface: ImageSurface, width: int) -> "_PixelWrapper":
        data = surface.get_data()
        return _PixelWrapper(list(data), width)

    def __init__(self, data: list[Colour], width: int) -> None:
        self._data: list[Colour] = data
        self._width = width

    @property
    def size(self) -> int:
        return self._width

    def get(self, x: int, y: int) -> Colour:
        index = self._get_index(x, y)
        return int(self._data[index])

    def set(self, x: int, y: int, colour: Colour) -> None:
        start_index = self._get_index(x, y)
        for index in range(start_index, start_index + 4):
            self._data[index] = colour

    def _get_index(self, x: int, y: int) -> int:
        return 4 * (y * self._width + x)

    def __len__(self) -> int:
        return int(len(self._data) / 4)

    def process_error(self, granularity: int = 9) -> None:
        for y, x in product(range(self.size), repeat=2):
            colour = self.get(x, y)
            new_colour = get_closest(colour, granularity)
            self.set(x, y, new_colour)
            error = new_colour - colour
            self._distribute_error(x, y, error)

    def _distribute_error(self, x: int, y: int, error: Colour) -> None:
        # Magic constants for Floyd distn
        self._add_error(7.0 / 16, x + 1, y, error)
        self._add_error(3.0 / 16, x - 1, y + 1, error)
        self._add_error(5.0 / 16, x, y + 1, error)
        self._add_error(1.0 / 16, x + 1, y + 1, error)

    def _add_error(self, factor: float, x: int, y: int, error: Colour) -> None:
        if x < 0 or x >= self.size or y < 0 or y >= self.size:
            return

        colour = self.get(x, y)
        self.set(x, y, colour + factor * error)


def get_closest(colour: Colour, steps: int = 1) -> Colour:
    return round((steps * colour) / 255) * floor(255 / steps)


PATTERNS = [
    get_square_surface,
    get_pattern,
    get_radial_surface,
]


def draw(
    context: Context,
    size: int,
    pattern_generator: Callable[[int], ImageSurface] = get_pattern,
) -> None:
    base_size = 50
    scale = size / base_size
    base_pattern = pattern_generator(base_size)
    data = _PixelWrapper.from_surface(base_pattern, base_size)
    data.process_error()

    context.set_white()
    context.square(0, 0, size)
    context.fill()

    context.set_black()
    for y, x in product(range(base_size), repeat=2):
        colour = data.get(x, y)
        context.circle(
            x * scale + scale / 2,
            y * scale + scale / 2,
            (255 - colour) / 255 * scale / 2,
        )
        context.fill()


def main() -> None:
    for index, pattern in enumerate(PATTERNS):
        export(
            output=f"run/02_dithering_{index}.png",
            pattern_generator=pattern,
            width=8_000,
        )


if __name__ == "__main__":
    main()
