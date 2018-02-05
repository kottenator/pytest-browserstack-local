import pytest

from pytest_browserstack_local.utils import (
    convert_camelcase, convert_to_arg, parse_config, BROWSERSTACK_ACCESS_KEY_ENV_VAR
)


@pytest.mark.parametrize('input_name, expected_output', [
    ('a', 'a'),
    ('abc', 'abc'),
    ('abc-def', 'abc-def'),
    ('localIdentifier', 'local-identifier'),
    ('HTTP', 'http'),
    ('ProxyHTTPRequest', 'proxy-http-request'),
], ids=[
    'one letter',
    'one word',
    'dashed',
    'camelcase',
    'uppercase',
    'camelcase with uppercase'
])
def test_convert_camelcase(input_name, expected_output):
    assert convert_camelcase(input_name) == expected_output


@pytest.mark.parametrize('input_name, expected_output', [
    ('a', '-a'),
    ('-a', '-a'),
    ('--a', '-a'),
    ('abc', '--abc'),
    ('-abc', '--abc'),
    ('--abc', '--abc'),
    ('abc-def', '--abc-def'),
    ('--abc-def', '--abc-def'),
    ('localIdentifier', '--local-identifier'),
    ('HTTP', '--http'),
    ('ProxyHTTPRequest', '--proxy-http-request'),
], ids=[
    'one letter',
    'one letter, -',
    'one letter, --',
    'one word',
    'one word, -',
    'one word, --',
    'dashed',
    'dashed, --',
    'camelcase',
    'uppercase',
    'camelcase with uppercase'
])
def test_convert_to_arg(input_name, expected_output):
    assert convert_to_arg(input_name) == expected_output


@pytest.mark.parametrize('input_data, expected_output', [
    (
        (
            {'browserstack_local_arguments': ['key=123', 'localIdentifier=456', 'only-automate']},
            None,
            None
        ),
        ['BrowserStackLocal', '--key', '123', '--local-identifier', '456', '--only-automate']
    ),
    (
        (
            None,
            {BROWSERSTACK_ACCESS_KEY_ENV_VAR: '111'},
            None
        ),
        ['BrowserStackLocal', '--key', '111']
    ),
    (
        (
            None,
            None,
            {'BrowserStackLocal': {'key': '777'}}
        ),
        ['BrowserStackLocal', '--key', '777']
    ),
    (
        (
            None,
            None,
            {'BrowserStackLocal': {'onlyAutomate': True}}
        ),
        ['BrowserStackLocal', '--only-automate']
    ),
    (
        (
            None,
            {BROWSERSTACK_ACCESS_KEY_ENV_VAR: '2'},
            {'BrowserStackLocal': {'key': '1'}}
        ),
        ['BrowserStackLocal', '--key', '2']
    ),
    (
        (
            {'browserstack_local_arguments': ['key=3']},
            {BROWSERSTACK_ACCESS_KEY_ENV_VAR: '2'},
            {'BrowserStackLocal': {'key': '1'}}
        ),
        ['BrowserStackLocal', '--key', '3']
    )
], ids=[
    'CLI args',
    'env var',
    'config',
    'config, bool arg',
    'config, env var',
    'config, env var, CLI args'
])
def test_parse_config(fake_config, input_data, expected_output):
    input_args, input_env_vars, input_config = input_data
    assert parse_config(fake_config(
        input_args, input_env_vars, input_config
    )) == expected_output
