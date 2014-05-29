from .util import (deserialize_response, deserialize_prepared_request,
                   from_list)
from datetime import datetime


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
        self.recorded_at = None
        self.json = interaction
        self.orig_response = response
        self.deserialize()

    def as_response(self):
        """Returns the Interaction as a Response object."""
        return self.recorded_response

    def deserialize(self):
        """Turns a serialized interaction into a Response."""
        r = deserialize_response(self.json['response'])
        r.request = deserialize_prepared_request(self.json['request'])
        self.recorded_at = datetime.strptime(
            self.json['recorded_at'], '%Y-%m-%dT%H:%M:%S'
        )
        self.recorded_response = r

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
                v = from_list(v)
                headers[k] = v.replace(text_to_replace, placeholder)

    def replace_in_body(self, text_to_replace, placeholder):
        body = self.json['request']['body']
        # If body is not a string
        if hasattr(body, 'replace'):
            if text_to_replace in body:
                self.json['request']['body'] = body.replace(
                    text_to_replace, placeholder
                )
        # If body is a dictionary
        else:
            body = self.json['request']['body'].get('string', '')
            if text_to_replace in body:
                self.json['request']['body']['string'] = body.replace(
                    text_to_replace, placeholder
                )

        body = self.json['response']['body'].get('string', '')
        if text_to_replace in body:
            self.json['response']['body']['string'] = body.replace(
                text_to_replace, placeholder
            )

    def replace_in_uri(self, text_to_replace, placeholder):
        for (obj, key) in (('request', 'uri'), ('response', 'url')):
            uri = self.json[obj][key]
            if text_to_replace in uri:
                self.json[obj][key] = uri.replace(
                    text_to_replace, placeholder
                )
