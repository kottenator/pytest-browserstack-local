import os
import shutil

import pytest


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
