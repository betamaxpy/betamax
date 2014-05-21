# -*- coding: utf-8 -*-
from .interaction import Interaction
from .util import (_option_from, serialize_prepared_request,
                   serialize_response, timestamp)
from betamax.matchers import matcher_registry
from betamax.serializers import serializer_registry, SerializerProxy
from datetime import datetime
from functools import partial

import os.path


class Cassette(object):

    default_cassette_options = {
        'record_mode': 'once',
        'match_requests_on': ['method', 'uri'],
        're_record_interval': None,
        'placeholders': [],
        'preserve_exact_body_bytes': False
    }

    def __init__(self, cassette_name, serialization_format, **kwargs):
        #: Short name of the cassette
        self.cassette_name = cassette_name

        self.serialized = None

        defaults = Cassette.default_cassette_options

        # Determine the record mode
        self.record_mode = _option_from('record_mode', kwargs, defaults)

        # Retrieve the serializer for this cassette
        self.serializer = SerializerProxy.find(
            serialization_format, kwargs.get('cassette_library_dir'),
            cassette_name
            )
        self.cassette_path = self.serializer.cassette_path

        # Determine which placeholders to use
        self.placeholders = kwargs.get('placeholders')
        if not self.placeholders:
            self.placeholders = defaults['placeholders']

        # Determine whether to preserve exact body bytes
        self.preserve_exact_body_bytes = _option_from(
            'preserve_exact_body_bytes', kwargs, defaults
            )

        # Initialize the interactions
        self.interactions = []

        # Initialize the match options
        self.match_options = set()

        self.load_interactions()
        self.serializer.allow_serialization = self.is_recording()

    @staticmethod
    def can_be_loaded(cassette_library_dir, cassette_name, serialize_with,
                      record_mode):
        # If we want to record a cassette we don't care if the file exists
        # yet
        recording = False
        if record_mode in ['once', 'all', 'new_episodes']:
            recording = True

        serializer = serializer_registry.get(serialize_with)
        if not serializer:
            raise ValueError(
                'Serializer {0} is not registered with Betamax'.format(
                    serialize_with
                    ))

        cassette_path = serializer.generate_cassette_name(
            cassette_library_dir, cassette_name
            )
        # Otherwise if we're only replaying responses, we should probably
        # have the cassette the user expects us to load and raise.
        return os.path.exists(cassette_path) or recording

    def clear(self):
        # Clear out the interactions
        self.interactions = []
        # Serialize to the cassette file
        self._save_cassette()

    @property
    def earliest_recorded_date(self):
        """The earliest date of all of the interactions this cassette."""
        if self.interactions:
            i = sorted(self.interactions, key=lambda i: i.recorded_at)[0]
            return i.recorded_at
        return datetime.now()

    def eject(self):
        self._save_cassette()

    def find_match(self, request):
        """Find a matching interaction based on the matchers and request.

        This uses all of the matchers selected via configuration or
        ``use_cassette`` and passes in the request currently in progress.

        :param request: ``requests.PreparedRequest``
        :returns: :class:`Interaction <Interaction>`
        """
        opts = self.match_options
        # Curry those matchers
        matchers = [partial(matcher_registry[o].match, request) for o in opts]

        for i in self.interactions:
            if i.match(matchers):  # If the interaction matches everything
                if self.record_mode == 'all':
                    # If we're recording everything and there's a matching
                    # interaction we want to overwrite it, so we remove it.
                    self.interactions.remove(i)
                    break
                return i

        # No matches. So sad.
        return None

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

    def sanitize_interactions(self):
        for i in self.interactions:
            i.replace_all(self.placeholders)

    def save_interaction(self, response, request):
        interaction = self.serialize_interaction(response, request)
        self.interactions.append(Interaction(interaction, response))

    def serialize_interaction(self, response, request):
        return {
            'request': serialize_prepared_request(
                request,
                self.preserve_exact_body_bytes
                ),
            'response': serialize_response(
                response,
                self.preserve_exact_body_bytes
                ),
            'recorded_at': timestamp(),
        }

    # Private methods
    def _save_cassette(self):
        self.sanitize_interactions()

        cassette_data = {
            'http_interactions': [i.json for i in self.interactions],
            'recorded_with': 'betamax/{version}'
        }
        self.serializer.serialize(cassette_data)
