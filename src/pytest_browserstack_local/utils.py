import re


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

    for kv in config.getoption('browserstack_local_arguments'):
        if '=' in kv:
            key, value = kv.split('=', 1)
            browserstack_local_cmd.append(convert_to_arg(key))
            browserstack_local_cmd.append(value)
        else:
            browserstack_local_cmd.append(convert_to_arg(kv))

    return browserstack_local_cmd
