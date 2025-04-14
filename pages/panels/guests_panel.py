
from typing import Optional
from pages.base_page import BasePage
from helpers.logger import logger

ADULT = "adults"
CHILDREN = "children"
INFANTS="infants"
PETS = "pets"

class GuestsPanel(BasePage):
    
    labels = (ADULT,CHILDREN,INFANTS,PETS)
    hints = ("Ages 13 or above","Ages 2 – 12","Under 2","Bringing a service animal?")
    
    def __init__(self, page):
        super().__init__(page)
        self.page = page
        self.count_total_guests = 0
    
    def get_count_total_guest(self):
        return self.count_total_guests
    
    def get_count_total_gust_str(self):
        count =  self.get_count_total_guest()
        return f"{count} guests" if  self.get_count_total_guest() > 1 else f"{count} guest"
 
        
    
    def validate_labels_and_hints(self):
        logger.info("Validate Guset lables and hints")
        labels_and_hints = dict(zip(self.labels, self.hints))
        for key,value in labels_and_hints.items():
            if not self.get_element_text(self.page.locator(f"xpath=(//h3[.='{key.capitalize()}']//ancestor::div//*[.='{value}'])[1]")):
                logger.error(f"Failed to validate: '{key}' and hint: '{value}'")    
                assert False
            logger.info(f"Success validate: '{key}' and hint: '{value}'")     
        
        
        
    # common paths 
    def __get_increase_path_by_type(self,_type:str):
        return f"button[data-testid='stepper-{_type}-increase-button']"
    
    def __get_decrease_path_by_type(self,_type:str):
        return f"button[data-testid='stepper-{_type}-decrease-button']"
    
    def __get_value_path_by_type(self,_type:str):
        return f"span[data-testid='stepper-{_type}-value']"
    
    # adults 
    def increase_adult(self):
        logger.info("Increase adult")
        increase_adult_locator = self.page.locator(self.__get_increase_path_by_type(ADULT))
        return self.click_element(increase_adult_locator)
        
    def decrease_adult(self):
        logger.info("Decrease adult")
        decrease_adult_locator = self.page.locator(self.__get_decrease_path_by_type(ADULT))
        return self.click_element(decrease_adult_locator)
    
    
    def get_adult_value(self):
        logger.info("Get adult value")
        return self.get_element_text(self.page.locator(self.__get_value_path_by_type(ADULT)))
    
    # childrens
    def increase_children(self):
        logger.info("Increase children")
        increase_adult_locator = self.page.locator(self.__get_increase_path_by_type(CHILDREN))
        return self.click_element(increase_adult_locator)
        
    def decrease_children(self):
        logger.info("Decrease children")
        decrease_adult_locator = self.page.locator(self.__get_decrease_path_by_type(CHILDREN))
        return self.click_element(decrease_adult_locator)
    
    
    def get_children_value(self):
        logger.info("Get children value")
        return self.get_element_text(self.page.locator(self.__get_value_path_by_type(CHILDREN)))
    
    
    def set_guests(self, adults: Optional[int] = None, children: Optional[int] = None, infants: Optional[int] = None):
        count_total_guests=0
        # Set adults
        if adults and adults >= 1:
            for _ in range(adults):
                if not self.increase_adult():
                    return False
                count_total_guests+=1
        # Set children
        if children and children >= 1:
            for _ in range(children):
                if not self.increase_children():
                    return False
                count_total_guests+=1
                
        self.count_total_guests = count_total_guests
        return True
        