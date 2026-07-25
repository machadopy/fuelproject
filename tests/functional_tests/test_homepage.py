from django.test import LiveServerTestCase
from django.contrib.staticfiles.testing import StaticLiveServerTestCase
from utils.browser import make_chromebrowser
from selenium.webdriver.common.by import By
import time
import pytest


@pytest.mark.functional_test
class BaseFunctionalTest(StaticLiveServerTestCase):
    def setUp(self) -> None:
        self.browser = make_chromebrowser()
        return super().setUp()
    
    def tearDown(self) -> None:
        self.browser.quit()
        return super().tearDown()
        
    def sleep(self,seconds = 5):
        time.sleep(seconds)

class HomePageFunctionalTest(BaseFunctionalTest):
    def test_test(self):
        browser = self.browser
        browser.get(f'{self.live_server_url}/usuarios/user_login/')
        h1 = browser.find_element(By.TAG_NAME, 'h1')
        self.assertIn('Login', h1.text)
