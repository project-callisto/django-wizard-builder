from .base import FunctionalTest
from unittest import skip

class ItemValidationTest(FunctionalTest):

    def test_cannot_add_empty_list_items(self):
        # Edith goes to the home page and accidentally tries to submit
        # an empty report. She hits Enter on the empty input box
        self.browser.get(self.server_url)
        self.get_report_input_box().send_keys('\n')

        # The home page refreshes, and there is an error message saying
        # that reports cannot be blank
        error = self.browser.find_element_by_css_selector('.has-error')
        self.assertEqual(error.text, "You can't have an empty report")

        # She tries again with some text for the item, which now works
        self.get_report_input_box().send_keys('Shadiness occurred\n')
        self.check_for_row_in_report_table('Report 1: Shadiness occurred')

        # She now decides to submit a second blank report
        self.get_report_input_box().send_keys('\n')

        # She receives a similar warning on the report page
        self.check_for_row_in_report_table('Report 1: Shadiness occurred')
        error = self.browser.find_element_by_css_selector('.has-error')
        self.assertEqual(error.text, "You can't have an empty report")

        # And she can correct it by filling some text in
        self.get_report_input_box().send_keys('It happened again\n')
        self.check_for_row_in_report_table('Report 1: Shadiness occurred')
        self.check_for_row_in_report_table('Report 2: It happened again')

