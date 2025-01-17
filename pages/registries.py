from urllib.parse import urljoin

from selenium.webdriver.common.by import By

import settings
from base.locators import (
    ComponentLocator,
    GroupLocator,
    Locator,
)
from components.navbars import RegistriesNavbar
from components.registration import SubmittedSideNavbar
from pages.base import (
    GuidBasePage,
    OSFBasePage,
)


class BaseRegistriesPage(OSFBasePage):
    base_url = urljoin(settings.OSF_HOME, 'registries/')
    url_addition = ''
    navbar = ComponentLocator(RegistriesNavbar)

    def __init__(self, driver, verify=False, provider=None):
        self.provider = provider
        if provider:
            self.provider_id = provider['id']
            self.provider_name = provider['attributes']['name']

        super().__init__(driver, verify)

    @property
    def url(self):
        """Set the URL based on the provider except when the provider is OSF."""
        if self.provider and self.provider_id != 'osf':
            self.base_url = urljoin(self.base_url, self.provider_id) + '/'
        return urljoin(self.base_url, self.url_addition)


class RegistriesLandingPage(BaseRegistriesPage):
    identity = Locator(
        By.CSS_SELECTOR, '[data-test-registries-list-paragraph]', settings.LONG_TIMEOUT
    )
    search_box = Locator(By.ID, 'search')


class RegistriesDiscoverPage(BaseRegistriesPage):
    url_addition = 'discover'

    identity = Locator(
        By.CSS_SELECTOR, 'div[data-analytics-scope="Registries Discover page"]'
    )
    search_box = Locator(By.ID, 'search-input')
    loading_indicator = Locator(By.CSS_SELECTOR, '.ball-scale', settings.LONG_TIMEOUT)

    # Group Locators
    search_results = GroupLocator(By.CSS_SELECTOR, '._title_1wvii8')


class BaseSubmittedRegistrationPage(GuidBasePage):
    base_url = settings.OSF_HOME
    url_addition = ''
    side_navbar = ComponentLocator(SubmittedSideNavbar)
    title = Locator(By.CSS_SELECTOR, '[data-test-registration-title]')

    def __init__(self, driver, verify=False, guid=''):
        # Set the cookie that prevents the New Feature popover from appearing on
        # submitted registration pages since this popover can get in the way of other
        # actions.
        driver.add_cookie({'name': 'metadataFeaturePopover', 'value': '1'})

        super().__init__(driver, verify, guid)

    @property
    def url(self):
        return self.base_url + '/' + self.guid + '/' + self.url_addition


class RegistrationDetailPage(BaseSubmittedRegistrationPage):
    """This is the Registration Overview Page"""

    identity = Locator(
        By.CSS_SELECTOR, '[data-test-page-heading]', settings.LONG_TIMEOUT
    )

    narrative_summary = Locator(By.CSS_SELECTOR, '[data-test-read-only-response]')
    updates_dropdown = Locator(By.CSS_SELECTOR, '[data-test-update-button]')
    update_registration_button = Locator(
        By.CSS_SELECTOR, '[data-test-update-dropdown-create-new-revision]'
    )
    update_registration_dialogue = Locator(
        By.CSS_SELECTOR, '[data-test-new-update-dialog-main]'
    )
    update_registration_dialogue_next = Locator(
        By.CSS_SELECTOR, '[data-test-new-update-dialog-footer-next]'
    )
    associated_project_link = Locator(
        By.CSS_SELECTOR, 'a[data-analytics-name="Registered from"]'
    )
    open_practice_resource_data = Locator(By.CSS_SELECTOR, '[data-test-resource-link]')
    add_resource_button = Locator(By.CSS_SELECTOR, 'button[aria-label="Add resource"]')
    doi_input_field = Locator(By.XPATH, '//input[@name="pid"]')
    resource_list = Locator(
        By.XPATH, '//li[text()="This registration has no resources."]'
    )
    resource_type_dropdown = Locator(
        By.CSS_SELECTOR, '[data-test-power-select-dropdown]'
    )
    data_icon = Locator(By.CSS_SELECTOR, 'img[data-analytics-name="data"]')
    dropdown_options = GroupLocator(
        By.CSS_SELECTOR,
        '#ember-basic-dropdown-wormhole > div > ul > li>span',
    )

    def select_from_dropdown_listbox(self, selection):
        for option in self.dropdown_options:
            if option.text == selection:
                option.click()
                break

    preview_button = Locator(By.CSS_SELECTOR, '[data-test-preview-button]')
    resource_type_add_button = Locator(By.CSS_SELECTOR, '[data-test-add-button]')
    resouce_type = Locator(By.CSS_SELECTOR, '[data-test-resource-card-type]')
    resouce_type_link = Locator(By.CSS_SELECTOR, '[data-test-resource-card-pid-link]')
    resource_type_delete_button = Locator(
        By.CSS_SELECTOR, 'button[aria-label="Delete resource"]'
    )
    resource_type_delete_confirm = Locator(
        By.CSS_SELECTOR, '[data-test-confirm-delete]'
    )
    resource_type_edit_button = Locator(
        By.CSS_SELECTOR, 'button[aria-label="Edit resource"]'
    )
    resource_description = Locator(
        By.XPATH, '//textarea[@class="ember-text-area ember-view form-control"]'
    )
    save_button = Locator(By.CSS_SELECTOR, '[data-test-save-button]')
    resource_card_description = Locator(
        By.CSS_SELECTOR, '[data-test-resource-card-description]'
    )


