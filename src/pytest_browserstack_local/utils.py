import os
import re


BROWSERSTACK_ACCESS_KEY_ENV_VAR = 'BROWSERSTACK_ACCESS_KEY'


def convert_camelcase(s):
    """
    Convert:

    - 'ABC' -> 'abc'
    - 'abcDef' -> 'abc-def'
    - 'abcXDef' -> 'abc-x-def'

    Credits to https://stackoverflow.com/questions/1175208

    :param str s:
    :rtype: str
    """
    s = re.sub('(.)([A-Z][a-z]+)', r'\1-\2', s)
    return re.sub('([a-z0-9])([A-Z])', r'\1-\2', s).lower()


def convert_to_arg(s):
    """
    Convert:

    - 'x' -> '-x'
    - '-x' -> '-x'
    - '--x' -> '-x'
    - 'abc' -> '--abc'
    - '-abc' -> '--abc'
    - 'abc-def' -> '--abc-def'
    - 'abcDef' -> '--abc-def'
    - '--abc-def' -> '--abc-def'
    - '--abcDef' -> '--abc-def'

    :param str s:
    :rtype: str
    """
    s = re.sub(r'^-+', '', s)

    if len(s) == 1:
        return '-{}'.format(s)
    else:
        return '--{}'.format(convert_camelcase(s))


def parse_config(config):
    """
    Parse BrowserStackLocal configuration (user input) into command-line arguments.

    :param config: pytest config instance
    :rtype: list[str]
    """
    browserstack_local_path = config.getoption('browserstack_local_path')
    browserstack_local_cmd = [browserstack_local_path]
    browserstack_local_config = {}

    # Integration with ``pytest-variables``
    for key, value in config._variables.get('BrowserStackLocal', {}).items():
        # ``False`` value is skipped as there was no such argument.
        if value is False:
            continue

        # Both ``True`` and ``None`` values are used for "flag" arguments (i.e. no value).
        if value is True:
            value = None

        browserstack_local_config[convert_to_arg(key)] = value

    if BROWSERSTACK_ACCESS_KEY_ENV_VAR in os.environ:
        browserstack_local_config['--key'] = os.getenv(BROWSERSTACK_ACCESS_KEY_ENV_VAR)

    # CLI arguments override ``pytest-variables``.
    for kv in config.getoption('browserstack_local_arguments'):
        key, value = kv.split('=', 1) if '=' in kv else (kv, None)
        browserstack_local_config[convert_to_arg(key)] = value

    for key, value in browserstack_local_config.items():
        browserstack_local_cmd.append(key)

        if value is not None:
            browserstack_local_cmd.append(str(value))

    return browserstack_local_cmd
