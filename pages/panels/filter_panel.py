from pages.base_page import BasePage


class FilterPanel(BasePage):
    
    def __init__(self, page):
        super().__init__(page)
        self.page = page
        
    def click_property_type(self):
        assert self.click_element(self.page.locator("xpath=(//*[.='Property type'])[1]"),timeout=50000)
    
    def select_filter_property_type(self,property_type:str):
        assert self.click_element(self.page.locator(f"xpath=(//*[.='{property_type}'])[1]"),timeout=50000)
        
    def click_show_places(self):
        assert self.click_element(self.page.locator("xpath=//footer//*[contains(text(),'Show')]"))
        
    def filter_by_aprtment(self):
        self.click_property_type()
        self.select_filter_property_type("Apartment")
        self.click_show_places()