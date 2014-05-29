"""
betamax
=======

See http://betamax.rtfd.org/ for documentation.

:copyright: (c) 2013 by Ian Cordasco
:license: Apache 2.0, see LICENSE for more details

"""

from .exceptions import BetamaxError
from .recorder import Betamax
from .matchers import BaseMatcher
from .serializers import BaseSerializer

__all__ = [BetamaxError, Betamax, BaseMatcher, BaseSerializer]
__author__ = 'Ian Cordasco'
__copyright__ = 'Copyright 2013 Ian Cordasco'
__license__ = 'Apache 2.0'
__title__ = 'betamax'
__version__ = '0.3.1'
__version_info__ = tuple(int(i) for i in __version__.split('.'))
