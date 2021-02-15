class Field:

    def __init__(self, name: str, byte_size: int, field_description: str, field_rules: [], field_units: str):

        self.name = name
        self.byteSize = byte_size
        self.fieldDescription = field_description
        self.fieldRules = field_rules

        self.fieldUnits = field_units

        self.fieldValue = 0

    def setFieldValue(self, value):

        # add rule checks

        print(f'setting field {self.name} to {value}')
        self.fieldValue = value