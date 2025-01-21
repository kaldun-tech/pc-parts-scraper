from product_resolvers.cc_resolver import CanadaComputersResolver

PRODUCT_ID = "GSKILL RipJaws 32GB"
PRODUCT_URL = "https://www.canadacomputers.com/en/desktop-memory/99478/g-skill-ripjaws-v-32gb-2x16gb-ddr4-3200mhz-cl16-udimm-f4-3200c16d-32gvk.html"
PRODUCT_TITLE = "GSKILL RipJaws 32GB"

def handle(event, context):
    print("Hello World")
    # Test with a real product from Canada Computers
    resolver = CanadaComputersResolver(
        product_id=PRODUCT_ID,
        product_url=PRODUCT_URL,
        product_title=PRODUCT_TITLE
    )
    product = resolver.resolve()
    print(product)

handle(None, None)
