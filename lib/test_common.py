# coding=utf-8
from unittest import TestCase
from common import get_link_from_query

class TestGet_link_from_query(TestCase):
    def simple(self):
        string = "http://s.aliexpress.com/R3Ij6Rr6"
        expected = string
        actual = get_link_from_query(string)
        if actual != expected:
            self.fail(self)

    def mixed_string(self):
        string =  """
        Введи ссылку на алиэкспрессе и я постараюсь сказать, как изменялась цена твоего товара
Например,
https://ru.aliexpress.com/item/seo-url/32750549213.html fdsfdsf
"""
        expected = "https://ru.aliexpress.com/item/seo-url/32750549213.html"
        actual = get_link_from_query(string)
        if actual != expected:
            self.fail(self)
