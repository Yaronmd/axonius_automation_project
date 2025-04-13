import re
import time
from helpers.parse_helper import  parse_places
from pages.base_page import BasePage
from helpers.logger import logger
from pages.panels.check_in_out_panel import CheckInOutPanel
from pages.panels.filter_panel import FilterPanel
from pages.panels.guests_panel import GuestsPanel
from typing import Optional

def handle_new_window_popup(popup):
    """Handles the newly opened popup (window)."""
    print(f"New window title: {popup.title()}")
    popup.wait_for_load_state('domcontentloaded')  # Wait for the new window to load
    print(f"New window URL: {popup.url()}")
    
class MainPage(BasePage):
    
    __url_str = "https://www.airbnb.com/"
    
    
    __main_path_for_card_container = "//div[@data-testid='card-container']"
  
  
    __destination_path = "input[data-testid='structured-search-input-field-query']" 
    __guest_path = "div[data-testid='structured-search-input-field-guests-button']"
    __search_button_path = "button[data-testid='structured-search-input-search-button']"
    __filter_path = "category-bar-filter-button"
    # littel locators path 
    __selected_location_path = "xpath=//button[@data-testid='little-search-location']"
    __selected_check_in_out_path = "xpath=//button[@data-testid='little-search-anytime']//div"
    __selected_guest_path = "xpath=(//button[@data-testid='little-search-guests']//div)[1]"
    
    
    def __init__(self, page):
        super().__init__(page)
        self.destination_locator = page.locator(self.__destination_path)
        self.guest_button_locator = page.locator(selector=self.__guest_path)
        self.search_button_locator = page.locator(selector=self.__search_button_path)
        self.guest_panel:GuestsPanel = None
        self.check_in_out_panel:CheckInOutPanel = None
        self.filter_panel:FilterPanel = None
        
    def navigate_to_airbnb(self):
        self.navigate_to(self.__url_str)
    
    def set_destination(self,destination:str):
        logger.info(f"Setting destination: '{destination}'")
        assert self.fill_text(locator=self.destination_locator,text=destination,press_enter=True)

    def set_random_checkin_and_checkout_between_current_months(self):
        self.check_in_out_panel = CheckInOutPanel(page=self.page)
        return self.check_in_out_panel.select_random_checkin_and_checkout()
    
    def click_who_button(self):
        logger.info(f"click 'who' button")
        if self.click_element(locator=self.guest_button_locator):
            self.guest_panel = GuestsPanel(page=self.page)
        else:
            assert False
    
    def set_guests(self,adults:Optional[int]=None,children:Optional[int]=None):
        assert self.guest_panel.set_guests(adults=adults,children=children)
    
    def click_search_button(self):
        assert self.click_element(self.search_button_locator)
    
    def click_filter_button(self):
        if self.click_element(self.page.get_by_test_id(self.__filter_path)):
            self.filter_panel = FilterPanel(page=self.page)
        else:
            assert False
        
    def validate_selected_location(self,location:str):
        logger.info(f"Validate loction:{location} selected")
        assert self.is_element_visible(self.page.locator(f"{self.__selected_location_path}//div[.='{location}']"))
    
    def get_selected_checkin_out(self):
        logger.info("Getting select checkout checkin...")
        text =  self.get_element_text(self.page.locator(self.__selected_check_in_out_path))
        if not text:
            return False
        if '\u2009' in text:
            text = text.replace('\u2009',' ')
        logger.info(f"gett: {text}")
        return text
            
    
    def get_number_of_selected_guests(self):
        text =  self.get_element_text(self.page.locator(self.__selected_guest_path))
        if not text:
            return False
        return text.replace('\xa0', ' ')
        
        
    def get_list_of_places(self):
    
        title_items = self.get_list_of_all_inner_texts_in_elements(locator=self.page.locator(f"xpath={self.__main_path_for_card_container}//*[@data-testid='listing-card-title']"))
        subtitle_items = self.get_list_of_all_inner_texts_in_elements(locator=self.page.locator(f"xpath={self.__main_path_for_card_container}//*[@data-testid='listing-card-subtitle']"))
        price_items = self.get_list_of_all_inner_texts_in_elements(locator=self.page.locator(f"xpath={self.__main_path_for_card_container}//*[@data-testid='price-availability-row']//*[contains(text(),'total')]"),timeout=50000)
        price_per_night_items = self.get_list_of_all_inner_texts_in_elements(locator=self.page.locator(f"xpath={self.__main_path_for_card_container}//*[@data-testid='price-availability-row']//*[contains(text(),'per') or contains(text(),'month')]"),timeout=50000)
        rating_items = self.get_list_of_all_inner_texts_in_elements(locator=self.page.locator(f"xpath={self.__main_path_for_card_container}//*[contains(text(), 'out of 5 average rating')]"))
                
        if not title_items or not subtitle_items or not price_items:
            return None
        
        return parse_places(title_items=title_items,subtitle_items=subtitle_items,price_items_per_night=price_per_night_items,price_items=price_items,rating_items=rating_items)
        
        
    def select_highest_rated_place(self,place):
        
        path =  f"xpath=(//*[.='{place['title']}']//parent::div//*[contains(text(),'{place['real_price']}')]//ancestor::div[@data-testid='card-container']//a)[1]"
        self.is_element_visible(self.page.locator(path),timeout=100000)
        self.navigate_to(self.get_full_url_from_href(self.page.locator(path).get_attribute('href')))
        # close translation popup
        self.click_element(self.page.locator("button[aria-label='Close']"))
            
        


    