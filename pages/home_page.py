from pages.base_page import BasePage


class HomePage(BasePage):
    SEARCH_INPUT  = "input[name='search']"
    SEARCH_BUTTON = "#search button[type='button']"
    BASE_URL      = "https://tutorialsninja.com/demo/"

    def open(self):
        self.navigate(self.BASE_URL)
        self.page.wait_for_load_state("networkidle")

    def search(self, query: str):
        self.page.fill(self.SEARCH_INPUT, query)
        self.page.click(self.SEARCH_BUTTON)
        self.page.wait_for_load_state("networkidle")
