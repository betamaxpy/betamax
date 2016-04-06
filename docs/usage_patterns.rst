Usage Patterns
==============

Below are suggested patterns for using Betamax efficiently.

Configuring Betamax in py.test's conftest.py
--------------------------------------------

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

An Example from github3.py
^^^^^^^^^^^^^^^^^^^^^^^^^^

You can configure other aspects of Betamax via the ``conftest.py`` file. For
example, in github3.py, I do the following:

.. code-block:: python

    import os

    record_mode = 'none' if os.environ.get('TRAVIS_GH3') else 'once'

    with betamax.Betamax.configure() as config:
        config.cassette_library_dir = 'tests/cassettes/'
        config.default_cassette_options['record_mode'] = record_mode
        config.define_cassette_placeholder(
            '<AUTH_TOKEN>',
            os.environ.get('GH_AUTH', 'x' * 20)
        )

In essence, if the tests are being run on `Travis CI`_, then we want to make
sure to not try to record new cassettes or interactions. We also, want to
ensure we're authenticated when possible but that we do not leave our
placeholder in the cassettes when they're replayed.

Using Human Readble JSON Cassettes
----------------------------------

Using the ``PrettyJSONSerializer`` provided by the ``betamax_serializers``
package provides human readable JSON cassettes. Cassettes output in this way
make it easy to compare modifications to cassettes to ensure only expected
changes are introduced.

While you can use the ``serialize_with`` option when creating each individual
cassette, it is simpler to provide this setting globally. The following example
demonstrates how to configure Betamax to use the ``PrettyJSONSerializer`` for
all newly created cassettes:

.. code-block:: python

    from betamax_serializers import pretty_json
    betamax.Betamax.register_serializer(pretty_json.PrettyJSONSerializer)
    # ...
    config.default_cassette_options['serialize_with'] = 'prettyjson'

Updating Existing Betamax Cassettes to be Human Readable
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

If you already have a library of cassettes when applying the previous
configuration update, then you will probably want to also update all your
existing cassettes into the new human readable format. The following script
will help you transform your existing cassettes:

.. code-block:: python

    import os
    import glob
    import json
    import sys

    try:
        cassette_dir = sys.argv[1]
        cassettes = glob.glob(os.path.join(cassette_dir, '*.json'))
    except:
        print('Usage: {0} CASSETTE_DIRECTORY'.format(sys.argv[0]))
        sys.exit(1)

    for cassette_path in cassettes:
        with open(cassette_path, 'r') as fp:
            data = json.load(fp)
        with open(cassette_path, 'w') as fp:
            json.dump(data, fp, sort_keys=True, indent=2,
                      separators=(',', ': '))
    print('Updated {0} cassette{1}.'.format(
        len(cassettes), '' if len(cassettes) == 1 else 's'))

Copy and save the above script as ``fix_cassettes.py`` and then run it like:

.. code-block:: bash

    python fix_cassettes.py PATH_TO_CASSETTE_DIRECTORY

If you're not already using a version control system (e.g., git, svn) then it
is recommended you make a backup of your cassettes first in the event something
goes wrong.

.. [#] http://pytest.org/latest/plugins.html

.. _py.test: http://pytest.org/latest/
.. _Travis CI: https://travis-ci.org/
