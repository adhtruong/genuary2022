"""
Alphabet : A, B
Constants : F + −
Axiom : A
Production rules:
A → +BF−AFA−FB+
B → −AF+BFB+FA−
"""
from math import pi, sin
from typing import Sequence, TypeVar

from cairo import LineCap

from pycairo_util.cairo_context import Context, export

_Symbol = TypeVar("_Symbol")


def generate(
    iterations: int,
    rules: dict[_Symbol, Sequence[_Symbol]],
    axiom: tuple[_Symbol, ...],
) -> list[_Symbol]:
    result = list(axiom)
    for _ in range(iterations):
        new_result: list[_Symbol] = []
        for symbol in result:
            new_result.extend(rules.get(symbol, (symbol,)))
        result = new_result
    return result


def draw_hilbert_curve(context: Context, size: float, iterations: int) -> None:
    symbols = generate(
        iterations,
        {
            "A": "+BF-AFA-FB+",
            "B": "-AF+BFB+FA-",
        },
        tuple("A"),
    )

    line_size = size / (2**iterations - 1)
    pieces = 25
    for symbol in symbols:
        if symbol == "F":
            for i in range(pieces):
                context.set_grey(sin(i / pieces * 2 * pi) / 4 + 1 / 4)
                context.line_to(i / pieces * line_size, 0)
                context.line_to((i + 1) / pieces * line_size, 0)
                context.stroke()
            context.translate(line_size, 0)
        elif symbol == "+":
            context.rotate(-pi / 2)
        elif symbol == "-":
            context.rotate(pi / 2)


def draw(context: Context, size: int) -> None:
    context.set_white()
    context.square(0, 0, size)
    context.fill()

    margin = size / 20
    context.translate(margin, size - margin)

    context.set_line_width(size / 100)
    context.set_line_cap(LineCap.ROUND)
    context.set_black()

    iterations = 5

    draw_hilbert_curve(context, size - 2 * margin, iterations)
    context.stroke()


if __name__ == "__main__":
    export(output="run/08_single_curve.png", width=8_000)
