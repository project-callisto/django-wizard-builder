from .base import FunctionalTest
from selenium import webdriver
from selenium.webdriver.common.keys import Keys

class NewVisitorTest(FunctionalTest):

    def test_can_start_a_report_and_submit_it(self):
        #Edith visits Callisto
        self.browser.get(self.server_url)

        # She notices the page title and header mentions Callisto
        self.assertIn('Callisto', self.browser.title)
        header_text = self.browser.find_element_by_tag_name('h1').text
        self.assertIn('Crapllisto', header_text)

        # She is invited to enter a report straight away
        inputbox = self.get_report_input_box()
        self.assertEqual(
            inputbox.get_attribute('placeholder'),
            'Write it down'
        )

        # She types "Something shady happened" into a text box
        inputbox.send_keys('Something shady happened')

        # When she hits enter, the page updates, and now the page lists
        # "Report 1: Something shady happened" as an item in a list
        inputbox.send_keys(Keys.ENTER)
        edith_report_url = self.browser.current_url
        self.assertRegex(edith_report_url, '/profiles/.+')

        self.check_for_row_in_report_table('Report 1: Something shady happened')

        # She enters another report
        inputbox = self.get_report_input_box()
        inputbox.send_keys('Another shady thing went down')

        # When she hits enter, the page updates, and now the page lists
        # both reports as an item in a list
        inputbox.send_keys(Keys.ENTER)

        self.check_for_row_in_report_table('Report 1: Something shady happened')
        self.check_for_row_in_report_table('Report 2: Another shady thing went down')

        # Now a new user, Francis, comes along to the site

        ## New browser session w/o cookies, etc
        self.browser.quit()
        self.browser = webdriver.Firefox()

        # Francis visits the home page. No sign of Edith's report
        self.browser.get(self.server_url)
        page_text = self.browser.find_element_by_tag_name('body').text
        self.assertNotIn('Something shady happened', page_text)
        self.assertNotIn('Another shady thing went down', page_text)

        # Francis starts a new report himself
        inputbox = self.get_report_input_box()
        inputbox.send_keys('I dunno man')
        inputbox.send_keys(Keys.ENTER)

        # Francis gets his own unique URL
        francis_report_url = self.browser.current_url
        self.assertRegex(francis_report_url, '/profiles/.+')
        self.assertNotEqual(francis_report_url, edith_report_url)

        # Still no trace of Edith's report
        page_text = self.browser.find_element_by_tag_name('body').text
        self.assertNotIn('Something shady happened', page_text)
        self.assertIn('I dunno man', page_text)