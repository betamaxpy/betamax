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
