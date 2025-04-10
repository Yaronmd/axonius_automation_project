from pages.base_page import BasePage
from helpers.logger import logger
from pages.panels.guests_panel import GuestsPanel
from typing import Optional

class MainPage(BasePage):
    
    __url_str = "https://www.airbnb.com/"
    
    # locators path
    __destination_path = "input[data-testid='structured-search-input-field-query']" 
    __guest_path = "div[data-testid='structured-search-input-field-guests-button']"
    def __init__(self, page):
        super().__init__(page)
        self.destination_locator = page.locator(self.__destination_path)
        self.guest_button_locator = page.locator(selector=self.__guest_path)
        self.guest_panel:GuestsPanel = None
        
    def navigate_to_airbnb(self):
        self.navigate_to(self.__url_str)
    
    def set_destination(self,destination:str):
        logger.info(f"Setting destination: '{destination}'")
        return self.fill_text(locator=self.destination_locator,text=destination,press_enter=True)
            
    
    def click_who_button(self):
        logger.info(f"click 'who' button")
        if self.click_element(locator=self.guest_button_locator):
            self.guest_panel = GuestsPanel(page=self.page)
            return True
        return False
    
    def set_guests(self,adults:Optional[int],children:Optional[int]):
        return self.guest_panel.set_guests(adults=adults,children=children)
    
           
        
        


    
    