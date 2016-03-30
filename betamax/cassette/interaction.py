from requests.cookies import extract_cookies_to_jar
from datetime import datetime

from betamax import util


class Interaction(object):

    """The Interaction object represents the entirety of a single interaction.

    The interaction includes the date it was recorded, its JSON
    representation, and the ``requests.Response`` object complete with its
    ``request`` attribute.

    This object also handles the filtering of sensitive data.

    No methods or attributes on this object are considered public or part of
    the public API. As such they are entirely considered implementation
    details and subject to change. Using or relying on them is not wise or
    advised.

    """

    def __init__(self, interaction, response=None):
        self.json = interaction
        self.orig_response = response
        self.recorded_response = self.deserialize()

    def as_response(self):
        """Return the Interaction as a Response object."""
        self.recorded_response = self.deserialize()
        return self.recorded_response

    @property
    def recorded_at(self):
        return datetime.strptime(self.json['recorded_at'], '%Y-%m-%dT%H:%M:%S')

    def deserialize(self):
        """Turn a serialized interaction into a Response."""
        r = util.deserialize_response(self.json['response'])
        r.request = util.deserialize_prepared_request(self.json['request'])
        extract_cookies_to_jar(r.cookies, r.request, r.raw)
        return r

    def match(self, matchers):
        """Return whether this interaction is a match."""
        request = self.json['request']
        return all(m(request) for m in matchers)

    def replace(self, text_to_replace, placeholder):
        """Replace sensitive data in this interaction."""
        self.replace_in_headers(text_to_replace, placeholder)
        self.replace_in_body(text_to_replace, placeholder)
        self.replace_in_uri(text_to_replace, placeholder)

    def replace_all(self, replacements, key_order=('replace', 'placeholder')):
        """Easy way to accept all placeholders registered."""
        (replace_key, placeholder_key) = key_order
        for r in replacements:
            self.replace(r[replace_key], r[placeholder_key])

    def replace_in_headers(self, text_to_replace, placeholder):
        for obj in ('request', 'response'):
            headers = self.json[obj]['headers']
            for k, v in list(headers.items()):
                v = util.from_list(v)
                headers[k] = v.replace(text_to_replace, placeholder)

    def replace_in_body(self, text_to_replace, placeholder):
        for obj in ('request', 'response'):
            body = self.json[obj]['body']
            old_style = hasattr(body, 'replace')
            if not old_style:
                body = body.get('string', '')

            if text_to_replace in body:
                body = body.replace(text_to_replace, placeholder)
            if old_style:
                self.json[obj]['body'] = body
            else:
                self.json[obj]['body']['string'] = body

    def replace_in_uri(self, text_to_replace, placeholder):
        for (obj, key) in (('request', 'uri'), ('response', 'url')):
            uri = self.json[obj][key]
            if text_to_replace in uri:
                self.json[obj][key] = uri.replace(
                    text_to_replace, placeholder
                )
