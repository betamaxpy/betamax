"""
betamax
=======

See http://betamax.rtfd.org/ for documentation.

:copyright: (c) 2013 by Ian Cordasco
:license: Apache 2.0, see LICENSE for more details

"""

from betamax.exceptions import BetamaxError
from betamax.recorder import Betamax
from betamax.matchers import BaseMatcher

__all__ = [BetamaxError, Betamax, BaseMatcher]
__author__ = 'Ian Cordasco'
__copyright__ = 'Copyright 2013 Ian Cordasco'
__license__ = 'Apache 2.0'
__title__ = 'betamax'
__version__ = '0.1.4'
__version_info__ = tuple(int(i) for i in __version__.split('.'))
