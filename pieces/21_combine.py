from functools import partial
from importlib import import_module

from cairo import FORMAT_ARGB32, ImageSurface

from pycairo_util.cairo_context import Context, export

dithering = import_module("pieces.02_dithering")


_PREVIOUS = [
    "pieces.14_something_you_woudnt_make",
    "pieces.05_destroy_a_square",
    "pieces.07_sol_lewitt",
]


def render_previous(module: str, size: int) -> ImageSurface:
    surface = ImageSurface(FORMAT_ARGB32, size, size)
    context = Context(surface)
    import_module(module).draw(context, size)
    return surface


def draw(context: Context, size: int, previous: str) -> None:
    dithering.draw(context, size, partial(render_previous, previous))


def main() -> None:
    for module in _PREVIOUS:
        _, module_name = module.split(".")
        export(output=f"run/output_{module_name}.png", previous=module)


if __name__ == "__main__":
    main()
