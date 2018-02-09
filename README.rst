pytest-browserstack-local |travis-ci|
=====================================

.. |travis-ci| image:: https://travis-ci.org/kottenator/pytest-browserstack-local.svg?branch=develop
               :target: https://travis-ci.org/kottenator/pytest-browserstack-local

.. raw:: html

    <img src="https://user-images.githubusercontent.com/371674/36011905-7c6e2530-0d28-11e8-9fe7-b4613c1ea942.png" height="100px">

``py.test`` plugin to run ``BrowserStackLocal`` in background during the test session.

Install
-------

.. code-block :: bash

    pip install pytest-browserstack-local

Use
---

Let's assume you're using ``pytest-selenium`` with ``pytest-django``.

It's a good example because Django runs so-called ``LiveServer`` of your app on ``localhost``
for test purposes and that's a perfect reason why we need ``BrowserStackLocal``.

But it can be *anything else* which runs your app on ``localhost``.

Also let's assume that you have downloaded `BrowserStackLocal
<https://www.browserstack.com/automate/python#setting-local-tunnel>`_ and it's on your
*system path* now (though there is an option to provide explicit path to the binary).

.. code-block :: python

    # tests/test_home_page.py

    def test_home_page_title(selenium, live_server):
        selenium.get(live_server.url)
        assert selenium.title == "Home page - My Django Project"

Now run your tests in BrowserStack:

.. code-block :: bash

    export BROWSERSTACK_USERNAME="<secret-name>"   # used by ``pytest-selenium``
    export BROWSERSTACK_ACCESS_KEY="<secret-key>"  # used by ``pytest-selenium``
                                                   # and by ``pytest-browserstack-local``
    py.test tests/test_home_page.py \
        --driver BrowserStack \
        --capability os Windows \
        --capability os_version 10 \
        --capability browser IE \
        --capability browserstack.local True \
        --browserstack-local

Note: there are two cases how you can run ``BrowserStackLocal`` - as a foreground process
and as a daemon process. ``pytest-browserstack-local`` supports both but it's better to
use the latter one (because in the first case we're scanning the process output for a
specific text, which is a bit "hacky"):

.. code-block :: bash

    --browserstack-local-argument daemon=start

CLI arguments
-------------

- ``--browserstack-local`` - enable ``pytest-browserstack-local`` plugin.
  Without it - no other argument will take effect.
- ``--browserstack-local-path`` - path to ``BrowserStackLocal`` binary.
  Default: ``BrowserStackLocal`` in *system path*.
- ``--browserstack-local-argument`` - pass an argument for ``BrowserStackLocal`` binary.
  You can specify it multiple times. Pass it in any of the following formats:

  - ``--browserstack-local-argument local-identifier=ABC123``
  - ``--browserstack-local-argument localIdentifier=ABC123``

  And for *boolean arguments* (aka "flags") use one of the following formats:

  - ``--browserstack-local-argument only-automate``
  - ``--browserstack-local-argument onlyAutomate``

  No value must be presented!

  See all the possible arguments in `BrowserStackLocal docs
  <https://www.browserstack.com/local-testing#configuration>`_
  (or just do ``BrowserStackLocal --help``).

Environment variables
---------------------

- ``BROWSERSTACK_ACCESS_KEY`` - access key for your BrowserStack account.

Configuration file
------------------

``pytest-browserstack-local`` plugin is integrated with ``pytest-variables``.

You can put all the ``BrowStackLocal`` arguments into a file
(e.g. ``browserstack-local-config.json``):

.. code-block ::

    {
      "BrowserStackLocal": {
        "key": "XYZ",
        "proxyHost": "localhost",
        "proxyPort": "12345",
        "proxyUser": "admin",
        "proxyPass": "12345",
        "onlyAutomate": true
      }
    }

And then use it in CLI via ``pytest-variables``:

.. code-block :: bash

    py.test --variables browserstack-local-config.json

You can use any of the following formats for *keys* in the config file:

- ``local-identifier``
- ``localIdentifier``

See all the possible arguments in `BrowserStackLocal docs
<https://www.browserstack.com/local-testing#configuration>`_
(or just do ``BrowserStackLocal --help``).

Fixtures
--------

- ``browserstack_local`` - a ``dict`` with the ``BrowserStackLocal`` process info.

  There are two cases:

  - Foreground process (e.g.):

    .. code-block :: python

        {
            'process': subprocess.Popen(...),
            'daemon': None,
            'cmd': ['BrowserStackLocal', '--key', '<secret-key>']
        }

  - Daemon process (e.g.):

    .. code-block :: python

        {
            'process': None,
            'daemon': {
                'state': 'connected',
                'pid': 48213,
                'message': 'Connected'
            },
            'cmd': ['BrowserStackLocal', '--key', '<secret-key>', '--daemon', 'start']
        }

Development
-----------

- Make a fork (if you're not me).
- Checkout the repo.
- Create a virtualenv.
- ``pip install -e '.[test]'``
- Do your changes.
- ``py.test``
- Make a pull-request ;)

I'm always open for great ideas, but even more - for contribution.

Run a real test
~~~~~~~~~~~~~~~

If you want to try it *for real*: download & install `BrowserStackLocal
<https://www.browserstack.com/automate/python#setting-local-tunnel>`_ and then run:

.. code-block:: bash

    export BROWSERSTACK_USERNAME="<secret-name>"
    export BROWSERSTACK_ACCESS_KEY="<secret-key>"

    py.test -m sensitive \
        --driver BrowserStack \
        --capability os Windows \
        --capability os_version 10 \
        --capability browser IE \
        --capability browserstack.local True \
        --browserstack-local \
        --browserstack-local-path ./BrowserStackLocal

This will run a *hidden* Selenium test that runs real ``BrowserStackLocal`` and checks
a ``localhost``-hosted page on BrowserStack.
