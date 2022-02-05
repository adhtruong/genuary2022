from math import pi, sqrt

from pycairo_util.cairo_context import Context, export


def draw_hexagon(context: Context, radius: float, n: int = 6) -> None:
    context.save()
    context.new_sub_path()
    context.rotate(pi / n)
    for _ in range(n):
        context.line_to(radius, 0)
        context.rotate(2 * pi / n)
    context.close_path()
    context.restore()


def draw_lines(
    context: Context,
    radius: float,
    rotation_offset: float,
) -> None:
    context.save()
    context.rotate(rotation_offset)
    for i in range(6):
        if i % 2 == 0:
            context.line_to(0, 0)
            context.line_to(radius, 0)
            context.stroke()

        context.rotate(2 * pi / 6)
    context.restore()


def draw_row(
    context: Context,
    radius: float,
    length: float,
    base_width: float,
    number_of_tiles: int,
) -> None:
    context.save()
    context.set_black()
    for i in range(number_of_tiles + 1):
        context.save()
        context.set_line_width(base_width / 4)
        draw_hexagon(context, radius)
        context.stroke()

        rotation_offset = pi / 6
        line_width = base_width / 2
        if i % 2 != 0:
            rotation_offset += pi
            line_width = base_width

        context.set_line_width(line_width)
        draw_lines(context, radius, rotation_offset)

        context.restore()

        context.translate(length, 0)
    context.restore()


def draw(context: Context, size: int) -> None:
    context.set_white()
    context.square(0, 0, size)
    context.fill()

    number_of_tiles = 8
    length = size / number_of_tiles
    radius = length / sqrt(3)

    context.translate(0, size / 2)
    for i in range(-5, 5):
        context.save()
        context.translate(length / 2 if i % 2 != 0 else 0, radius * 3 / 2 * i)
        draw_row(context, radius, length, size / 128, number_of_tiles)
        context.restore()

    context.translate(0, size / 2)


def main() -> None:
    export(output="run/29_isometric_perspective.png", width=8_000)


if __name__ == "__main__":
    main()
