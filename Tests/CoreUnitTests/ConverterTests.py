import pytest
from Core.TypeConverter import convertEngineeringToRaw, convertRawToEngineering

class ConverterTests:

    def test_one(self):
        value = 5
        lsb = 0.025
        raw_value = convertRawToEngineering(value, lsb)
        assert raw_value == 200
