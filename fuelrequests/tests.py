from django.test import TestCase

from fuelrequests.forms import FuelReqForms


class FuelReqFormsTests(TestCase):
    def test_tags_field_is_not_in_form(self):
        form = FuelReqForms()

        self.assertNotIn('tags', form.fields)
