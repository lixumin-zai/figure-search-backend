from pathlib import Path
import io
import base64
import re

import streamlit.components.v1 as components
from PIL import Image

frontend_dir = (Path(__file__).parent / "frontend").absolute()
_component_func = components.declare_component(
    "streamlit_camera", path=str(frontend_dir)
)

def _data_url_to_image(data_url: str) -> Image:
    """Convert base64 data string an Pillow Image"""
    _, _data_url = data_url.split(";base64,")
    return _data_url

def camera(is_restart):
    component_value = _component_func(data = is_restart)
    if component_value is None:
        return "", " "
    if component_value:
        image_base64, verification_code = component_value["image"], component_value["text"]
        return _data_url_to_image(image_base64), verification_code
    else:
        return "", ""