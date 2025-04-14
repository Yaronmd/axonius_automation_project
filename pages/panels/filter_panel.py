from pages.base_page import BasePage
from helpers.logger import logger

class FilterPanel(BasePage):
    """
    Represents the filter  selection panel for the Airbnb automation test suite.
    """
    def __init__(self, page):
        super().__init__(page)
        self.page = page
        
    def click_property_type(self):
        logger.info("Click Property type")
        assert self.click_element(self.page.locator("xpath=(//*[.='Property type'])[1]"),timeout=50000)
    
    def select_filter_property_type(self,property_type:str):
        logger.info(f"Click filter by :'{property_type}'")
        assert self.click_element(self.page.locator(f"xpath=(//*[.='{property_type}'])[1]"),timeout=50000)
        
    def click_show_places(self):
        logger.info(f"Click apply to Show places")
        assert self.click_element(self.page.locator("xpath=//footer//*[contains(text(),'Show')]"))
        
    def filter_by_aprtment(self):
        """Filter by aprtment"""
        self.click_property_type()
        self.select_filter_property_type("Apartment")
        self.click_show_places()