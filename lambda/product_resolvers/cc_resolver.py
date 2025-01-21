from models.store import Store
from models.product import Product
from playwright.sync_api import sync_playwright, TimeoutError

class CanadaComputersResolver:
    def __init__(self, product_id: str, product_url: str, product_title: str):
        self.store_name = Store.CANADA_COMPUTERS
        self.product_id = product_id
        self.product_url = product_url
        self.product_title = product_title

    def resolve(self) -> Product:
        with sync_playwright() as p:
            # Handle exception case if product
            try:
                # Not headless to observe browser TODO set headless=True
                browser = p.chromium.launch(
                    args=["--disable-gpu", "--single-process"], headless=False)
                page = browser.new_page()
                page.set_default_timeout(5000)
                page.goto(self.product_url)

                price = page.locator('.current-price-value').text_content()
                price = price.strip().replace('$', '')

                buy_now_text = page.locator('button.buy-now').text_content().strip()
                is_in_stock = buy_now_text == "Buy Now"
                result = Product(self.product_id, self.product_title, price,
                    self.product_url, self.store_name, is_in_stock)

                browser.close()
                return result
            except TimeoutError:
                price = page.locator('.current-price-value').text_content().strip().replace('$', '')
                result = Product(self.product_id, self.product_title, price,
                    self.product_url, self.store_name, False)
                return result
