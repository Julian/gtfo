import click

from gtfo import __version__, itinerary, roundtrip


def _itinerary(destinations):
    search = itinerary()
    for departure, arrival in zip(destinations, destinations[1:]):
        search = search.departing(departure).arriving(arrival)
    return search


def _roundtrip(destinations):
    departure, arrival = destinations
    return roundtrip().departing(departure).returning(arrival)


@click.command(context_settings=dict(help_option_names=["-h", "--help"]))
@click.version_option(version=__version__, prog_name="gtfo")
@click.option(
    "-i", "--itinerary", "type",
    flag_value=_itinerary,
)
@click.argument("destinations", nargs=-1)
def main(destinations, type):
    if type is None:
        if len(destinations) > 2:
            search = _itinerary(destinations=destinations)
        else:
            search = _roundtrip(destinations=destinations)
    search.open()
