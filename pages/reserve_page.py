from datetime import datetime
from helpers.parse_helper import convert_price_to_int, format_date_range
from pages.base_page import BasePage
from helpers.logger import logger

class ReservePage(BasePage):
    
  
    __title_path_str = "checkout-product-details-listing-card"
    __dates_details = "xpath=(//div[.='Trip details']//parent::div//div[2]//div)[1]"
    __guests_details = "xpath=(//div[.='Trip details']//parent::div//div[2]//div)[2]"
    __price_per_night_path = "pd-title-ACCOMMODATION"
    __total_price_path ="price-item-total"
    __select_county_code_path = "login-signup-countrycode"
    __phone_input_path = "login-signup-phonenumber"
    
    def __init__(self, page):
        super().__init__(page)
        self.page = page
        
        
    def get_title(self):
        return self.get_element_text(self.page.get_by_test_id(self.__title_path_str),timeout=50000) 
    
    def get_date_value(self):
        return self.get_element_text(self.page.locator(self.__dates_details),timeout=50000)
    
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
        # logger.info(format_date_range(start_date,end_date))
        # assert self.get_date_value() == format_date_range(start_date,end_date)
        # assert all(guest in self.get_guest_value() for guest in number_of_guests) if number_of_guests else False
        # assert place["price_per_night"] in self.get_price_per_night_value()
        assert place["price_number"]>= convert_price_to_int(self.get_total_price_value())
    
    def select_county_code(self,county_code:str):
        assert self.click_element(self.page.locator(self.__select_county_code_path).get_by_role("option",name="93AF"))
        
            