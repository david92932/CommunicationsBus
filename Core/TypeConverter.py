class TypeConverter:
    """
    Helper class to Convert between engineering and raw values
    """

    def __init__(self):
        pass

    def convertEngineeringToRaw(self, engineering_value, lsb):
        """
        engineering_value to convert into raw
        """

        return engineering_value / lsb

    def convertRawToEngineering(self, raw_value, lsb):
        """
        raw_value to convert into engineering
        """

        return raw_value * lsb

