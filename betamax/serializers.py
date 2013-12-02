serializer_registry = {}


class BaseSerializer(object):

    """
    Class that serves as the base for all custom serializers.

    Inheriting from this class will allow your custom serializer to be
    registered for use. This will provide the ``cassette_library`` and
    ``cassette_name`` for saving an entire cassette.

    Usage::

        from betamax import Betamax, BaseSerializer

        class MySerializer(BaseSerializer):
            name = 'my'

            def serialize(self, cassette):
                # Custom serialization method goes here

            def deserialize(self):
                # Custom de-serialization method goes here

        Betamax.register_serializer(MySerializer)

    The last line is necessary for all of this to work.

    A cassette that will be passed in will be a dictionary. The structure of
    that dictionary is described elsewhere in the documentation but is
    reproduced here for ease of reference::

        {
          "http_interactions": [
            {
              "request": {
                {
                  "body": "...",
                  "method": "GET",
                  "uri": "http://example.com",
                  "headers": {
                    // ...
                  }
                }
              },
              "response": {
                {
                  "body": {
                    "encoding": "utf-8",
                    "string": "..."
                  },
                  "url": "http://example.com",
                  "status_code": 200,
                  "headers": {
                    // ...
                  }
                }
              },
              "recorded_at": "2013-09-28T01:25:38"
            }
          ],
          "recorded_with": "betamax"
        }

    You are being trusted to not alter the cassette in anyway.

    """

    name = None

    def __init__(self, cassette_library, cassette_name):
        if not self.name:
            raise ValueError('Serializers must have names')

        if not (cassette_library and cassette_name):
            raise ValueError('Both cassette_library and cassette_name must be'
                             ' provided')

        self.cassette_library = cassette_library
        self.cassette_name = cassette_name

    def serialize(self, cassette):
        """This is a method that must be implemented by the user.

        :param dict cassette: A dictionary containing the cassette to be
            serialized
        """
        raise NotImplementedError('The serializer must be implemented on'
                                  ' %s' % self.__class__.name__)

    def deserialize(self):
        """This is a method that must be implemented by the user."""
        raise NotImplementedError('The serializer must be implemented on'
                                  ' %s' % self.__class__.name__)
