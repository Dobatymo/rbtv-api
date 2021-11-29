from itertools import islice
from typing import Any, Dict, Optional, Sequence
from unittest import TestCase

from rbtv import API

KEYS = {
    "bohnePortrait": ["mgmtid", "name", "role", "episodeCount", "images"],
    "blogResponse": [
        "id",
        "title",
        "subtitle",
        "isDisabled",
        "publishDate",
        "createDate",
        "lastChangeDate",
        "authors",
        "titleImage",
        "thumbImage",
        "links",
        "isVisibleInPromo",
        "promoImage",
        "isSponsored",
        "category",
        "raffles",
    ],
    "mediaShowResponse": [
        "id",
        "title",
        "description",
        "genre",
        "duration",
        "isExternal",
        "thumbnail",
        "backgroundImage",
        "slideshowImages",
        "links",
        "hosts",
        "seasons",
        "hasUnsortedEpisodes",
        "lastEpisode",
        "podcast",
        "statusPublicNote",
    ],
}


def has_keys(d: Dict[str, Any], keys: Sequence[str]) -> bool:
    for key in keys:
        if key not in d:
            return False

    return True


def cmp_seq_keys(truth, result, keys: Sequence[str], limit: Optional[int] = None) -> bool:

    for a, b in islice(zip(truth, result), limit):
        for key in keys:
            if a[key] != b[key]:
                return False

    return True


class ApiTest(TestCase):
    @classmethod
    def setUpClass(cls):
        cls.api = API()

    def test_get_bohnen_portraits(self):
        result = self.api.get_bohnen_portraits()
        truth = [
            {"mgmtid": 6, "name": "Budi"},
            {"mgmtid": 14, "name": "Etienne"},
            {"mgmtid": 31, "name": "Nils"},
            {"mgmtid": 33, "name": "Simon"},
        ]
        self.assertTrue(cmp_seq_keys(truth, result, ["mgmtid", "name"], 4))

        self.assertTrue(has_keys(result[0], KEYS["bohnePortrait"]))

    def test_get_blog_posts(self):
        result = list(islice(self.api.get_blog_posts(), 1))[0]
        self.assertTrue(has_keys(result, KEYS["blogResponse"]))

    def test_get_shows(self):
        result = list(islice(self.api.get_shows(), 1))[0]
        self.assertTrue(has_keys(result, KEYS["mediaShowResponse"]))


if __name__ == "__main__":
    import unittest

    unittest.main()
