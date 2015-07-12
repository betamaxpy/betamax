Third-Party Packages
====================

Betamax was created to be a very close imitation of `VCR`_. As such, it has
the default set of request matchers and a subset of the supported cassette
serializers for VCR.

As part of my own usage of Betamax, and supporting other people's usage of 
Betamax, I've created (and maintain) two third party packages that provide 
extra request matchers and cassette serializers.

- `betamax-matchers`_
- `betamax-serializers`_

For simplicity, those modules will be documented here instead of on their own 
documentation sites.

Request Matchers
----------------

There are three third-party request matchers provided by the 
`betamax-matchers`_ package:

- :class:`~betamax_matchers.form_urlencoded.URLEncodedBodyMatcher`, 
  ``'form-urlencoded-body'``
- :class:`~betamax_matchers.json_body.JSONBodyMatcher`, ``'json-body'``
- :class:`~betamax_matchers.multipart.MultipartFormDataBodyMatcher`, 
  ``'multipart-form-data-body'``

In order to use any of these we have to register them with Betamax. Below we 
will register all three but you do not need to do that if you only need to use 
one:

.. code-block:: python

    import betamax
    from betamax_matchers import form_urlencoded
    from betamax_matchers import json_body
    from betamax_matchers import multipart

    betamax.Betamax.register_request_matcher(
        form_urlencoded.URLEncodedBodyMatcher
        )
    betamax.Betamax.register_request_matcher(
        json_body.JSONBodyMatcher
        )
    betamax.Betamax.register_request_matcher(
        multipart.MultipartFormDataBodyMatcher
        )

All of these classes inherit from :class:`betamax.BaseMatcher` which means 
that each needs a name that will be used when specifying what matchers to use 
with Betamax. I have noted those next to the class name for each matcher 
above. Let's use the JSON body matcher in an example though:

.. code-block:: python

    import betamax
    from betamax_matchers import json_body
    # This example requires at least requests 2.5.0
    import requests

    betamax.Betamax.register_request_matcher(
        json_body.JSONBodyMatcher
        )

    
    def main():
        session = requests.Session()
        recorder = betamax.Betamax(session, cassette_library_dir='.')
        url = 'https://httpbin.org/post'
        json_data = {'key': 'value',
                     'other-key': 'other-value',
                     'yet-another-key': 'yet-another-value'}
        matchers = ['method', 'uri', 'json-body']

        with recorder.use_cassette('json-body-example', match_requests_on=matchers):
            r = session.post(url, json=json_data)


    if __name__ == '__main__':
        main()

If we ran that request without those matcher with hash seed randomization, 
then we would occasionally receive exceptions that a request could not be 
matched. That is because dictionaries are not inherently ordered so the body 
string of the request can change and be any of the following:

.. code-block:: js

    {"key": "value", "other-key": "other-value", "yet-another-key": 
    "yet-another-value"}

.. code-block:: js

    {"key": "value", "yet-another-key": "yet-another-value", "other-key": 
    "other-value"}

.. code-block:: js

    {"other-key": "other-value", "yet-another-key": "yet-another-value", 
    "key": "value"}


.. code-block:: js

    {"yet-another-key": "yet-another-value", "key": "value", "other-key": 
    "other-value"}

.. code-block:: js

    {"yet-another-key": "yet-another-value", "other-key": "other-value", 
    "key": "value"}

.. code-block:: js

    {"other-key": "other-value", "key": "value", "yet-another-key": 
    "yet-another-value"}

But using the ``'json-body'`` matcher, the matcher will parse the request and 
compare python dictionaries instead of python strings. That will completely 
bypass the issues introduced by hash randomization. I use this matcher 
extensively in `github3.py`_\ 's tests.

Cassette Serializers
--------------------

By default, Betamax only comes with the JSON serializer.  
`betamax-serializers`_ provides extra serializer classes that users have 
contributed.

For example, as we've seen elsewhere in our documentation, the default JSON 
serializer does not create beautiful or easy to read cassettes. As a 
substitute for that, we have the 
:class:`~betamax_serializers.pretty_json.PrettyJSONSerializer` that does that 
for you.

.. code-block:: python

    from betamax import Betamax
    from betamax_serializers import pretty_json

    import requests

    Betamax.register_serializer(pretty_json.PrettyJSONSerializer)

    session = requests.Session()
    recorder = Betamax(session)
    with recorder.use_cassette('testpretty', serialize_with='prettyjson'):
        session.request(method=method, url=url, ...)


This will give us a pretty-printed cassette like:

.. literalinclude:: ../examples/cassettes/more-complicated-cassettes.json
    :language: js

.. links

.. _VCR:
    https://relishapp.com/vcr/vcr
.. _betamax-matchers:
    https://pypi.python.org/pypi/betamax-matchers
.. _betamax-serializers:
    https://pypi.python.org/pypi/betamax-serializers
.. _github3.py:
    https://github.com/sigmavirus24/github3.py
