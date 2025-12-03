import os
import subprocess
from lxml import etree as ET


def render_png(svg, outpath: str, zoom: int = 2, dpi: int | float = 300):
    et = ET.ElementTree(svg)
    et.write("temp_output.svg", pretty_print=True)
    subprocess.run(
        [
            "resvg",
            "-z",
            str(zoom),
            "--dpi",
            str(dpi),
            "--image-rendering",
            "high-quality",
            "temp_output.svg",
            outpath,
        ],
        capture_output=True,
        text=True,
    )
    os.remove("temp_output.svg")
