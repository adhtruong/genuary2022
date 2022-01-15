from dataclasses import dataclass
from random import seed, uniform

from pycairo_util.cairo_context import Context, export


@dataclass
class Square:
    x: float
    y: float
    size: float

    def intersects(self, other: "Square") -> bool:
        return not (
            self.x + self.size < other.x
            or other.x + other.size < self.x
            or self.y + self.size < other.y
            or other.y + other.size < self.y
        )


def get_squares(
    context: Context,
    square: Square,
    attempts: int,
    original_size: int,
    iterations: int = 1,
) -> None:
    context.set_line_width(original_size / (200 * (3 - iterations)))
    context.square(square.x, square.y, square.size)
    context.stroke()
    if iterations <= 0:
        return

    context.save()
    context.translate(square.x, square.y)

    new_squares: list[Square] = []
    for _ in range(attempts):
        new_square = Square(
            uniform(0, square.size),
            uniform(0, square.size),
            uniform(square.size / 30, square.size / 3),
        )

        if new_square.x + new_square.size >= square.size or new_square.y + new_square.size >= square.size:
            continue

        if any(map(new_square.intersects, new_squares)):
            continue

        new_squares.append(new_square)

    for new_square in new_squares:
        get_squares(context, new_square, int(attempts / 10), original_size, iterations - 1)

    context.restore()


def draw(context: Context, size: int) -> None:
    seed(0)

    context.set_white()
    context.square(0, 0, size)
    context.fill()

    context.set_line_width(size / 500)
    context.set_black()
    get_squares(context, Square(0, 0, size), attempts=100_000, original_size=size, iterations=2)


def main() -> None:
    export(output="run/12_packing.png", width=8_000)


if __name__ == "__main__":
    main()