class RegistrationMetadataPage(BaseSubmittedRegistrationPage):
    url_addition = 'metadata'
    identity = Locator(By.CSS_SELECTOR, '[data-test-display-resource-type-general]')

    metadata_description = Locator(
        By.CSS_SELECTOR, '[data-test-display-node-description]'
    )
    edit_metadata_description_button = Locator(
        By.CSS_SELECTOR, '[data-test-edit-node-description-button]'
    )
    save_metadata_description_button = Locator(
        By.CSS_SELECTOR, '[data-test-save-node-description-button]'
    )
    contributors_list = Locator(By.CSS_SELECTOR, '[data-test-contributors-list]')
    contributor_search_button = Locator(By.XPATH, '//input[@class="btn btn-default"]')
    add_displayed_contributor_button = Locator(
        By.CSS_SELECTOR, '[a.btn.btn-success.contrib-button.btn-mini]'
    )
    search_input = Locator(By.XPATH, '//input[@class="form-control"]')
    resource_type = Locator(
        By.CSS_SELECTOR, '[data-test-display-resource-type-general]'
    )
    resource_language = Locator(
        By.CSS_SELECTOR, '[data-test-display-resource-language]'
    )
    resource_type_dropdown = Locator(
        By.CSS_SELECTOR, '[data-test-select-resource-type]'
    )
    resource_language_dropdown = Locator(
        By.CSS_SELECTOR, '[data-test-select-resource-language]'
    )

    dropdown_options = GroupLocator(
        By.CSS_SELECTOR,
        '#ember-basic-dropdown-wormhole > div > ul > li>span',
    )

    def select_from_dropdown_listbox(self, selection):
        for option in self.dropdown_options:
            if option.text == selection:
                option.click()
                break

    resource_information_save_button = Locator(
        By.CSS_SELECTOR, '[data-test-save-resource-metadata-button]'
    )
    funder_name = Locator(By.XPATH, '//span[@class="ember-power-select-status-icon"]')
    funder_name_search_input = Locator(
        By.XPATH, '//input[@class="ember-power-select-search-input"]'
    )
    award_title = Locator(By.XPATH, '//input[@name="award_title"]')
    award_info_URI = Locator(By.XPATH, '//input[@name="award_uri"]')
    award_number = Locator(By.XPATH, '//input[@name="award_number"]')
    add_funder_button = Locator(By.XPATH, '//button[text()="Add funder"]')
    delete_funder_button = Locator(By.XPATH, '//button[text()="Delete funder"][2]')
    save_funder_info_button = Locator(
        By.CSS_SELECTOR, '[data-test-save-funding-metadata-button]'
    )
    display_funder_name = Locator(By.CSS_SELECTOR, '[data-test-display-funder-name]')
    display_award_title = Locator(
        By.CSS_SELECTOR, '[data-test-display-funder-award-title]'
    )
    display_award_number = Locator(
        By.CSS_SELECTOR, '[data-test-display-funder-award-number]'
    )
    dispaly_award_info_uri = Locator(
        By.CSS_SELECTOR, '[data-test-display-funder-award-uri]'
    )


