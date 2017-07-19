from __future__ import print_function

from selenium import webdriver
from selenium.webdriver.support.ui import WebDriverWait

# expectations for driver:
#   [return] execute_script (javascript)

class CookieClicker(object):
    """docstring for CookieClicker."""
    def __init__(self, driver):
        self.__driver__ = driver
        self.__game_loaded__ = False

    def __execute__(self, javascript_string):
        assert self.is_game_loaded()
        return self.__driver__.execute_script(javascript_string)

    def is_game_loaded(self):
        return self.__game_loaded__

    def sync_wait_for_game_to_load(self, timeout=10):
        def wait_for_cookie(driver):
            res = driver.execute_script("return Game;")
            if res is None:
                return False
            return res

        wait = WebDriverWait(driver, timeout)
        wait.until(wait_for_cookie)
        self.__game_loaded__ = True

    def __game_milliseconds_elapsed__(self):
        return self.__execute__("return Game.time - Game.startDate;")

    def __cookies__(self):
        return self.__execute__("return Game.cookies;")

    def __reset_hard__(self):
        self.__execute__("return Game.reset(true);")

if __name__ == '__main__':
    driver = webdriver.Firefox()
    driver.get('http://orteil.dashnet.org/cookieclicker/')

    try:
        clicker = CookieClicker(driver)
        clicker.sync_wait_for_game_to_load()
    except TimeoutException as e:
        raise
    except Exception as e:
        raise
    finally:
        driver.quit()
