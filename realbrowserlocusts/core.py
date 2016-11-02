import time
import sys
from selenium.webdriver.support.ui import WebDriverWait
from selenium.common.exceptions import WebDriverException

from locust import events
from locust.exception import StopLocust


def wrapForLocust(instance, request_type, name, func, *args, **kwargs):
    start_time = time.time()

    try:
        result = func(*args, **kwargs)

    except WebDriverException, e:
        events.locust_error.fire(locust_instance=instance, exception=e, tb=sys.exc_info()[2])

    except Exception as e:
        total_time = round(time.time() - start_time, 4)
        events.request_failure.fire(request_type=request_type, name=name, response_time=total_time, exception=e)
        raise StopLocust()

    else:
        total_time = round(time.time() - start_time, 4)
        events.request_success.fire(request_type=request_type, name=name, response_time=total_time, response_length=0)
        return result


class RealBrowserClient(object):

    def __init__(self, driver, wait_time_to_finish, screen_width, screen_height):
        self.driver = driver
        self.driver.set_window_size(screen_width, screen_height)
        self.wait = WebDriverWait(self.driver, wait_time_to_finish)

    def timed_event_for_locust(self, request_type, message, func, *args, **kwargs):
        """
        Use this method whenever you have a logical sequence of browser steps that you would like to time. Group these in a seperate, not @task method and call them using this method. These will show up in the locust web interface with timings

        Args:
            request_type (str): the type of request
            message (str): name to be reported to events.request_*.fire
            func (Function): callable to be timed and logged
            *args: arguments to be used when calling func
            **kwargs: Arbitrary keyword args used for calling func

        Returns:
            func(*args, **kwargs) if this function invocation does not raise an exception

        Raises:
            StopLocust: whenever func raises an exception, this exception is catched, logged to locust as a failure and a StopLocust exception is raised.
        """
        return wrapForLocust(self, request_type, message, func, *args, **kwargs)

    def __getattr__(self, attr):
        """Forward all messages this client doesn't understand to it's webdriver"""
        return getattr(self.driver, attr)
