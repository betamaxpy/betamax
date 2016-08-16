"""
betamax.

=======

See https://betamax.readthedocs.io/ for documentation.

:copyright: (c) 2013-2016 by Ian Cordasco
:license: Apache 2.0, see LICENSE for more details

"""

from .decorator import use_cassette
from .exceptions import BetamaxError
from .matchers import BaseMatcher
from .recorder import Betamax
from .serializers import BaseSerializer

__all__ = ('BetamaxError', 'Betamax', 'BaseMatcher', 'BaseSerializer',
           'use_cassette')
__author__ = 'Ian Cordasco'
__copyright__ = 'Copyright 2013-2014 Ian Cordasco'
__license__ = 'Apache 2.0'
__title__ = 'betamax'
__version__ = '0.8.0'
__version_info__ = tuple(int(i) for i in __version__.split('.'))
