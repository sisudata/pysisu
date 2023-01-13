from unittest import mock

import pytest
from pysisu import PySisu


@mock.patch("pysisu.pysisu_class.PYSISU_VERSION", "1.1.0")
@mock.patch("requests.Response.json", lambda x: {"info": {"version": "2.0.0"}})
def test_major_version_exception():
    with pytest.raises(Exception, match="breaking changes"):
        PySisu("test")


@mock.patch("pysisu.pysisu_class.PYSISU_VERSION", "0.1.0")
@mock.patch("requests.Response.json", lambda x: {"info": {"version": "0.2.0"}})
def test_experimental_minor_version_exception():
    with pytest.raises(Exception, match="breaking changes"):
        PySisu("test")


@mock.patch("pysisu.pysisu_class.PYSISU_VERSION", "1.2.3")
@mock.patch("requests.Response.json", lambda x: {"info": {"version": "1.3.0"}})
def test_minor_version_warning():
    with pytest.warns(UserWarning, match="Pysisu has been updated from"):
        PySisu("test")


@mock.patch("requests.Response.json", lambda x: {})
def test_pypi_failure_warning():
    with pytest.warns(UserWarning, match="Unable to verify"):
        PySisu("test")


@mock.patch("pysisu.pysisu_class.PYSISU_VERSION", "0.0.0")
def test_compatibility_check_skipped_in_pytest(pysisu_client):
    with pytest.raises(Exception, match="breaking changes"):
        PySisu("test")

    # mocked fixture compatibility check will not raise an Exception
    assert pysisu_client
