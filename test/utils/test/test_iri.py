from __future__ import annotations

import logging
from contextlib import ExitStack
from pathlib import PurePath, PurePosixPath, PureWindowsPath
from typing import Union

import pytest

from test.utils.iri import file_uri_to_path, rebase_url


@pytest.mark.parametrize(
    ["file_uri", "path_class", "expected_result"],
    [
        (
            "file:///example/some%20/thing/",
            PurePosixPath,
            PurePosixPath("/example/some /thing/"),
        ),
        (
            "file:///c:/path/to%20/file",
            PureWindowsPath,
            PureWindowsPath("c:\\path\\to \\file"),
        ),
        (
            "file:c:/path/to%24/file",
            PureWindowsPath,
            PureWindowsPath("c:\\path\\to$\\file"),
        ),
        (
            "file:///C%3A/Users/iwana/d/github.com/iafork/rdflib/test/data/suites/w3c/dawg-data-r2/basic/manifest.ttl",
            PureWindowsPath,
            PureWindowsPath(
                "\\C:\\Users\\iwana\\d\\github.com\\iafork\\rdflib\\test\\data\\suites\\w3c\\dawg-data-r2\\basic\\manifest.ttl"
            ),
        ),
        (
            "file:///C:/Users/iwana/d/github.com/iafork/rdflib/test/data/suites/w3c/dawg-data-r2/basic/manifest.ttl",
            PureWindowsPath,
            PureWindowsPath(
                "C:/Users/iwana/d/github.com/iafork/rdflib/test/data/suites/w3c/dawg-data-r2/basic/manifest.ttl".replace(
                    "/", "\\"
                )
            ),
        ),
    ],
)
def test_file_uri_to_path(
    file_uri: str,
    path_class: type[PurePath],
    expected_result: Union[PurePath, type[Exception]],
) -> None:
    """
    Tests that
    """
    catcher: pytest.ExceptionInfo[Exception] | None = None

    with ExitStack() as xstack:
        if isinstance(expected_result, type) and issubclass(expected_result, Exception):
            catcher = xstack.enter_context(pytest.raises(expected_result))
        result = file_uri_to_path(file_uri, path_class)
        logging.debug("result = %s", result)
    if catcher is not None:
        assert catcher is not None
        assert catcher.value is not None
    else:
        assert isinstance(expected_result, PurePath)
        assert expected_result == result


@pytest.mark.parametrize(
    ["old_url", "old_base", "new_base", "expected_result"],
    [
        (
            "https://example.com/2013/RDFXMLTests/a%20/b.xml?c=1#frag",
            "https://example.com/2013/RDFXMLTests/",
            "file:///example/local/path/",
            "file:///example/local/path/a%20/b.xml?c=1#frag",
        ),
        (
            "file:///example/local/path/a%20/b.xml?c=1#frag",
            "file:///example/local/path/",
            "https://example.com/2013/RDFXMLTests/",
            "https://example.com/2013/RDFXMLTests/a%20/b.xml?c=1#frag",
        ),
        (
            "https://example.com/2013/RDFXMLTests/a%20/b.xml?c=1#frag",
            "https://example.com/2013/RDFXMLTests/",
            "file:///c:/example/local/path/",
            "file:///c:/example/local/path/a%20/b.xml?c=1#frag",
        ),
        (
            "file:///c:/example/local/path/a%20/b.xml?c=1#frag",
            "file:///c:/example/local/path/",
            "https://example.com/2013/RDFXMLTests/",
            "https://example.com/2013/RDFXMLTests/a%20/b.xml?c=1#frag",
        ),
    ],
)
def test_rebase_url(
    old_url: str,
    old_base: str,
    new_base: str,
    expected_result: Union[str, type[Exception]],
) -> None:
    """
    Tests that
    """
    catcher: pytest.ExceptionInfo[Exception] | None = None

    with ExitStack() as xstack:
        if isinstance(expected_result, type) and issubclass(expected_result, Exception):
            catcher = xstack.enter_context(pytest.raises(expected_result))
        result = rebase_url(old_url, old_base, new_base)
        logging.debug("result = %s", result)
    if catcher is not None:
        assert catcher is not None
        assert catcher.value is not None
    else:
        assert isinstance(expected_result, str)
        assert expected_result == result
