import pytest


from pytest_mock import mocker
from src.generate_tables import (
    delete_trades_table,
    generate_trades_table,
    generate_trader_table,
    delete_trader_table,
)
 

def test_delete(mocker):
    execute = mocker.patch("src.generate_tables.execute_statement")
    delete_trades_table()
    execute.assert_called_with("DROP TABLE trades")
    delete_trader_table()
    execute.assert_called_with("DROP TABLE traders")


def test_generate_trades(mocker):
    table_string = """CREATE TABLE trades (
        trade_id int NOT NULL IDENTITY(1,1),
        currency_pair varchar(6),
        amount float,
        price float,
        trade_date DATETIME,
        trader_id int,
        CONSTRAINT PK_trades PRIMARY KEY (trade_id),
        CONSTRAINT FK_trade_id FOREIGN KEY (trader_id) REFERENCES traders(trader_id)
        );
    """
    execute = mocker.patch("src.generate_tables.execute_statement")
    generate_trades_table()
    execute.assert_called_with(table_string)


def test_generate_traders(mocker):
    table_string = """CREATE TABLE traders (
        name varchar(50) UNIQUE,
        trader_id int NOT NULL IDENTITY(1,1),
        CONSTRAINT PK_trader PRIMARY KEY (trader_id)
        );
    """
    execute = mocker.patch("src.generate_tables.execute_statement")
    generate_trader_table()
    execute.assert_called_with(table_string)
