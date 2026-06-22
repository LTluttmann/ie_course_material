import io
import base64
import numpy as np

from PIL import Image, ImageDraw, ImageChops
from io import BytesIO
from typing import Union, Literal



def resize(img: Image.Image, largest_size: int = None, min_size: int = None) -> Image.Image:
    if largest_size is not None and min_size is not None:
        assert largest_size > min_size
    if largest_size is None and min_size is None:
        return img
    if min_size is not None:
        return resize_with_min_size(img, min_size=min_size)
    longer_side = np.argmax(img.size)
    percent = (largest_size / float(img.size[longer_side]))
    if percent < 1:
        imsize = tuple(map(lambda x: int(x * percent), img.size))
        img = img.resize(imsize, Image.Resampling.LANCZOS)
    return img


def resize_with_min_size(image: Image.Image, min_size: int = 1028) -> Image.Image:
    width, height = image.size
    short_side = min(width, height)

    scale = min_size / short_side
    new_width = int(width * scale)
    new_height = int(height * scale)

    resized_image = image.resize((new_width, new_height), Image.Resampling.LANCZOS)
    return resized_image


def encode_image(image_or_path: Union[str, Image.Image], largest_size: int = None, format: Literal["JPEG", "PNG"] = "PNG"):
    # Bilddatei einlesen und in Base64 umwandeln
    if isinstance(image_or_path, str):
        image = Image.open(image_or_path)
    else:
        image = image_or_path
    if largest_size is not None:
        image = resize(image, largest_size=largest_size)

    buffer = BytesIO()
    image.save(buffer, format=format)
    base64_image = base64.b64encode(buffer.getvalue()).decode("utf-8")
    return base64_image
