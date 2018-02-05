import pytest


@pytest.mark.sensitive
def test_remote(httpserver, selenium):
    httpserver.serve_content('<h1>Hello, World!</h1>')
    selenium.get(httpserver.url)
    heading = selenium.find_element_by_tag_name('h1')

    assert heading
    assert heading.text == "Hello, World!"


@pytest.mark.sensitive
def test_process(browserstack_local):
    print(browserstack_local)
    assert browserstack_local['process'] or browserstack_local['daemon']
