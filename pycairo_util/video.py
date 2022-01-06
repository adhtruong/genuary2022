import os
import tempfile
from functools import partial
from typing import Any, Callable, Iterable, Union

import cv2  # type: ignore
from more_itertools import peekable

_RENDER_METHOD = Callable[[str, int], Any]


def _render_frame(directory: os.PathLike, render_method: _RENDER_METHOD, frame: int) -> str:
    file, path = tempfile.mkstemp(dir=str(directory), suffix=".png")
    os.close(file)
    render_method(path, frame)
    return path


def create_video_from_images(
    paths: Iterable[Union[os.PathLike, str]],
    output_path: Union[os.PathLike, str],
    frame_rate: float,
) -> None:
    if frame_rate <= 0:
        raise ValueError("Frame rate must be positive")

    paths = peekable(paths)
    first_path = paths.peek()
    width, height = cv2.imread(first_path).shape[:2]
    codec = cv2.VideoWriter_fourcc(*"avc1")
    out = cv2.VideoWriter(output_path, codec, frame_rate, (width, height))
    try:
        for path in paths:
            out.write(cv2.imread(path))
    finally:
        out.release()


def render_canvases(
    render_method: _RENDER_METHOD,
    frames: int,
    frame_rate: float,
    output_path: Union[os.PathLike, str],
) -> None:
    if frames <= 0:
        raise ValueError("frame must be positive")

    if frame_rate <= 0:
        raise ValueError("frame_rate must be positive")

    with tempfile.TemporaryDirectory() as directory:
        render_frame = partial(_render_frame, directory, render_method)
        paths = map(render_frame, range(frames))
        create_video_from_images(paths, output_path, frame_rate)
