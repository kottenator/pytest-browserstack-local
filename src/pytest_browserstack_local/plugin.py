import pytest

from .process import start_daemon, start_process, stop_process
from .utils import parse_config


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
        help=(
            'Path to BrowserStackLocal binary. '
            'Default: BrowserStackLocal (i.e. it should be in PATH).'
        )
    )
    group.addoption(
        '--browserstack-local-argument',
        action='append',
        default=[],
        dest='browserstack_local_arguments',
        help=(
            'BrowserStackLocal argument in a form: '
            '--browserstack-local-argument localIdentifier=12345. Can be set multiple times.'
        )
    )


@pytest.hookimpl(trylast=True)
def pytest_configure(config):
    if config.getoption('browserstack_local'):
        browserstack_local_cmd = parse_config(config)
        config._browserstack_local_cmd = browserstack_local_cmd

        if '--daemon' in browserstack_local_cmd:
            config._browserstack_local_daemon = start_daemon(browserstack_local_cmd)
        else:
            config._browserstack_local_process = start_process(browserstack_local_cmd)


def pytest_unconfigure(config):
    browserstack_local_process = getattr(config, '_browserstack_local_process', None)

    if browserstack_local_process:
        print("Stopping BrowserStackLocal process ...")
        stop_process(browserstack_local_process.pid)
        del config._browserstack_local_process

    browserstack_local_daemon = getattr(config, '_browserstack_local_daemon', None)

    if browserstack_local_daemon:
        print("Stopping BrowserStackLocal daemon ...")
        stop_process(browserstack_local_daemon['pid'])
        del config._browserstack_local_daemon


@pytest.fixture
def browserstack_local(request):
    config = request.config

    if config.getoption('browserstack_local'):
        return {
            'process': getattr(config, '_browserstack_local_process', None),
            'daemon': getattr(config, '_browserstack_local_daemon', None),
            'cmd': config._browserstack_local_cmd
        }
