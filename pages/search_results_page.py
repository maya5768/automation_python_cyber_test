from pages.base_page import BasePage
from utils.price_parser import parse_price


class SearchResultsPage(BasePage):
    PRODUCT_CARD = "div.product-layout"

    # XPath locators (required by assignment spec)
    LINK_XPATH      = ".//div[@class='caption']//h4/a"
    PRICE_NEW_XPATH = ".//span[@class='price-new']"
    PRICE_XPATH     = ".//p[@class='price']"
    NEXT_BTN_XPATH  = "//ul[contains(@class,'pagination')]//a[normalize-space(text())='>']"

    def get_items_under_price(self, max_price: float, limit: int = 5) -> list[str]:
        urls = []

        while len(urls) < limit:
            cards = self.page.locator(self.PRODUCT_CARD).all()
            if not cards:
                break

            for card in cards:
                if len(urls) >= limit:
                    break

                price_el = card.locator(f"xpath={self.PRICE_NEW_XPATH}")
                if price_el.count() > 0:
                    price_text = price_el.first.inner_text()
                else:
                    price_el = card.locator(f"xpath={self.PRICE_XPATH}")
                    if price_el.count() == 0:
                        continue
                    price_text = price_el.first.inner_text()

                price = parse_price(price_text)

                if 0 < price <= max_price:
                    link = card.locator(f"xpath={self.LINK_XPATH}").first
                    href = link.get_attribute("href")
                    if href:
                        urls.append(href)

            next_btn = self.page.locator(f"xpath={self.NEXT_BTN_XPATH}")
            if next_btn.count() > 0 and len(urls) < limit:
                next_btn.first.click()
                self.page.wait_for_load_state("networkidle")
            else:
                break

        return urls[:limit]
