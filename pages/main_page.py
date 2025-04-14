import re
import time
from playwright.sync_api import Locator
from helpers.parse_helper import  extract_prices, parse_price
from pages.base_page import BasePage
from helpers.logger import logger
from pages.panels.check_in_out_panel import CheckInOutPanel
from pages.panels.filter_panel import FilterPanel
from pages.panels.guests_panel import GuestsPanel
from typing import Optional

def handle_new_window_popup(popup):
    """Handles the newly opened popup (window)."""
    print(f"New window title: {popup.title()}")
    popup.wait_for_load_state('domcontentloaded')
    print(f"New window URL: {popup.url()}")
    
class MainPage(BasePage):
    """
    Page object representing the main page of Airbnb.
    Provides methods to interact with the search form, guest panel,
    check-in/out panel, filter panel, and list of places.
    """
    
    __url_str = "https://www.airbnb.com/"
    __main_path_for_card_container = "card-container"
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
        logger.info("Setting guests")
        assert self.guest_panel.set_guests(adults=adults,children=children)
    
    def click_search_button(self):
        assert self.click_element(self.search_button_locator)
    
    def click_filter_button(self):
        if self.click_element(self.page.get_by_test_id(self.__filter_path)):
            self.filter_panel = FilterPanel(page=self.page)
        else:
            assert False
            
    # --- funcations for Validation for the serach bar ----    
    def validate_selected_location(self,location:str):
        logger.info(f"Validate loction:{location} selected")
        assert self.is_element_visible(self.page.locator(f"{self.__selected_location_path}//div[.='{location}']"))
    
    def get_selected_checkin_out(self):
        """
        Retrieve the checkin/out value from the top sarchbar page.
        """
        logger.info("Getting select checkout checkin...")
        text =  self.get_element_text(self.page.locator(self.__selected_check_in_out_path))
        if not text:
            return False
        if '\u2009' in text:
            text = text.replace('\u2009',' ')
        logger.info(f"gett: {text}")
        return text
            
    def get_number_of_selected_guests(self):
        """
        Retrieve the number of guests selected from the top sarchbar page.
        """
        text =  self.get_element_text(self.page.locator(self.__selected_guest_path))
        if not text:
            return False
        return text.replace('\xa0', ' ')
        
        
    def get_list_of_places(self):
        """
        Retrieve and parse a list of places from the search results.
        """
        places = []
        locators = self.wait_for_all_elements(locator=self.page.get_by_test_id(self.__main_path_for_card_container))
        for locator in locators:
            if isinstance(locator,Locator):                
                title = locator.get_by_test_id("listing-card-title").text_content()
                subtitle = locator.get_by_test_id("listing-card-subtitle").first.text_content()
                prices =  locator.get_by_test_id("price-availability-row").text_content()
                per_night, total = extract_prices(prices)
                try:
                    rating = locator.locator("xpath=//span[contains(text(), 'out of 5 average rating')]").text_content().strip()
                    rating = float(rating.split()[0])
                except Exception as e:
                    rating = 0.0
    
                link = locator.locator("xpath=//a").first.get_attribute("href")
                
            
                places.append({"title":title,"subtitle":subtitle,"price_per_night":parse_price(per_night),"total_price":parse_price(total),"rating":rating,"link":self.get_full_url_from_href(link)})
                
        logger.info(places)
        return places
        
        
    def select_place(self,place):
        """
        Select a place by navigating to its details page and dismissing any translation pop-up.
        """
        self.navigate_to(place["link"])
        # close translation popup
        self.click_element(self.page.locator("button[aria-label='Close']"))
            
        


    