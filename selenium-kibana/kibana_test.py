import unittest
from selenium import webdriver
# from selenium.webdriver.common.by import By
from time import sleep


class KibanaSelenium(unittest.TestCase):

    def setUp(self):
        profile = webdriver.FirefoxProfile()
        profile.set_preference('network.http.phishy-userpass-length', 255)
        self.driver = webdriver.Firefox(firefox_profile=profile)
        self.username = 'operator'
        self.password = 'changeme'
        self.ip = '192.168.1.52'
        self.url = 'https://{user}:{passw}@{ip}/kibana/'.format(
            user=self.username,
            passw=self.password,
            ip=self.ip
        )

    def _url_load(self, url):
        driver = self.driver
        driver.get(url)
        sleep(2)
        return driver

    def _url_test(self, url, text):
        driver = self._url_load(url)
        assert text in driver.title
        return driver

    def test_kibana_login(self):
        self._url_test(self.url, 'Kibana')

    def test_kibana_settings_create_pattern(self):
        driver = self._url_test(self.url, 'Kibana')
        css = 'button.btn.btn-success'
        # If the  title is Discover - kibana it was created before
        # so we need to recreate it
        if driver.title == 'Discover - Kibana':
            settings = driver.find_element_by_css_selector(
                'div.navbar-collapse.collapse '
                '> ul:nth-of-type(3) > li:nth-of-type(6) > a.ng-binding')
            settings.click()
        sleep(3)
        driver.find_element_by_name('form')
        elem = driver.find_element_by_css_selector(css)
        elem.submit()

    '''
    def test_kibana_status(self):
        driver = self._url_test(self.url, 'Kibana')
        elem = driver.find_element(By.CSS_SELECTOR,
                                   'a[href=\'/kibana/status\']')
        elem.click()
    '''
    def tearDown(self):
        self.driver.close()

if __name__ == "__main__":
    unittest.main()
