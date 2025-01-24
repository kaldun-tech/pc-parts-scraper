from typing import Optional
from models.store import Store
from models.product import Product
from playwright.sync_api import sync_playwright, TimeoutError, Page

class NeweggResolver:
    def __init__(self, product_id: str, product_url: str, product_title: str):
        self.store_name = Store.NEWEGG
        self.product_id = product_id
        self.product_url = product_url
        self.product_title = product_title

    def _extract_price(self, page: Page) -> Optional[float]:
        """Extract price from Newegg page."""
        try:
            # Try different price selectors
            price_selectors = [
                '.price-current strong',  # Main price
                '.price-main-product',    # Alternative price layout
                '[data-price]'            # Data attribute price
            ]
            
            for selector in price_selectors:
                try:
                    price_elem = page.locator(selector).first
                    if price_elem:
                        price_text = price_elem.inner_text()
                        # Clean up price text and convert to float
                        price = float(price_text.replace('$', '').replace(',', '').strip())
                        return price
                except:
                    continue
            
            return None
        except Exception as e:
            print(f"Error extracting price: {str(e)}")
            return None

    def _check_availability(self, page: Page) -> bool:
        """Check if the product is available on Newegg."""
        try:
            # Check various availability indicators
            unavailable_selectors = [
                '.product-inventory:has-text("OUT OF STOCK")',
                '.message-error:has-text("This item is currently out of stock")',
                'button.btn-message:has-text("AUTO NOTIFY")'
            ]
            
            for selector in unavailable_selectors:
                if page.locator(selector).count() > 0:
                    return False
            
            # Check for "Add to Cart" button
            add_to_cart_button = page.locator('.btn-primary:has-text("Add to Cart")')
            return add_to_cart_button.count() > 0
        except Exception as e:
            print(f"Error checking availability: {str(e)}")
            return False

    def resolve(self) -> Product:
        with sync_playwright() as p:
            try:
                browser = p.chromium.launch(
                    args=["--disable-gpu", "--single-process"], 
                    headless=True
                )
                page = browser.new_page()
                page.set_default_timeout(10000)

                # Add headers to avoid bot detection
                page.set_extra_http_headers({
                    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36'
                })

                # Go to URL and wait for network to be idle
                page.goto(self.product_url, wait_until='networkidle')
                page.wait_for_load_state('domcontentloaded')

                # Extract price and availability
                price = self._extract_price(page)
                is_available = self._check_availability(page)

                return Product(
                    id=self.product_id,
                    title=self.product_title,
                    url=self.product_url,
                    price=price,
                    is_available=is_available,
                    store=self.store_name
                )

            except TimeoutError:
                print(f"Timeout while accessing {self.product_url}")
                return Product(
                    id=self.product_id,
                    title=self.product_title,
                    url=self.product_url,
                    price=None,
                    is_available=False,
                    store=self.store_name
                )
            except Exception as e:
                print(f"Error resolving product: {str(e)}")
                return Product(
                    id=self.product_id,
                    title=self.product_title,
                    url=self.product_url,
                    price=None,
                    is_available=False,
                    store=self.store_name
                )
            finally:
                if 'browser' in locals():
                    browser.close()
