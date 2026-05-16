from unittest import TestCase
from utils.pagination import make_pagination

class TestPagination(TestCase):


    def test_pagination_returns_rigth_range(self):
        pagination = make_pagination(
            page_range= list(range(1,21)),
            page_current=5,
            page_qty=4
        )['pagination']
        self.assertEqual([4,5,6,7], pagination)
    
    def test_pagination_10_returns_rigth_range(self):
        pagination = make_pagination(
            page_range= list(range(1,21)),
            page_current=10,
            page_qty=4
        )['pagination']
        self.assertEqual([9,10,11,12], pagination)
    
    def test_pagination_15_returns_rigth_range(self):
        pagination = make_pagination(
            page_range= list(range(1,21)),
            page_current=15,
            page_qty=4
        )['pagination']
        self.assertEqual([14,15,16,17], pagination)

    def test_pagination_17_returns_rigth_range(self):
        pagination = make_pagination(
            page_range= list(range(1,21)),
            page_current=17,
            page_qty=4
        )['pagination']
        self.assertEqual([16,17,18,19], pagination)

    def test_pagination_18_returns_rigth_range(self):
        pagination = make_pagination(
            page_range= list(range(1,21)),
            page_current=18,
            page_qty=4
        )['pagination']
        self.assertEqual([17,18,19,20], pagination)

    def test_pagination_19_returns_rigth_range(self):
        pagination = make_pagination(
            page_range= list(range(1,21)),
            page_current=19,
            page_qty=4
        )['pagination']
        self.assertEqual([17,18,19,20], pagination)

    def test_pagination_20_returns_rigth_range(self):
        pagination = make_pagination(
            page_range= list(range(1,21)),
            page_current=20,
            page_qty=4
        )['pagination']
        self.assertEqual([17,18,19,20], pagination)