class RegistrationFilesListPage(BaseSubmittedRegistrationPage):
    url_addition = 'files'
    identity = Locator(By.CSS_SELECTOR, '[data-test-file-providers-list]')
    file_list_button = Locator(By.CSS_SELECTOR, '[data-test-file-list-link]')
    loading_indicator = Locator(By.CSS_SELECTOR, '.ball-scale')
    first_file_name = Locator(By.CSS_SELECTOR, '[data-test-file-name]')
    first_file_options_button = Locator(
        By.CSS_SELECTOR, '[data-test-file-download-share-trigger]'
    )
    download_link = Locator(By.CSS_SELECTOR, '[data-test-download-button]')
    embed_link = Locator(By.CSS_SELECTOR, '[data-test-embed-button]')
    copy_js_link = Locator(By.CSS_SELECTOR, '[data-test-copy-js]')
    copy_html_link = Locator(By.CSS_SELECTOR, '[data-test-copy-html]')


class RegistrationFileDetailPage(GuidBasePage):
    identity = Locator(By.CSS_SELECTOR, '[data-test-file-renderer')
    file_name = Locator(By.CSS_SELECTOR, 'h2[data-test-filename]')
    first_file_options_button = Locator(
        By.CSS_SELECTOR, '[data-test-file-download-share-trigger]'
    )
    download_link = Locator(By.CSS_SELECTOR, '[data-test-download-button]')
    embed_link = Locator(By.CSS_SELECTOR, '[data-test-embed-button]')
    copy_js_link = Locator(By.CSS_SELECTOR, '[data-test-copy-js]')
    copy_html_link = Locator(By.CSS_SELECTOR, '[data-test-copy-html]')
    versions_button = Locator(By.CSS_SELECTOR, '[data-test-versions-button]')
    first_revision_toggle_button = Locator(
        By.CSS_SELECTOR, '[data-test-file-version-toggle-button]'
    )
    copy_md5_link = Locator(
        By.CSS_SELECTOR, 'div[data-test-file-version-section="md5"] > button'
    )
    copy_sha2_link = Locator(
        By.CSS_SELECTOR, 'div[data-test-file-version-section="sha2"] > button'
    )
    tags_button = Locator(By.CSS_SELECTOR, '[data-test-tags-button]')
    tags_input_box = Locator(By.CSS_SELECTOR, 'li.emberTagInput-new > input')

    tags = GroupLocator(
        By.CSS_SELECTOR, 'ul[data-test-tags-widget-tag-input] > li > span'
    )

    def get_tag(self, tag_value):
        for tag in self.tags:
            if tag.text == tag_value:
                return tag
        return None


class RegistrationResourcesPage(BaseSubmittedRegistrationPage):
    url_addition = 'resources'
    identity = Locator(By.CSS_SELECTOR, '[data-test-add-resource-section]')


class RegistrationWikiPage(BaseSubmittedRegistrationPage):
    url_addition = 'wiki'
    identity = Locator(By.ID, 'wikiName')


class RegistrationComponentsPage(BaseSubmittedRegistrationPage):
    url_addition = 'components'
    identity = Locator(By.CSS_SELECTOR, '[data-test-components-page-heading]')


class RegistrationLinksPage(BaseSubmittedRegistrationPage):
    url_addition = 'links'
    identity = Locator(By.CSS_SELECTOR, '[data-test-links-page-heading]')


class RegistrationAnalyticsPage(BaseSubmittedRegistrationPage):
    url_addition = 'analytics'
    identity = Locator(By.CSS_SELECTOR, '[data-test-analytics-page-heading]')


class RegistrationCommentsPage(BaseSubmittedRegistrationPage):
    url_addition = 'comments'
    identity = Locator(By.CSS_SELECTOR, '._CommentsList_kh9x27')


