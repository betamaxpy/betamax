What is a cassette?
===================

A cassette is a set of recorded interactions serialized to a specific format.
Currently the only supported format is JSON_. A cassette has a list (or array)
of interactions and information about the library that recorded it. This means
that the cassette's structure (using JSON) is

.. code:: javascript

    {
      'http_interactions': [
        // ...
      ],
      'recorded_with': 'betamax'
    }


.. _JSON: http://json.org
