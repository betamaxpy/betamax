Long Term Usage Patterns
========================

Now that we've covered the basics in :ref:`getting_started`, let's look at
some patterns and problems we might encounter when using Betamax over a period
of months instead of minutes.

Adding New Requests to a Cassette
---------------------------------

Let's reuse an example. Specifically let's reuse our
:file:`examples/more_complicated_cassettes.py` example.

.. literalinclude:: ../examples/more_complicated_cassettes.py
    :language: python

Let's add a new ``POST`` request in there:

.. code-block:: python

        session.post('https://httpbin.org/post',
                     params={'id': '20'},
                     json={'some-other-attribute': 'some-other-value'})

If we run this cassette now, we should expect to see that there was an
exception because Betamax couldn't find a matching request for it. We expect
this because the post requests have two completely different bodies, right?
Right. The problem you'll find is that by default Betamax **only** matches on
the URI and the Method. So Betamax will find a matching request/response pair
for ``("POST", "https://httpbin.org/post?id=20")`` and reuse it. So now we
need to update how we use Betamax so it will match using the ``body`` as well:

.. literalinclude:: ../examples/more_complicated_cassettes_2.py
    :language: python

Now when we run that we should see something like this:

.. literalinclude:: ../examples/more_complicated_cassettes_2.traceback
    :language: pytb

This is what we do expect to see. So, how do we fix it?

We have a few options to fix it.

Option 1: Re-recording the Cassette
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

One of the easiest ways to fix this situation is to simply remove the cassette
that was recorded and run the script again. This will recreate the cassette
and subsequent runs will work just fine.

To be clear, we're advocating for this option that the user do:

.. code::

    $ rm examples/cassettes/{{ cassette-name }}

This is the favorable option if you don't foresee yourself needing to add new
interactions often.

Option 2: Changing the Record Mode
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

A different way would be to update the recording mode used by Betamax. We
would update the line in our file that currently reads:

.. code-block:: python

    with recorder.use_cassette('more-complicated-cassettes',
                               serialize_with='prettyjson',
                               match_requests_on=matchers):

to add one more parameter to the call to :meth:`~betamax.Betamax.use_cassette`.
We want to use the ``record`` parameter to tell Betamax to use either the
``new_episodes`` or ``all`` modes. Which you choose depends on your use case.

``new_episodes`` will only record new request/response interactions that
Betamax sees. ``all`` will just re-record every interaction every time. In our
example, we'll use ``new_episodes`` so our code now looks like:

.. code-block:: python

    with recorder.use_cassette('more-complicated-cassettes',
                               serialize_with='prettyjson',
                               match_requests_on=matchers,
                               record='new_episodes'):

Known Issues
------------

Tests Periodically Slow Down
~~~~~~~~~~~~~~~~~~~~~~~~~~~~

**Description:**

Requests checks if it should use or bypass proxies using the standard library
function ``proxy_bypass``. This has been known to cause slow downs when using
Requests and can cause your recorded requests to slow down as well.

Betamax presently has no way to prevent this from being called as it operates
at a lower level in Requests than is necessary.

**Workarounds:**

- Mock gethostbyname method from socket library, to force a localhost setting,
  e.g.,

  .. code-block:: python

      import socket
      socket.gethostbyname = lambda x: '127.0.0.1'

- Set ``trust_env`` to ``False`` on the session used with Betamax. This will
  prevent Requests from checking for proxies and whether it needs bypass them.

**Related bugs:**

- https://github.com/sigmavirus24/betamax/issues/96

- https://github.com/kennethreitz/requests/issues/2988

..
    Template for known issues

    Descriptive Title
    ~~~~~~~~~~~~~~~~~

    **Description:**

    <Description of issue>

    **Workaround(s):**

    - List

    - of

    - workarounds

    **Related bug(s):**

    - List

    - of

    - bug

    - links
