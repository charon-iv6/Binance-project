import datetime
# import decimal
import hashlib
import hmac
from urllib.parse import urlencode
import mysql.connector
import requests
### Exceptions ###
from exceptions import *

### Receive Basic Info ###
api_exchangeInfo = "https://fapi.binance.com/fapi/v1/exchangeInfo"
exchangeInfo = requests.get(url=api_exchangeInfo).json()

### APIs ###
TESTNET = True
# ================= API-BASE(DO NOT CHANGE) ================= #
if not TESTNET:
    BASE = "https://fapi.binance.com/"
else:
    BASE = "https://testnet.binancefuture.com/"
API_INFO = BASE + "fapi/v1/exchangeInfo"
API_PRICE = BASE + "fapi/v1/ticker/price"
API_LEVERAGE = BASE + "fapi/v1/leverage"
API_MARGIN = BASE + "fapi/v1/marginType"
API_ORDER = BASE + "fapi/v1/order"
API_POSITIONS = BASE + "fapi/v2/positionRisk"
API_BALANCE = BASE + "fapi/v2/balance"
# ================= CONFIGS ================= #
RECV_WINDOW: int = 5000

# ================= DATABASE(CONFIG) ================= #
DB_HOST = "localhost"
DB_USER = "root"
DB_PASS = ""
DB_NAME = "terminaltrade"


def DB_CONNECTOR():
    mydb: mysql = mysql.connector.connect(
        host=DB_HOST,
        user=DB_USER,
        password=DB_PASS,
        database=DB_NAME
    )
    return mydb


