from math import pi, sin
from random import seed, uniform

from pycairo_util.cairo_context import Context, export


def get_position(
    height: float,
    max_width: float,
    curves: float,
    steps: int,
    step: int,
) -> tuple[float, float]:
    base = step / steps
    x_offset = max_width * (1 - base)
    return (
        x_offset + (sin(2 * pi * curves * base) * abs(x_offset) / 2),
        height * base,
    )


def draw_reed(
    context: Context,
    height: float,
    max_width: float,
    curves: float,
) -> None:
    context.save()
    context.line_to(0, 0)

    positions = (
        get_position(
            height=height,
            max_width=max_width,
            curves=curves,
            steps=100,
            step=step,
        )
        for step in range(100)
    )
    for x, y in positions:
        context.line_to(x, -y)
    positions = (
        get_position(
            height=height,
            max_width=-max_width,
            curves=curves,
            steps=100,
            step=step,
        )
        for step in range(100, -1, -1)
    )
    for x, y in positions:
        context.line_to(x, -y)
    context.close_path()
    context.restore()


def draw(context: Context, size: int) -> None:
    seed(1)

    context.set_white()
    context.square(0, 0, size)
    context.fill()

    for _ in range(100):
        context.save()
        context.translate(uniform(0, size), size)
        context.set_grey(uniform(0.1, 0.75))
        draw_reed(
            context,
            uniform(size / 3, size),
            uniform(size / 30, size / 20),
            uniform(2, 3.5),
        )
        context.fill()
        context.restore()


def main() -> None:
    export(output="run/23_abstract_vegetation.png", width=8_000)


if __name__ == "__main__":
    main()
