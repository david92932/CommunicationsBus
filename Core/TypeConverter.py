class TypeConverter:

    def __init__(self):
        pass

    def convertEngineeringToRaw(self, engineering_value, lsb):

        return engineering_value / lsb

    def convertRawToEngineering(self, raw_value, lsb):

        return raw_value * lsb

