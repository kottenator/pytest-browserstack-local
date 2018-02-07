import os
import pytest


@pytest.fixture(autouse=True)
def clean_fake_locks():
    for lock_name in ['default', '789']:
        lock_file = 'browserstack-local-identifier-{}.lock'.format(lock_name)

        if os.path.exists(lock_file):
            os.remove(lock_file)


@pytest.mark.sensitive
def test_remote(httpserver, selenium):
    httpserver.serve_content('<h1>Hello, World!</h1>')
    selenium.get(httpserver.url)
    heading = selenium.find_element_by_tag_name('h1')

    assert heading
    assert heading.text == "Hello, World!"


def test_plugin_process_run(testdir):
    """
    Test that ``BrowserStackLocal`` subprocess is created and has a PID.

    :param testdir: ``pytester`` fixture.
    """
    testdir.makepyfile("""
        def test_plugin_process_run(browserstack_local):
            assert not browserstack_local['daemon']
            assert browserstack_local['process']
            assert browserstack_local['process'].pid
            assert browserstack_local['cmd'] == ['BrowserStackLocal', '--key', '123']
    """)

    result = testdir.runpytest('--browserstack-local', '--browserstack-local-argument', 'key=123')
    result.assert_outcomes(passed=1)


def test_plugin_daemon_run(testdir):
    """
    Test that ``BrowserStackLocal`` daemon is invoked and has a PID.

    :param testdir: ``pytester`` fixture.
    """
    testdir.makepyfile("""
        def test_plugin_daemon_run(browserstack_local):
            assert not browserstack_local['process']
            assert browserstack_local['daemon']
            assert browserstack_local['daemon']['pid']
            assert browserstack_local['cmd'] == [
                'BrowserStackLocal', '--key', '123', '--daemon', 'start'
            ]
    """)

    result = testdir.runpytest(
        '--browserstack-local', '--browserstack-local-argument', 'key=123',
        '--browserstack-local-argument', 'daemon=start'
    )
    result.assert_outcomes(passed=1)
