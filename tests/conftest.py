import os


def pytest_addoption(parser):
    group = parser.getgroup('browserstack-local-test')
    group.addoption(
        '--browserstack-local-real',
        action='store_true',
        help='Run real BrowserStackLocal instead of fake one in tests.'
    )


def pytest_configure(config):
    if not config.getoption('browserstack_local_real'):
        os.environ['PATH'] = os.pathsep.join(
            [os.path.join(os.path.dirname(__file__), 'fakes')] +
            os.getenv('PATH', '').split(os.pathsep)
        )
