from selenium import webdriver
from selenium.webdriver.common.keys import Keys
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
        self.assertIn('Callisto', self.browser.title)
        header_text = self.browser.find_element_by_tag_name('h1').text
        self.assertIn('Callisto', header_text)

        # She is invited to enter a report straight away
        inputbox = self.browser.find_element_by_id('id_new_report')
        self.assertEqual(
            inputbox.get_attribute('placeholder'),
            'Write it down'
        )

        # She types "Something shady happened" into a text box
        inputbox.send_keys('Something shady happened')

        # When she hits enter, the page updates, and now the page lists
        # "Report: Something shady happened" as an item in a list
        inputbox.send_keys(Keys.ENTER)

        table = self.browser.find_element_by_id('id_report_table')
        rows = table.find_elements_by_tag_name('tr')
        self.assertTrue(
            any(row.text == 'Report: Something shady happened' for row in rows),
            "New report did not appear in table"
        )

        # There is a button allowing her to submit. She submits the report
        self.fail('Finish the test!')

        # The page updates again, and now shows the report as submitted


if __name__ == '__main__':
    unittest.main(warnings='ignore')