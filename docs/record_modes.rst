Record Modes
============

Betamax, like `VCR`_, has four modes that it can use to record cassettes:

- ``'all'``
- ``'new_episodes'``
- ``'none'``
- ``'once'``

You can only ever use one record mode. Below are explanations and examples of
each record mode. The explanations are blatantly taken from VCR's own `Record
Modes documentation`_.

All
---

The ``'all'`` record mode will:

- Record new interactions.
- Never replay previously recorded interactions.

This can be temporarily used to force VCR to re-record a cassette (i.e., to
ensure the responses are not out of date) or can be used when you simply want
to log all HTTP requests.

Given our file, ``examples/record_modes/all/example.py``,

.. literalinclude:: ../examples/record_modes/all/example.py
    :language: python

Every time we run it, our cassette 
(``examples/record_modes/all/all-example.json``) will be updated with new 
values.

New Episodes
------------

The ``'new_episodes'`` record mode will:

- Record new interactions.
- Replay previously recorded interactions.

It is similar to the ``'once'`` record mode, but will always record new
interactions, even if you have an existing recorded one that is similar
(but not identical, based on the :match_request_on option).

Given our file, ``examples/record_modes/new_episodes/example_original.py``, 
with which we have already recorded 
``examples/record_modes/new_episodes/new-episodes-example.json``

.. literalinclude:: ../examples/record_modes/new_episodes/example_original.py
    :language: python

If we then run ``examples/record_modes/new_episodes/example_updated.py``

.. literalinclude:: ../examples/record_modes/new_episodes/example_updated.py
    :language: python

The new request at the end of the file will be added to the cassette without 
updating the other interactions that were already recorded.

None
----

Once
----

.. _VCR: https://relishapp.com/vcr/vcr
.. _Record Modes documentation:
    https://relishapp.com/vcr/vcr/v/2-9-3/docs/record-modes/
