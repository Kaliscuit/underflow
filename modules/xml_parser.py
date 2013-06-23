import xml.etree.ElementTree as xml_tree


def xml_to_dict(xml_str):
    xml_doc = xml_tree.fromstring(xml_str)
    doc_dict = {}
    for child in xml_doc:
        doc_dict[child.tag] = child.text
    return doc_dict