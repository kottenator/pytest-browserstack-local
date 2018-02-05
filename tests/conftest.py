import os


def pytest_configure():
    os.environ['PATH'] = os.pathsep.join(
        [os.path.join(os.path.dirname(__file__), 'fakes')] +
        os.getenv('PATH', '').split(os.pathsep)
    )
