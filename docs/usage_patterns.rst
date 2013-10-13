Usage Patterns
==============

Below are suggested patterns for using Betamax efficiently.

Usage with py.test
------------------

Betamax and github3.py (the project which instigated the creation of Betamax) 
both utilize py.test_ and its feature of configuring how the tests run with 
``conftest.py`` [#]_. One pattern that I have found useful is to include this 
in your ``conftest.py`` file:

.. code-block:: python

    import betamax

    with betamax.Betamax.configure() as config:
        config.cassette_library_dir = 'tests/cassettes/'

This configures your cassette directory for all of your tests. If you do not 
check your cassettes into your version control system, then you can also add:

.. code-block:: python

    import os

    if not os.path.exists('tests/cassettes'):
        os.makedirs('tests/cassettes')


You can configure other aspects of Betamax via the ``conftest.py`` file. For 
example, in github3.py, I do the following:

.. code-block:: python

    import os

    record_mode = 'never' if os.environ.get('TRAVIS_GH3') else 'once'

    with betamax.Betamax.configure() as config:
        config.cassette_library_dir = 'tests/cassettes/'
        config.default_cassette_options['record_mode'] = record_mode
        config.define_cassette_placeholder(
            '<AUTH_TOKEN>',
            os.environ.get('GH_AUTH', 'x' * 20)
        )

In essence, if the tests are being run on TravisCI_, then we want to make sure 
to not try to record new cassettes or interactions. We also, want to make sure 
we're authenticated when possible but that we do not leave our placeholder in 
the cassettes when they're replayed.


.. _py.test: http://pytest.org/latest/
.. _[#]: http://pytest.org/latest/plugins.html
.. _TravisCI: https://travis-ci.org/
