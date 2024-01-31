from src.translation.description_autocat import DescriptionAutocat

class Description:

    def __init__(
        self, desc: str        
    ):
        self.desc = desc 

    def has_description_autocat(self):
        return self.desc in DescriptionAutocat.description_autocat_map        


    def autocat(self):
        return DescriptionAutocat.description_autocat_map[self.desc]    