Integrating Betamax with Test Frameworks
========================================

It's nice to have a way to integrate libraries you use for testing into your
testing frameworks. Having considered this, the authors of and contributors to
Betamax have included integrations in the package. Betamax comes with
integrations for py.test and unittest. (If you need an integration for another
framework, please suggest it and send a patch!)

PyTest Integration
------------------

.. versionadded:: 0.5.0

.. versionchanged:: 0.6.0

When you install Betamax, it now installs two `py.test`_ fixtures by default.
To use it in your tests you need only follow the `instructions`_ on pytest's
documentation. To use the ``betamax_session`` fixture for an entire class of
tests you would do:

.. code-block:: python

    # tests/test_http_integration.py
    import pytest

    @pytest.mark.usefixtures('betamax_session')
    class TestMyHttpClient:
        def test_get(self, betamax_session):
            betamax_session.get('https://httpbin.org/get')

This will generate a cassette name for you, e.g.,
``tests.test_http_integration.TestMyHttpClient.test_get``. After running this
test you would have a cassette file stored in your cassette library directory
named ``tests.test_http_integration.TestMyHttpClient.test_get.json``. To use
this fixture at the module level, you need only do

.. code-block:: python

    # tests/test_http_integration.py
    import pytest

    pytest.mark.usefixtures('betamax_session')


    class TestMyHttpClient:
        def test_get(self, betamax_session):
            betamax_session.get('https://httpbin.org/get')

    class TestMyOtherHttpClient:
        def test_post(self, betamax_session):
            betamax_session.post('https://httpbin.org/post')

If you need to customize the recorder object, however, you can instead use the
``betamax_recorder`` fixture:

.. code-block:: python

    # tests/test_http_integration.py
    import pytest

    pytest.mark.usefixtures('betamax_recorder')


    class TestMyHttpClient:
        def test_post(self, betamax_recorder):
            betamax_recorder.current_cassette.match_options.add('json-body')
            session = betamax_recorder.session

            session.post('https://httpbin.org/post', json={'foo': 'bar'})


Unittest Integration
--------------------

.. versionadded:: 0.5.0

When writing tests with unittest, a common pattern is to either import
:class:`unittest.TestCase` or subclass that and use that subclass in your
tests. When integrating Betamax with your unittest testsuite, you should do
the following:

.. code-block:: python

    from betamax.fixtures import unittest


    class IntegrationTestCase(unitest.BetamaxTestCase):
        # Add your the rest of the helper methods you want for your
        # integration tests


    class SpecificTestCase(IntegrationTestCase):
        def test_something(self):
            # Test something

The unittest integration provides the following attributes on the test case
instance:

- ``session`` the instance of ``BetamaxTestCase.SESSION_CLASS`` created for
  that test.

- ``recorder`` the instance of :class:`betamax.Betamax` created.

The integration also generates a cassette name from the test case class name
and test method. So the cassette generated for the above example would be
named ``SpecificTestCase.test_something``. To override that behaviour, you
need to override the
:meth:`~betamax.fixtures.BetamaxTestCase.generate_cassette_name` method in
your subclass.

If you are subclassing :class:`requests.Session` in your application, then it
follows that you will want to use that in your tests. To facilitate this, you
can set the ``SESSION_CLASS`` attribute. To give a fuller example, let's say
you're changing the default cassette name and you're providing your own
session class, your code might look like:

.. code-block:: python

    from betamax.fixtures import unittest

    from myapi import session


    class IntegrationTestCase(unitest.BetamaxTestCase):
        # Add your the rest of the helper methods you want for your
        # integration tests
        SESSION_CLASS = session.MyApiSession

        def generate_cassette_name(self):
            classname = self.__class__.__name__
            method = self._testMethodName
            return 'integration_{0}_{1}'.format(classname, method)

.. _py.test: http://pytest.org/latest/
.. _instructions:
    http://pytest.org/latest/fixture.html#using-fixtures-from-classes-modules-or-projects
