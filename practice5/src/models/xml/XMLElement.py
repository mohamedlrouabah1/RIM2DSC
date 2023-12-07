class XMLElement:
    def __init__(self, xml_dict):
        # self.tag = tag
        # self.attributes = attributes
        self.text_content = None
        # TODO: recursively creat XMLElement for all childrens of the current tag.
        self.children 