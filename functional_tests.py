from selenium import webdriver
import unittest

class NewVisitorTest(unittest.TestCase):

    def setUp(self):
        self.browser = webdriver.Firefox()
        self.browser.implicitly_wait(3)

    def tearDown(self):
        self.browser.quit()

    def test_can_start_a_report_and_submit_it(self):
        #Edith visits Callisto
        self.browser.get('http://localhost:8000')

        # She notices the page title and header mentions Callisto
        self.assertIn('To-Do', self.browser.title)
        self.fail('Finish the test!')

        # She is invited to enter a report straight away

        # She types "Something shady happened" into a text box

        # When she hits enter, the page updates, and now the page lists
        # "Report: Something shady happened" as an item in a list

        # There is a button allowing her to submit. She submits the report

        # The page updates again, and now shows the report as submitted

if __name__ == '__main__':
    unittest.main(warnings='ignore')