"""
version.py
Defines __version__ in both package and development modes
"""
from importlib.metadata import version, PackageNotFoundError
try:
    __version__=version("SVGPatcher")
except PackageNotFoundError:
    import os
    import toml
    root=os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
    pyproject_path=os.path.join(root,"pyproject.toml")
    pyproject=toml.load(pyproject_path)
    __version__=pyproject["project"]["version"]