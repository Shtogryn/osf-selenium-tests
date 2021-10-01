import pytest
import requests
from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.select import Select
from selenium.webdriver.support.wait import WebDriverWait

import markers
import settings
from pages.landing import LandingPage
from pages.login import (
    CASAuthorizationPage,
    ForgotPasswordPage,
    GenericCASPage,
    InstitutionalLoginPage,
    Login2FAPage,
    LoginPage,
    LoginToSPage,
    UnsupportedInstitutionLoginPage,
    login,
)
from pages.register import RegisterPage


@pytest.fixture
def login_page(driver):
    login_page = LoginPage(driver)
    login_page.goto()
    return login_page


@markers.smoke_test
class TestLoginPage:
    @markers.core_functionality
    def test_institutional_login(self, driver, login_page):
        """Check that you arrive on the institutional login page and the institution dropdown is populated.
        We can't actually test institutional login.
        """
        login_page.institutional_login_button.click()
        institutional_login_page = InstitutionalLoginPage(driver, verify=True)
        assert len(institutional_login_page.dropdown_options) > 1

    @markers.core_functionality
    def test_orcid_login(self, driver, login_page):
        """Check that you arrive on the orcid login page."""
        login_page.orcid_login_button.click()

        # If user is logged out of ORCID, ORCID's Oauth service will use
        # redirect link before landing on ORCID sign in page
        WebDriverWait(driver, 10).until(EC.url_contains('https://orcid.org/signin'))

        # Oauth will redirect to callback url with "error" if anything goes wrong
        assert 'error' not in driver.current_url

    def test_osf_home_link(self, driver, login_page):
        login_page.osf_home_link.click()
        assert LandingPage(driver, verify=True)

    def test_sign_up_button(self, driver, login_page):
        login_page.sign_up_button.click()
        assert RegisterPage(driver, verify=True)

    def test_reset_password_link(self, driver, login_page):
        login_page.reset_password_link.click()
        assert ForgotPasswordPage(driver, verify=True)

    def test_need_help_link(self, driver, login_page):
        login_page.need_help_link.click()
        assert 'https://help.osf.io' and 'Sign-in-to-OSF' in driver.current_url

    def test_cos_footer_link(self, driver, login_page):
        login_page.cos_footer_link.click()
        assert driver.current_url == 'https://www.cos.io/'

    def test_terms_of_use_footer_link(self, driver, login_page):
        login_page.terms_of_use_footer_link.click()
        assert (
            driver.current_url
            == 'https://github.com/CenterForOpenScience/cos.io/blob/master/TERMS_OF_USE.md'
        )

    def test_privacy_policy_footer_link(self, driver, login_page):
        login_page.privacy_policy_footer_link.click()
        assert (
            driver.current_url
            == 'https://github.com/CenterForOpenScience/cos.io/blob/master/PRIVACY_POLICY.md'
        )

    def test_status_footer_link(self, driver, login_page):
        login_page.status_footer_link.click()
        assert driver.current_url == 'https://status.cos.io/'


