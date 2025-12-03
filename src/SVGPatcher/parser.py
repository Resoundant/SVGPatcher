from lxml import etree as ET


def load_svg(path: str):
    try:
        tree = ET.parse(path)
        root = tree.getroot()
        if not root.tag.endswith("svg"):
            raise "Root element is not <svg>"
        return root
    except ET.ParseError as e:
        raise f"Invalid SVG file: {e}"


def get_elements(root, keys: list | None = None):
    namespaces = {"re": "http://exslt.org/regular-expressions"}

    id_expression = "//*[re:test(@id, '\\{\\{(.*?)\\}\\}')]"
    id_elements = root.xpath(id_expression, namespaces=namespaces)

    text_expression = "//*[re:test(text(), '\\{\\{(.*?)\\}\\}')]"
    text_elements = root.xpath(text_expression, namespaces=namespaces)

    if keys:
        keys_expression = f"//*[re:test(@id, '^({"|".join(keys)})$')]"
        id_elements += root.xpath(keys_expression, namespaces=namespaces)

    return id_elements, text_elements
