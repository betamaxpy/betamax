# noqa: D100
# -*- coding: utf-8 -*-
from .base import BaseMatcher
from requests.compat import urlparse


class PathMatcher(BaseMatcher):
    """Match based on the path of the request."""

    name = 'path'

    def match(self, request, recorded_request):  # noqa: D102
        request_path = urlparse(request.url).path
        recorded_path = urlparse(recorded_request['uri']).path
        return request_path == recorded_path
