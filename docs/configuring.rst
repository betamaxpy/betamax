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
    config.default_cassette_options['preserve_exact_body_bytes'] = True


.. links

.. _VCR: https://relishapp.com/vcr/vcr
