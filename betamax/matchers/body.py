# -*- coding: utf-8 -*-
from .base import BaseMatcher
from betamax.util import deserialize_prepared_request


class BodyMatcher(BaseMatcher):
    # Matches based on the body of the request
    name = 'body'

    def match(self, request, recorded_request):
        recorded_request = deserialize_prepared_request(recorded_request)

        if request.body:
            if isinstance(recorded_request.body, type(request.body)):
                request_body = request.body
            else:
                request_body = request.body.encode('utf-8')
        else:
            request_body = b''

        return recorded_request.body == request_body