@markers.dont_run_on_prod
class Test2FAPage:
    """This test logs in as a user with 2 Factor Authentication enabled and verifies that after entering their
    login credentials as normal the user is then directed to a 2 Factor Authentication page. The test verifies the
    various elements on this page, but it does not complete the login process as Selenium does not currently have
    a way of accessing the one time pass code generated by the authentication provider.
    """

    def test_one_time_password_required(self, driver):
        login(
            driver, user=settings.CAS_2FA_USER, password=settings.CAS_2FA_USER_PASSWORD
        )
        # verify that you are now on the 2 Factor Authentication page
        two_factor_page = Login2FAPage(driver, verify=True)
        assert two_factor_page.username_input.present()
        assert two_factor_page.oneTimePassword_input.present()
        # click the Verify button and verify that you receive an error message that a one-time password is required
        two_factor_page.verify_button.click()
        assert (
            two_factor_page.login_error_message.text == 'One-time password is required.'
        )

    def test_invalid_one_time_password(self, driver):
        login(
            driver, user=settings.CAS_2FA_USER, password=settings.CAS_2FA_USER_PASSWORD
        )
        two_factor_page = Login2FAPage(driver, verify=True)
        # Enter an invalid one-time password and click the Verify button and verify that you receive an error message
        two_factor_page.oneTimePassword_input.send_keys_deliberately('999999')
        two_factor_page.verify_button.click()
        assert (
            two_factor_page.login_error_message.text
            == 'The one-time password you entered is incorrect.'
        )

    def test_cancel_2fa_login(self, driver):
        login(
            driver, user=settings.CAS_2FA_USER, password=settings.CAS_2FA_USER_PASSWORD
        )
        two_factor_page = Login2FAPage(driver, verify=True)
        # click the Cancel link and verify that you are redirected back to the OSF home page
        two_factor_page.cancel_link.click()
        assert LandingPage(driver, verify=True)

    def test_need_help_link(self, driver):
        login(
            driver, user=settings.CAS_2FA_USER, password=settings.CAS_2FA_USER_PASSWORD
        )
        two_factor_page = Login2FAPage(driver, verify=True)
        two_factor_page.need_help_link.click()
        assert (
            'https://help.osf.io'
            and 'Enable-or-Disable-Two-Factor-Authentication' in driver.current_url
        )


@markers.dont_run_on_prod
class TestToSPage:
    """This test logs in as a user that has not accepted the OSF Terms of Service and verifies that after entering
    their login credentials as normal the user is then directed to a Terms of Service acceptance page. The test
    verifies the various elements on this page, but it does not complete the acceptance of the terms of service
    since that would spoil the user setup data for future test runs.
    """

    def test_continue_button_disabled(self, driver):
        login(
            driver, user=settings.CAS_TOS_USER, password=settings.CAS_TOS_USER_PASSWORD
        )
        tos_page = LoginToSPage(driver, verify=True)
        # verify that at first the Continue button is disabled and then becomes enabled after checking the checkbox
        assert driver.find_element(By.ID, 'primarySubmitButton').get_property(
            'disabled'
        )
        tos_page.tos_checkbox.click()
        assert tos_page.continue_button.is_enabled()

    def test_terms_of_use_link(self, driver):
        login(
            driver, user=settings.CAS_TOS_USER, password=settings.CAS_TOS_USER_PASSWORD
        )
        tos_page = LoginToSPage(driver, verify=True)
        tos_page.terms_of_use_link.click()
        assert (
            driver.current_url
            == 'https://github.com/CenterForOpenScience/cos.io/blob/master/TERMS_OF_USE.md'
        )

    def test_privacy_policy_link(self, driver):
        login(
            driver, user=settings.CAS_TOS_USER, password=settings.CAS_TOS_USER_PASSWORD
        )
        tos_page = LoginToSPage(driver, verify=True)
        tos_page.privacy_policy_link.click()
        assert (
            driver.current_url
            == 'https://github.com/CenterForOpenScience/cos.io/blob/master/PRIVACY_POLICY.md'
        )

    def test_cancel_tos_link(self, driver):
        login(
            driver, user=settings.CAS_TOS_USER, password=settings.CAS_TOS_USER_PASSWORD
        )
        tos_page = LoginToSPage(driver, verify=True)
        # click the Cancel link and verify that you are redirected back to the OSF home page
        tos_page.cancel_link.click()
        assert LandingPage(driver, verify=True)


class TestGenericPages:
    """Generic pages have no service in the login/logout url. Typically users should not be able to access
    these pages through the standard authentication workflow. The tests in this class manually manipulate the
    urls used in order to get to these pages so that we can verify that they do function just in case they
    are ever needed.
    """

    def test_generic_logged_in_page(self, driver, must_be_logged_in):
        """Test the generic CAS logged in page by manually navigating to a CAS page without a service in the url"""
        driver.get(settings.CAS_DOMAIN + '/login')
        logged_in_page = GenericCASPage(driver, verify=True)
        assert (
            logged_in_page.auto_redirect_message.text
            == "Auto-redirection didn't happen ..."
        )
        assert logged_in_page.status_message.text == 'Login successful'

    def test_generic_logged_out_page(self, driver):
        """Test the generic CAS logged out page by manually navigating to a CAS page without a service in the url"""
        driver.get(settings.CAS_DOMAIN + '/logout')
        logged_out_page = GenericCASPage(driver, verify=True)
        assert (
            logged_out_page.auto_redirect_message.text
            == "Auto-redirection didn't happen ..."
        )
        assert logged_out_page.status_message.text == 'Logout successful'


