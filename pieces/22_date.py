from datetime import date
from itertools import product

from pycairo_util.cairo_context import Context, export

_EPOCH_START_DATE = date(1970, 1, 1)


def get_date_as_binary(date_: date, length: int = 16) -> list[bool]:
    days = (date_ - _EPOCH_START_DATE).days
    bool_values = list(format(days, "b"))
    if len(bool_values) > length:
        raise RuntimeError()
    return [
        *(False for _ in range(length - len(bool_values))),
        *map(lambda i: bool(int(i)), bool_values),
    ]


def draw_pattern(context: Context, size: float, reverse: bool) -> None:
    context.set_line_width(size / 30)
    for i in range(20):
        context.circle(0, 0, i / 20 * size)
        colour = i / 20
        if reverse:
            colour = 1 - colour
        context.set_grey(colour)
        context.stroke()


def draw(context: Context, size: int, date_: date) -> None:
    context.set_white()
    context.square(0, 0, size)
    context.fill()

    for (x, y), value in zip(
        product(range(4), repeat=2),
        get_date_as_binary(date_, 16),
    ):
        context.save()
        context.translate(
            (x + 0.5) * size / 4,
            (y + 0.5) * size / 4,
        )
        draw_pattern(context, size / 12, value)
        context.restore()


def main() -> None:
    for date_ in (date(2022, 1, 22), date(2023, 1, 22)):
        export(
            output=f"run/22_date_{date_.isoformat()}.png",
            width=8_000,
            date_=date_,
        )


if __name__ == "__main__":
    main()
