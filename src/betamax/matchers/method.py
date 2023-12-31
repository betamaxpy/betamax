# noqa: D100
# -*- coding: utf-8 -*-
from .base import BaseMatcher


class MethodMatcher(BaseMatcher):
    """Match based on the method of the request."""

    name = 'method'

    def match(self, request, recorded_request):  # noqa: D102
        return request.method == recorded_request['method']
