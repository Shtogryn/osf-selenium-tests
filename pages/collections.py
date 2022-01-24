from urllib.parse import urljoin

from selenium.webdriver.common.by import By

import settings
from base.locators import (
    ComponentLocator,
    Locator,
)
from components.navbars import CollectionsNavbar
from pages.base import OSFBasePage


class BaseCollectionPage(OSFBasePage):
    """The base page from which all collection pages inherit."""

    base_url = settings.OSF_HOME + '/collections/'
    url_addition = ''
    navbar = ComponentLocator(CollectionsNavbar)

    def __init__(self, driver, verify=False, provider=None):
        self.provider = provider
        if provider:
            self.provider_id = provider['id']
            self.provider_name = provider['attributes']['name']

        super().__init__(driver, verify)

    @property
    def url(self):
        """Set the URL based on the provider domain."""
        return urljoin(self.base_url, self.provider_id) + '/' + self.url_addition

    def verify(self):
        """Return true if you are on the expected page.
        Checks both the general page identity and the branding.
        """
        if self.provider:
            return super().verify() and self.provider_name in self.navbar.title.text
        return super().verify()


class CollectionDiscoverPage(BaseCollectionPage):
    url_addition = 'discover'

    identity = Locator(By.CSS_SELECTOR, 'div[data-test-provider-branding]')
    loading_indicator = Locator(By.CSS_SELECTOR, '.ball-scale')


class CollectionSubmitPage(BaseCollectionPage):
    url_addition = 'submit'

    identity = Locator(By.CSS_SELECTOR, 'div[data-test-collections-submit-sections]')
    project_selector = Locator(
        By.CSS_SELECTOR, 'span[class="ember-power-select-placeholder"]'
    )
    project_help_text = Locator(
        By.CSS_SELECTOR, '.ember-power-select-option--search-message'
    )
    project_selector_project = Locator(By.CSS_SELECTOR, '.ember-power-select-option')
    license_dropdown_trigger = Locator(By.CLASS_NAME, 'ember-basic-dropdown-trigger')
    first_license_option = Locator(
        By.CSS_SELECTOR, '.ember-power-select-options > li:nth-child(1)'
    )
    description_textbox = Locator(By.CSS_SELECTOR, 'textarea[name="description"]')
    tags_input = Locator(By.CLASS_NAME, 'emberTagInput-input')
    project_metadata_save = Locator(
        By.CSS_SELECTOR, '[data-test-project-metadata-save-button]'
    )
    project_contributors_continue = Locator(
        By.CSS_SELECTOR, '[data-test-submit-section-continue]'
    )
    type_dropdown_trigger = Locator(By.CLASS_NAME, 'ember-basic-dropdown-trigger')
    first_type_option = Locator(
        By.CSS_SELECTOR, '.ember-power-select-options > li:nth-child(1)'
    )
    collection_metadata_continue = Locator(
        By.CSS_SELECTOR, '[data-test-submit-section-continue]'
    )
    add_to_collection_button = Locator(
        By.CSS_SELECTOR, '[data-test-collections-submit-submit-button]'
    )
    modal_add_to_collection_button = Locator(
        By.CSS_SELECTOR,
        '[data-test-collection-submission-confirmation-modal-add-button]',
    )