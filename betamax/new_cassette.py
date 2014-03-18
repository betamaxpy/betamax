from betamax.serializers import serializer_registry, SerializerProxy
from betamax.cassette import Interaction
from datetime import datetime


class NewCassette(object):

    default_cassette_options = {
        'record_mode': 'once',
        'match_requests_on': ['method', 'uri'],
        're_record_interval': None,
        'placeholders': []
    }

    def __init__(self, cassette_name, serialization_format, **kwargs):
        #: Short name of the cassette
        self.cassette_name = cassette_name

        # Determine the record mode
        self.record_mode = kwargs.get(
            'record_mode',
            NewCassette.default_cassette_options['record_mode']
            )

        # Retrieve the serializer for this cassette
        serializer = serializer_registry.get(serialization_format)
        if serializer is None:
            raise ValueError(
                'No serializer registered for {0}'.format(serialization_format)
                )

        self.serializer = SerializerProxy(serializer, cassette_name,
                                          self.is_recording())

        # Determine which placeholders to use
        self.placeholders = kwargs.get(
            'placeholders',
            NewCassette.default_cassette_options['placeholders']
            )

        # Initialize the interactions
        self.interactions = []

        # Initialize the match options
        self.match_options = set()

        self.load_interactions()

    @property
    def earliest_recorded_date(self):
        """The earliest date of all of the interactions this cassette."""
        if self.interactions:
            i = sorted(self.interactions, key=lambda i: i.recorded_at)[0]
            return i.recorded_at
        return datetime.now()

    def is_empty(self):
        """Determines if the cassette when loaded was empty."""
        return not self.serialized

    def is_recording(self):
        """Returns if the cassette is recording."""
        values = {
            'none': False,
            'once': self.is_empty(),
        }
        return values.get(self.record_mode, True)

    def load_interactions(self):
        if self.serialized is None:
            self.serialized = self.serializer.deserialize()

        interactions = self.serialized.get('http_interactions', [])
        self.interactions = [Interaction(i) for i in interactions]

        for i in self.interactions:
            i.replace_all(self.placeholders, ('placeholder', 'replace'))
