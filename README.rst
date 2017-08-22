====
gtfo
====

Searching for flights is amazingly painful.

If a first world problem leads to debilitating mental instability, is it
now not a first world problem anymore?

Save me...

Usage
-----

.. code-block:: sh

    $ gtfo JFK JNB

or

.. code-block:: python

    from gtfo import roundtrip
    roundtrip().departing("JFK").returning("JNB").open()


Flights API Usage
-----------------

This module is not intended to be used programmatically. Google has a
`QPX Flights API <https://developers.google.com/qpx-express/>`_ for this
purpose, but it has some prerequisites to gain access to it, and limits
when using it.

This module literally is just to programatically generate the URLs for
human-centric searches, so that you can then open them in a browser.
