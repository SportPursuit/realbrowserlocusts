import logging

from locust import Locust
from locust.exception import LocustError
from selenium import webdriver
from core import RealBrowserClient
from xvfbwrapper import Xvfb

logger = logging.getLogger(__name__)


class RealBrowserLocust(Locust):

    _browser = None
    client = None
    timeout = 30
    screen_width = None
    screen_height = None
    headless = True

    def __init__(self):
        super(RealBrowserLocust, self).__init__()
        if self.screen_width is None:
            raise LocustError("You must specify a screen_width for the browser")
        if self.screen_height is None:
            raise LocustError("You must specify a screen_height for the browser")

        if self._browser == webdriver.PhantomJS and self.headless:
            logger.warning('Using headless mode and PhantomJS is redundant.')

    def run(self):
        display = None

        if self.headless:
            display = Xvfb(width=self.screen_width, height=self.screen_height)
            display.start()

        try:
            self.client = RealBrowserClient(self._browser(), self.timeout, self.screen_width, self.screen_height)
            super(RealBrowserLocust, self).run()

        finally:
            if display is not None:
                display.stop()


class ChromeLocust(RealBrowserLocust):
    """
    This is the abstract Locust class which should be subclassed. It provides a Firefox webdriver that logs GET's and waits to locust
    """
    _browser = webdriver.Chrome


class FirefoxLocust(RealBrowserLocust):
    """
    This is the abstract Locust class which should be subclassed. It provides a Firefox webdriver that logs GET's and waits to locust
    """
    _browser = webdriver.Firefox


class PhantomJSLocust(RealBrowserLocust):
    """
    This is the abstract Locust class which should be subclassed. It provides a PhantomJS webdriver that logs GET's and waits to locust
    """
    _browser = webdriver.PhantomJS

