class CategoryRules:

    starts_with_rules_tuples = [
        ("CVS/PHARMACY", "Pharmacy"),
        ("DUNKIN", "Coffee Shops"),
        ("HERTZ", "Rental Cars"),
        ("MTA", "Public Transportation"),
        ("SEAMLSSUPTHAI", "Food Delivery"),
        ("SHELL OIL", "Gas & Fuel"),
        ("SLICE", "Food Delivery"),
        ("TWP", "Newspapers & Magazines"),
        ("VISIBLE", "Mobile Phone")
    ]

    contains_rules_tuples = [
        ("LAUNDRY CARD", "Laundry"),
        ("WALL-ST-JOURNAL", "Newspapers & Magazines")
    ]

    @classmethod
    def initialize_category_rules(cls):
        sw_rules = []
        for tup in cls.starts_with_rules_tuples:
            swr = {'term': tup[0], 'category': tup[1]}
            sw_rules.append(swr)
        cls.starts_with_rules = sw_rules
        cont_rules = []
        for tup in cls.contains_rules_tuples:
            cr = {'term': tup[0], 'category': tup[1]}
            cont_rules.append(cr)
        cls.contains_rules = cont_rules