class ORDERS:
    def __init__(self, TOKEN:str, PAIR:str, TYPE:str, SIDE:str, AMOUNT=None, PRICE=None, MARGIN=None,
                 LEVERAGE=None):
        self.TOKEN: str = TOKEN
        self.APIKEY: str = ""
        self.SECRETKEY: str = ""
        ### Check Functions ###
        self.AK_SK_Validator()
        # ================= TESTNET(OPTIONAL) ================= #
        self.TESTNET_APIKEY: str = ""
        self.TESTNET_SECRETKEY: str = ""
        # ================= ORDER-DETAILS(DON'T TOUCH) ================= #
        self.TYPE: str = TYPE
        self.PAIR: str = PAIR
        self.SIDE: str = SIDE
        self.AMOUNT: float = AMOUNT
        if PRICE is not None:
            self.PRICE: float = PRICE
        self.TIMEIN: str = "GTC"
        if MARGIN is not None:
            self.MARGIN: str = MARGIN
        if LEVERAGE is not None:
            if LEVERAGE > 125:
                raise Leverage_Wrong
            elif 1 > LEVERAGE:
                raise Leverage_Wrong
        self.LEVERAGE: int = LEVERAGE

    """def TokenChecker(self):
        mydb = DB_CONNECTOR()
        mycursor = mydb.cursor()
        mycursor.execute("SELECT token FROM users WHERE token=%s", (self.TOKEN,))
        try:
            mycursor.fetchall()[0]
        except IndexError:
            raise Token_Wrong"""

    def symbol_price(self):
        URL = BASE + "/fapi/v1/ticker/price"
        req = requests.get(URL).json()
        for i in req:
            if i['symbol'] == self.PAIR:
                price = i['price']
                return price

    def GET_KEYS(self, key):
        mydb = DB_CONNECTOR()
        mycursor = mydb.cursor()
        if key.upper() == "API":
            mycursor.execute(f"SELECT apikey FROM users WHERE token=%s", (self.TOKEN,))
        elif key.upper() == "SECRET":
            mycursor.execute(f"SELECT secretkey FROM users WHERE token=%s", (self.TOKEN,))
        else:
            raise INTERNAL_WrongKey
        try:
            apikey = mycursor.fetchall()[0][0]
        except:
            raise AK_SK_Database
        return apikey

    def AK_SK_Validator(self):
        apikey:str = self.GET_KEYS("API")
        secret:str = self.GET_KEYS("SECRET")
        ts:int = int(datetime.datetime.now().timestamp() * 1000)
        header = {"X-MBX-APIKEY": apikey}
        params = {
            'recvWindow': 5000,
            'timestamp': ts
        }
        query_string = urlencode(params)
        params['signature'] = hmac.new(secret.encode('utf-8'), query_string.encode('utf-8'), hashlib.sha256).hexdigest()
        r = requests.get(url=API_BALANCE, headers=header, params=params).json()
        if 'code' in r:
            raise AK_SK_Invalid
        else:
            self.APIKEY = apikey
            self.SECRETKEY = secret

    def Validate_leverage(self):
        # Validate Leverage for Pair
        apikey: str = self.APIKEY
        secret: str = self.SECRETKEY
        ts: int = int(datetime.datetime.now().timestamp() * 1000)
        header = {"X-MBX-APIKEY": apikey}
        URL = API_LEVERAGE
        params = {
            'symbol': self.PAIR,
            'leverage': self.LEVERAGE,
            'timestamp': ts
        }
        query_string = urlencode(params)
        params['signature'] = hmac.new(secret.encode('utf-8'), query_string.encode('utf-8'), hashlib.sha256).hexdigest()
        r = requests.post(url=URL, headers=header, params=params)
        if "symbol" in r.json():
            return "yes"
        elif r.json()['code'] == -4028:
            raise Leverage_Wrong
        elif r.json()['code'] == -4161:
            raise Leverage_Rediction_NotSupported
        else:
            print(r.json())
            raise Leverage_Unknown_Error

    def change_Margin(self):
        apikey: str = self.APIKEY
        secret: str = self.SECRETKEY
        if self.MARGIN == "ISOLATED" or self.MARGIN == "CROSSED":
            ts = int(datetime.datetime.now().timestamp() * 1000)
            header = {"X-MBX-APIKEY": apikey}
            URL = API_MARGIN
            params = {
                'symbol': self.PAIR,
                'marginType': self.MARGIN,
                'timestamp': ts
            }
            query_string = urlencode(params)
            params['signature'] = hmac.new(secret.encode('utf-8'), query_string.encode('utf-8'),
                                           hashlib.sha256).hexdigest()
            r = requests.post(url=URL, headers=header, params=params)
            print(r.json()['code'])
            print(f"---- {r.json()} ----")
            if r.json()['code'] == -4047:
                raise Margin_Couldnt_Change
            else:
                return r.json()
        else:
            raise Margin_Wrong

    def ORDER(self):
        apikey: str = self.APIKEY
        secret: str = self.SECRETKEY
        ts: int = int(datetime.datetime.now().timestamp() * 1000)
        header = {"X-MBX-APIKEY": apikey}
        amount: str = Precision_amount(self.PAIR, self.AMOUNT)
        if self.TYPE == "MARKET":
            params = {
                'symbol': self.PAIR,
                'side': self.SIDE,
                'type': 'MARKET',
                'quantity': amount,
                'recvWindow': RECV_WINDOW,
                'timestamp': ts
            }
        elif self.TYPE == "LIMIT":
            price = Precision_price(symbol=self.PAIR, price=self.PRICE)
            params = {
                'symbol': self.PAIR,
                'side': self.SIDE,
                'type': 'LIMIT',
                'quantity': amount,
                'price': price,
                'timeInForce': self.TIMEIN,
                'recvWindow': RECV_WINDOW,
                'timestamp': ts
            }
        else:
            raise

        query_string = urlencode(params)
        params['signature'] = hmac.new(secret.encode('utf-8'), query_string.encode('utf-8'), hashlib.sha256).hexdigest()
        r = requests.post(url=API_ORDER, headers=header, params=params)
        if "orderId" in r.json():
            return r.json()
        elif r.json()['code'] == -2019:
            raise MARKET_Margin_Insufficient
        elif r.json()['code'] == -4061:
            raise Market_Not_OneWayMode
        elif r.json()['code'] == -4003:
            raise Market_Amount_InSufficient
        else:
            raise Market_Error

    def close_Order(self):
        apikey:str = self.APIKEY
        secret:str = self.SECRETKEY
        ts:int = int(datetime.datetime.now().timestamp() * 1000)
        header = {"X-MBX-APIKEY": apikey}
        amount = Precision_amount(self.PAIR, self.AMOUNT)
        if self.SIDE == "BUY":
            side = "SELL"
        elif self.SIDE == "SELL":
            side = "BUY"
        else:
            raise
        params = {
            'symbol': self.PAIR,
            'side': side,
            'type': 'MARKET',
            'quantity': amount,
            'recvWindow': 5000,
            'timestamp': ts
        }
        query_string = urlencode(params)
        params['signature'] = hmac.new(secret.encode('utf-8'), query_string.encode('utf-8'), hashlib.sha256).hexdigest()
        r = requests.post(url=API_ORDER, headers=header, params=params)
        if "orderId" in r.json():
            return r.json()
        else:
            raise Close_Error

    def submit_Order(self):
        mydb = DB_CONNECTOR()
        mycursor = mydb.cursor()
        now = datetime.datetime.now()
        trdate = now.strftime("%Y-%m-%d %H:%M:%S")
        Price = self.symbol_price()
        sql = "INSERT INTO terminal_logs (token, pair, type, side, price, amount, leverage, margin, date) VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s)"
        val = (self.TOKEN, self.PAIR, self.TYPE, self.SIDE, Price, self.AMOUNT, str(self.LEVERAGE), self.MARGIN, trdate)
        try:
            mycursor.execute(sql, val)
        except Exception as e:
            print(e)
        mydb.commit()


