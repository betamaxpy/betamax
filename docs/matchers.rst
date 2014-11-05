Matchers
========

You can specify how you would like Betamax to match requests you are making 
with the recorded requests. You have the following options for default 
(built-in) matchers:

======= =========
Matcher Behaviour
======= =========
body    This matches by checking the equality of the request bodies.
headers This matches by checking the equality of all of the request headers
host    This matches based on the host of the URI
method  This matches based on the method, e.g., ``GET``, ``POST``, etc.
path    This matches on the path of the URI
query   This matches on the query part of the URI
uri     This matches on the entirety of the URI
======= =========

Default Matchers
----------------

By default, Betamax matches on ``uri`` and ``method``.

Specifying Matchers
-------------------

You can specify the matchers to be used in the entire library by configuring 
Betamax like so:

.. code-block:: python

    import betamax

    with betamax.Betamax.configure() as config:
        config.default_cassette_options['match_requests_on'].extend([
            'headers', 'body'
        ])

Instead of configuring global state, though, you can set it per cassette. For 
example:

.. code-block:: python

    import betamax
    import requests


    session = requests.Session()
    recorder = betamax.Betamax(session)
    match_on = ['uri', 'method', 'headers', 'body']
    with recorder.use_cassette('example', match_requests_on=match_on):
        # ...


Making Your Own Matcher
-----------------------

So long as you are matching requests, you can define your own way of matching.  
Each request matcher has to inherit from ``betamax.BaseMatcher`` and implement 
``match``.

.. autoclass:: betamax.BaseMatcher
    :members:

Some examples of matchers are in the source reproduced here:

.. literalinclude:: ../betamax/matchers/headers.py
    :language: python

.. literalinclude:: ../betamax/matchers/host.py
    :language: python

.. literalinclude:: ../betamax/matchers/method.py
    :language: python

.. literalinclude:: ../betamax/matchers/path.py
    :language: python

.. literalinclude:: ../betamax/matchers/path.py
    :language: python

.. literalinclude:: ../betamax/matchers/uri.py
    :language: python

When you have finished writing your own matcher, you can instruct betamax to 
use it like so:

.. code-block:: python

    import betamax

    class MyMatcher(betamax.BaseMatcher):
        name = 'my'

        def match(self, request, recorded_request):
            return True

    betamax.Betamax.register_request_matcher(MyMatcher)

To use it, you simply use the name you set like you use the name of the 
default matchers, e.g.:

.. code-block:: python

    with Betamax(s).use_cassette('example', match_requests_on=['uri', 'my']):
        # ...


``on_init``
~~~~~~~~~~~

As you can see in the code for ``URIMatcher``, we use ``on_init`` to 
initialize an attribute on the ``URIMatcher`` instance. This method serves to 
provide the matcher author with a different way of initializing the object 
outside of the ``match`` method. This also means that the author does not have 
to override the base class' ``__init__`` method.
