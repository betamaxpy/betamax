matcher_registry = {}

from .base import BaseMatcher
from .body import BodyMatcher
from .headers import HeadersMatcher
from .host import HostMatcher
from .method import MethodMatcher
from .path import PathMatcher
from .query import QueryMatcher
from .uri import URIMatcher


__all__ = ['BaseMatcher', 'BodyMatcher', 'HeadersMatcher', 'HostMatcher',
           'MethodMatcher', 'PathMatcher', 'QueryMatcher', 'URIMatcher']


_matchers = [BodyMatcher, HeadersMatcher, HostMatcher, MethodMatcher,
             PathMatcher, QueryMatcher, URIMatcher]
matcher_registry.update(dict((m.name, m()) for m in _matchers))
del _matchers
