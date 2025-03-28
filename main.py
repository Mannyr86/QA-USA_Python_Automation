from helpers import is_url_reachable
from data import URBAN_ROUTES_URL

class TestUrbanRoutes:
    @classmethod
    def setup_class(cls):
        # Check if the Urban Routes server is reachable
        if is_url_reachable(URBAN_ROUTES_URL):
            print("Connected to the Urban Routes server")
        else:
            print("Cannot connect to Urban Routes. Check the server is on and still running")

    def test_set_route(self):
        # Add in S8
        print("Function created for set route")
        pass

    def test_select_plan(self):
        # Add in S8
        print("Function created for select plan")
        pass

    def test_fill_phone_number(self):
        # Add in S8
        print("Function created for fill phone number")
        pass

    def test_fill_card(self):
        # Add in S8
        print("Function created for fill card")
        pass

    def test_comment_for_driver(self):
        # Add in S8
        print("Function created for comment for driver")
        pass

    def test_order_blanket_and_handkerchiefs(self):
        # Add in S8
        print("Function created for order blanket and handkerchiefs")
        pass

    def test_order_2_ice_creams(self):
    for i in range(2):  # Loop runs twice
        # Add in S8
        pass

    def test_car_search_model_appears(self):
        # Add in S8
        print("Function created for car search model appears")
        pass

    def test_example(self):  # Fixed indentation
        assert True  # Example test case
