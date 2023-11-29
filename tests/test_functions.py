import pytest
from pytest_mock import mocker
from src.functions import execute_statement


def test_execute_query(mocker):
    conn = mocker.patch(
        "src.functions.pyodbc.connect"
    )  # remove actual call to database
    assert execute_statement("")  # runs correctly
