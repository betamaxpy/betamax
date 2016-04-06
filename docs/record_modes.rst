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

The ``'none'`` record mode will:

- Replay previously recorded interactions.
- Cause an error to be raised for any new requests.

This is useful when your code makes potentially dangerous HTTP requests. The
``'none'`` record mode guarantees that no new HTTP requests will be made.

Given our file, ``examples/record_modes/none/example_original.py``, with a 
cassette that already has interactions recorded in 
``examples/record_modes/none/none-example.json``

.. literalinclude:: ../examples/record_modes/none/example_original.py
    :language: python

If we then run ``examples/record_modes/none/example_updated.py``

.. literalinclude:: ../examples/record_modes/none/example_updated.py
    :language: python

We'll see an exception indicating that new interactions were prevented:

.. literalinclude:: ../examples/record_modes/none/example_updated.traceback
    :language: pytb

Once
----

The ``'once'`` record mode will:

- Replay previously recorded interactions.
- Record new interactions if there is no cassette file.
- Cause an error to be raised for new requests if there is a cassette file.

It is similar to the ``'new_episodes'`` record mode, but will prevent new,
unexpected requests from being made (i.e. because the request URI changed
or whatever).

``'once'`` is the default record mode, used when you do not set one.

If we have a file, ``examples/record_modes/once/example_original.py``,

.. literalinclude:: ../examples/record_modes/once/example_original.py
    :language: python

And we run it, we'll see a cassette named 
``examples/record_modes/once/once-example.json`` has been created.

If we then run ``examples/record_modes/once/example_updated.py``,

.. literalinclude:: ../examples/record_modes/once/example_updated.py
    :language: python

We'll see an exception similar to the one we see when using the ``'none'`` 
record mode.

.. literalinclude:: ../examples/record_modes/once/example_updated.traceback
    :language: pytb



.. _VCR: https://relishapp.com/vcr/vcr
.. _Record Modes documentation:
    https://relishapp.com/vcr/vcr/v/2-9-3/docs/record-modes/
