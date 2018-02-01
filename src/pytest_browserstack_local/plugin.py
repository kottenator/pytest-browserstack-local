import pytest


def pytest_addoption(parser):
    group = parser.getgroup('browserstack-local')
    group.addoption(
        '--browserstack-local',
        action='store_true',
        help='Run BrowserStackLocal in background while test session is running.'
    )


@pytest.hookimpl(trylast=True)
def pytest_configure(config):
    browserstack_local_config = config._variables.get('BrowserStackLocal', {})
    config._browserstack_local_config = browserstack_local_config


@pytest.fixture(autouse=True, scope='session')
def browserstack_local_process(request):
    if request.config.getoption('browserstack_local'):
        print("Running BrowserStackLocal ... (fake)")
