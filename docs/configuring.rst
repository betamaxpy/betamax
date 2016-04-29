Configuring Betamax
===================

By now you've seen examples where we pass a great deal of keyword arguments to 
:meth:`~betamax.Betamax.use_cassette`. You have also seen that we used 
:meth:`betamax.Betamax.configure`. In this section, we'll go into a deep 
description of the different approaches and why you might pick one over the 
other.

Global Configuration
--------------------

Admittedly, I am not too proud of my decision to borrow this design from 
`VCR`_, but I did and I use it and it isn't entirely terrible. (Note: I do 
hope to come up with an elegant way to redesign it for v1.0.0 but that's a 
long way off.)

The best way to configure Betamax globally is by using 
:meth:`betamax.Betamax.configure`. This returns a 
:class:`betamax.configure.Configuration` instance. This instance can be used 
as a context manager in order to make the usage look more like `VCR`_'s way of 
configuring the library. For example, in `VCR`_, you might do

.. code-block:: ruby

    VCR.configure do |config|
      config.cassette_library_dir = 'examples/cassettes'
      config.default_cassette_options[:record] = :none
      # ...
    end

Where as with Betamax you might do

.. code-block:: python

    from betamax import Betamax

    with Betamax.configure() as config:
        config.cassette_library_dir = 'examples/cassettes'
        config.default_cassette_options['record_mode'] = 'none'

Alternatively, since the object returned is really just an object and does not 
do anything special as a context manager, you could just as easily do

.. code-block:: python

    from betamax import Betamax

    config = Betamax.configure()
    config.cassette_library_dir = 'examples/cassettes'
    config.default_cassette_options['record_mode'] = 'none'

We'll now move on to specific use-cases when configuring Betamax. We'll 
exclude the portion of each example where we create a 
:class:`~betamax.configure.Configuration` instance.

Setting the Directory in which Betamax Should Store Cassette Files
``````````````````````````````````````````````````````````````````

Each and every time we use Betamax we need to tell it where to store (and 
discover) cassette files. By default we do this by setting the 
``cassette_library_dir`` attribute on our ``config`` object, e.g., 

.. code-block:: python

    config.cassette_library_dir = 'tests/integration/cassettes'

Note that these paths are relative to what Python thinks is the current 
working directory. Wherever you run your tests from, write the path to be 
relative to that directory.

Setting Default Cassette Options
````````````````````````````````

Cassettes have default options used by Betmax if none are set. For example,

- The default record mode is ``once``.

- The default matchers used are ``method`` and ``uri``.

- Cassettes do **not** preserve the exact body bytes by default.

These can all be configured as you please. For example, if you want to change 
the default matchers and preserve exact body bytes, you would do

.. code-block:: python

    config.default_cassette_options['match_requests_on'] = [
        'method',
        'uri',
        'headers',
    ]
    config.preserve_exact_body_bytes = True

Filtering Sensitive Data
````````````````````````

It's unlikely that you'll want to record an interaction that will not require
authentication. For this we can define placeholders in our cassettes. Let's
use a very real example.

Let's say that you want to get your user data from GitHub using Requests. You
might have code that looks like this:

.. code-block:: python

    def me(username, password, session):
        r = session.get('https://api.github.com/user', auth=(username, password))
        r.raise_for_status()
        return r.json()

You would test this something like:

.. code-block:: python

    import os

    import betmax
    import requests

    from my_module import me

    session = requests.Session()
    recorder = betamax.Betamax(session)
    username = os.environ.get('USERNAME', 'testuser')
    password = os.environ.get('PASSWORD', 'testpassword')

    with recorder.use_cassette('test-me'):
        json = me(username, password, session)
        # assertions about the JSON returned

The problem is that now your username and password will be recorded in the
cassette which you don't then want to push to your version control. How can we
prevent that from happening?

.. code-block:: python

    import base64

    username = os.environ.get('USERNAME', 'testuser')
    password = os.environ.get('PASSWORD', 'testpassword')
    config.define_cassette_placeholder(
        '<GITHUB-AUTH>',
        base64.b64encode(
            '{0}:{1}'.format(username, password).encode('utf-8')
        )
    )

.. note::

    Obviously you can refactor this a bit so you can pull those environment
    variables out in only one place, but I'd rather be clear than not here.

The first time you run the test script you would invoke your tests like so:

.. code-block:: sh

    $ USERNAME='my-real-username' PASSWORD='supersecretep@55w0rd' \
      python test_script.py

Future runs of the script could simply be run without those environment
variables, e.g.,

.. code-block:: sh

    $ python test_script.py

This means that you can run these tests on a service like Travis-CI without
providing credentials.

In the event that you can not anticipate what you will need to filter out,
version 0.7.0 of Betamax adds ``before_record`` and ``before_playback`` hooks.
These two hooks both will pass the
:class:`~betamax.cassette.interaction.Interaction` and
:class:`~betamax.cassette.cassette.Cassette` to the function provided. An
example callback would look like:

.. code-block:: python

    def hook(interaction, cassette):
        pass

