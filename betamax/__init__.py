"""
github3
=======

See http://github3py.rtfd.org/ for documentation.

:copyright: (c) 2012-2013 by Ian Cordasco
:license: Modified BSD, see LICENSE for more details

"""

from betamax.exceptions import BetamaxError
from betamax.recorder import Betamax
from betamax.matchers import BaseMatcher

__all__ = [BetamaxError, Betamax, BaseMatcher]
__author__ = 'Ian Cordasco'
__copyright__ = 'Copyright 2013 Ian Cordasco'
__license__ = 'Modified BSD'
__title__ = 'betamax'
__version__ = '0.1.1'
__version_info__ = tuple(int(i) for i in __version__.split('.'))
