from typing import Optional
from playwright.sync_api import sync_playwright, TimeoutError, Page, Browser, Locator, Error
from models.store import Store
from models.product import Product

class AmazonResolver:
    """Resolver for Amazon product pages."""

    def __init__(self, product_id: str, product_url: str, product_title: str) -> None:
        """
        Initialize the Amazon resolver.

        Args:
            product_id: Unique identifier for the product
            product_url: Amazon product page URL
            product_title: Product title
        """
        self.store_name: Store = Store.AMAZON
        self.product_id: str = product_id
        self.product_url: str = product_url
        self.product_title: str = product_title

    def _extract_price(self, page: Page) -> Optional[float]:
        """
        Extract price from Amazon page.
        
        Args:
            page: Playwright page object
            
        Returns:
            Float price if found, None otherwise
        """
        try:
            # Try different price selectors as Amazon uses various layouts
            price_selectors: list[str] = [
                'span.a-price-whole',
                '#priceblock_ourprice',
                '#price_inside_buybox',
                '#newBuyBoxPrice'
            ]

            for selector in price_selectors:
                try:
                    price_elem: Optional[Locator] = page.locator(selector).first
                    if price_elem:
                        price_text: str = price_elem.inner_text()
                        # Clean up price text and convert to float
                        price: float = float(price_text.replace('$', '').replace(',', '').strip())
                        return price
                except (ValueError, AttributeError) as e:
                    print(f"Failed to extract price with selector {selector}: {str(e)}")
                    continue

            return None
        except Error as e:
            print(f"Playwright error while extracting price: {str(e)}")
            return None
        except TypeError as e:
            print(f"Type error while processing price: {str(e)}")
            return None

    def _check_availability(self, page: Page) -> bool:
        """
        Check if the product is available on Amazon.
        
        Args:
            page: Playwright page object
            
        Returns:
            True if product is available, False otherwise
        """
        try:
            # Check various availability indicators
            unavailable_selectors: list[str] = [
                '#outOfStock',
                '#availabilityInsideBuyBox_feature_div:has-text("Currently unavailable")',
                '#buybox-see-all-buying-choices:has-text("See All Buying Options")'
            ]

            for selector in unavailable_selectors:
                if page.locator(selector).count() > 0:
                    return False

            # Check for "Add to Cart" button
            add_to_cart_button: Locator = page.locator('#add-to-cart-button')
            return add_to_cart_button.count() > 0
        except Error as e:
            print(f"Playwright error while checking availability: {str(e)}")
            return False
        except TypeError as e:
            print(f"Type error while checking availability: {str(e)}")
            return False

    def resolve(self) -> Product:
        """
        Resolve product information from Amazon.
        
        Returns:
            Product object with price and availability information
        """
        browser: Optional[Browser] = None
        try:
            with sync_playwright() as p:
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
                price: Optional[float] = self._extract_price(page)
                in_stock: bool = self._check_availability(page)

                return Product(
                    id=self.product_id,
                    name=self.product_title,
                    url=self.product_url,
                    price=price,
                    in_stock=in_stock,
                    store=self.store_name
                )

        except TimeoutError:
            print(f"Timeout while accessing {self.product_url}")
            return self._create_error_product()
        except Error as e:
            print(f"Playwright error while accessing {self.product_url}: {str(e)}")
            return self._create_error_product()
        except ValueError as e:
            print(f"Error parsing product data: {str(e)}")
            return self._create_error_product()
        except ConnectionError as e:
            print(f"Network error while accessing {self.product_url}: {str(e)}")
            return self._create_error_product()
        finally:
            if browser:
                browser.close()

    def _create_error_product(self) -> Product:
        """
        Create a Product object for error cases.
        
        Returns:
            Product object with default error values
        """
        return Product(
            id=self.product_id,
            name=self.product_title,
            url=self.product_url,
            price=None,
            in_stock=False,
            store=self.store_name
        )
