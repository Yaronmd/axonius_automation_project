from datetime import datetime
import time
from helpers.parse_helper import parse_number_of_guests
from helpers.write_to_file_helper import log_results_to_temp_folder
from pages.base_page import BasePage
from helpers.logger import logger
from typing import Optional

class PlacePage(BasePage):
    
    __title_path_str = "xpath=//*[@data-section-id='TITLE_DEFAULT']//h1"
    __reserve_button_path_str = "xpath=(//button[@data-testid='homes-pdp-cta-btn'])[2]"
    __checkin_path_str = "change-dates-checkIn"
    __checkout_path_str = "div[data-testid='change-dates-checkOut']"
    __guest_path_str = "#GuestPicker-book_it-trigger"
    __price_per_night_str = "xpath=(//*[.='night']//parent::div//span)[3]"
    __total_price_str = "xpath=(//*[.='Total']//parent::span//parent::div//span)[2]"
    
    def __init__(self, page):
        super().__init__(page)
    
   
    
    def click_reserve(self):
        assert self.click_element(self.page.locator(self.__reserve_button_path_str))
    
    def get_title(self):
        return self.get_element_text(self.page.locator(self.__title_path_str),timeout=50000)
    
    def get_checkin_value(self):
        return self.get_element_text(self.page.get_by_test_id(self.__checkin_path_str))
    def get_checkout_value(self):
        return self.get_element_text(self.page.locator(self.__checkout_path_str))
    def get_guest_value(self):
        return self.get_element_text(self.page.locator(self.__guest_path_str))
    
    def get_total_price_value(self):
        return self.get_element_text(self.page.locator(self.__total_price_str),timeout=50000)
    
    def get_price_per_night_value(self):
        return self.get_element_text(self.page.locator(self.__price_per_night_str))
    
    
    def validate_selcted_place(self,place:dict,start_date:datetime,end_date:datetime,number_of_guests:int):
        logger.info("Validate selected place values")
        checkin_value = datetime.strptime(self.get_checkin_value(), "%m/%d/%Y")
        checkout_value = datetime.strptime(self.get_checkout_value(), "%m/%d/%Y")
        assert checkin_value.date() == start_date.date()
        assert checkout_value.date() == end_date.date()
        assert number_of_guests == int(parse_number_of_guests(self.get_guest_value()))
        assert place.get("real_price") == self.get_total_price_value()
    
    def save_resrevtion_to_log(self):
     
        log_results_to_temp_folder(file_name="reserve_detail",titile=self.get_title(),checkin=self.get_checkin_value(),checkout=self.get_checkout_value(),price_per_night=self.get_price_per_night_value(),total_price=self.get_total_price_value())
        
        
        
        