API
===

.. module:: betamax

.. autoclass:: Betamax
    :members:

.. autoclass:: betamax.configure.Configuration
    :members:


Examples
--------

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
