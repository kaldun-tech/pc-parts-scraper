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
                browser = p.chromium.launch(
                    args=["--disable-gpu", "--single-process"], headless=True)
                page = browser.new_page()
                page.set_default_timeout(15000)  # Increase timeout to 15 seconds

                # Go to URL and wait for network to be idle
                page.goto(self.product_url, wait_until='networkidle')

                # Wait for the main content to be present
                page.wait_for_load_state('domcontentloaded')

                try:
                    # Log the page content if in development
                    print(f"Page URL: {page.url}")
                    if page.url != self.product_url:
                        print(f"Redirected from {self.product_url} to {page.url}")

                    # First check if we got redirected to an error page
                    if "404" in page.url or page.locator('text=Page Not Found').count() > 0:
                        print(f"Product page not found: {self.product_url}")
                        return Product(self.product_id, self.product_title, "0",
                            self.product_url, self.store_name, False)

                    # Try to get price with explicit wait
                    price_elem = page.wait_for_selector('.current-price-value', timeout=10000)
                    if price_elem:
                        price = price_elem.text_content().strip().replace('$', '')
                    else:
                        print(f"Price element not found for {self.product_url}")
                        price = "0"

                    # Check multiple indicators for stock status
                    is_in_stock = False

                    # Check if the buy button exists and is enabled
                    buy_button = page.locator('button.buy-now')
                    if buy_button.is_visible():
                        buy_now_text = buy_button.text_content().strip().lower()
                        button_disabled = buy_button.get_attribute('disabled')
                        # Double check with stock status text if available
                        try:
                            stock_status = page.locator('.pi-data-stock').text_content().strip().lower()
                        except TimeoutError as e:
                            print(f"Stock status element not found: {str(e)}")
                            stock_status = ""  # If stock status element not found

                        # Check if button is enabled and has valid text
                        is_in_stock = (
                            not button_disabled and 
                            any(text in buy_now_text for text in ['buy now', 'add to cart']) and
                            'out of stock' not in stock_status
                        )

                    result = Product(self.product_id, self.product_title, price,
                        self.product_url, self.store_name, is_in_stock)

                    browser.close()
                    return result
                except TimeoutError as e:
                    print(f"Timeout error getting price: {str(e)}")
                    price = "0"
                    result = Product(self.product_id, self.product_title, price,
                        self.product_url, self.store_name, False)
                    return result
            except TimeoutError as e:
                print(f"Timeout error during page load: {str(e)}")
                price = "0"
                result = Product(self.product_id, self.product_title, price,
                    self.product_url, self.store_name, False)
                return result
