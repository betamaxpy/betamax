# -*- coding: utf-8 -*-
from .base import BaseMatcher


class DigestAuthMatcher(BaseMatcher):
    name = 'digest-auth'

    def match(self, request, recorded_request):
        request_digest = self.digest_parts(request.headers)
        recorded_digest = self.digest_parts(recorded_request['headers'])
        return request_digest == recorded_digest

    def digest_parts(self, headers):
        auth = headers.get('Authorization') or headers.get('authorization')
        if not auth:
            return None
        auth = auth.strip('Digest ')
        excludes = ('cnonce', 'response')
        return [p for p in auth.split(', ') if not p.startswith(excludes)]
