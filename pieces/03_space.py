from dataclasses import dataclass
from math import cos, pi, sin
from random import random, seed, uniform

from pycairo_util.cairo_context import Context, export


def polar_to_cart(radius: float, angle: float) -> tuple[float, float]:
    return radius * cos(angle), radius * sin(angle)


@dataclass
class Point:
    radius: float
    angle: float
    grey: float
    alpha: float
    size: float


def get_points(seed_: int, number_of_points: int, size: int) -> list[Point]:
    seed(seed_)
    return [
        Point(
            size - random() * size,
            angle=random() * 2 * pi,
            grey=random() * 0.6 + 0.4,
            alpha=random(),
            size=2 * uniform(size / 500, size / 5000),
        )
        for _ in range(number_of_points)
    ]


def draw(context: Context, size: int) -> None:
    context.set_black()
    context.square(0, 0, size)
    context.fill()

    context.translate(size / 2, size / 2)

    for point in get_points(0, 1000, size):
        for i in range(5):
            radius = point.radius * 1.005**i
            context.set_grey(point.grey * 1.05**i, point.alpha)
            x = radius * cos(point.angle)
            y = radius * sin(point.angle)
            context.circle(x, y, point.size)
            context.fill()


def main() -> None:
    export(
        output="run/03_space.png",
        width=8_000,
        height=8_000,
    )


if __name__ == "__main__":
    main()
