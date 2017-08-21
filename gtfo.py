from datetime import date
import webbrowser

from hyperlink import URL
from pyrsistent import dq, pset, s
import attr


@attr.s(repr=False)
class InvalidSearch(Exception):

    _leg = attr.ib()
    _message = attr.ib()

    def __str__(self):
        return "{self._leg}: {self._message}".format(self=self)


BASE = URL.from_text(u"https://www.google.com/flights/?f=0&gl=us")


def _url(self):
    parameters = (u"=".join(each) for each in self._parameters())
    return BASE.replace(fragment=u"search;" + u";".join(parameters))


def _open(self, *airports):
    webbrowser.open(self.url().to_text())


@attr.s
class _Leg(object):

    _departing = attr.ib(default=s())
    _arriving = attr.ib(default=s())
    _date = attr.ib(default=None)

    @property
    def complete(self):
        return self._departing and self._arriving

    def departing(self, *airports, **kwargs):
        kwargs.update(
            departing=pset(airports),
            date=_to_date(
                year=kwargs.pop("year", None),
                month=kwargs.pop("month", None),
                day=kwargs.pop("day", None),
            ),
        )
        return attr.evolve(self, **kwargs)

    def arriving(self, *airports):
        return attr.evolve(self, arriving=pset(airports))

    def parameters(self):
        if not self._departing:
            raise InvalidSearch(leg=self, message="needs a departing airport")

        date = u"" if self._date is None else self._date.strftime(u"%Y-%m-%d")
        return "_".join(
            [u",".join(self._departing), u",".join(self._arriving), date],
        )


@attr.s
class _RoundtripFlightSearch(object):

    url = _url
    open = _open

    _departing = attr.ib(default=s())
    _departing_on = attr.ib(default=None)
    _returning = attr.ib(default=s())
    _returning_on = attr.ib(default=None)

    def departing(self, *airports, **kwargs):
        kwargs.update(
            departing=pset(airports),
            departing_on=_to_date(
                year=kwargs.pop("year", None),
                month=kwargs.pop("month", None),
                day=kwargs.pop("day", None),
            ),
        )
        return attr.evolve(self, **kwargs)

    def returning(self, *airports, **kwargs):
        kwargs.update(
            returning=pset(airports),
            returning_on=_to_date(
                year=kwargs.pop("year", None),
                month=kwargs.pop("month", None),
                day=kwargs.pop("day", None),
            ),
        )
        return attr.evolve(self, **kwargs)

    def itinerary(self):
        return itinerary().departing(
            *self._departing,
            year=self._departing_on.year,
            month=self._departing_on.month,
            day=self._departing_on.day
        ).arriving(
            *self._returning
        ).departing(
            *self._returning,
            year=self._returning_on.year,
            month=self._returning_on.month,
            day=self._returning_on.day
        ).arriving(*self._departing)

    def _parameters(self):
        yield u"f", u",".join(self._departing)
        yield u"t", u",".join(self._returning)
        if self._departing_on is not None:
            yield u"d", self._departing_on.strftime(u"%Y-%m-%d")
        if self._returning_on is not None:
            yield "r", self._returning_on.strftime(u"%Y-%m-%d")


@attr.s
class _ItinerarySearch(object):

    _legs = attr.ib(default=dq(_Leg()))

    url = _url
    open = _open

    def departing(self, *airports, **kwargs):
        legs, leg = self._with_last_incomplete_leg()
        legs = legs.append(leg.departing(*airports, **kwargs))
        return attr.evolve(self, legs=legs)

    def arriving(self, *airports, **kwargs):
        legs, leg = self._with_last_incomplete_leg()
        legs = legs.append(leg.arriving(*airports, **kwargs))
        return attr.evolve(self, legs=legs)

    def _with_last_incomplete_leg(self):
        last = self._legs[len(self._legs) - 1]
        if last.complete:
            return self._legs, _Leg()
        return self._legs.pop(), last

    def _parameters(self):
        yield u"iti", u"*".join(leg.parameters() for leg in self._legs)
        yield u"tt", u"m"  # TODO: What is this?


def itinerary(**kwargs):
    return _ItinerarySearch(**kwargs)


def roundtrip(**kwargs):
    return _RoundtripFlightSearch(**kwargs)


def _to_date(year, month, day):
    if year is month is day is None:
        return None
    return date.today().replace(year=year, month=month, day=day)
