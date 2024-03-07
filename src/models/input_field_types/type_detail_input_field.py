from src.authorities.authority_finder import AuthorityFinder
from src.models.persistence.type_detail import TypeDetail

class TypeDetailInputField:

    def what_to_persist(self, value):
        tdid = self.get_type_detail(value)
        return {self.line_item_field_name(): tdid}

    def line_item_field_name(self):
        return "type_detail_id"

    def get_type_detail(self, input_type):
        """
        Just lower-case the input
        """
        authority_finder = AuthorityFinder()
        type_to_lookup = input_type.lower()
        id = authority_finder.authority_lookup("type_detail", type_to_lookup)
        if id:
            return id
        else:
            return TypeDetail.id_for_unknown()