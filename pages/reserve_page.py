from datetime import datetime
import json
from helpers.parse_helper import convert_price_to_int, format_date_range, parse_date_range
from pages.base_page import BasePage
from helpers.logger import logger

class ReservePage(BasePage):
    
  
    __title_path_str = "checkout-product-details-listing-card"
    __title_path_str_2 = "#LISTING_CARD-title"
    __dates_details = "xpath=(//div[.='Trip details']//parent::div//div[2]//div)[1]"
    __dates_details_str_2 = "xpath = (//*[.='Dates']//parent::div//div)[2]"
    __guests_details = "xpath=(//div[.='Trip details']//parent::div//div[2]//div)[2]"
    __price_per_night_path = "pd-title-ACCOMMODATION"
    __total_price_path ="price-item-total"
    __phone_input_path = "login-signup-phonenumber"
    
    def __init__(self, page):
        super().__init__(page)
        self.page = page
        
        
    def get_title(self):
        title =  self.get_element_text(self.page.get_by_test_id(self.__title_path_str),timeout=30000)
        if not title:
            title = self.get_element_text(self.page.locator(self.__title_path_str_2),timeout=10000)
        return title
    
    def get_date_value(self):
        date_value = self.get_element_text(self.page.locator(self.__dates_details),timeout=30000)
        if not date_value:
            date_value = self.get_element_text(self.page.locator(self.__dates_details_str_2),timeout=10000)
        return date_value
    
    def get_checkin_value(self):
        return self.get_element_text(self.page.get_by_test_id(self.__checkin_path_str))
    def get_checkout_value(self):
        return self.get_element_text(self.page.locator(self.__checkout_path_str))
    def get_guest_value(self):
        return self.get_element_text(self.page.locator(self.__guests_details))
    
    def get_total_price_value(self):
        return self.get_element_text(self.page.get_by_test_id(self.__total_price_path))
    
    def get_price_per_night_value(self):
        return self.get_element_text(self.page.get_by_test_id(self.__price_per_night_path))
    
    
    def validate_reseverion_detail(self,place:dict,start_date:datetime,end_date:datetime,number_of_guests:[int]):
        logger.info("Validate reseverion_details")
        # date_value = self.get_date_value()
        # if date_value:
        #     start,end = parse_date_range(date_text=date_value)
        #     if "," in date_value:
        #         assert format_date_range(start,end) == format_date_range(start_date,end_date)
        #     else:
        #         assert format_date_range(start,end,get_year=False)  == format_date_range(start_date,end_date,get_year=False)
            
        # assert self.get_title() == place["title"]
        # logger.info(format_date_range(start_date,end_date))
        # assert self.get_date_value() == format_date_range(start_date,end_date)
        # assert all(guest in self.get_guest_value() for guest in number_of_guests) if number_of_guests else False
        # assert place["price_per_night"] in self.get_price_per_night_value()

        assert place["price_number"] >= convert_price_to_int(self.get_total_price_value())
    
    def select_country_code(self,counrty_name:str):
        with open("helpers/countries_with_codes.json", "r") as f:
            countries = json.load(f)
            for country in countries:
                if country["name"].lower() == counrty_name.lower():
                    self.page.locator("select#country").select_option(value=country["value"])
                    
    def set_phone_number(self,phone_number:str):
        logger.info(f"Setting phone number:'{phone_number}'")
        assert self.fill_text(self.page.get_by_test_id(self.__phone_input_path),text=phone_number,press_enter=True)
        
            