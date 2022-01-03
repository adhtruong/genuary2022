from pycairo_util.cairo_context import Context, export


def draw(context: Context, size: int) -> None:
    context.set_white()
    context.square(0, 0, size)
    context.fill()


def main() -> None:
    export()


if __name__ == "__main__":
    main()
