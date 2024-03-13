class DescriptionInputField:

    def what_to_persist(self, value):
        return {self.line_item_field_name(): value}

    def line_item_field_name(self):
        return "description"
