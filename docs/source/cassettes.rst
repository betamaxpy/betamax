What is a cassette?
===================

A cassette is a set of recorded interactions serialized to a specific format.
Currently the only supported format is JSON_. A cassette has a list (or array)
of interactions and information about the library that recorded it. This means
that the cassette's structure (using JSON) is

.. code:: javascript

    {
      "http_interactions": [
        // ...
      ],
      "recorded_with": "betamax"
    }

Each interaction is the object representing the request and response as well
as the date it was recorded. The structure of an interaction is

.. code:: javascript

    {
      "request": {
        // ...
      },
      "response": {
        // ...
      },
      "recorded_at": "2013-09-28T01:25:38"
    }

Each request has the body, method, uri, and an object representing the
headers. A serialized request looks like:

.. code:: javascript

    {
      "body": {
        "string": "...",
        "encoding": "utf-8"
      },
      "method": "GET",
      "uri": "http://example.com",
      "headers": {
        // ...
      }
    }

A serialized response has the status_code, url, and objects
representing the headers and the body. A serialized response looks like:

.. code:: javascript

    {
      "body": {
        "encoding": "utf-8",
        "string": "..."
      },
      "url": "http://example.com",
      "status": {
        "code": 200,
        "message": "OK"
      },
      "headers": {
        // ...
      }
    }

If you put everything together, you get:

.. _cassette-dict:

.. code:: javascript

    {
      "http_interactions": [
        {
          "request": {
            {
              "body": {
                "string": "...",
                "encoding": "utf-8"
              },
              "method": "GET",
              "uri": "http://example.com",
              "headers": {
                // ...
              }
            }
          },
          "response": {
            {
              "body": {
                "encoding": "utf-8",
                "string": "..."
              },
              "url": "http://example.com",
              "status": {
                "code": 200,
                "message": "OK"
              },
              "headers": {
                // ...
              }
            }
          },
          "recorded_at": "2013-09-28T01:25:38"
        }
      ],
      "recorded_with": "betamax"
    }

If you were to pretty-print a cassette, this is vaguely what you would see.
Keep in mind that since Python does not keep dictionaries ordered, the items
may not be in the same order as this example.

.. note::

    **Pro-tip** You can pretty print a cassette like so:
    ``python -m json.tool cassette.json``.

What is a cassette library?
===========================

When configuring Betamax, you can choose your own cassette library directory.
This is the directory available from the current directory in which you want
to store your cassettes.

For example, let's say that you set your cassette library to be
``tests/cassettes/``. In that case, when you record a cassette, it will be
saved there. To continue the example, let's say you use the following code:

.. code:: python

    from requests import Session
    from betamax import Betamax


    s = Session()
    with Betamax(s, cassette_library_dir='tests/cassettes').use_cassette('example'):
        r = s.get('https://httpbin.org/get')

You would then have the following directory structure::

    .
    `-- tests
        `-- cassettes
            `-- example.json

.. _JSON: http://json.org
