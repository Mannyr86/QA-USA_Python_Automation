import logging
from selenium import webdriver
from pages import UrbanRoutesPage
from helpers import is_url_reachable
from data import URBAN_ROUTES_URL
from selenium.webdriver.support import expected_conditions as EC

# Set up logging
logging.basicConfig(level=logging.INFO)

class TestUrbanRoutes:

    @classmethod
    def setup_class(cls):
        from selenium.webdriver.chrome.options import Options

        # Set Chrome options
        chrome_options = Options()
        chrome_options.set_capability("goog:loggingPrefs", {'performance': 'ALL'})
        cls.driver = webdriver.Chrome(options=chrome_options)

        # Check if the URL is reachable before proceeding
        if is_url_reachable(URBAN_ROUTES_URL):
            logging.info("Connected to the Urban Routes server")
            cls.driver.get(URBAN_ROUTES_URL)
            cls.page = UrbanRoutesPage(cls.driver)
        else:
            logging.error("Cannot connect to Urban Routes. Check the server is on and still running")
            raise Exception("Cannot connect to Urban Routes server")

    def test_set_route(self):
        self.page.set_address("123 Main Street")
        # Add assertion to verify that the address is correctly set in the UI
        from_address = self.page.driver.find_element(*self.page.from_field).get_attribute('value')
        to_address = self.page.driver.find_element(*self.page.to_field).get_attribute('value')
        assert from_address == "123 Main Street", f"Expected '123 Main Street', but got {from_address}"
        assert to_address == "123 Main Street", f"Expected '123 Main Street', but got {to_address}"

    def test_select_plan(self):
        self.page.select_supportive_plan()
        # Verify that the 'Supportive' plan is selected
        selected_tariff = self.page.driver.find_element(*self.page.selected_tariff).text
        assert "Supportive" in selected_tariff, f"Expected 'Supportive' plan, but got {selected_tariff}"

    def test_fill_phone_number(self):
        # Fill in the phone number and click 'Next'
        self.page.fill_phone_number("1234567890")

        # Wait for the 'Next' button to be clickable (ensure it's ready before clicking)
        next_button = self.page.wait.until(EC.element_to_be_clickable(self.page.next_button))
        next_button.click()

        # Verify that the phone input field contains the expected value
        phone_value = self.page.driver.find_element(*self.page.phone_input).get_attribute('value')
        assert phone_value == "1234567890", f"Expected phone number '1234567890', but got {phone_value}"

    def test_fill_card(self):
        self.page.add_credit_card("4111111111111111", "12/26", "123")
        # Verify that the card number input is filled correctly
        card_value = self.page.driver.find_element(*self.page.card_number_input).get_attribute('value')
        assert card_value == "4111111111111111", f"Expected card number '4111111111111111', but got {card_value}"

    def test_comment_for_driver(self):
        self.page.write_driver_comment("Please call when you arrive.")
        # Verify that the comment was correctly entered (assuming it's visible in the UI)
        comment_value = self.page.driver.find_element(*self.page.comment_field).get_attribute('value')
        assert comment_value == "Please call when you arrive.", f"Expected comment 'Please call when you arrive.', but got {comment_value}"

    def test_order_blanket_and_handkerchiefs(self):
        self.page.order_blanket_and_handkerchiefs()
        # Verify that the toggle is selected
        blanket_state = self.page.driver.find_element(*self.page.blanket_toggle_selected)
        assert blanket_state.is_selected(), "Blanket and handkerchiefs toggle is not selected"

    def test_order_2_ice_creams(self):
        self.page.order_ice_cream(quantity=2)
        # Verify that two ice cream buttons were clicked (this could be confirmed by checking the UI or a counter)
        ice_cream_buttons = self.page.wait.until(
            EC.presence_of_all_elements_located(self.page.ice_cream_button)
        )
        assert len(ice_cream_buttons) == 2, f"Expected 2 ice creams, but got {len(ice_cream_buttons)}"

    def test_car_search_model_appears(self):
        self.page.order_taxi()
        assert self.page.is_car_search_modal_displayed()

    def test_example(self):
        # Placeholder test to ensure the framework is running correctly
        assert True

    @classmethod
    def teardown_class(cls):
        logging.info("Closing the browser.")
        cls.driver.quit()
