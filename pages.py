from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.wait import WebDriverWait
from selenium.common.exceptions import TimeoutException, NoSuchElementException
from helpers import retrieve_phone_code
import logging

# Set up logging
logging.basicConfig(level=logging.INFO)

class UrbanRoutesPage:
    def __init__(self, driver):
        self.driver = driver
        self.wait = WebDriverWait(driver, 10)

    # Locators
    from_field = (By.ID, 'from')
    to_field = (By.ID, 'to')
    call_taxi_button = (By.XPATH, '//button[contains(text(), "Call a taxi")]')
    supportive_plan_option = (By.XPATH, '//div[contains(@class, "tariff") and contains(text(), "Supportive")]')
    selected_tariff = (By.CLASS_NAME, 'is-selected')
    phone_input = (By.XPATH, '//input[@placeholder="Phone number"]')
    code_input = (By.XPATH, '//input[@placeholder="Code"]')
    next_button = (By.XPATH, '//button[contains(text(), "Next")]')
    card_button = (By.XPATH, '//div[text()="Add card"]')
    card_number_input = (By.XPATH, '//input[@placeholder="Card number"]')
    expiry_input = (By.XPATH, '//input[@placeholder="MM/YY"]')
    cvv_input = (By.ID, 'code')
    link_button = (By.XPATH, '//button[contains(text(), "Link")]')
    comment_field = (By.XPATH, '//textarea[@placeholder="Comment for the driver"]')
    blanket_toggle = (By.XPATH, '//div[contains(text(), "Blanket and handkerchiefs")]')
    blanket_toggle_selected = (By.CLASS_NAME, 'is-active')
    ice_cream_button = (By.XPATH, '//button[contains(text(), "Ice cream")]')
    modal_car_search = (By.CLASS_NAME, 'searching-car-modal')

    # Methods
    def set_address(self, address):
        logging.info(f"Setting address from: {address}")
        self.driver.find_element(*self.from_field).send_keys(address)
        self.driver.find_element(*self.to_field).send_keys(address)

    def select_supportive_plan(self):
        try:
            current_tariff = self.driver.find_element(*self.selected_tariff)
            if "Supportive" in current_tariff.text:
                logging.info("✅ 'Supportive' plan already selected.")
                return
        except NoSuchElementException:
            logging.info("🔍 'Supportive' plan not selected yet.")

        try:
            logging.info("🔍 Selecting 'Supportive' plan...")

            # Wait for the supportive plan option to be clickable before clicking it
            element = self.wait.until(EC.element_to_be_clickable(self.supportive_plan_option))

            # Perform the click action
            element.click()

            # Optional: Re-check if selection succeeded
            self.wait.until(lambda driver: "Supportive" in driver.find_element(*self.selected_tariff).text)
            logging.info("✅ 'Supportive' plan selected successfully.")

        except TimeoutException:
            logging.error("❌ Timeout: 'Supportive' plan could not be selected.")
            self.driver.save_screenshot("supportive_plan_click_error.png")
            raise TimeoutException("Timeout while trying to select 'Supportive' plan.")

    def fill_phone_number(self, phone):
        logging.info("Filling in phone number.")
        self.driver.find_element(*self.phone_input).send_keys(phone)
        self.driver.find_element(*self.next_button).click()

        # Get the SMS code from the logs
        code = retrieve_phone_code(self.driver)
        self.driver.find_element(*self.code_input).send_keys(code)
        self.driver.find_element(*self.next_button).click()

    def add_credit_card(self, number, expiry, cvv):
        logging.info("Adding credit card details.")
        self.driver.find_element(*self.card_button).click()
        self.wait.until(EC.visibility_of_element_located(self.card_number_input)).send_keys(number)
        self.driver.find_element(*self.expiry_input).send_keys(expiry)
        self.driver.find_element(*self.cvv_input).send_keys(cvv)
        # Shift focus by pressing TAB to enable the "Link" button
        self.driver.find_element(*self.cvv_input).send_keys(Keys.TAB)
        self.wait.until(EC.element_to_be_clickable(self.link_button)).click()

    def write_driver_comment(self, comment):
        logging.info(f"Writing comment for the driver: {comment}")
        self.driver.find_element(*self.comment_field).send_keys(comment)

    def order_blanket_and_handkerchiefs(self):
        logging.info("Ordering blanket and handkerchiefs.")
        blanket = self.driver.find_element(*self.blanket_toggle)
        blanket.click()
        if not self.driver.find_element(*self.blanket_toggle_selected).is_displayed():
            logging.error("❌ Blanket and handkerchiefs toggle did not activate.")
            raise Exception("Blanket and handkerchiefs toggle not selected.")

    def order_ice_cream(self, quantity):
        logging.info(f"Ordering {quantity} ice creams.")
        for _ in range(quantity):
            self.driver.find_element(*self.ice_cream_button).click()

    def order_taxi(self):
        logging.info("Ordering a taxi.")
        self.driver.find_element(*self.call_taxi_button).click()

    def is_car_search_modal_displayed(self):
        try:
            self.wait.until(EC.visibility_of_element_located(self.modal_car_search))
            return True
        except TimeoutException:
            logging.error("❌ Car search modal not displayed.")
            return False

    def _safe_click(self, element):
        try:
            element.click()
        except Exception as e:
            logging.warning(f"⚠️ Regular click failed: {e}. Using JavaScript click.")
            self.driver.execute_script("arguments[0].click();", element)
