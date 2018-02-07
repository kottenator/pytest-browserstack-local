import os

import pytest


pytest_plugins = ['pytester']


def pytest_configure():
    os.environ['PATH'] = os.pathsep.join(
        [os.path.join(os.path.dirname(__file__), 'fakes')] +
        os.getenv('PATH', '').split(os.pathsep)
    )


@pytest.fixture
def fake_config(monkeypatch):
    return lambda args, envs, cfg: FakeConfig(args, envs, cfg, monkeypatch)


class FakeConfig:
    def __init__(self, args, envs, cfg, monkeypatch):
        self._variables = {}
        self._fake_args = {
            'browserstack_local_path': 'BrowserStackLocal',
            'browserstack_local_arguments': []
        }

        if cfg:
            self._variables.update(cfg)

        if envs:
            for k, v in envs.items():
                monkeypatch.setenv(k, v)

        if args:
            self._fake_args.update(args)

    def getoption(self, name):
        return self._fake_args.get(name)
