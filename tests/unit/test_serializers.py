import pytest
import unittest

from betamax import serializers


class TestSerializers(unittest.TestCase):
    def test_base_serializer_cannot_be_instantiated(self):
        with pytest.raises(ValueError):
            serializers.BaseSerializer('', '')