class TestLoginErrors:
    """Test the inline error messages on the CAS login page when user enters invalid login data"""

    def test_missing_email(self, driver, login_page):
        login_page.submit_button.click()
        assert login_page.login_error_message.text == 'Email is required.'

    def test_missing_password(self, driver, login_page):
        login_page.username_input.send_keys_deliberately('foo')
        login_page.submit_button.click()
        assert login_page.login_error_message.text == 'Password is required.'

    def test_invalid_email_and_password(self, driver, login_page):
        login_page.username_input.send_keys_deliberately('foo')
        login_page.password_input.send_keys_deliberately('foo')
        login_page.submit_button.click()
        assert (
            login_page.login_error_message.text
            == 'The email or password you entered is incorrect.'
        )

    def test_invalid_password(self, driver, login_page):
        login_page.username_input.send_keys_deliberately(settings.USER_ONE)
        login_page.password_input.send_keys_deliberately('foo')
        login_page.submit_button.click()
        assert (
            login_page.login_error_message.text
            == 'The email or password you entered is incorrect.'
        )


class TestCustomExceptionPages:
    """CAS has several customized exception pages which share the same style and appearance as the CAS login pages.
    Not all of them can be easily tested. Those that can will require the manipulation of urls to reach the pages.
    """

    def test_service_not_authorized_page(self, driver):
        """Test the Service not authorized exception page by having an invalid service in the url"""
        driver.get(settings.CAS_DOMAIN + '/login?service=https://noservice.osf.io/')
        exception_page = GenericCASPage(driver, verify=True)
        assert exception_page.navbar_brand.text == 'OSF HOME'
        assert exception_page.status_message.text == 'Service not authorized'

    def test_verification_key_login_failed_page(self, driver):
        """Test the Verification key login failed exception page by having an invalid verification_key parameter
        in the url
        """
        driver.get(
            settings.CAS_DOMAIN
            + '/login?service='
            + settings.CAS_DOMAIN
            + '/login/?next='
            + settings.CAS_DOMAIN
            + '/&username='
            + settings.USER_ONE
            + '&verification_key=foo'
        )
        exception_page = GenericCASPage(driver, verify=True)
        assert exception_page.navbar_brand.text == 'OSF HOME'
        assert exception_page.status_message.text == 'Verification key login failed'

    def test_flow_less_page_not_found_page(self, driver):
        """Test the Page Not Found exception page by having an invalid path in the url. CAS only supports 3 valid paths:
        /login, /logout, or /oauth.
        """
        driver.get(settings.CAS_DOMAIN + '/nopath')
        exception_page = GenericCASPage(driver, verify=True)
        # Since this exception page is flow-less (a.k.a. OSF unaware) the navbar will display OSF CAS instead of OSF HOME
        assert exception_page.navbar_brand.text == 'OSF CAS'
        assert exception_page.status_message.text == 'Page Not Found'

    @markers.dont_run_on_prod
    def test_account_not_confirmed_page(self, driver):
        login(
            driver,
            user=settings.UNCONFIRMED_USER,
            password=settings.UNCONFIRMED_USER_PASSWORD,
        )
        exception_page = GenericCASPage(driver, verify=True)
        assert exception_page.navbar_brand.text == 'OSF HOME'
        assert exception_page.status_message.text == 'Account not confirmed'

    @markers.dont_run_on_prod
    def test_account_disabled_page(self, driver):
        login(
            driver,
            user=settings.DEACTIVATED_USER,
            password=settings.DEACTIVATED_USER_PASSWORD,
        )
        exception_page = GenericCASPage(driver, verify=True)
        assert exception_page.navbar_brand.text == 'OSF HOME'
        assert exception_page.status_message.text == 'Account disabled'


