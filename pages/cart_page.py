from pages.base_page import BasePage
from utils.price_parser import parse_price


class CartPage(BasePage):
    URL = "https://tutorialsninja.com/demo/index.php?route=checkout/cart"

    def get_total(self) -> float:
        self.navigate(self.URL)
        self.page.wait_for_load_state("networkidle")
        self.take_screenshot("cart_page")

        for row in self.page.locator("table tr").all():
            cells = row.locator("td").all()
            if len(cells) >= 2:
                label = cells[0].inner_text().strip().lower()
                if label == "total":
                    return parse_price(cells[-1].inner_text())
        return 0.0
