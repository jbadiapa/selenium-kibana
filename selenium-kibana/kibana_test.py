
import unittest
import sys
from selenium import webdriver
from selenium.common.exceptions import NoSuchElementException
from selenium.common.exceptions import NoAlertPresentException
from selenium.webdriver.common.desired_capabilities import DesiredCapabilities
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

from time import sleep


class KibanaSelenium(unittest.TestCase):

    USERNAME = 'operator'
    PASSWORD = 'changeme'
    PROTOCOL = 'https'
    PORT = 443
    IP = 'localhost'

    def setUp(self):
        self.driver = webdriver.Firefox()
        self.driver.implicitly_wait(30)
        self.verificationErrors = []
        self.accept_next_alert = True
        self.url = '{protocol}://{user}:{passwd}@{ip}:{port}/kibana/'.format(
            protocol=KibanaSelenium.PROTOCOL,
            user=KibanaSelenium.USERNAME,
            passwd=KibanaSelenium.PASSWORD,
            ip=KibanaSelenium.IP,
            port=KibanaSelenium.PORT)

    def _url_load(self, url):
        driver = self.driver
        for i in range(20):
            driver.get(url)
            driver.set_window_size(1024, 768)
            element = driver.find_element_by_tag_name('html')
            if len(element.text) > 0:
                sleep(1)
                break
        return driver

    def _url_test(self, url, text):
        driver = self._url_load(url)
        return driver

    def test_kibana_login(self):
        self._url_test(self.url, 'Kibana')

    def test_kibana_settings_create_pattern(self):

        driver = self._url_test(self.url, 'Kibana')
        driver.maximize_window()
        for i in range(20):
            try:
                driver.find_element_by_link_text("Settings").click()
                break
            except Exception:
                print ('title: {}'.format(driver.title))
        driver.find_element_by_css_selector("button.btn.btn-success").click()

    def is_element_present(self, how, what):
        try:
            self.driver.find_element(by=how, value=what)
        except NoSuchElementException:
            return False
        return True

    def is_alert_present(self):
        try:
            self.driver.switch_to_alert()
        except NoAlertPresentException:
            return False
        return True

    def close_alert_and_get_its_text(self):
        try:
            alert = self.driver.switch_to_alert()
            alert_text = alert.text
            if self.accept_next_alert:
                alert.accept()
            else:
                alert.dismiss()
            return alert_text
        finally:
            self.accept_next_alert = True

    def tearDown(self):
        self.driver.close()
        self.assertEqual([], self.verificationErrors)


def parse_arguments():
    arguments = {'--ip': 'localhost',
                 '--protocol': 'https',
                 '--username': 'operator',
                 '--password': 'changeme',
                 '--port': '443'}
    iterations = list(sys.argv)
    for arg in iterations:
        if arg in arguments.keys():
            pos = sys.argv.index(arg)
            sys.argv.pop(pos)
            arguments[arg] = sys.argv.pop(pos)

    KibanaSelenium.USERNAME = arguments['--username']
    KibanaSelenium.PASSWORD = arguments['--password']
    KibanaSelenium.IP = arguments['--ip']
    KibanaSelenium.PROTOCOL = arguments['--protocol']
    KibanaSelenium.PORT = arguments['--port']


if __name__ == "__main__":
    parse_arguments()
    unittest.main()
