# -*- coding: utf-8 -*-
"""A set of fixtures to integrate Betamax with py.test.

.. autofunction:: betamax_session

"""

from __future__ import absolute_import

import re
import warnings

import pytest
import requests

from .. import recorder as betamax


def _sanitize(name):
    """Replace problematic characters.

    Replaces characters which might be problematic when contained in
    strings which will be used as file names with '-'s.
    """
    return re.sub(r'[\s/<>:\\"|?*]', '-', name)


def _cassette_name(request, parametrized):
    """Determine a cassette name from request.

    :param request:
        A request object from pytest giving us context information for the
        fixture.
    :param parametrized:
        Whether the name should consider parametrized tests.
    :returns:
        A cassette name.
    """
    cassette_name = ''

    if request.module is not None:
        cassette_name += request.module.__name__ + '.'

    if request.cls is not None:
        cassette_name += request.cls.__name__ + '.'

    if parametrized:
        cassette_name += _sanitize(request.node.name)
    else:
        cassette_name += request.function.__name__
        if request.node.name != request.function.__name__:
            warnings.warn(
                "betamax_recorder and betamax_session currently don't include "
                "parameters in the cassette name. "
                "Use betamax_parametrized_recorder/_session to include "
                "parameters. "
                "This behavior will be the default in betamax 1.0",
                FutureWarning, stacklevel=3)

    return cassette_name


def _betamax_recorder(request, parametrized=True):
    cassette_name = _cassette_name(request, parametrized=parametrized)
    session = requests.Session()
    recorder = betamax.Betamax(session)
    recorder.use_cassette(cassette_name)
    recorder.start()
    request.addfinalizer(recorder.stop)
    return recorder


@pytest.fixture
def betamax_recorder(request):
    """Generate a recorder with a session that has Betamax already installed.

    This will create a new Betamax instance with a generated cassette name.
    The cassette name is generated by first using the module name from where
    the test is collected, then the class name (if it exists), and then the
    test function name. For example, if your test is in ``test_stuff.py`` and
    is the method ``TestStuffClass.test_stuff`` then your cassette name will be
    ``test_stuff_TestStuffClass_test_stuff``. If the test is parametrized,
    the parameters will not be included in the name. In case you need that,
    use betamax_parametrized_recorder instead. This will change in 1.0.0,
    where parameters will be included by default.

    :param request:
        A request object from pytest giving us context information for the
        fixture.
    :returns:
        An instantiated recorder.
    """
    return _betamax_recorder(request, parametrized=False)


@pytest.fixture
def betamax_session(betamax_recorder):
    """Generate a session that has Betamax already installed.

    See `betamax_recorder` fixture.

    :param betamax_recorder:
        A recorder fixture with a configured request session.
    :returns:
        An instantiated requests Session wrapped by Betamax.
    """
    return betamax_recorder.session


@pytest.fixture
def betamax_parametrized_recorder(request):
    """Generate a recorder with a session that has Betamax already installed.

    This will create a new Betamax instance with a generated cassette name.
    The cassette name is generated by first using the module name from where
    the test is collected, then the class name (if it exists), and then the
    test function name with parameters if parametrized.
    For example, if your test is in ``test_stuff.py`` and
    the method is ``TestStuffClass.test_stuff`` with parameter ``True`` then
    your cassette name will be
    ``test_stuff_TestStuffClass_test_stuff[True]``.

    :param request:
        A request object from pytest giving us context information for the
        fixture.
    :returns:
        An instantiated recorder.
    """
    warnings.warn(
        "betamax_parametrized_recorder and betamax_parametrized_session "
        "will be removed in betamax 1.0. Their behavior will be the "
        "default.",
        DeprecationWarning)
    return _betamax_recorder(request, parametrized=True)


@pytest.fixture
def betamax_parametrized_session(betamax_parametrized_recorder):
    """Generate a session that has Betamax already installed.

    See `betamax_parametrized_recorder` fixture.

    :param betamax_parametrized_recorder:
        A recorder fixture with a configured request session.
    :returns:
        An instantiated requests Session wrapped by Betamax.
    """
    return betamax_parametrized_recorder.session
