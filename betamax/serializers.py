import json

NOT_IMPLEMENTED_ERROR_MSG = ('This method must be implemented by classes'
                             ' inheriting from BaseSerializer.')


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

    def __init__(self, cassette_path):
        if not self.name:
            raise ValueError("Serializer's name attribute must be a string"
                             " value, not None.")

        #: Provided by Betamax library when Serializer is instantiated
        self.cassette_path = cassette_path

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

        The return value is not checked.

        :param dict cassette_data: A dictionary with two keys:
            ``http_interactions``, ``recorded_with``.
        """
        raise NotImplementedError(NOT_IMPLEMENTED_ERROR_MSG)

    def deserialize(self):
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

        :returns: dictionary
        """
        raise NotImplementedError(NOT_IMPLEMENTED_ERROR_MSG)


class JSONSerializer(BaseSerializer):
    # Serializes and deserializes a cassette to JSON
    name = 'json'

    @staticmethod
    def generate_cassette_name(cassette_library_dir, cassette_name):
        import os.path
        return os.path.join(cassette_library_dir,
                            '{0}.{1}'.format(cassette_name, 'json'))

    def serialize(self, cassette_data):
        with open(self.cassette_path, 'w+') as fd:
            json.dump(cassette_data, fd)

    def deserialize(self):
        with open(self.cassette_path, 'r+') as fd:
            try:
                cassette_data = json.load(fd)
            except ValueError:
                cassette_data = {}

        return cassette_data


serializer_registry = {}
serializer_registry.update({JSONSerializer.name: JSONSerializer})
