# noqa: D100
from .base import BaseSerializer

import json
import os


class JSONSerializer(BaseSerializer):
    """Serialize and deserialize a cassette to JSON."""

    name = 'json'
    stored_as_binary = False

    @staticmethod
    def generate_cassette_name(cassette_library_dir, cassette_name):  # noqa: D102, E501
        return os.path.join(cassette_library_dir,
                            '{0}.{1}'.format(cassette_name, 'json'))

    def serialize(self, cassette_data):  # noqa: D102
        return json.dumps(cassette_data)

    def deserialize(self, cassette_data):  # noqa: D102
        try:
            deserialized_data = json.loads(cassette_data)
        except ValueError:
            deserialized_data = {}

        return deserialized_data
