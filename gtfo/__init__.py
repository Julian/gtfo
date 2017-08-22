from gtfo._version import __version__
from gtfo import core


def itinerary(**kwargs):
    return core._ItinerarySearch(**kwargs)


def roundtrip(**kwargs):
    return core._RoundtripFlightSearch(**kwargs)