You would then register this callback:

.. code-block:: python

    # Either
    config.before_record(callback=hook)
    # Or
    config.before_playback(callback=hook)

You can register callables for both hooks. If you wish to ignore an
interaction and prevent it from being recorded or replayed, you can call the
:meth:`~betamax.cassette.interaction.Interaction.ignore`. You also have full
access to all of the methods and attributes on an instance of an Interaction.
This will allow you to inspect the response produced by the interaction and
then modify it. Let's say, for example, that you are talking to an API that
grants authorization tokens on a specific request. In this example, you might
authenticate initially using a username and password and then use a token
after authenticating. You want, however, for the token to be kept secret. In
that case you might configure Betamax to replace the username and password,
e.g.,

.. code-block:: python

    config.define_cassette_placeholder('<USERNAME>', username)
    config.define_cassette_placeholder('<PASSWORD>', password)

And you would also write a function that, prior to recording, finds the token,
saves it, and obscures it from the recorded version of the cassette:

.. code-block:: python

    from betamax.cassette import cassette


    def sanitize_token(interaction, current_cassette):
        # Exit early if the request did not return 200 OK because that's the
        # only time we want to look for Authorization-Token headers
        if interaction.data['response']['status']['code'] != 200:
            return

        headers = interaction.data['response']['headers']
        token = headers.get('Authorization-Token')
        # If there was no token header in the response, exit
        if token is None:
            return

        # Otherwise, create a new placeholder so that when cassette is saved,
        # Betamax will replace the token with our placeholder.
        current_cassette.placeholders.append(
            cassette.Placeholder(placeholder='<AUTH_TOKEN>', replace=token)
        )

This will dynamically create a placeholder for that cassette only. Once we
have our hook, we need merely register it like so:

.. code-block:: python

    config.before_record(callback=sanitize_token)

And we no longer need to worry about leaking sensitive data.


Setting default serializer
``````````````````````````

If you want to use a specific serializer for every cassette, you can set
``serialize_with`` as a default cassette option. For example, if you wanted to
use the ``prettyjson`` serializer for every cassette you would do:

.. code-block:: python

    config.default_cassette_options['serialize_with'] = 'prettyjson'

Per-Use Configuration
---------------------

Each time you create a :class:`~betamax.Betamax` instance or use
:meth:`~betamax.Betamax.use_cassette`, you can pass some of the options from
above.

Setting the Directory in which Betamax Should Store Cassette Files
``````````````````````````````````````````````````````````````````

When using per-use configuration of Betamax, you can specify the cassette
directory when you instantiate a :class:`~betamax.Betamax` object:

.. code-block:: python

    session = requests.Session()
    recorder = betamax.Betamax(session,
                               cassette_library_dir='tests/cassettes/')

Setting Default Cassette Options
````````````````````````````````

You can also set default cassette options when instantiating a
:class:`~betamax.Betamax` object:

.. code-block:: python

    session = requests.Session()
    recorder = betamax.Betamax(session, default_cassette_options={
        'record_mode': 'once',
        'match_requests_on': ['method', 'uri', 'headers'],
        'preserve_exact_body_bytes': True
    })

You can also set the above when calling :meth:`~betamax.Betamax.use_cassette`:

.. code-block:: python

    session = requests.Session()
    recorder = betamax.Betamax(session)
    with recorder.use_cassette('cassette-name',
                               preserve_exact_body_bytes=True,
                               match_requests_on=['method', 'uri', 'headers'],
                               record='once'):
        session.get('https://httpbin.org/get')

Filtering Sensitive Data
````````````````````````

Filtering sensitive data on a per-usage basis is the only difficult (or
perhaps, less convenient) case. Cassette placeholders are part of the default
cassette options, so we'll set this value similarly to how we set the other
default cassette options, the catch is that placeholders have a specific
structure. Placeholders are stored as a list of dictionaries. Let's use our
example above and convert it.

.. code-block:: python

    import base64

    username = os.environ.get('USERNAME', 'testuser')
    password = os.environ.get('PASSWORD', 'testpassword')
    session = requests.Session()

    recorder = betamax.Betamax(session, default_cassette_options={
        'placeholders': [{
            'placeholder': '<GITHUB-AUTH>',
            'replace': base64.b64encode(
                '{0}:{1}'.format(username, password).encode('utf-8')
            ),
        }]
    })

Note that what we passed as our first argument is assigned to the
``'placeholder'`` key while the value we're replacing is assigned to the
``'replace'`` key.

This isn't the typical way that people filter sensitive data because they tend
to want to do it globally.

Mixing and Matching
-------------------

It's not uncommon to mix and match configuration methodologies. I do this in
`github3.py`_. I use global configuration to filter sensitive data and set
defaults based on the environment the tests are running in. On Travis-CI, the
record mode is set to ``'none'``. I also set how we match requests and when we
preserve exact body bytes on a per-use basis.

.. links

.. _VCR: https://relishapp.com/vcr/vcr
.. _github3.py: https://github.com/sigmavirus24/github3.py
