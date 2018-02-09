import json
import os
import shutil

import pytest

from pytest_browserstack_local.utils import BROWSERSTACK_ACCESS_KEY_ENV_VAR

TEST_DIR = os.path.dirname(os.path.dirname(__file__))
RUN_DIR = os.path.join(TEST_DIR, 'run')
TEST_ACCESS_KEY = '123'
WRONG_ACCESS_KEY = '111'


@pytest.fixture(autouse=True)
def clean_fake_locks():
    if os.path.exists(RUN_DIR):
        shutil.rmtree(RUN_DIR)
    os.mkdir(RUN_DIR)


@pytest.mark.sensitive
def test_remote(httpserver, selenium):
    httpserver.serve_content('<h1>Hello, World!</h1>')
    selenium.get(httpserver.url)
    heading = selenium.find_element_by_tag_name('h1')

    assert heading
    assert heading.text == "Hello, World!"


def test_plugin_process_ok(testdir):
    """
    Test that ``BrowserStackLocal`` subprocess is created and has a PID.

    :param testdir: ``pytester`` fixture.
    """
    testdir.makepyfile("""
        def test_process(browserstack_local):
            assert not browserstack_local['daemon']
            assert browserstack_local['process']
            assert browserstack_local['process'].pid
            assert browserstack_local['cmd'] == ['BrowserStackLocal', '--key', '{}']
    """.format(TEST_ACCESS_KEY))

    result = testdir.runpytest(
        '--browserstack-local', '--browserstack-local-argument', 'key={}'.format(TEST_ACCESS_KEY)
    )
    result.assert_outcomes(passed=1)


def test_plugin_process_fail(testdir):
    """
    Test that ``BrowserStackLocal`` subprocess is not created when there's wrong access key.

    :param testdir: ``pytester`` fixture.
    """
    testdir.makepyfile("""
        def test_process(browserstack_local):
            assert browserstack_local == {{
                'daemon': None,
                'process': None,
                'cmd': ['BrowserStackLocal', '--key', '{}']
            }}
    """.format(WRONG_ACCESS_KEY))

    result = testdir.runpytest(
        '--browserstack-local', '--browserstack-local-argument', 'key={}'.format(WRONG_ACCESS_KEY)
    )
    result.assert_outcomes(passed=1)


def test_plugin_daemon_ok(testdir):
    """
    Test that ``BrowserStackLocal`` daemon is invoked and has a PID.

    :param testdir: ``pytester`` fixture.
    """
    testdir.makepyfile("""
        def test_daemon(browserstack_local):
            assert not browserstack_local['process']
            assert browserstack_local['daemon']
            assert browserstack_local['daemon']['pid']
            assert browserstack_local['cmd'] == [
                'BrowserStackLocal', '--key', '{}', '--daemon', 'start'
            ]
    """.format(TEST_ACCESS_KEY))

    result = testdir.runpytest(
        '--browserstack-local', '--browserstack-local-argument', 'key={}'.format(TEST_ACCESS_KEY),
        '--browserstack-local-argument', 'daemon=start'
    )
    result.assert_outcomes(passed=1)


def test_plugin_daemon_fail(testdir):
    """
    Test that ``BrowserStackLocal`` daemon is not invoked when there's wrong access key.

    :param testdir: ``pytester`` fixture.
    """
    testdir.makepyfile("""
        def test_daemon(browserstack_local):
            assert browserstack_local == {{
                'daemon': None,
                'process': None,
                'cmd': ['BrowserStackLocal', '--key', '{}', '--daemon', 'start']
            }}
    """.format(WRONG_ACCESS_KEY))

    result = testdir.runpytest(
        '--browserstack-local', '--browserstack-local-argument', 'key={}'.format(WRONG_ACCESS_KEY),
        '--browserstack-local-argument', 'daemon=start'
    )
    result.assert_outcomes(passed=1)


def test_plugin_conf_file(testdir):
    """
    Test that ``BrowserStackLocal`` reads parameters from a config file.

    :param testdir: ``pytester`` fixture.
    """
    conf_file = os.path.join(RUN_DIR, 'browserstack-local-test.json')

    with open(conf_file, 'w') as f:
        json.dump({'BrowserStackLocal': {'key': TEST_ACCESS_KEY}}, f)

    testdir.makepyfile("""
        def test_daemon(browserstack_local):
            assert browserstack_local['cmd'] == [
                'BrowserStackLocal', '--key', '{}', '--daemon', 'start'
            ]
    """.format(TEST_ACCESS_KEY))

    result = testdir.runpytest(
        '--browserstack-local', '--variables', conf_file,
        '--browserstack-local-argument', 'daemon=start'
    )
    result.assert_outcomes(passed=1)


def test_plugin_env_var(testdir, monkeypatch):
    """
    Test that ``BrowserStackLocal`` reads parameters (e.g. access key) passed as
    environment variables.

    :param testdir: ``pytester`` fixture.
    """
    monkeypatch.setenv(BROWSERSTACK_ACCESS_KEY_ENV_VAR, TEST_ACCESS_KEY)

    testdir.makepyfile("""
        def test_daemon(browserstack_local):
            assert browserstack_local['cmd'] == [
                'BrowserStackLocal', '--key', '{}', '--daemon', 'start'
            ]
    """.format(TEST_ACCESS_KEY))

    result = testdir.runpytest(
        '--browserstack-local', '--browserstack-local-argument', 'daemon=start'
    )
    result.assert_outcomes(passed=1)


def test_plugin_env_var_vs_conf_file(testdir, monkeypatch):
    """
    Test that ``BrowserStackLocal`` parameter (e.g. access key) passed as an environment variable
    has higher priority that the one from a config file.

    :param testdir: ``pytester`` fixture.
    """
    monkeypatch.setenv(BROWSERSTACK_ACCESS_KEY_ENV_VAR, '555')
    conf_file = os.path.join(RUN_DIR, 'browserstack-local-test.json')

    with open(conf_file, 'w') as f:
        json.dump({'BrowserStackLocal': {'key': '333'}}, f)

    testdir.makepyfile("""
            def test_daemon(browserstack_local):
                assert browserstack_local['cmd'] == [
                    'BrowserStackLocal', '--key', '555', '--daemon', 'start'
                ]
        """)

    result = testdir.runpytest(
        '--browserstack-local', '--variables', conf_file,
        '--browserstack-local-argument', 'daemon=start'
    )
    result.assert_outcomes(passed=1)


def test_plugin_env_var_vs_arg(testdir, monkeypatch):
    """
    Test that ``BrowserStackLocal`` parameter (e.g. access key) passed as an environment variable
    has lower priority that the one from a command-line argument.

    :param testdir: ``pytester`` fixture.
    """
    monkeypatch.setenv(BROWSERSTACK_ACCESS_KEY_ENV_VAR, '555')

    testdir.makepyfile("""
            def test_daemon(browserstack_local):
                assert browserstack_local['cmd'] == [
                    'BrowserStackLocal', '--key', '777', '--daemon', 'start'
                ]
        """)

    result = testdir.runpytest(
        '--browserstack-local', '--browserstack-local-argument', 'key=777',
        '--browserstack-local-argument', 'daemon=start'
    )
    result.assert_outcomes(passed=1)
