import math
from pathlib import Path
from typing import Any, Callable, Iterator

from cairo import FORMAT_ARGB32
from cairo import Context as _Context
from cairo import ImageSurface, Surface

from pycairo_util.core import register, run
from pycairo_util.video import render_canvases


@register
def width() -> int:
    return 1000


@register
def height(width: int) -> int:
    return width


@register
def size(width: int, height: int) -> int:
    if width != height:
        raise RuntimeError("Unable to resolve size")
    return width


@register
def output() -> str:
    return "run/output.png"


@register(name="surface")
def get_surface(width: int, height: int, output: str) -> Iterator[Surface]:
    surface = ImageSurface(FORMAT_ARGB32, width, height)
    yield surface
    Path(output).parent.mkdir(parents=True, exist_ok=True)
    surface.write_to_png(output)


class Context(_Context):
    def square(self, x: float, y: float, size: float) -> None:
        self.rectangle(x, y, size, size)
        self.close_path()

    def circle(self, xc: float, yc: float, radius: float) -> None:
        self.arc(xc, yc, radius, 0, 2 * math.pi)

    def set_grey(self, grey: float, alpha: float = 1) -> None:
        self.set_source_rgba(grey, grey, grey, alpha)

    def set_black(self, alpha: float = 1) -> None:
        self.set_grey(0, alpha)

    def set_white(self, alpha: float = 1) -> None:
        self.set_grey(1, alpha)


@register
def context(surface: Surface) -> Context:
    return Context(surface)


def get_entry_point() -> Callable:
    import __main__

    return getattr(__main__, "draw")


def export(**kwargs: Any) -> None:
    if "draw" in kwargs:
        draw = kwargs["draw"]
    else:
        draw = get_entry_point()

    run(draw, **kwargs)


def export_video(frames: int = 60, frame_rate: int = 30, output: str = "output.mp4", **kwargs) -> None:
    if "draw" in kwargs:
        draw = kwargs["draw"]
    else:
        draw = get_entry_point()

    def render(output: str, frame: int) -> None:
        nonlocal kwargs
        kwargs_copy = kwargs.copy()
        kwargs_copy.update(output=output, frame=frame, percent=frame / frames)
        run(draw, **kwargs_copy)

    render_canvases(render, frames, frame_rate, output)
