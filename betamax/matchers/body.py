# -*- coding: utf-8 -*-
from .base import BaseMatcher
from ..cassette.util import deserialize_prepared_request


class BodyMatcher(BaseMatcher):
    # Matches based on the body of the request
    name = 'body'

    def match(self, request, recorded_request):
        recorded_request = deserialize_prepared_request(recorded_request)
        return recorded_request.body == (request.body or b'')
