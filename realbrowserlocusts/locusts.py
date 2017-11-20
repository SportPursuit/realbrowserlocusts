# pylint:disable=too-few-public-methods
""" Combine Locust with Selenium Web Driver """
import logging
from locust import Locust
from locust.exception import LocustError
from selenium import webdriver
from realbrowserlocusts.core import RealBrowserClient

_LOGGER = logging.getLogger(__name__)


class RealBrowserLocust(Locust):
    """
   This is the abstract Locust class which should be subclassed.
   """
    _browser = None
    client = None
    timeout = 30
    screen_width = None
    screen_height = None

    def __init__(self):
        super(RealBrowserLocust, self).__init__()
        if self.screen_width is None:
            raise LocustError("You must specify a screen_width "
                              "for the browser")
        if self.screen_height is None:
            raise LocustError("You must specify a screen_height "
                              "for the browser")
    def create_client(self):
        profile = webdriver.FirefoxProfile()
        profile.accept_untrusted_certs = True
        return RealBrowserClient(self._browser(profile), self.timeout, self.screen_width, self.screen_height)

    def restart_client(self):
        self.client.close()
        return self.create_client()

    def run(self):
        display = None

        try:
            self.client = RealBrowserClient(self._browser, self.timeout, self.screen_width, self.screen_height)
            super(RealBrowserLocust, self).run()
        finally:
            if display is not None:
                display.stop()

class ChromeLocust(RealBrowserLocust):
    """
    Provides a Chrome webdriver that logs GET's and waits to locust
    """
    _browser = webdriver.Chrome


class HeadlessChromeLocust(RealBrowserLocust):
    """
    Provides a headless Chrome webdriver that logs GET's and waits to locust
    """
    options = webdriver.ChromeOptions()
    options.add_argument('headless')
    options.add_argument('disable-gpu')
    _browser = webdriver.Chrome(chrome_options=options)


class FirefoxLocust(RealBrowserLocust):
    """
    Provides a Firefox webdriver that logs GET's and waits to locust
    """
    _browser = webdriver.Firefox

class PhantomJSLocust(RealBrowserLocust):
    """
    Provides a PhantomJS webdriver that logs GET's and waits to locust
    """
    _browser = webdriver.PhantomJS

