Serializers
===========

You can tell Betamax how you would like it to serialize the cassettes when 
saving them to a file. By default Betamax will serialize your cassettes to 
JSON. The only default serializer is the JSON serializer, but writing your own 
is very easy.

Creating Your Own Serializer
----------------------------

Betamax handles the structuring of the cassette and writing to a file, your 
serializer simply takes a `dictionary <cassette-dict>`_ and returns a string.

Every Serializer has to inherit from :class:`betamax.BaseSerializer` and 
implement three methods:

- ``betamax.BaseSerializer.generate_cassette_name`` which is a static method.  
  This will take the directory the user (you) wants to store the cassettes in 
  and the name of the cassette and generate the file name.

- :py:meth:`betamax.BaseSerializer.seralize` is a method that takes the 
  dictionary and returns the dictionary serialized as a string

- :py:meth:`betamax.BaseSerializer.deserialize` is a method that takes a 
  string and returns the data serialized in it as a dictionary.


.. autoclass:: betamax.BaseSerializer
    :members:

Here's the default (JSON) serializer as an example:

.. literalinclude:: ../betamax/serializers/json_serializer.py
    :language: python


This is incredibly simple. We take advantage of the :mod:`os.path` to properly 
join the directory name and the file name. Betamax uses this method to find an 
existing cassette or create a new one.

Next we have the :py:meth:`betamax.serializers.JSONSerializer.serialize` which 
takes the cassette dictionary and turns it into a string for us. Here we are 
just leveraging the :mod:`json` module and its ability to dump any valid 
dictionary to a string.

Finally, there is the 
:py:meth:`betamax.serializers.JSONSerializer.deserialize` method which takes a 
string and turns it into the dictionary that betamax needs to function.
