from .defaults import *
import os

os_env = os.environ

USER_ONE = os_env.get('USER_ONE')
USER_ONE_PASSWORD = os_env.get('USER_ONE_PASSWORD')

USER_TWO = os_env.get('USER_TWO')
USER_TWO_PASSWORD = os_env.get('USER_TWO_PASSWORD')

DRIVER = 'Remote'

caps = {
    'chrome': {'browser': 'Chrome', 'os': 'Windows', 'os_version': '10', 'resolution': '1024x768'},
    'edge': {'browser': 'Edge', 'os': 'Windows', 'os_version': '10', 'resolution': '1024x768'},
    'firefox': {'browser': 'Firefox', 'os': 'Windows', 'os_version': '10', 'resolution': '1024x768'},
    'msie': {'browser': 'IE', 'os': 'Windows', 'os_version': '7', 'resolution': '1024x768'},
    'android': {'device': 'Samsung Galaxy S8', 'realMobile': 'true', 'os_version': '7.0'},
    'ios': {'device': 'iPhone 7', 'realMobile': 'true', 'os_version': '10.0'},
    'safari': {'browser': 'Safari', 'os': 'OS X', 'os_version': 'Sierra', 'resolution': '1024x768'}
}

BUILD = os_env.get('TEST_BUILD') or 'firefox'
DESIRED_CAP = caps[BUILD]

OSF_HOME = 'https://staging.osf.io'
API_DOMAIN = 'https://staging-api.osf.io'
