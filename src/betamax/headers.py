"""Backport of urllib3's HTTPHeaderDict for older versions of requests.

This code was originally licensed under the MIT License and is copyrighted by
Andrey Petrov and contributors to urllib3.

This version was imported from:
https://github.com/shazow/urllib3/blob/3bd63406bef7c16d007c17563b6af14582567d4b/urllib3/_collections.py
"""
import sys

from collections import Mapping, MutableMapping

__all__ = ('HTTPHeaderDict',)

PY3 = sys.version_info >= (3, 0)


class HTTPHeaderDict(MutableMapping):
    """A ``dict`` like container for storing HTTP Headers.

    :param headers:
        An iterable of field-value pairs. Must not contain multiple field names
        when compared case-insensitively.

    :param kwargs:
        Additional field-value pairs to pass in to ``dict.update``.

    Field names are stored and compared case-insensitively in compliance with
    RFC 7230. Iteration provides the first case-sensitive key seen for each
    case-insensitive pair.

    Using ``__setitem__`` syntax overwrites fields that compare equal
    case-insensitively in order to maintain ``dict``'s api. For fields that
    compare equal, instead create a new ``HTTPHeaderDict`` and use ``.add``
    in a loop.

    If multiple fields that are equal case-insensitively are passed to the
    constructor or ``.update``, the behavior is undefined and some will be
    lost.

    >>> headers = HTTPHeaderDict()
    >>> headers.add('Set-Cookie', 'foo=bar')
    >>> headers.add('set-cookie', 'baz=quxx')
    >>> headers['content-length'] = '7'
    >>> headers['SET-cookie']
    'foo=bar, baz=quxx'
    >>> headers['Content-Length']
    '7'
    """

    def __init__(self, headers=None, **kwargs):  # noqa: D107
        super(HTTPHeaderDict, self).__init__()
        self._container = {}
        if headers is not None:
            if isinstance(headers, HTTPHeaderDict):
                self._copy_from(headers)
            else:
                self.extend(headers)
        if kwargs:
            self.extend(kwargs)

    def __setitem__(self, key, val):  # noqa: D105
        self._container[key.lower()] = (key, val)
        return self._container[key.lower()]

    def __getitem__(self, key):  # noqa: D105
        val = self._container[key.lower()]
        return ', '.join(val[1:])

    def __delitem__(self, key):  # noqa: D105
        del self._container[key.lower()]

    def __contains__(self, key):  # noqa: D105
        return key.lower() in self._container

    def __eq__(self, other):  # noqa: D105
        if not isinstance(other, Mapping) and not hasattr(other, 'keys'):
            return False
        if not isinstance(other, type(self)):
            other = type(self)(other)
        return (dict((k.lower(), v) for k, v in self.itermerged()) ==
                dict((k.lower(), v) for k, v in other.itermerged()))

    def __ne__(self, other):  # noqa: D105
        return not self.__eq__(other)

    if not PY3:  # Python 2
        iterkeys = MutableMapping.iterkeys
        itervalues = MutableMapping.itervalues

    __marker = object()

    def __len__(self):  # noqa: D105
        return len(self._container)

    def __iter__(self):  # noqa: D105
        # Only provide the originally cased names
        for vals in self._container.values():
            yield vals[0]

    def pop(self, key, default=__marker):
        """Remove specified key and return the value.

        D.pop(k[,d]) -> v

        If key is not found, d is returned if given, otherwise KeyError is
        raised.
        """
        # Using the MutableMapping function directly fails due to the private
        # marker.
        # Using ordinary dict.pop would expose the internal structures.
        # So let's reinvent the wheel.
        try:
            value = self[key]
        except KeyError:
            if default is self.__marker:
                raise
            return default
        else:
            del self[key]
            return value

    def discard(self, key):  # noqa: D102
        try:
            del self[key]
        except KeyError:
            pass

    def add(self, key, val):
        """Add a (name, value) pair.

        Doesn't overwrite the value if it already exists.

        >>> headers = HTTPHeaderDict(foo='bar')
        >>> headers.add('Foo', 'baz')
        >>> headers['foo']
        'bar, baz'
        """
        key_lower = key.lower()
        new_vals = key, val
        # Keep the common case aka no item present as fast as possible
        vals = self._container.setdefault(key_lower, new_vals)
        if new_vals is not vals:
            # new_vals was not inserted, as there was a previous one
            if isinstance(vals, list):
                # If already several items got inserted, we have a list
                vals.append(val)
            else:
                # vals should be a tuple then, i.e. only one item so far
                # Need to convert the tuple to list for further extension
                self._container[key_lower] = [vals[0], vals[1], val]

    def extend(self, *args, **kwargs):
        """Import any type of generic header-like object.

        Adapted version of MutableMapping.update in order to insert items
        with self.add instead of self.__setitem__
        """
        if len(args) > 1:
            raise TypeError("extend() takes at most 1 positional "
                            "arguments ({0} given)".format(len(args)))
        other = args[0] if len(args) >= 1 else ()

        if isinstance(other, HTTPHeaderDict):
            for key, val in other.iteritems():
                self.add(key, val)
        elif isinstance(other, Mapping):
            for key in other:
                self.add(key, other[key])
        elif hasattr(other, "keys"):
            for key in other.keys():
                self.add(key, other[key])
        else:
            for key, value in other:
                self.add(key, value)

        for key, value in kwargs.items():
            self.add(key, value)

    def getlist(self, key):
        """Return a list of all the values for the named field.

        Returns an empty list if the key doesn't exist.
        """
        try:
            vals = self._container[key.lower()]
        except KeyError:
            return []
        else:
            if isinstance(vals, tuple):
                return [vals[1]]
            else:
                return vals[1:]

    # Backwards compatibility for httplib
    getheaders = getlist
    getallmatchingheaders = getlist
    iget = getlist

    def __repr__(self):  # noqa: D105
        return "%s(%s)" % (type(self).__name__, dict(self.itermerged()))

    def _copy_from(self, other):
        for key in other:
            val = other.getlist(key)
            if isinstance(val, list):
                # Don't need to convert tuples
                val = list(val)
            self._container[key.lower()] = [key] + val

    def copy(self):  # noqa: D102
        clone = type(self)()
        clone._copy_from(self)
        return clone

    def iteritems(self):
        """Iterate over all header lines, including duplicate ones."""
        for key in self:
            vals = self._container[key.lower()]
            for val in vals[1:]:
                yield vals[0], val

    def itermerged(self):
        """Iterate over all headers, merging duplicate ones together."""
        for key in self:
            val = self._container[key.lower()]
            yield val[0], ', '.join(val[1:])

    def items(self):  # noqa: D102
        return list(self.iteritems())

    @classmethod
    def from_httplib(cls, message):  # Python 2
        """Read headers from a Python 2 httplib message object."""
        # python2.7 does not expose a proper API for exporting multiheaders
        # efficiently. This function re-reads raw lines from the message
        # object and extracts the multiheaders properly.
        headers = []

        for line in message.headers:
            if line.startswith((' ', '\t')):
                key, value = headers[-1]
                headers[-1] = (key, value + '\r\n' + line.rstrip())
                continue

            key, value = line.split(':', 1)
            headers.append((key, value.strip()))

        return cls(headers)
