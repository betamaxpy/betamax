from .base import BaseSerializer

import os
try:
    import cPickle as pickle
except ImportError:
    import pickle


class PickleSerializer(BaseSerializer):
    # Serializes and deserializes a cassette with pickle
    name = 'pickle'
    read_mode = 'rb'
    write_mode = 'wb'

    @staticmethod
    def generate_cassette_name(cassette_library_dir, cassette_name):
        return os.path.join(cassette_library_dir,
                            '{0}.{1}'.format(cassette_name, 'pickle'))

    def serialize(self, cassette_data):
        return pickle.dumps(cassette_data)

    def deserialize(self, cassette_data):
        try:
            deserialized_data = pickle.loads(cassette_data)
        except (ValueError, EOFError):
            deserialized_data = {}

        return deserialized_data