@markers.smoke_test
class TestInstitutionLoginPage:
    @pytest.fixture
    def institution_login_page(self, driver):
        institution_login_page = InstitutionalLoginPage(driver)
        institution_login_page.goto()
        return institution_login_page

    def test_enable_sign_in_button(self, driver, institution_login_page):
        """When you first go to the Institution Login page the Sign In button is disabled. It
        only becomes enabled after selecting an institution from the dropdown list.
        """
        assert driver.find_element(By.ID, 'institutionSubmit').get_property('disabled')
        institution_select = Select(institution_login_page.institution_dropdown)
        # select the first institution in the dropdown - index 0 is the message '-- select an institution --'
        institution_select.select_by_index(1)
        assert institution_login_page.sign_in_button.is_enabled()

    def test_osf_home_link(self, driver, institution_login_page):
        institution_login_page.osf_home_link.click()
        assert LandingPage(driver, verify=True)

    def test_sign_up_button(self, driver, institution_login_page):
        institution_login_page.sign_up_button.click()
        assert RegisterPage(driver, verify=True)

    def test_cant_find_institution_link(self, driver, institution_login_page):
        institution_login_page.cant_find_institution_link.click()
        assert UnsupportedInstitutionLoginPage(driver, verify=True)

    def test_need_help_link(self, driver, institution_login_page):
        institution_login_page.need_help_link.click()
        assert 'https://help.osf.io' and 'Sign-in-to-OSF' in driver.current_url

    def test_sign_in_with_osf_link(self, driver, institution_login_page):
        institution_login_page.sign_in_with_osf_link.click()
        assert LoginPage(driver, verify=True)

    def test_cos_footer_link(self, driver, institution_login_page):
        institution_login_page.cos_footer_link.click()
        assert driver.current_url == 'https://www.cos.io/'

    def test_terms_of_use_footer_link(self, driver, institution_login_page):
        institution_login_page.terms_of_use_footer_link.click()
        assert (
            driver.current_url
            == 'https://github.com/CenterForOpenScience/cos.io/blob/master/TERMS_OF_USE.md'
        )

    def test_privacy_policy_footer_link(self, driver, institution_login_page):
        institution_login_page.privacy_policy_footer_link.click()
        assert (
            driver.current_url
            == 'https://github.com/CenterForOpenScience/cos.io/blob/master/PRIVACY_POLICY.md'
        )

    def test_status_footer_link(self, driver, institution_login_page):
        institution_login_page.status_footer_link.click()
        assert driver.current_url == 'https://status.cos.io/'


