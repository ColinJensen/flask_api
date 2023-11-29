from functions import execute_statement


def delete_trades_table():
    "Drops table: trades. trader table must not exist or FK constraint violated."
    if execute_statement("DROP TABLE trades"):
        print("deleted table")


def generate_trades_table():
    "creates trades table. trades PK: trade_id traders FK: trader_id. Constains trade data"
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

    if execute_statement(table_string):
        print("created trades table")
    else:
        print("Could not create trades table (see above error message)")


def delete_trader_table():
    "drops table: trader"
    if execute_statement("DROP TABLE traders"):
        print("deleted table")


def generate_trader_table():
    "Creates trader table. PK: trader_id (auto_increments). Contains unique name."
    table_string = """CREATE TABLE traders (
        name varchar(50) UNIQUE,
        trader_id int NOT NULL IDENTITY(1,1),
        CONSTRAINT PK_trader PRIMARY KEY (trader_id)
        );
    """
    if execute_statement(table_string):
        print("created trader table")
    else:
        print("Could not create trader table (see above error message)")


if __name__ == "__main__":
    delete_trades_table()  # must be first cause FK constraint
    delete_trader_table()
    generate_trader_table()
    generate_trades_table()
    execute_statement("EXEC InsertTraders")
    execute_statement("EXEC InsertTrades")
