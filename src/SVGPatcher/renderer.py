from lxml import etree as ET
import resvg_py


def render_png(svg, outpath: str, zoom: int = 2, dpi: int | float = 300):
    svg_string = ET.tostring(svg, encoding="utf-8").decode("utf-8")
    png_output = resvg_py.svg_to_bytes(svg_string=svg_string, zoom=zoom, dpi=dpi)
    with open(outpath, "wb") as binary_file:
        binary_file.write(png_output)
