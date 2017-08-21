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
        self.assertURLIs(
            roundtrip().departing(
                "JFK", year=2017, month=9, day=6,
            ).returning(
                "JNB", year=2017, month=10, day=12,
            ), u"https://www.google.com/flights/?f=0&gl=us#search;f=JFK;t=JNB;d=2017-09-06;r=2017-10-12",
        )

    def test_roundtrip_departure_date(self):
        self.assertURLIs(
            roundtrip().departing(
                "JFK", year=2017, month=9, day=6,
            ).returning("JNB"),
            u"https://www.google.com/flights/?f=0&gl=us#search;f=JFK;t=JNB;d=2017-09-06",
        )

    def test_roundtrip_partial_date(self):
        today = date.today()
        self.assertEqual(
            roundtrip().departing("JFK", day=6).returning("JNB", month=3),
            roundtrip().departing(
                "JFK",
                year=today.year,
                month=today.month,
                day=6,
            ).returning("JNB", year=today.year, month=3, day=today.day),
        )

    def test_roundtrip_return_date(self):
        self.assertURLIs(
            roundtrip().departing("JFK").returning(
                "JNB", year=2017, month=9, day=6,
            ),
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
        self.assertURLIs(
            itinerary().departing(
                "JFK", year=2017, month=9, day=5,
            ).arriving(
                "JNB",
            ).departing(
                "CPT", year=2017, month=9, day=9,
            ).arriving(
                "JFK", "EWR",
            ),
            u"https://www.google.com/flights/?f=0&gl=us#search;iti=JFK_JNB_2017-09-05*CPT_JFK,EWR_2017-09-09;tt=m",
        )

    def test_itinerary_partial_date(self):
        today = date.today()
        self.assertEqual(
            itinerary().departing("JFK", day=6).arriving("JNB"),
            itinerary().departing(
                "JFK",
                year=today.year,
                month=today.month,
                day=6,
            ).arriving("JNB"),
        )

    def test_itinerary_one_departure_leg(self):
        self.assertURLIs(
            itinerary().departing("JFK"),
            u"https://www.google.com/flights/?f=0&gl=us#search;iti=JFK__;tt=m",
        )

    def test_itinerary_departure_date(self):
        self.assertURLIs(
            itinerary().departing(
                "JFK", year=2017, month=9, day=6,
            ).arriving("JNB"),
            u"https://www.google.com/flights/?f=0&gl=us#search;iti=JFK_JNB_2017-09-06;tt=m",
        )

    def test_itinerary_cannot_skip_departure(self):
        so_far_so_good = itinerary().arriving("JFK")
        with self.assertRaises(InvalidSearch):
            so_far_so_good.url()  # BOOM!
