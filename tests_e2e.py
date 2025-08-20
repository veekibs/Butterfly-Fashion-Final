import unittest
from selenium import webdriver
from selenium.webdriver.chrome.service import Service

class HomepageTitleTest(unittest.TestCase):

    def setUp(self):
        """This method runs BEFORE each test"""
        service = Service('./chromedriver') 
        self.driver = webdriver.Chrome(service=service)

    def test_homepage_title(self):
        """
        This is the first test
        It checks if the homepage title is correct
        """
        # 1. Navigate to the homepage
        self.driver.get("http://127.0.0.1:8000/")

        # 2. Assert that the text "butterfly fashion" is in the page title
        self.assertIn("butterfly fashion", self.driver.title)

    def tearDown(self):
        """This method runs after each test."""
        # Close the browser window
        self.driver.quit()

# This allows the script to be run from the CLI
if __name__ == "__main__":
    unittest.main()