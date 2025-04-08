# pages.py
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

class UrbanRoutesPage:
    def __init__(self, driver):
        self.driver = driver
        self.wait = WebDriverWait(driver, 10)

    # Locators (selectors)
    from_field = (By.ID, 'from')
    to_field = (By.ID, 'to')
    phone_field = (By.XPATH, '//input[@placeholder="Phone number"]')
    card_number_field = (By.XPATH, '//input[@placeholder="Card number"]')
    comment_field = (By.XPATH, '//textarea[@placeholder="Comment for the driver"]')

    # Methods to interact with the form
    def set_address(self, address_from, address_to):
        self.driver.find_element(*self.from_field).send_keys(address_from)
        self.driver.find_element(*self.to_field).send_keys(address_to)

    # Method to get the values from the fields (getter methods)
    def get_from(self):
        return self.driver.find_element(*self.from_field).get_attribute("value")

    def get_to(self):
        return self.driver.find_element(*self.to_field).get_attribute("value")

    def get_phone_number(self):
        return self.driver.find_element(*self.phone_field).get_attribute("value")

    def get_card_number(self):
        return self.driver.find_element(*self.card_number_field).get_attribute("value")

    def get_comment(self):
        return self.driver.find_element(*self.comment_field).get_attribute("value")

    # Additional methods for interacting with the page
    def select_supportive_plan(self):
        supportive_plan_option = (By.XPATH, '//div[contains(@class, "tariff") and contains(text(), "Supportive")]')
        selected_tariff = (By.CLASS_NAME, 'is-selected')
        self.driver.find_element(*supportive_plan_option).click()
        WebDriverWait(self.driver, 10).until(
            EC.text_to_be_present_in_element(selected_tariff, "Supportive")
        )

    def get_selected_tariff(self):
        selected_tariff = (By.CLASS_NAME, 'is-selected')
        return self.driver.find_element(*selected_tariff).text

    def fill_phone_number(self, phone_number):
        self.driver.find_element(*self.phone_field).send_keys(phone_number)

    def add_credit_card(self, card_number, expiry_date, cvv):
        self.driver.find_element(*self.card_number_field).send_keys(card_number)
        # Assuming there are other fields for expiry and CVV
        self.driver.find_element(By.XPATH, '//input[@placeholder="MM/YY"]').send_keys(expiry_date)
        self.driver.find_element(By.XPATH, '//input[@placeholder="CVV"]').send_keys(cvv)

    def write_driver_comment(self, comment):
        self.driver.find_element(*self.comment_field).send_keys(comment)
