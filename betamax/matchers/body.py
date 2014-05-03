# -*- coding: utf-8 -*-
from .base import BaseMatcher


class BodyMatcher(BaseMatcher):
    # Matches based on the body of the request
    name = 'body'

    def match(self, request, recorded_request):
        return request.body == recorded_request['body']
