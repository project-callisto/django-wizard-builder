from .base import FunctionalTest
from unittest import skip

class ItemValidationTest(FunctionalTest):
    @skip
    def test_cannot_add_empty_list_items(self):
        # Edith goes to the home page and accidentally tries to submit
        # an empty report. She hits Enter on the empty input box

        # The home page refreshes, and there is an error message saying
        # that reports cannot be blank

        # She tries again with some text for the item, which now works

        # Perversely, she now decides to submit a second blank report

        # She receives a similar warning on the list page

        # And she can correct it by filling some text in
        self.fail('write me!')
