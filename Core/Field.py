class Field:

    def __init__(self, name, byte_size, field_description, field_rules, field_units):

        self.name = name
        self.byteSize = byte_size
        self.fieldDescription = field_description
        self.fieldRules = field_rules
        self.fieldUnits = field_units

        self.fieldValue = 0