class Account:
    def __init__(self, TOKEN):
        self.TOKEN: str = TOKEN
        self.APIKEY = ""
        self.SECRETKEY = ""
        ### Check Functions ###
        self.AK_SK_Validator()
        # ================= TESTNET(OPTIONAL) ================= #
        self.TESTNET_APIKEY = ""
        self.TESTNET_SECRETKEY = ""

    def GET_KEYS(self, key):
        mydb = DB_CONNECTOR()
        mycursor = mydb.cursor()
        if key.upper() == "API":
            mycursor.execute(f"SELECT apikey FROM users WHERE token=%s", (self.TOKEN,))
        elif key.upper() == "SECRET":
            mycursor.execute(f"SELECT secretkey FROM users WHERE token=%s", (self.TOKEN,))
        else:
            raise INTERNAL_WrongKey
        try:
            apikey = mycursor.fetchall()[0][0]
        except:
            raise AK_SK_Database
        return apikey

    def AK_SK_Validator(self):
        apikey = self.GET_KEYS("API")
        secret = self.GET_KEYS("SECRET")
        ts = int(datetime.datetime.now().timestamp() * 1000)
        header = {"X-MBX-APIKEY": apikey}
        base = API_BALANCE
        params = {
            'recvWindow': 5000,
            'timestamp': ts
        }
        query_string = urlencode(params)
        params['signature'] = hmac.new(secret.encode('utf-8'), query_string.encode('utf-8'),
                                       hashlib.sha256).hexdigest()
        r = requests.get(url=base, headers=header, params=params).json()
        if 'code' in r:
            raise AK_SK_Invalid
        else:
            self.APIKEY = apikey
            self.SECRETKEY = secret

    def open_Positions(self):
        apikey = self.APIKEY
        secret = self.SECRETKEY
        ts = int(datetime.datetime.now().timestamp() * 1000)
        header = {"X-MBX-APIKEY": apikey}
        base = API_POSITIONS
        params = {
            'recvWindow': RECV_WINDOW,
            'timestamp': ts
        }
        query_string = urlencode(params)
        params['signature'] = hmac.new(secret.encode('utf-8'), query_string.encode('utf-8'),
                                       hashlib.sha256).hexdigest()
        r = requests.get(url=base, headers=header, params=params).json()
        if 'code' in r:
            raise AK_SK_Invalid
        else:
            total = []
            for i in r:
                if i['notional'] != '0':
                    total.append(i)
            for bb in total:
                entryPrice = float(bb['entryPrice'])
                markPrice = float(bb['markPrice'])
                unRealizedProfit = float(bb['unRealizedProfit'])
                if markPrice > entryPrice and unRealizedProfit > 0:
                    bb['side'] = 'LONG'
                elif markPrice < entryPrice and unRealizedProfit < 0:
                    bb['side'] = 'LONG'
                elif markPrice < entryPrice and unRealizedProfit > 0:
                    bb['side'] = 'SHORT'
                elif markPrice > entryPrice and unRealizedProfit < 0:
                    bb['side'] = 'SHORT'
            return total

    def get_Balance(self):
        apikey: str = self.APIKEY
        secret: str = self.SECRETKEY
        ts: int = int(datetime.datetime.now().timestamp() * 1000)
        header = {"X-MBX-APIKEY": apikey}
        params = {
            'recvWindow': RECV_WINDOW,
            'timestamp': ts
        }
        query_string = urlencode(params)
        params['signature'] = hmac.new(secret.encode('utf-8'), query_string.encode('utf-8'), hashlib.sha256).hexdigest()
        r = requests.get(url=API_BALANCE, headers=header, params=params).json()
        # print(r)
        if 'code' in r:
            raise AK_SK_Invalid
        else:
            for balance in r:
                if balance["asset"] == "USDT":
                    B = balance["availableBalance"]
                    B = float("{:.2f}".format(float(B)))
                    return B


'''def percentage(percent, number):
    return (percent * number) / 100.0'''


def get_Precision_amount(symbol: str, method: str):
    symbols = exchangeInfo['symbols']
    for coins in symbols:
        if coins["symbol"] == symbol:
            quantityPrecision = coins["quantityPrecision"]
            PricePrecision = coins["pricePrecision"]
            if method == "amount":
                return quantityPrecision
            elif method == "price":
                return PricePrecision


def Precision_amount(symbol: str, amount: float):
    QuantityPrecision = "{:." + str(get_Precision_amount(symbol=symbol, method="amount")) + "f" + "}"
    F_Amount = QuantityPrecision.format(amount)
    # Return str
    return F_Amount


def Precision_price(symbol: str, price: float):
    QuantityPrecision = "{:." + str(get_Precision_amount(symbol=symbol, method="price")) + "f" + "}"
    F_Price = QuantityPrecision.format(price)
    # Return str
    return F_Price
