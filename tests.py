from datetime import date
from unittest import TestCase

from hyperlink import URL

from gtfo import InvalidSearch, itinerary, roundtrip


class TestSearch(TestCase):
    def assertURLIs(self, search, expected):
        self.assertEqual(search.url(), URL.from_text(expected))

    def test_roundtrip(self):
        self.assertURLIs(
            roundtrip().departing("JFK").returning("JNB"),
            u"https://www.google.com/flights/?f=0&gl=us#search;f=JFK;t=JNB",
        )

    def test_multiple_airports(self):
        self.assertURLIs(
            roundtrip().departing(
                "JFK", "EWR", "LGA", "SWF",
            ).returning(
                "JNB", "CPT",
            ),
            u"https://www.google.com/flights/?f=0&gl=us#search;f=JFK,EWR,LGA,SWF;t=JNB,CPT",
        )

    def test_roundtrip_with_dates(self):
        departing_on = date(year=2017, month=9, day=6)
        returning_on = date(year=2017, month=10, day=12)
        self.assertURLIs(
            roundtrip().departing(
                "JFK", on=departing_on,
            ).returning(
                "JNB", on=returning_on,
            ), u"https://www.google.com/flights/?f=0&gl=us#search;f=JFK;t=JNB;d=2017-09-06;r=2017-10-12",
        )

    def test_roundtrip_departure_date(self):
        departing_on = date(year=2017, month=9, day=6)
        self.assertURLIs(
            roundtrip().departing("JFK", on=departing_on).returning("JNB"),
            u"https://www.google.com/flights/?f=0&gl=us#search;f=JFK;t=JNB;d=2017-09-06",
        )

    def test_roundtrip_return_date(self):
        returning_on = date(year=2017, month=9, day=6)
        self.assertURLIs(
            roundtrip().departing("JFK").returning("JNB", on=returning_on),
            u"https://www.google.com/flights/?f=0&gl=us#search;f=JFK;t=JNB;r=2017-09-06",
        )

    def test_itinerary(self):
        self.assertURLIs(
            itinerary().departing(
                "JFK", "EWR",
            ).arriving(
                "JNB",
            ).departing(
                "JNB",
            ).arriving(
                "JFK", "EWR",
            ),
            u"https://www.google.com/flights/?f=0&gl=us#search;iti=JFK,EWR_JNB_*JNB_JFK,EWR_;tt=m",
        )

    def test_itinerary_with_dates(self):
        first_leg_date = date(year=2017, month=9, day=5)
        second_leg_date = date(year=2017, month=9, day=9)
        self.assertURLIs(
            itinerary().departing(
                "JFK", on=first_leg_date,
            ).arriving(
                "JNB",
            ).departing(
                "CPT", on=second_leg_date,
            ).arriving(
                "JFK", "EWR",
            ),
            u"https://www.google.com/flights/?f=0&gl=us#search;iti=JFK_JNB_2017-09-05*CPT_JFK,EWR_2017-09-09;tt=m",
        )

    def test_itinerary_one_departure_leg(self):
        self.assertURLIs(
            itinerary().departing("JFK"),
            u"https://www.google.com/flights/?f=0&gl=us#search;iti=JFK__;tt=m",
        )

    def test_itinerary_departure_date(self):
        departing_on = date(year=2017, month=9, day=6)
        self.assertURLIs(
            itinerary().departing("JFK", on=departing_on).arriving("JNB"),
            u"https://www.google.com/flights/?f=0&gl=us#search;iti=JFK_JNB_2017-09-06;tt=m",
        )

    def test_itinerary_cannot_skip_departure(self):
        so_far_so_good = itinerary().arriving("JFK")
        with self.assertRaises(InvalidSearch):
            so_far_so_good.url()  # BOOM!
