from selenium.webdriver.common.by import By

import settings
from base.locators import (
    ComponentLocator,
    Locator,
)
from components.navbars import MeetingsNavbar
from pages.base import OSFBasePage


class BaseMeetingsPage(OSFBasePage):

    navbar = ComponentLocator(MeetingsNavbar)


class MeetingsPage(BaseMeetingsPage):
    url = settings.OSF_HOME + '/meetings/'

    identity = Locator(
        By.CSS_SELECTOR, 'img[alt="Logo for OSF meeting"]', settings.VERY_LONG_TIMEOUT
    )
    register_button = Locator(
        By.CSS_SELECTOR, 'button[data-test-register-button]', settings.LONG_TIMEOUT
    )
    register_text = Locator(By.CSS_SELECTOR, 'div[data-test-register-panel-text]')
    upload_button = Locator(
        By.CSS_SELECTOR, 'button[data-test-upload-button]', settings.LONG_TIMEOUT
    )
    upload_text = Locator(By.CSS_SELECTOR, 'div[data-test-upload-panel-text]')
    top_meeting_link = Locator(
        By.CSS_SELECTOR,
        'div[data-test-meetings-list-item-name] > a',
    )
    filter_input = Locator(
        By.CSS_SELECTOR, 'div[data-test-meetings-list-search] > div > input'
    )
    sort_caret_name_asc = Locator(
        By.CSS_SELECTOR, 'button[data-test-ascending-sort="name"]'
    )
    sort_caret_name_desc = Locator(
        By.CSS_SELECTOR, 'button[data-test-descending-sort="name"]'
    )
    aps_logo = Locator(By.CSS_SELECTOR, ' img[data-test-aps-img]')
    bitss_logo = Locator(By.CSS_SELECTOR, 'img[data-test-bitss-img]')
    nrao_logo = Locator(By.CSS_SELECTOR, 'img[data-test-nrao-img]')
    spsp_logo = Locator(By.CSS_SELECTOR, 'img[data-test-spsp-img]')
    skeleton_row = Locator(
        By.CSS_SELECTOR, 'div[data-test-ember-content-placeholders-text-line]'
    )


class MeetingDetailPage(BaseMeetingsPage):
    # test url functionality
    url = settings.OSF_HOME + '/view/'

    identity = Locator(
        By.CSS_SELECTOR, 'div._toggle-button-and-homepage-link-container_1h8tly'
    )
    meeting_title = Locator(By.CSS_SELECTOR, 'h1[data-test-meeting-name]')
    entry_download_button = Locator(
        By.CSS_SELECTOR,
        'div[data-test-submissions-list-item-download] > button',
    )
    first_entry_link = Locator(
        By.CSS_SELECTOR,
        'div[data-test-submissions-list-item-title] > a',
    )
    title = Locator(By.CSS_SELECTOR, '#nodeTitleEditable', settings.LONG_TIMEOUT)
    filter_input = Locator(By.CSS_SELECTOR, 'input[placeholder="Search"]')
    sort_caret_title_asc = Locator(
        By.CSS_SELECTOR, 'button[data-test-ascending-sort="title"]'
    )
