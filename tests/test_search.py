import pytest
import allure
from pages.home_page import HomePage
from pages.login_page import LoginPage
from pages.search_results_page import SearchResultsPage
from tests.conftest import load_cases

_LOGIN = next(c for c in load_cases("login_data.json") if c["expected"] == "success")


class TestSearch:
    @pytest.mark.parametrize("case", load_cases("search_data.json"), ids=lambda c: c["id"])
    @allure.title("Search: {case[id]}")
    def test_search_under_price(self, page, case):
        LoginPage(page).login_or_register(_LOGIN["email"], _LOGIN["password"])

        home = HomePage(page)
        home.open()
        home.search(case["query"])

        urls = SearchResultsPage(page).get_items_under_price(
            case["max_price"], case["limit"]
        )

        if case["expect_results"]:
            assert len(urls) > 0, f"Expected results for '{case['query']}' under {case['max_price']}"
        else:
            assert len(urls) == 0, f"Expected no results but found {len(urls)}"
