import os
import pytest
import unittest

from betamax.serializers import BaseSerializer, JSONSerializer


class TestJSONSerializer(unittest.TestCase):
    def setUp(self):
        self.cassette_dir = 'fake_dir'
        self.cassette_name = 'cassette_name'

    def test_generate_cassette_name(self):
        assert (os.path.join('fake_dir', 'cassette_name.json') ==
                JSONSerializer.generate_cassette_name(self.cassette_dir,
                                                      self.cassette_name))

    def test_generate_cassette_name_with_instance(self):
        serializer = JSONSerializer()
        assert (os.path.join('fake_dir', 'cassette_name.json') ==
                serializer.generate_cassette_name(self.cassette_dir,
                                                  self.cassette_name))


class Serializer(BaseSerializer):
    name = 'test'


class TestBaseSerializer(unittest.TestCase):
    def test_serialize_is_an_interface(self):
        serializer = Serializer()
        with pytest.raises(NotImplementedError):
            serializer.serialize({})

    def test_deserialize_is_an_interface(self):
        serializer = Serializer()
        with pytest.raises(NotImplementedError):
            serializer.deserialize('path')

    def test_requires_a_name(self):
        with pytest.raises(ValueError):
            BaseSerializer()
