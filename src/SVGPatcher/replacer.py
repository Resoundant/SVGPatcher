from lxml import etree as ET


def replace_placeholders(placeholders: dict, id_elements: list, text_elements: list):
    for text_elem in text_elements:
        for placeholder, value in placeholders.items():
            if placeholder in text_elem.text:
                replace_text(text_elem, placeholder, value)

    for id_elem in id_elements:
        for placeholder, value in placeholders.items():
            if id_elem.attrib["id"] == placeholder and id_elem.tag.endswith("image"):
                replace_image(id_elem, value)

            if (
                id_elem.attrib["id"] == placeholder
                and id_elem.tag.endswith("rect")
                and "url(#" in id_elem.attrib["fill"]
            ):
                img_elem = rect_to_img(id_elem)
                replace_image(img_elem, value)


def replace_text(elem, placeholder: str, value: str):
    try:
        elem.text = elem.text.replace(placeholder, value)
    except:
        raise f"Something went wrong while replacing text for the following elem: {ET.tostring(elem, pretty_print=True)}"


def replace_image(elem, img_path: str):
    if not elem.tag.endswith("image"):
        raise f"Something went wrong while replacing image for the following elem: {ET.tostring(elem, pretty_print=True)}"

    href_key = list(filter(lambda e: "href" in e, elem.attrib.keys()))[0]

    elem.set(href_key, img_path)


def replace_elem(old_elem, new_elem):
    old_elem.getparent().replace(old_elem, new_elem)
    return new_elem


def rect_to_img(elem):
    img = ET.Element(
        "{http://www.w3.org/2000/svg}image",
        {
            "href": "",
            "x": elem.attrib.get("x"),
            "y": elem.attrib.get("y"),
            "width": elem.attrib.get("width"),
            "height": elem.attrib.get("height"),
        },
    )

    return replace_elem(elem, img)