@markers.dont_run_on_prod
class TestOauthAPI:
    def test_authorization_online(self, driver, must_be_logged_in):
        client_id = settings.DEVAPP_CLIENT_ID
        client_secret = settings.DEVAPP_CLIENT_SECRET
        redirect_uri = 'https://www.google.com/'
        requested_scope = (
            'osf.nodes.metadata_read osf.nodes.access_read osf.nodes.data_read'
        )
        authorization_url = (
            settings.CAS_DOMAIN
            + '/oauth2/authorize?response_type=code&client_id='
            + client_id
            + '&redirect_uri='
            + redirect_uri
            + '&scope='
            + requested_scope
            + '&access_type=online'
        )
        # navigate to the authorization url in the browser
        driver.get(authorization_url)
        authorization_page = CASAuthorizationPage(driver, verify=True)
        assert authorization_page.navbar_brand.text == 'OSF HOME'
        assert authorization_page.status_message.text == 'Approve or deny authorization'
        # click allow button to redirect to callback url with authorization code
        authorization_page.allow_button.click()
        callback_url = driver.current_url
        # parse out authorization code from callback url
        authorization_code = callback_url.partition('?code=')[2]
        token_url = settings.CAS_DOMAIN + '/oauth2/token'
        # set the body parameters for the POST including the authorization code
        body_params = {
            'code': authorization_code,
            'grant_type': 'authorization_code',
            'client_id': client_id,
            'client_secret': client_secret,
            'redirect_uri': redirect_uri,
        }
        r = requests.post(token_url, data=body_params)
        assert r.status_code == 200
        # get the access token from the response
        access_token = r.json()['access_token']
        # use the access token to check profile
        profile_url = settings.CAS_DOMAIN + '/oauth2/profile'
        headers = {'Authorization': 'Bearer ' + access_token}
        r = requests.get(profile_url, headers=headers)
        # verify the profile response
        assert r.status_code == 200
        assert (
            r.json()['scope'] == requested_scope.split()
        )  # response has a comma separated list while the scopes in authorization url are separated by spaces
        assert r.json()['service'] == redirect_uri
        assert r.json()['attributes']['oauthClientId'] == client_id
        # lastly we want to revoke the access token
        revoke_url = settings.CAS_DOMAIN + '/oauth2/revoke'
        # set the body parameters for the POST with the access token to be revoked
        body_params = {'token': access_token}
        r = requests.post(revoke_url, data=body_params)
        # verify revoke status code returns 204 if revoke was successful
        assert r.status_code == 204
        # now try profile again with access code and verify that access code has been successfully revoked
        headers = {'Authorization': 'Bearer ' + access_token}
        r = requests.get(profile_url, headers=headers)
        assert r.status_code == 401
        assert r.json()['error'] == 'expired_accessToken'

    def test_authorization_offline(self, driver, must_be_logged_in):
        client_id = settings.DEVAPP_CLIENT_ID
        client_secret = settings.DEVAPP_CLIENT_SECRET
        redirect_uri = 'https://www.google.com/'
        requested_scope = 'osf.full_write osf.users.profile_write'
        authorization_url = (
            settings.CAS_DOMAIN
            + '/oauth2/authorize?response_type=code&client_id='
            + client_id
            + '&redirect_uri='
            + redirect_uri
            + '&scope='
            + requested_scope
            + '&access_type=offline&approval_prompt=force'
        )
        # navigate to the authorization url in the browser
        driver.get(authorization_url)
        authorization_page = CASAuthorizationPage(driver, verify=True)
        assert authorization_page.navbar_brand.text == 'OSF HOME'
        assert authorization_page.status_message.text == 'Approve or deny authorization'
        # click allow button to redirect to callback url with authorization code
        authorization_page.allow_button.click()
        callback_url = driver.current_url
        # parse out authorization code from callback url
        authorization_code = callback_url.partition('?code=')[2]
        # set the body parameters for the POST including the authorization code
        body_params = {
            'code': authorization_code,
            'grant_type': 'authorization_code',
            'client_id': client_id,
            'client_secret': client_secret,
            'redirect_uri': redirect_uri,
        }
        token_url = settings.CAS_DOMAIN + '/oauth2/token'
        r = requests.post(token_url, data=body_params)
        assert r.status_code == 200
        # get the access token from the response
        access_token = r.json()['access_token']
        # since it is an offline request there will also be a Refresh token
        refresh_token = r.json()['refresh_token']
        # use the access token to get profile
        profile_url = settings.CAS_DOMAIN + '/oauth2/profile'
        headers = {'Authorization': 'Bearer ' + access_token}
        r = requests.get(profile_url, headers=headers)
        # verify the profile response
        assert r.status_code == 200
        assert (
            r.json()['scope'] == requested_scope.split()
        )  # response has a comma separated list while the scopes in authorization url are separated by spaces
        assert r.json()['service'] == redirect_uri
        assert r.json()['attributes']['oauthClientId'] == client_id
        # now use the refresh token from above to request another access token
        body_params_refresh = {
            'refresh_token': refresh_token,
            'grant_type': 'refresh_token',
            'client_id': client_id,
            'client_secret': client_secret,
            'redirect_uri': redirect_uri,
        }
        token_url = settings.CAS_DOMAIN + '/oauth2/token'
        r = requests.post(token_url, data=body_params_refresh)
        assert r.status_code == 200
        # next get the access token returned from the refresh token response and use it to again get profile
        access_token_refresh = r.json()['access_token']
        profile_url = settings.CAS_DOMAIN + '/oauth2/profile'
        headers = {'Authorization': 'Bearer ' + access_token_refresh}
        r = requests.get(profile_url, headers=headers)
        # again verify the profile response
        assert r.status_code == 200
        assert (
            r.json()['scope'] == requested_scope.split()
        )  # response has a comma separated list while the scopes in authorization url are separated by spaces
        assert r.json()['service'] == client_id
        assert r.json()['attributes']['oauthClientId'] == client_id
        # lastly we want to revoke the refresh token
        revoke_url = settings.CAS_DOMAIN + '/oauth2/revoke'
        # set the body parameters for the POST with the refresh token to be revoked
        body_params = {'token': refresh_token}
        r = requests.post(revoke_url, data=body_params)
        # verify revoke status code returns 204 if revoke was successful
        assert r.status_code == 204
        # now try profile again with access code that was granted from refresh token and verify that access code has also been successfully revoked
        headers = {'Authorization': 'Bearer ' + access_token_refresh}
        r = requests.get(profile_url, headers=headers)
        assert r.status_code == 401
        assert r.json()['error'] == 'expired_accessToken'
        # also check profile on original access code, it should also be revoked
        headers = {'Authorization': 'Bearer ' + access_token}
        r = requests.get(profile_url, headers=headers)
        assert r.status_code == 401
        assert r.json()['error'] == 'expired_accessToken'

    def test_authorization_single_scope(self, driver, must_be_logged_in):
        client_id = settings.DEVAPP_CLIENT_ID
        client_secret = settings.DEVAPP_CLIENT_SECRET
        redirect_uri = 'https://www.google.com/'
        requested_scope = 'osf.nodes.metadata_write'  # request just 1 access type
        authorization_url = (
            settings.CAS_DOMAIN
            + '/oauth2/authorize?response_type=code&client_id='
            + client_id
            + '&redirect_uri='
            + redirect_uri
            + '&scope='
            + requested_scope
            + '&access_type=online&approval_prompt=force'
        )
        # navigate to the authorization url in the browser
        driver.get(authorization_url)
        authorization_page = CASAuthorizationPage(driver, verify=True)
        assert authorization_page.navbar_brand.text == 'OSF HOME'
        assert authorization_page.status_message.text == 'Approve or deny authorization'
        # click allow button to redirect to callback url with authorization code
        authorization_page.allow_button.click()
        callback_url = driver.current_url
        # parse out authorization code from callback url
        authorization_code = callback_url.partition('?code=')[2]
        token_url = settings.CAS_DOMAIN + '/oauth2/token'
        # set the body parameters for the POST including the authorization code
        body_params = {
            'code': authorization_code,
            'grant_type': 'authorization_code',
            'client_id': client_id,
            'client_secret': client_secret,
            'redirect_uri': redirect_uri,
        }
        r = requests.post(token_url, data=body_params)
        assert r.status_code == 200
        # get the access token from the response
        access_token = r.json()['access_token']
        # use the access token to check profile
        profile_url = settings.CAS_DOMAIN + '/oauth2/profile'
        headers = {'Authorization': 'Bearer ' + access_token}
        r = requests.get(profile_url, headers=headers)
        # verify the profile response
        assert r.status_code == 200
        # response will contain list of 2 scopes, the first of which will be empty (otherwise response would be a string and not a list)
        scope_list = list(('', requested_scope))
        assert r.json()['scope'] == scope_list
        assert r.json()['service'] == redirect_uri
        assert r.json()['attributes']['oauthClientId'] == client_id
        # lastly we want to revoke the access token
        revoke_url = settings.CAS_DOMAIN + '/oauth2/revoke'
        # set the body parameters for the POST with the access token to be revoked
        body_params = {'token': access_token}
        r = requests.post(revoke_url, data=body_params)
        # verify revoke status code returns 204 if revoke was successful
        assert r.status_code == 204
        # now try profile again with access code and verify that access code has been successfully revoked
        headers = {'Authorization': 'Bearer ' + access_token}
        r = requests.get(profile_url, headers=headers)
        assert r.status_code == 401
        assert r.json()['error'] == 'expired_accessToken'

    def test_deny_authorization(self, driver, must_be_logged_in):
        client_id = settings.DEVAPP_CLIENT_ID
        redirect_uri = 'https://www.google.com/'
        requested_scope = 'osf.full_read osf.users.email_read'
        authorization_url = (
            settings.CAS_DOMAIN
            + '/oauth2/authorize?response_type=code&client_id='
            + client_id
            + '&redirect_uri='
            + redirect_uri
            + '&scope='
            + requested_scope
            + '&access_type=offline&approval_prompt=force'
        )
        # navigate to the authorization url in the browser
        driver.get(authorization_url)
        authorization_page = CASAuthorizationPage(driver, verify=True)
        assert authorization_page.navbar_brand.text == 'OSF HOME'
        assert authorization_page.status_message.text == 'Approve or deny authorization'
        # click deny button to redirect to callback url with access denied error message
        authorization_page.deny_button.click()
        callback_url = driver.current_url
        # parse out error message from callback url
        message = callback_url.partition('?error=')[2]
        assert message == 'access_denied'

    def test_authorization_failed_missing_client_id(self, driver, must_be_logged_in):
        client_id = ''  # no client id
        redirect_uri = 'https://www.google.com/'
        requested_scope = 'osf.full_read osf.full_write'
        authorization_url = (
            settings.CAS_DOMAIN
            + '/oauth2/authorize?response_type=code&client_id='
            + client_id
            + '&redirect_uri='
            + redirect_uri
            + '&scope='
            + requested_scope
            + '&access_type=online&approval_prompt=force'
        )
        # navigate to the authorization url in the browser
        driver.get(authorization_url)
        # verify exception page
        exception_page = GenericCASPage(driver, verify=True)
        assert exception_page.navbar_brand.text == 'OSF HOME'
        assert exception_page.status_message.text == 'Authorization failed'
        assert exception_page.error_detail.text == 'missing_request_param: client_id'

    def test_authorization_failed_invalid_redirect_uri(self, driver, must_be_logged_in):
        client_id = settings.DEVAPP_CLIENT_ID
        redirect_uri = 'https://www.gogle.com/'  # typo in redirect uri
        requested_scope = 'osf.nodes.access_write osf.users.profile_read'
        authorization_url = (
            settings.CAS_DOMAIN
            + '/oauth2/authorize?response_type=code&client_id='
            + client_id
            + '&redirect_uri='
            + redirect_uri
            + '&scope='
            + requested_scope
            + '&access_type=online&approval_prompt=force'
        )
        # navigate to the authorization url in the browser
        driver.get(authorization_url)
        # verify exception page
        exception_page = GenericCASPage(driver, verify=True)
        assert exception_page.navbar_brand.text == 'OSF HOME'
        assert exception_page.status_message.text == 'Authorization failed'
        assert (
            exception_page.error_detail.text
            == 'invalid_redirect_url: https://www.gogle.com/'
        )

    def test_authorization_failed_invalid_scope(self, driver, must_be_logged_in):
        client_id = settings.DEVAPP_CLIENT_ID
        redirect_uri = 'https://www.google.com/'
        requested_scope = 'everything'  # not a valid scope for OSF
        authorization_url = (
            settings.CAS_DOMAIN
            + '/oauth2/authorize?response_type=code&client_id='
            + client_id
            + '&redirect_uri='
            + redirect_uri
            + '&scope='
            + requested_scope
            + '&access_type=online&approval_prompt=force'
        )
        # navigate to the authorization url in the browser
        driver.get(authorization_url)
        # verify exception page
        exception_page = GenericCASPage(driver, verify=True)
        assert exception_page.navbar_brand.text == 'OSF HOME'
        assert exception_page.status_message.text == 'Authorization failed'
        assert exception_page.error_detail.text == 'invalid_scope: everything'
