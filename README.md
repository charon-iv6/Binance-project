# Binance-Trade-Project
Binance Futures Terminal-Trade(API) &amp; Binance

------------------------------------------------------------------------------------------------------------------------

**Install Requirements:** ```pip install flask request jsonify mysql-connector-python```

**Config: Edit `config.json` file --- `mudle_TrV2.py --> TESTNET` - DATABASE HOST & USER & PASS & NAME**
```
V2 Changes:
    1. The Project Is Now More Professional In Terms Of Classes And Objects...
    2. It Prevents SQLi Attack In The Parameters.
    3. More Orderly & More Simple.
```



**USAGE:** 
----------
   1. First Insert MYSQL Backup File Inside Your MYSQL (Create a DB named terminaltrade Then Insert Backup File).

   **For Every User We have a Specific Token Inside users Table(Inside DB), Script Query The DB and Ask For APIKEY & SECERETKEY of The USER.**
      
   2. `python3 TrV1.py`

Open Order: IP:PORT/open
--------------------------------
```
{
     "token":"USER'S TOKEN IN DB: str",
     "pair":"BTCUSDT",
     "type":"market - limit",
     "side":"buy - sell",
     "price":"None - float number",
     "amount":((USDT / CoinPrice) * leverage): float,
     "leverage":Leverage To Save In DB: int,
     "margin":"crossed - isolated"
}
```


Closing Order: IP:PORT/close
----------------------------------
```
{
     "token":"USER'S TOKEN IN DB: str",
     "pair":"BTCUSDT",
     "amount":"Opened Order Amount: str",
     "side":"buy - sell"
}
```
Account Balance: IP:PORT/balance
----------------------------------
```
{
     "token":"USER'S TOKEN IN DB: str"
}
```

Account Open Positions: IP:PORT/positions
-----------------------------------
```
{
    
     "token":"USER'S TOKEN IN DB: str"
    
}
```

**TODO**
- [x] Fixed Some Minor Problem
- [ ] Create FRONTEND Panel