class RegistrationJustificationForm(GuidBasePage):
    identity = Locator(By.CSS_SELECTOR, '[data-test-link-back-to-registration]')

    justification_textbox = Locator(
        By.CSS_SELECTOR, 'textarea[name="revisionJustification"]'
    )
    justification_next_button = Locator(By.CSS_SELECTOR, '[data-test-goto-next-page]')
    cancel_update_button = Locator(By.CSS_SELECTOR, '[data-test-delete-button]')
    cancel_update_modal = Locator(
        By.CSS_SELECTOR, 'div[data-analytics-scope="Delete button modal"]'
    )
    confirm_cancel_button = Locator(By.CSS_SELECTOR, '[data-test-confirm-delete]')

    navbar_justification = Locator(By.CSS_SELECTOR, '[data-test-link="justification"]')
    navbar_summary = Locator(By.CSS_SELECTOR, '[data-test-link="1-summary"]')
    navbar_review = Locator(By.CSS_SELECTOR, '[data-test-link="review"]')

    summary_review_questions = Locator(
        By.CSS_SELECTOR, 'p[data-test-revised-responses-list-no-update]'
    )
    summary_textbox = Locator(By.CSS_SELECTOR, 'textarea[name="__responseKey_summary"]')
    summary_review_button = Locator(By.CSS_SELECTOR, '[data-test-goto-review]')

    submit_revision = Locator(By.CSS_SELECTOR, '[data-test-submit-revision]')
    accept_changes = Locator(By.CSS_SELECTOR, '[data-test-accept-changes]')
    toast_message = Locator(By.ID, 'toast-container')


class JustificationReviewForm(GuidBasePage):
    identity = Locator(By.ID, 'JustificationPageLabel')

    link_to_registration = Locator(
        By.CSS_SELECTOR, '[data-analytics-name="Go to registration"]'
    )


class RegistrationAddNewPage(BaseRegistriesPage):
    url_addition = 'new'
    identity = Locator(
        By.CSS_SELECTOR, 'form[data-test-new-registration-form]', settings.LONG_TIMEOUT
    )
    has_project_button = Locator(
        By.CSS_SELECTOR, 'form > div > fieldset > div:nth-child(2)'
    )
    no_project_button = Locator(
        By.CSS_SELECTOR, 'form > div > fieldset > div:nth-child(3)'
    )
    project_listbox_trigger = Locator(
        By.CSS_SELECTOR,
        'label[data-test-project-select] > div.ember-basic-dropdown-trigger.ember-power-select-trigger',
    )
    schema_listbox_trigger = Locator(
        By.CSS_SELECTOR,
        'label[data-test-schema-select] > div.ember-basic-dropdown-trigger.ember-power-select-trigger',
    )
    create_draft_button = Locator(
        By.CSS_SELECTOR, 'button[data-test-start-registration-button]'
    )

    # The following generic ember dropdown listbox options locator should work for both
    # the Project listox and the Schema listbox
    dropdown_options = GroupLocator(
        By.CSS_SELECTOR,
        '#ember-basic-dropdown-wormhole > div > ul >li.ember-power-select-option',
    )

    @property
    def url(self):
        """Have to override the url for the Add New Page since this page does
        include 'osf' in the url for OSF Registries
        """
        if self.provider is None:
            self.provider_id = 'osf'
        return urljoin(self.base_url, self.provider_id) + '/' + self.url_addition

    def select_from_dropdown_listbox(self, selection):
        for option in self.dropdown_options:
            if option.text == selection:
                option.click()
                break


class BaseRegistrationDraftPage(BaseRegistriesPage):
    base_url = settings.OSF_HOME + '/registries/drafts/'
    url_addition = ''

    def __init__(self, driver, verify=False, draft_id=''):
        self.draft_id = draft_id
        super().__init__(driver, verify)

    @property
    def url(self):
        return self.base_url + self.draft_id + '/' + self.url_addition

    loading_indicator = Locator(By.CSS_SELECTOR, '.ball-scale')
    page_heading = Locator(By.CSS_SELECTOR, 'h2[data-test-page-heading]')
    next_page_button = Locator(By.CSS_SELECTOR, 'a[data-test-goto-next-page] > button')
    first_file_name = Locator(By.CSS_SELECTOR, 'span[data-test-file-name]')
    missing_data_ind = Locator(By.CSS_SELECTOR, 'svg[data-icon="exclamation-circle"]')
    sampling_plan_page_link = Locator(
        By.CSS_SELECTOR, 'a[data-test-link="3-sampling-plan"]'
    )
    review_page_link = Locator(By.CSS_SELECTOR, 'a[data-test-link="review"]')


