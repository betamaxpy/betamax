Implementation Details
======================

Everything here is an implementation detail and subject to volatile change. I 
would not rely on anything here for any mission critical code.

Gzip Content-Encoding
---------------------

By default, requests sets an ``Accept-Encoding`` header value that includes 
``gzip`` (specifically, unless overridden, requests always sends 
``Accept-Encoding: gzip, deflate, compress``). When a server supports this and 
responds with a response that has the ``Content-Encoding`` header set to 
``gzip``, ``urllib3`` automatically decompresses the body for requests. This 
can only be prevented in the case where the ``stream`` parameter is set to 
``True``. Since Betamax refuses to alter the headers on the response object in 
any way, we force ``stream`` to be ``True`` so we can capture the compressed 
data before it is decompressed. We then properly repopulate the response 
object so you perceive no difference in the interaction.

To preserve the response exactly as is, we then must ``base64`` encode the 
body of the response before saving it to the file object. In other words, 
whenever a server responds with a compressed body, you will not have a human 
readable response body. There is, at the present moment, no way to configure 
this so that this does not happen and because of the way that Betamax works, 
you can not remove the ``Content-Encoding`` header to prevent this from 
happening.

Class Details
-------------

.. autoclass:: betamax.cassette.Cassette
    :members:

.. autoclass:: betamax.cassette.Interaction
    :members:
