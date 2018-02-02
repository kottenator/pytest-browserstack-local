import pytest
from subprocess import Popen


def pytest_addoption(parser):
    group = parser.getgroup('browserstack-local')
    group.addoption(
        '--browserstack-local',
        action='store_true',
        help='Run BrowserStackLocal in background while test session is running.'
    )
    group.addoption(
        '--browserstack-local-path',
        default='BrowserStackLocal',
        help='Path to BrowserStackLocal binary.'
    )


@pytest.hookimpl(trylast=True)
def pytest_configure(config):
    if config.getoption('browserstack_local'):
        browserstack_local_path = config.getoption('browserstack_local_path')
        browserstack_local_config = config._variables.get('BrowserStackLocal', {})
        config._browserstack_local_config = browserstack_local_config
        print("Starting BrowserStackLocal ...")
        config._browserstack_local_process = Popen([browserstack_local_path])


def pytest_unconfigure(config):
    browserstack_local_process = getattr(config, '_browserstack_local_process', None)

    if browserstack_local_process:
        print("Stopping BrowserStackLocal ...")
        browserstack_local_process.kill()
        browserstack_local_process.communicate()
        del config._browserstack_local_process


@pytest.fixture
def browserstack_local_process(request):
    return getattr(request.config, '_browserstack_local_process', None)
