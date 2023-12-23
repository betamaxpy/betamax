# noqa: D100
# -*- coding: utf-8 -*-
from .base import BaseMatcher


class HeadersMatcher(BaseMatcher):
    """Match based on the headers of the request."""

    name = 'headers'

    def match(self, request, recorded_request):  # noqa: D102
        return dict(request.headers) == self.flatten_headers(recorded_request)

    def flatten_headers(self, request):  # noqa: D102
        from betamax.util import from_list
        headers = request['headers'].items()
        return dict((k, from_list(v)) for (k, v) in headers)
