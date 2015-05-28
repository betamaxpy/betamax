API
===

.. module:: betamax

.. autoclass:: Betamax
    :members:

.. autoclass:: betamax.configure.Configuration
    :members:

.. automodule:: betamax.fixtures.pytest

Examples
--------

Basic Usage
^^^^^^^^^^^

Let `example.json` be a file in a directory called `cassettes` with the 
content:

.. code-block:: javascript

    {
      "http_interactions": [
        {
          "request": {
            "body": {
              "string": "",
              "encoding": "utf-8"
            },
            "headers": {
              "User-Agent": ["python-requests/v1.2.3"]
            },
            "method": "GET",
            "uri": "https://httpbin.org/get"
          },
          "response": {
            "body": {
              "string": "example body",
              "encoding": "utf-8"
            },
            "headers": {},
            "status": {
              "code": 200,
              "message": "OK"
            },
            "url": "https://httpbin.org/get"
          }
        }
      ],
      "recorded_with": "betamax"
    }

The following snippet will not raise any exceptions

.. code-block:: python

    from betamax import Betamax
    from requests import Session


    s = Session()

    with Betamax(s, cassette_library_dir='cassettes') as betamax:
        betamax.use_cassette('example', record='none')
        r = s.get("https://httpbin.org/get")

On the other hand, this will raise an exception:

.. code-block:: python

    from betamax import Betamax
    from requests import Session


    s = Session()

    with Betamax(s, cassette_library_dir='cassettes') as betamax:
        betamax.use_cassette('example', record='none')
        r = s.post("https://httpbin.org/post",
                   data={"key": "value"})


pytest Integration
^^^^^^^^^^^^^^^^^^

.. versionadded:: 0.5.0

When you install Betamax, it now installs a `pytest`_ fixture by default. To
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


.. _pytest: http://pytest.org/latest/
.. _instructions:
    http://pytest.org/latest/fixture.html#using-fixtures-from-classes-modules-or-projects


.. _opinions:

Opinions at Work
----------------

If you use ``requests``'s default ``Accept-Encoding`` header, servers that 
support gzip content encoding will return responses that Betamax cannot 
serialize in a human-readable format. In this event, the cassette will look 
like this:

.. code-block:: javascript
    :emphasize-lines: 17

    {
      "http_interactions": [
        {
          "request": {
            "body": {
              "base64_string": "",
              "encoding": "utf-8"
            },
            "headers": {
              "User-Agent": ["python-requests/v1.2.3"]
            },
            "method": "GET",
            "uri": "https://httpbin.org/get"
          },
          "response": {
            "body": {
              "base64_string": "Zm9vIGJhcgo=",
              "encoding": "utf-8"
            },
            "headers": {
              "Content-Encoding": ["gzip"]
            },
            "status": {
              "code": 200,
              "message": "OK"
            },
            "url": "https://httpbin.org/get"
          }
        }
      ],
      "recorded_with": "betamax"
    }


Forcing bytes to be preserved
-----------------------------

You may want to force betamax to preserve the exact bytes in the body of a 
response (or request) instead of relying on the `opinions held by the library 
<opinions>`_. In this case you have two ways of telling betamax to do this.

The first, is on a per-cassette basis, like so:

.. code-block:: python

    from betamax import Betamax
    import requests


    session = Session()

    with Betamax.configure() as config:
        c.cassette_library_dir = '.'

    with Betamax(session).use_cassette('some_cassette',
                                       preserve_exact_body_bytes=True):
        r = session.get('http://example.com')


On the other hand, you may want to the preserve exact body bytes for all 
cassettes. In this case, you can do:

.. code-block:: python

    from betamax import Betamax
    import requests


    session = Session()

    with Betamax.configure() as config:
        c.cassette_library_dir = '.'
        c.preserve_exact_body_bytes = True

    with Betamax(session).use_cassette('some_cassette'):
        r = session.get('http://example.com')
