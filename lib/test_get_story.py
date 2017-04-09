from unittest import TestCase
from story import get_story


class TestGet_story(TestCase):
    def test_get_story(self):
        results = get_story(
            "https://ru.aliexpress.com/item/Softu-Fashion-Women-Shirt-Blouse-Summer-Tops-Chiffon-Casual-Shirt-O-Neck-Half-Sleeve-Floral-Printing/32748542874.html?aff_platform=aaf&cpt=1491481963070&sk=6mia6uvne&aff_trace_key=3e8274c1d1434c9590928662d0579b36-1491481963070-01771-6mia6uvne")
        if len(results) == 0:
            TestCase.fail(self)

    def test_with_number(self):
        query = "32748542874"
        results = get_story(query)
        if len(results) == 0:
            TestCase.fail(self)

    def test_with_short_link(self):
        query = "http://s.aliexpress.com/AR7FNvQf"
        results = get_story(query)
        if len(results) == 0:
            TestCase.fail(self)
