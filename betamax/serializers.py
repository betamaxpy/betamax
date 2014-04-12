import json
import os

NOT_IMPLEMENTED_ERROR_MSG = ('This method must be implemented by classes'
                             ' inheriting from BaseSerializer.')

serializer_registry = {}


class BaseSerializer(object):

    """
    Base Serializer class that provides an interface for other serializers.

    Usage::

        from betamax import Betamax, BaseSerializer


        class MySerializer(BaseSerializer):
            name = 'my'

            @staticmethod
            def generate_cassette_name(cassette_library_dir, cassette_name):
                # Generate a string that will give the relative path of a
                # cassette

            def serialize(self, cassette_data):
                # Take a dictionary and convert it to whatever

            def deserialize(self):
                # Uses a cassette file to return a dictionary with the
                # cassette information

        Betamax.register_serializer(MySerializer)

    The last line is absolutely necessary.

    """

    name = None

    @staticmethod
    def generate_cassette_name(cassette_library_dir, cassette_name):
        raise NotImplementedError(NOT_IMPLEMENTED_ERROR_MSG)

    def __init__(self):
        if not self.name:
            raise ValueError("Serializer's name attribute must be a string"
                             " value, not None.")

        self.on_init()

    def on_init(self):
        """Method to implement if you wish something to happen in ``__init__``.

        The return value is not checked and this is called at the end of
        ``__init__``. It is meant to provide the matcher author a way to
        perform things during initialization of the instance that would
        otherwise require them to override ``BaseSerializer.__init__``.
        """
        return None

    def serialize(self, cassette_data):
        """This is a method that must be implemented by the Serializer author.

        :param dict cassette_data: A dictionary with two keys:
            ``http_interactions``, ``recorded_with``.
        :returns: Serialized data as a string.
        """
        raise NotImplementedError(NOT_IMPLEMENTED_ERROR_MSG)

    def deserialize(self, cassette_data):
        """This is a method that must be implemented by the Serializer author.

        The return value is extremely important. If it is not empty, the
        dictionary returned must have the following structure::

            {
                'http_interactions': [{
                    # Interaction
                },
                {
                    # Interaction
                }],
                'recorded_with': 'name of recorder'
            }

        :params str cassette_data: The data serialized as a string which needs
            to be deserialized.
        :returns: dictionary
        """
        raise NotImplementedError(NOT_IMPLEMENTED_ERROR_MSG)


class SerializerProxy(BaseSerializer):

    """
    This is an internal implementation detail of the betamax library.

    No users implementing a serializer should be using this. Developers
    working on betamax need only understand that this handles the logic
    surrounding whether a cassette should be updated, overwritten, or created.

    It provides one consistent way for betamax to be confident in how it
    serializes the data it receives. It allows authors of Serializer classes
    to not have to duplicate how files are handled. It delegates the
    responsibility of actually serializing the data to those classes and
    handles the rest.

    """

    def __init__(self, serializer, cassette_path, allow_serialization=False):
        self.proxied_serializer = serializer
        self.allow_serialization = allow_serialization
        self.cassette_path = cassette_path

    def _ensure_path_exists(self):
        if not os.path.exists(self.cassette_path):
            open(self.cassette_path, 'w+').close()

    @staticmethod
    def generate_cassette_name(serializer, cassette_library_dir,
                               cassette_name):
        return serializer.generate_cassette_name(
            cassette_library_dir, cassette_name
            )

    def serialize(self, cassette_data):
        if not self.allow_serialization:
            return

        self._ensure_path_exists()

        with open(self.cassette_path, 'w') as fd:
            fd.write(self.proxied_serializer.serialize(cassette_data))

    def deserialize(self):
        self._ensure_path_exists()

        data = {}
        with open(self.cassette_path) as fd:
            data = self.proxied_serializer.deserialize(fd.read())

        return data


class JSONSerializer(BaseSerializer):
    # Serializes and deserializes a cassette to JSON
    name = 'json'

    @staticmethod
    def generate_cassette_name(cassette_library_dir, cassette_name):
        return os.path.join(cassette_library_dir,
                            '{0}.{1}'.format(cassette_name, 'json'))

    def serialize(self, cassette_data):
        return json.dumps(cassette_data)

    def deserialize(self, cassette_data):
        try:
            deserialized_data = json.loads(cassette_data)
        except ValueError:
            deserialized_data = {}

        return deserialized_data


_serializers = [JSONSerializer]
serializer_registry.update(dict((s.name, s()) for s in _serializers))
del _serializers
