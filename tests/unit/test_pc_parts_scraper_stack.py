import aws_cdk as core
import aws_cdk.assertions as assertions

from pc_parts_scraper.pc_parts_scraper_stack import PcPartsScraperStack

# example tests. To run these tests, uncomment this file along with the example
# resource in pc_parts_scraper/pc_parts_scraper_stack.py
def test_sqs_queue_created():
    app = core.App()
    stack = PcPartsScraperStack(app, "pc-parts-scraper")
    template = assertions.Template.from_stack(stack)
