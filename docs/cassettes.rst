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
      "body": "...",
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
      "status_code": 200,
      "headers": {
        // ...
      }
    }

If you put everything together, you get:

.. code:: javascript

    {
      "http_interactions": [
        {
          "request": {
            {
              "body": "...",
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
              "status_code": 200,
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
Keep in mind that Python since does not keep dictionaries ordered, the items
may not be in the same order as this example.

.. note::

    **Pro-tip** You can pretty print a cassette like so:
    ``python -m json.tool cassette.json``.

.. _JSON: http://json.org
