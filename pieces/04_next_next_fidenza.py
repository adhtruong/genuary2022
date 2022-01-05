from math import cos, pi, sin
from random import choice, random, seed, uniform
from typing import Any, NamedTuple

from opensimplex import noise2  # type: ignore
from opensimplex.opensimplex import OpenSimplex  # type: ignore

from pycairo_util.cairo_context import Context, export


class Vector(NamedTuple):
    x: float
    y: float

    @classmethod
    def from_polar(cls, size: float, angle: float) -> "Vector":
        return Vector(size * cos(angle), size * sin(angle))

    @classmethod
    def unit_polar(cls, angle: float) -> "Vector":
        return Vector(cos(angle), sin(angle))

    def __add__(self, other: Any) -> "Vector":
        return Vector(self.x + other[0], self.y + other[1])

    def __sub__(self, other: "Vector") -> "Vector":
        return Vector(self.x - other.x, self.y - other.y)


def get_random_vector(size: int) -> Vector:
    return Vector(
        uniform(-size / 10, size * 11 / 10),
        uniform(-size / 10, size * 11 / 10),
    )


def render_blocks(context: Context, size: int) -> None:
    colours = [random() for _ in range(5)]

    for _ in range(4000):
        context.save()
        point = get_random_vector(size)
        context.translate(point.x, point.y)
        context.rotate(
            noise2(point.x / size * 2, point.y / size * 2) * 2 * pi,
        )
        width = uniform(20, 40)
        height = uniform(30, 100)
        print(width, height)
        context.rectangle(-width / 2, -height / 2, width, height)
        context.set_grey(choice(colours), 0.9)
        context.fill_preserve()
        context.set_black()
        context.stroke()
        context.restore()


def draw(context: Context, size: int) -> None:
    seed(0)

    context.set_white()
    context.square(0, 0, size)
    context.fill()

    number_of_particles = 10_000
    iterations = 250

    noise = OpenSimplex().noise2
    for index in range(number_of_particles):
        print(f"Particle {index}/{number_of_particles}")
        position = get_random_vector(size)
        context.set_grey(random())
        for _ in range(iterations):
            context.circle(position.x, position.y, size / 500)
            context.fill()

            angle = noise(position.x / size * 2, position.y / size * 2) * 2 * pi
            position += (size / 1000 * cos(angle), size / 1000 * sin(angle))


def main() -> None:
    export(output="run/04_fidenza_.png", width=8_000)


if __name__ == "__main__":
    main()
