.. _getting_started:

Getting Started
===============

The first step is to make sure Betamax is right for you. Let's start by
answering the following questions

- Are you using `Requests`_?

  If you're not using Requests, Betamax is not for you. You should checkout
  `VCRpy`_.

- Are you using Sessions or are you using the functional API (e.g.,
  ``requests.get``)?

  If you're using the functional API, and aren't willing to use Sessions,
  Betamax is not *yet* for you.

So if you're using Requests and you're using Sessions, you're in the right
place.

Betamax officially supports `py.test`_ and `unittest`_ but it should integrate
well with nose as well.

Installation
------------

.. code-block:: bash

    $ pip install betamax

Configuration
-------------

When starting with Betamax, you need to tell it where to store the cassettes
that it creates. There's two ways to do this:

1. If you're using :class:`~betamax.recorder.Betamax` or
   :class:`~betamax.decorator.use_cassette` you can pass the
   ``cassette_library_dir`` option. For example,

   .. code-block:: python

       import betamax
       import requests

       session = requests.Session()
       recorder = betamax.Betamax(session, cassette_library_dir='cassettes')
       with recorder.use_cassette('introduction'):
           # ...

2. You can do it once, globally, for your test suite.

   .. code-block:: python

       import betamax

       with betamax.Betamax.configure() as config:
           config.cassette_library_dir = 'cassettes'

.. note::

    If you don't set a cassette directory, Betamax won't save cassettes to
    disk

There are other configuration options that *can* be provided, but this is the 
only one that is *required*.

Recording Your First Cassette
-----------------------------

Let's make a file named ``our_first_recorded_session.py``. Let's add the
following to our file:

.. literalinclude:: ../examples/our_first_recorded_session.py
    :language: python

If we then run our script, we'll see that a new file is created in our
specified cassette directory. It should look something like:

.. literalinclude:: ../examples/cassettes/our-first-recorded-session.json
    :language: javascript

Now, each subsequent time that we run that script, we will use the recorded
interaction instead of talking to the internet over and over again.

Recording More Complex Cassettes
--------------------------------

Most times we cannot isolate our tests to a single request at a time, so we'll
have cassettes that make multiple requests. Betamax can handle these with
ease, let's take a look at an example.

.. literalinclude:: ../examples/more_complicated_cassettes.py
    :language: python

Before we run this example, we have to install a new package:
``betamax-serializers``, e.g., ``pip install betamax-serializers``.

If we now run our new example, we'll see a new file appear in our
:file:`examples/cassettes/` directory named
:file:`more-complciated-cassettes.json`. This cassette will be much larger as
a result of making 3 requests and receiving 3 responses. You'll also notice
that we imported :mod:`betamax_serializers.pretty_json` and called
:meth:`~betamax.Betamax.register_serializer` with
:class:`~betamax_serializers.pretty_json.PrettyJSONSerializer`. Then we added
a keyword argument to our invocation of :meth:`~betamax.Betamax.use_cassette`,
``serialize_with='prettyjson'``.
:class:`~betamax_serializers.pretty_json.PrettyJSONSerializer` is a class
provided by the ``betamax-serializers`` package on PyPI that can serialize and
deserialize cassette data into JSON while allowing it to be easily human
readable and pretty. Let's see the results:

.. literalinclude:: ../examples/cassettes/more-complicated-cassettes.json
    :language: javascript

This makes the cassette easy to read and helps us recognize that requests and
responses are paired together. We'll explore cassettes more a bit later.

.. links

.. _Requests:
    http://docs.python-requests.org/
.. _VCRpy:
    https://github.com/kevin1024/vcrpy
.. _py.test:
    http://pytest.org/
.. _unittest:
    https://docs.python.org/3/library/unittest.html
