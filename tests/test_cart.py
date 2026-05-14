import pytest
import allure
from pages.cart_page import CartPage
from pages.home_page import HomePage
from pages.login_page import LoginPage
from pages.product_page import ProductPage
from pages.search_results_page import SearchResultsPage
from tests.conftest import load_cases

_LOGIN = next(c for c in load_cases("login_data.json") if c["expected"] == "success")


class TestCart:
    @pytest.mark.parametrize("case", load_cases("cart_data.json"), ids=lambda c: c["id"])
    @allure.title("Cart E2E: {case[id]}")
    def test_cart_total(self, page, case):
        LoginPage(page).login_or_register(_LOGIN["email"], _LOGIN["password"])

        home = HomePage(page)
        home.open()
        home.search(case["query"])

        urls = SearchResultsPage(page).get_items_under_price(case["max_price"], limit=5)
        assert len(urls) > 0, f"No products found for '{case['query']}' under {case['max_price']}"

        product = ProductPage(page)
        for url in urls:
            product.add_to_cart(url)

        total = CartPage(page).get_total()
        threshold = case["budget_per_item"] * len(urls)
        assert total <= threshold, f"Cart total {total} exceeds threshold {threshold}"
