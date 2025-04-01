from selenium.webdriver import Keys
from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions
from selenium.webdriver.support.wait import WebDriverWait
from helpers import retrieve_phone_code


class UrbanRoutesPage:

        from_field = (By.ID, 'from')
        to_field = (By.ID, 'to')
        call_taxi_button = (By.XPATH, '//button[contains(text(), "Call a taxi")]')

        def __init__(self, driver):
            self.driver = driver

        # Add methods to interact with these elements
        def set_from_field(self, address):
            self.driver.find_element(*self.from_field).send_keys(address)

        def set_to_field(self, address):
            self.driver.find_element(*self.to_field).send_keys(address)

        def click_call_taxi(self):
            self.driver.find_element(*self.call_taxi_button).click()