def replace_placeholders(placeholders: dict, id_elements: list, text_elements: list):
    for text_elem in text_elements:
        for placeholder, value in placeholders.items():
            if placeholder in text_elem.text:
                replace_text(text_elem, placeholder, value)

    for id_elem in id_elements:
        for placeholder, value in placeholders.items():
            if id_elem.attrib.get("id") == placeholder and id_elem.tag.endswith(
                "image"
            ):
                replace_image(id_elem, value)


def replace_text(elem, placeholder: str, value: str):
    try:
        elem.text = elem.text.replace(placeholder, value)
    except:
        raise f"Something went wrong while replacing text for the following elem: {elem}"


def replace_image(elem, img_path: str):
    if not elem.tag.endswith("image"):
        raise f"Something went wrong while replacing image for the following elem: {elem}"

    href_key = list(filter(lambda e: "href" in e, elem.attrib.keys()))[0]

    elem.set(href_key, img_path)
