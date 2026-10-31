import time

from bs4 import BeautifulSoup
from selenium.webdriver.common.by import By

from base.base_site import BaseSite


class Mintos(BaseSite):
    def __init__(self, args):
        login_form_selector = "//form[@class='login-form']"
        self.LOGIN_USERNAME_SELECTOR = login_form_selector + "//input[@id='login-username']"
        self.LOGIN_PASSWORD_SELECTOR = login_form_selector + "//input[@id='login-password']"
        self.LOGIN_BUTTON_SELECTOR = login_form_selector + "//input[@type='submit']"
        self.TOTP_FIELD_SELECTOR = login_form_selector + "//*[@class='m-form-input']//input[@type='text']"
        self.TOTP_BUTTON_SELECTOR = login_form_selector + "//input[@type='submit']"
        super(Mintos, self).__init__(args)
        self.INTEREST_STATEMENT_PAGE = "https://www.mintos.com/en/account-statement/"
        self.LOGIN_PAGE = "https://www.mintos.com/en/login"

    def _handle_totp_if_present(self):
        # TODO
        pass

    def get_statement(self, args):
        self.browser.get(self.INTEREST_STATEMENT_PAGE)

        start_date_field = self.browser.find_element(by=By.ID, value="statement-start-date")
        end_date_field = self.browser.find_element(by=By.ID, value="statement-start-date")
        # TODO filter date range

        # TODO download CSV into Mintos folder
