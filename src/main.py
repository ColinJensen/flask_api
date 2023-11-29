#Author: Colin Jensen
#Desc: Flask server with api for accessing trade data

from flask import Flask
from functions import select_statement, execute_statement


app = Flask(__name__)


@app.route("/")
def home():
    return select_statement("SELECT * FROM traders FOR JSON PATH")


# insert new trader
@app.route("/newtrader/<name>")
def insert_trader(name):
    "API call for inserting a trader into database"
    try:
        execute_statement(f"EXEC InsertIntoTrader '{name}'")
        return select_statement(
            f"EXEC GetTrader '{name}'"
        )  # shows newly created data. uses stored procedure
        # to avoid SQL injection
    except:
        return f"Error with insert statement. Invalid name {name}. Username may already exist"


@app.route("/gettrader/<name>")
def get_trader(name):
    "API call for a trader from the trader's unique name"
    try:
        return select_statement(f"EXEC GetTrader '{name}'")  
    # shows newly created data. uses stored procedure
        # to avoid SQL injection
    except:
        return f"Error with statement. Invalid name input {name}"


@app.route("/newtrade/<pair>/<amount>/<price>/<date>/<id>")
def insert_trade(pair, amount, price, date, id):
    if pair not in ["USDCHF", "GBPUSD", "EURUSD"]:
        return f'Invalid pair {pair}. Must be "USDCHF","GBPUSD","EURUSD"'
    try:
        float(amount)
    except:
        return f"Invalid amount {amount}. Must be a float"
    try:
        float(price)
    except:
        return f"Invalid price {price}. Must be a float"
    try:
        select_statement(f"EXEC GetTraderFromID '{id}'")
    except:
        return "Invalid ID. Please verify user exists"
    if execute_statement(
        f"EXEC InsertIntoTrade '{pair}', '{amount}', '{price}', '{date}', '{id}'"
    ):
        return "Success"
    else:
        return "Error with trade. Please check date is in format yyyymmdd HH:MM:SS"

@app.route("/gettrade/<id>")
def get_trade(id):
    try:
        return select_statement(f"EXEC GetTradeFromID '{id}'")
    except:
        return f"Error with statement. Invalid id {id}"

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=8000, debug=True)
