from functools import partial
from math import copysign, cos, pi, sin

from pycairo_util.cairo_context import Context, export, export_video

sign = partial(copysign, 1)


def draw(context: Context, size: int, percent: float = 0) -> None:
    context.set_white()
    context.square(0, 0, size)
    context.fill()

    context.translate(size / 2, size / 2)

    margin = size / 5
    total_size = size - 2 * margin
    squares = 20
    line_width = total_size / squares
    context.set_line_width(line_width)
    for index in range(squares, 0, -1):
        context.save()
        offset = total_size / 2 * cos(percent * 4 * pi)
        context.translate(
            offset * cos(index / squares * 2 * pi),
            offset * sin(index / squares * 2 * pi),
        )
        current_size = line_width * (index / 2)
        context.square(-current_size / 2, -current_size / 2, current_size)
        context.set_black(alpha=index / squares)
        context.stroke()
        context.restore()


def main() -> None:
    export(output="run/05_square.png", width=8_000)
    export_video(output="run/05_square.mp4", frames=120, width=2_000)


if __name__ == "__main__":
    main()
