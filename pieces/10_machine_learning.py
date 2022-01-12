from random import choice, randint, seed, uniform

from pycairo_util.cairo_context import Context, export


def draw_path(context: Context, units: int, unit_size: float) -> None:
    y = randint(0, units)
    for x in range(units + 1):
        context.line_to(x * unit_size, y * unit_size)
        if y + 1 == units / 2 and x == units / 2 - 1:
            choices = [-1]
        elif y - 1 == units / 2 and x == units / 2 - 1:
            choices = [1]
        else:
            choices = [-1, 1]
        y += choice(choices)

    line_width = uniform(unit_size / 10, unit_size / 5)
    context.set_line_width(line_width + unit_size / 5)
    context.set_black()
    context.stroke_preserve()

    context.set_line_width(line_width)
    context.set_white()
    context.stroke()

    # context.set_grey(uniform(0, 0.75))
    # context.stroke()


def draw(context: Context, size: int) -> None:
    seed(0)

    context.set_white()
    context.square(0, 0, size)
    context.fill()

    units = 10
    unit_size = size / units

    context.save()
    context.translate(size / 2, size / 2)
    context.circle(0, 0, unit_size / 4)
    context.set_black()
    context.fill()
    context.restore()

    for _ in range(50):
        draw_path(context, units, unit_size)


def main() -> None:
    export(output="run/10_machine_learning.png", width=8_000)


if __name__ == "__main__":
    main()
