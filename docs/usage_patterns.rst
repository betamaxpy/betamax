Usage Patterns
==============

Below are suggested patterns for using Betamax efficiently.

Configuring Betamax in py.test's conftest.py
--------------------------------------------

Betamax and github3.py (the project which instigated the creation of Betamax) 
both utilize py.test_ and its feature of configuring how the tests run with 
``conftest.py`` [#]_. One pattern that I have found useful is to include this 
in your ``conftest.py`` file:

.. code-block:: python

    import betamax

    with betamax.Betamax.configure() as config:
        config.cassette_library_dir = 'tests/cassettes/'

This configures your cassette directory for all of your tests. If you do not 
check your cassettes into your version control system, then you can also add:

.. code-block:: python

    import os

    if not os.path.exists('tests/cassettes'):
        os.makedirs('tests/cassettes')

An Example from github3.py
^^^^^^^^^^^^^^^^^^^^^^^^^^

You can configure other aspects of Betamax via the ``conftest.py`` file. For 
example, in github3.py, I do the following:

.. code-block:: python

    import os

    record_mode = 'never' if os.environ.get('TRAVIS_GH3') else 'once'

    with betamax.Betamax.configure() as config:
        config.cassette_library_dir = 'tests/cassettes/'
        config.default_cassette_options['record_mode'] = record_mode
        config.define_cassette_placeholder(
            '<AUTH_TOKEN>',
            os.environ.get('GH_AUTH', 'x' * 20)
        )

In essence, if the tests are being run on TravisCI_, then we want to make sure 
to not try to record new cassettes or interactions. We also, want to make sure 
we're authenticated when possible but that we do not leave our placeholder in 
the cassettes when they're replayed.

py.test Integration
-------------------

.. versionadded:: 0.5.0

When you install Betamax, it now installs a `py.test`_ fixture by default. To
use it in your tests you need only follow the `instructions`_ on pytest's
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


.. _TravisCI: https://travis-ci.org/
.. [#] http://pytest.org/latest/plugins.html
.. _py.test: http://pytest.org/latest/
.. _instructions:
    http://pytest.org/latest/fixture.html#using-fixtures-from-classes-modules-or-projects