class DraftRegistrationMetadataPage(BaseRegistrationDraftPage):
    url_addition = 'metadata'
    identity = Locator(
        By.CSS_SELECTOR, 'div[data-test-metadata-title]', settings.LONG_TIMEOUT
    )
    title_input = Locator(By.NAME, 'title')
    description_textarea = Locator(
        By.CSS_SELECTOR, 'div[data-test-metadata-description] > div > textarea'
    )
    category_listbox_trigger = Locator(
        By.CSS_SELECTOR,
        '#category > div.ember-basic-dropdown-trigger.ember-power-select-trigger',
    )
    license_listbox_trigger = Locator(
        By.CSS_SELECTOR,
        'div[data-test-select-license] > div.ember-basic-dropdown-trigger.ember-power-select-trigger',
    )
    first_selected_subject = Locator(By.CSS_SELECTOR, 'li[data-test-selected-subject]')
    expand_first_subject_button = Locator(
        By.CSS_SELECTOR, 'label[data-test-subject-browse-label] > button'
    )

    tags_input_box = Locator(By.CSS_SELECTOR, 'li.emberTagInput-new > input')
    next_page_button = Locator(By.CSS_SELECTOR, 'a[data-test-goto-next-page] > button')

    # The following generic ember dropdown listbox options locator should work for both
    # the Category listbox and the License listbox
    dropdown_options = GroupLocator(
        By.CSS_SELECTOR,
        '#ember-basic-dropdown-wormhole > div > ul >li.ember-power-select-option',
    )

    top_level_subjects = GroupLocator(
        By.CSS_SELECTOR, 'div[data-analytics-scope="Browse"] > ul > li'
    )
    # The following is for the list of second level subjects for the first top level
    # subject. NOTE: The first top level subject must be expanded (click the downward
    # caret to the right of the subject name) before this list is populated on the page.
    first_subject_second_level_subjects = GroupLocator(
        By.CSS_SELECTOR, 'div[data-analytics-scope="Browse"] > ul > li > div > ul > li'
    )

    def select_from_dropdown_listbox(self, selection):
        for option in self.dropdown_options:
            if option.text == selection:
                option.click()
                break

    def select_top_level_subject(self, selection):
        for subject in self.top_level_subjects:
            if subject.text == selection:
                # Find the checkbox element and click it to select the subject
                checkbox = subject.find_element_by_css_selector(
                    'input.ember-checkbox.ember-view'
                )
                checkbox.click()
                break


class DraftRegistrationSummaryPage(BaseRegistrationDraftPage):
    """Draft Summary Page for an Open Ended Registration Template"""

    url_addition = '1-summary'
    identity = Locator(By.NAME, '__responseKey_summary', settings.LONG_TIMEOUT)
    summary_textbox = Locator(By.NAME, '__responseKey_summary')
    review_page_button = Locator(By.CSS_SELECTOR, 'a[data-test-goto-review] > button')


class DraftRegistrationStudyInfoPage(BaseRegistrationDraftPage):
    """Draft Study Information Page for an OSF Preregistration Template"""

    url_addition = '1-study-information'
    identity = Locator(By.NAME, '__responseKey_q2', settings.LONG_TIMEOUT)
    hypothesis_textbox = Locator(By.NAME, '__responseKey_q2')


class DraftRegistrationDesignPlanPage(BaseRegistrationDraftPage):
    """Draft Design Plan Page for an OSF Preregistration Template"""

    url_addition = '2-design-plan'
    identity = Locator(
        By.CSS_SELECTOR, 'input[id^="radio-Experiment"]', settings.LONG_TIMEOUT
    )
    other_radio_button = Locator(By.CSS_SELECTOR, 'input[id^="radio-Other"]')
    no_blinding_checkbox = Locator(
        By.CSS_SELECTOR, 'div._Checkboxes_qxt8ij > div:nth-child(1) > input'
    )
    personnel_who_interact_checkbox = Locator(
        By.CSS_SELECTOR, 'div._Checkboxes_qxt8ij > div:nth-child(3) > input'
    )
    study_design_textbox = Locator(By.NAME, '__responseKey_q6|question')


