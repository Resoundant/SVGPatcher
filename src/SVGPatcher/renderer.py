import os
import subprocess
from lxml import etree as ET


def render_png(
    svg, outpath: str, zoom: int = 2, dpi: int | float = 300, keep_out_svg: bool = False
):
    out_svg = outpath.replace(".png", ".svg")
    et = ET.ElementTree(svg)
    et.write(out_svg, pretty_print=True)
    subprocess.run(
        [
            "resvg",
            "-z",
            str(zoom),
            "--dpi",
            str(dpi),
            "--image-rendering",
            "high-quality",
            out_svg,
            outpath,
        ],
        capture_output=True,
        text=True,
    )
    if not keep_out_svg:
        os.remove(out_svg)
