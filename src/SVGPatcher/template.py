from SVGPatcher.parser import get_placeholder_elements, load_svg
from SVGPatcher.renderer import render_png
from SVGPatcher.replacer import replace_placeholders


class SVGTemplate:
    def __init__(self, svg_path: str):
        self.svg_path = svg_path
        self.root = load_svg(svg_path)

    def get_elem(self, id):
        keys_expression = f"//*[@id='{id}']"
        elems = self.root.xpath(keys_expression)
        if len(elems):
            return elems[0]
        return None

    def set_image(self, id, image_id):
        elem = self.get_elem(id)
        if elem is not None:
            elem.attrib["id"] = image_id
        return self

    def set_fill(self, id, fill):
        elem = self.get_elem(id)
        if elem is not None:
            elem.set("fill", fill)
        return self

    def remove(self, id):
        elem = self.get_elem(id)
        if elem is not None:
            elem.getparent().remove(elem)
        return self

    def replace(self, placeholders: dict, new_copy=True):
        if new_copy:
            self.root = load_svg(self.svg_path)
        id_elements, text_elements = get_placeholder_elements(
            self.root, placeholders.keys()
        )
        replace_placeholders(placeholders, id_elements, text_elements)
        return self

    def png_bytes(self, zoom: int = 2, dpi: int | float = 300):
        return render_png(self.root, zoom=zoom, dpi=dpi)

    def save(self, outpath: str, zoom: int = 2, dpi: int | float = 300):
        render_png(self.root, outpath, zoom=zoom, dpi=dpi)
        return self