class DraftRegistrationSamplingPlanPage(BaseRegistrationDraftPage):
    """Draft Sampling Plan Page for an OSF Preregistration Template"""

    url_addition = '3-sampling-plan'
    identity = Locator(
        By.CSS_SELECTOR,
        'input[id^="radio-Registration prior to creation"]',
        settings.LONG_TIMEOUT,
    )
    reg_following_radio_button = Locator(
        By.CSS_SELECTOR, 'input[id^="radio-Registration following"]'
    )
    data_procedures_textbox = Locator(By.NAME, '__responseKey_q10|question')
    sample_size_textbox = Locator(By.NAME, '__responseKey_q11')


class DraftRegistrationVariablesPage(BaseRegistrationDraftPage):
    """Draft Variables Page for an OSF Preregistration Template"""

    url_addition = '4-variables'
    identity = Locator(By.NAME, '__responseKey_q14|question', settings.LONG_TIMEOUT)
    measured_vars_textbox = Locator(By.NAME, '__responseKey_q15|question')


class DraftRegistrationAnalysisPlanPage(BaseRegistrationDraftPage):
    """Draft Analysis Plan Page for an OSF Preregistration Template"""

    url_addition = '5-analysis-plan'
    identity = Locator(By.NAME, '__responseKey_q17|question', settings.LONG_TIMEOUT)
    stat_models_textbox = Locator(By.NAME, '__responseKey_q17|question')


class DraftRegistrationOtherPage(BaseRegistrationDraftPage):
    """Draft Other Page for an OSF Preregistration Template"""

    url_addition = '6-other'
    identity = Locator(By.NAME, '__responseKey_q23', settings.LONG_TIMEOUT)
    other_textbox = Locator(By.NAME, '__responseKey_q23')
    review_page_button = Locator(By.CSS_SELECTOR, 'a[data-test-goto-review] > button')


class DraftRegistrationReviewPage(BaseRegistrationDraftPage):
    url_addition = 'review'
    identity = Locator(
        By.CSS_SELECTOR,
        '[data-test-toggle-anchor-nav-button]',
        settings.LONG_TIMEOUT,
    )
    title = Locator(By.CSS_SELECTOR, 'p[data-test-review-response="title"]')
    description = Locator(By.CSS_SELECTOR, 'p[data-test-review-response="description"]')
    category = Locator(By.CSS_SELECTOR, 'p[data-test-review-response="category"]')
    license = Locator(By.CSS_SELECTOR, 'p[data-test-review-response="license"]')
    subject = Locator(By.CSS_SELECTOR, 'li[data-test-selected-subject]')
    tags = Locator(By.CSS_SELECTOR, 'ul[data-test-tags-widget-tag-input]')
    register_button = Locator(By.CSS_SELECTOR, 'button[data-test-goto-register]')
    invalid_responses_text = Locator(
        By.CSS_SELECTOR, 'div[data-test-invalid-responses-text]'
    )
    sample_size_question_error = Locator(
        By.CSS_SELECTOR, 'div[data-test-validation-errors="__responseKey_q11"]'
    )
    sample_size_response = Locator(
        By.CSS_SELECTOR, 'p[data-test-read-only-response="__responseKey_q11"]'
    )
    loading_indicator = Locator(By.CSS_SELECTOR, '.ball-scale')

    # Registration Modal
    immediate_radio_button = Locator(By.CSS_SELECTOR, 'input[value="immediate"]')
    submit_button = Locator(
        By.CSS_SELECTOR, 'button[data-test-submit-registration-button]'
    )


class RegistrationTombstonePage(BaseRegistriesPage):
    identity = Locator(
        By.CSS_SELECTOR,
        'div[data-analytics-scope="Tombstone page"]',
        settings.LONG_TIMEOUT,
    )
    tombstone_title = Locator(By.CSS_SELECTOR, 'h2[data-test-tombstone-title]')
