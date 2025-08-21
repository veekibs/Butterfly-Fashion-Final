import unittest
from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait, Select
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.chrome.service import Service

class HomepageTitleTest(unittest.TestCase):

    def setUp(self):
        """This method runs BEFORE each test"""
        service = Service('./chromedriver') 
        self.driver = webdriver.Chrome(service=service)
        # This makes the browser wait up to 10 seconds for elements to appear 
        self.wait = WebDriverWait(self.driver, 10)

    def test_homepage_title(self):
        """
        This is the first test
        It checks if the homepage title is correct
        """
        # 1. Navigate to the homepage
        self.driver.get("http://127.0.0.1:8000/")

        # 2. Assert that the text "butterfly fashion" is in the page title
        self.assertIn("butterfly fashion", self.driver.title)

    def test_happy_path_purchase(self):
        """
        Tests a complete user journey: adding an item, viewing the cart,
        and checking out successfully.
        """
        # Start on the homepage
        self.driver.get("http://127.0.0.1:8000/")

        # Find the first product card + click its "Add to Cart" button
        add_to_cart_button = self.wait.until(EC.element_to_be_clickable((By.CSS_SELECTOR, '.fpro .cart')))
        add_to_cart_button.click()

        # Wait for the cart icon number to update to "1"
        self.wait.until(EC.text_to_be_present_in_element((By.ID, 'cart-count'), '1'))
        
        # Navigate to the cart page
        self.driver.get("http://127.0.0.1:8000/cart/")

        # Find the charity dropdown + select an option
        charity_dropdown = self.wait.until(EC.presence_of_element_located((By.ID, 'charity-select')))
        Select(charity_dropdown).select_by_value('1')

        # Click the "Proceed to Checkout" button
        self.driver.find_element(By.ID, 'checkoutbtn').click()

        # Fill out the checkout form
        self.wait.until(EC.presence_of_element_located((By.ID, 'fname'))).send_keys('Test')
        self.driver.find_element(By.ID, 'lname').send_keys('User')
        self.driver.find_element(By.ID, 'email').send_keys('test@example.com')
        self.driver.find_element(By.ID, 'address1').send_keys('123 Code Lane')
        self.driver.find_element(By.ID, 'city').send_keys('London')
        self.driver.find_element(By.ID, 'postcode').send_keys('SW1A 0AA')
        self.driver.find_element(By.ID, 'card-number').send_keys('4242424242424242')
        self.driver.find_element(By.ID, 'expiry').send_keys('12/26')
        self.driver.find_element(By.ID, 'cvv').send_keys('123')
        
        # Submit the order
        submit_button = self.driver.find_element(By.CSS_SELECTOR, '.order-summary button')
        self.driver.execute_script("arguments[0].scrollIntoView({block: 'center'});", submit_button)
        submit_button.click()

        # Assert that we've landed on the "Order Complete" page
        self.wait.until(EC.url_contains('/order-complete/'))
        self.assertIn("order confirmation", self.driver.title)

    def tearDown(self):
        """This method runs after each test."""
        # Close the browser window
        self.driver.quit()

# This allows the script to be run from the CLI
if __name__ == "__main__":
    unittest.main()