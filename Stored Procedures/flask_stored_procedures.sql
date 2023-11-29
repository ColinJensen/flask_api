--This creates/alters all storage prodecures

--Inserts data from trader_names csv into traders
ALTER PROCEDURE InsertTraders
AS 
BULK INSERT TraderInsert FROM 'C:\Users\Colin\Desktop\code\flask_api\traderNames.csv' 
WITH (FIRSTROW = 2,FIELDTERMINATOR = ',', ROWTERMINATOR = '0x0a');

UPDATE traders set name = Trim(replace(name,char(13),''))

GO

--insert trade data from csv into temp table, removes weird spacing, then gets trader ID from trader table
--Finally, insert data into trades table
ALTER PROCEDURE InsertTrades
AS
DROP TABLE TradesWithoutKeys

CREATE TABLE TradesWithoutKeys (
        currency_pair varchar(6),
        amount float,
        price float,
        trade_date varchar(30),
        trader_name varchar(50),
        )
		

BULK INSERT TradesWithoutKeys FROM 'C:\Users\Colin\Desktop\code\flask_api\trades.csv' 
WITH (FIRSTROW = 2,FIELDTERMINATOR = ',', ROWTERMINATOR = '0x0a');


UPDATE TradesWithoutKeys set trader_name = Trim(replace(trader_name,char(13),'')) --needed to clear whitespace


--add seconds for time
UPDATE TradesWithoutKeys set trade_date = CONCAT(trade_date,':00')

INSERT INTO trades
SELECT A.currency_pair, A.amount, A.price, CONVERT(datetime,A.trade_date,1), B.trader_id
FROM TradesWithoutKeys As A
LEFT JOIN traders As B on TRIM(A.trader_name) = replace(B.name,char(13),'') --other table contains linux chars as well
GO 

--Get trader with specified ID
ALTER PROCEDURE GetTrader @TraderNameParam varchar(50)
AS
SELECT * 
FROM traders
WHERE name = @TraderNameParam
FOR JSON PATH
GO

--get trader with specified ID
--for validation of IDS
ALTER PROCEDURE GetTraderFromID @TraderIdParam Int
AS
SELECT * 
FROM traders
WHERE trader_id = @TraderIdParam
FOR JSON PATH
GO

--get trade with specified ID
ALTER PROCEDURE GetTradeFromID @TradeIdParam Int
AS
SELECT * 
FROM trades
WHERE trade_id = @TradeIdParam
FOR JSON PATH
GO

--Get all trades from trader with ID
ALTER PROCEDURE GetTradeFromTrader @TraderIdParam Int
AS
SELECT * 
FROM trades
WHERE trader_id = @TraderIdParam
FOR JSON PATH
GO


--Insert a row into trader
ALTER PROCEDURE InsertIntoTrader @NameParam varchar(50)
AS
INSERT INTO traders VALUES(@NameParam)
GO

--Insert a row into trade
ALTER PROCEDURE InsertIntoTrade 
        @currency_pair varchar(6),
        @amount float,
        @price float,
        @trade_date DATETIME,
        @trader_id int
AS
INSERT INTO trades VALUES(@currency_pair, @amount, @price, @trade_date, @trader_id)
