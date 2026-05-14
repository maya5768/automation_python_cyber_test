import random
from pages.base_page import BasePage


class ProductPage(BasePage):
    ADD_TO_CART   = "#button-cart"
    SUCCESS_ALERT = "div.alert-success"

    def _select_variants(self):
        for sel in self.page.locator("select[name^='option']").all():
            opts = sel.locator("option[value!='']").all()
            if opts:
                sel.select_option(random.choice(opts).get_attribute("value"))

        seen = set()
        for radio in self.page.locator("input[type='radio'][name^='option']").all():
            name = radio.get_attribute("name")
            if name not in seen:
                seen.add(name)
                radio.check()

    def add_to_cart(self, url: str) -> bool:
        self.navigate(url)
        self.page.wait_for_load_state("networkidle")
        self._select_variants()
        self.page.locator(self.ADD_TO_CART).click()

        try:
            self.page.wait_for_selector(self.SUCCESS_ALERT, timeout=5000)
            self.take_screenshot(f"added_{abs(hash(url)) % 9999}")
            return True
        except Exception:
            self.take_screenshot(f"failed_{abs(hash(url)) % 9999}")
            return False
