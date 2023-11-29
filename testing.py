from src.functions import execute_statement, select_statement
#from src.generate_tables import delete_trader_table

# execute_statement("EXEC InsertIntoTrader 'trader_18' ")
# execute_statement("EXEC InsertIntoTrade 'USDCHF', '1000', '10', '11-25-23 11:11:11', '1'")


print(select_statement("SELECT * FROM traders"))
