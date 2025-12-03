from parser import get_elements, load_svg
from renderer import render_png
from replacer import replace_placeholders


class SVGTemplate:
    def __init__(self, svg_path: str):
        self.svg_path = svg_path
        self.root = load_svg(svg_path)

    def replace(self, placeholders: dict):
        self.root = load_svg(self.svg_path)
        id_elements, text_elements = get_elements(self.root, placeholders.keys())
        replace_placeholders(placeholders, id_elements, text_elements)

    def save(self, outpath: str):
        render_png(self.root, outpath)
