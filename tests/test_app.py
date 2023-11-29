import pytest
from pytest_mock import mocker
from src.main import *
 


def test_home(mocker):
    "Test home page"
    select = mocker.patch("src.main.select_statement")  # mock out function call
    select.return_value = "RETURNED HOME"
    assert home() == "RETURNED HOME"
    select.assert_called_with("SELECT * FROM traders FOR JSON PATH")


def test_insert(mocker):
    "Test insert trader page. Mock out calls to run stored procedures then check to make sure stored procedures called"
    select = mocker.patch("src.main.select_statement")  # mock calls to DB
    execute = mocker.patch("src.main.execute_statement")
    select.return_value = "RETURNED INS"  # we will check the function returns this
    name = "Test_Name"
    assert insert_trader(name) == "RETURNED INS"  # check returning select statement
    execute.assert_called_with = (
        f"EXEC InsertIntoTrader '{name}'"  # make sure insert is called
    )
    select.assert_called_with(f"EXEC GetTrader '{name}'")  # function returns this call
    # Test if exception occurs
    execute.side_effect = Exception("mocked error")
    assert (
        insert_trader(name)
        == f"Error with insert statement. Invalid name {name}. Username may already exist"
    )

def test_get_trades(mocker):
    "Test get trader. just a select statement"
    select = mocker.patch("src.main.select_statement") 
    select.return_value = "RETURNED GET_TRADE"
    id = 47
    assert get_trade(id) == "RETURNED GET_TRADE"
    select.assert_called_with(f"EXEC GetTradeFromID '{id}'")
    #test error
    select.side_effect = Exception("mocked error")
    assert (
        get_trade(id)
        == f"Error with statement. Invalid id {id}"
    )

def test_get_trader(mocker):
    "Test get trader. just a select statement. Similar to get trades"
    select = mocker.patch("src.main.select_statement") 
    select.return_value = "RETURNED GET_TRADER"
    name = "test_name"
    assert get_trader(name) == "RETURNED GET_TRADER"
    select.assert_called_with(f"EXEC GetTrader '{name}'")
    #test error
    select.side_effect = Exception("mocked error")
    assert (
        get_trader(name)
        == f"Error with statement. Invalid name input {name}"
    )


def test_insert_trade_happy(mocker):
    "Happy path for insert trade. Assume every value is valid"
    select = mocker.patch("src.main.select_statement")  
    execute = mocker.patch("src.main.execute_statement")
    assert insert_trade('USDCHF', '100', '1', '20231118 5:14:23', 5) == "Success"

def test_insert_trade_invalid_pair(mocker):
    "Trade with an invalid pair will return a message saying so"
    #these mocks arent needed but we dont want a mistake to mess with live
    select = mocker.patch("src.main.select_statement")  
    execute = mocker.patch("src.main.execute_statement")
    assert insert_trade('5', '100', '1', '20231118 5:14:23', 5) == 'Invalid pair 5. Must be "USDCHF","GBPUSD","EURUSD"'

def test_invalid_amount_and_price(mocker):
    "Price and amount are both floats. This tests if both are incorrect"
    select = mocker.patch("src.main.select_statement")  
    execute = mocker.patch("src.main.execute_statement")
    assert insert_trade('USDCHF', 'a', '1', '20231118 5:14:23', 5) == "Invalid amount a. Must be a float"
    assert insert_trade('USDCHF', '100', 'b', '20231118 5:14:23', 5) == "Invalid price b. Must be a float"

def test_invalid_id(mocker):
    select = mocker.patch("src.main.select_statement")  
    select.side_effect = Exception("Invalid Index")
    #if no data is found,
    execute = mocker.patch("src.main.execute_statement")

def test_invalid_date(mocker):
    select = mocker.patch("src.main.select_statement")  
    execute = mocker.patch("src.main.execute_statement")
    execute.return_value = False
    #If statement is invalid, excecute statement returns false
    assert insert_trade('USDCHF', '100', '1', '20231118 5:14:23', 5) == "Error with trade. Please check date is in format yyyymmdd HH:MM:SS"
