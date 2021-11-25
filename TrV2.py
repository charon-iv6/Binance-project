from flask import Flask, request, jsonify
from mudle_TrV2 import *
import json
config = json.loads(open("config.json", "r").read())
app = Flask(__name__)
FORMAT = "utf-8"
# FLASK CONFIG #
SERVER:str = config["HOST"]
PORT:int = config["PORT"]


@app.route('/open', methods=['POST'])
def term():
    Req = None
    try:
        Req = request.get_json()
        print(Req)
    except:
        return jsonify({"Error": -2314})
    if Req['type'].upper() == 'MARKET':
        try:
            Token: str = Req['token']
            Pair: str = Req['pair'].upper()
            Side: str = Req['side'].upper()
            Amount: float = float(Req['amount'])
            Leverage: int = int(Req['leverage'])
            Margin: str = Req['margin'].upper()
        except:
            return jsonify({"Error": -2415})

        try:
            MAIN = ORDERS(TOKEN=Token, PAIR=Pair,
                          TYPE="MARKET", SIDE=Side,
                          AMOUNT=Amount, MARGIN=Margin,
                          LEVERAGE=Leverage)
        except AK_SK_Database:
            return jsonify({"Error": -2543})
        except AK_SK_Invalid:
            return jsonify({"Error": -2543})
        except Leverage_Wrong:
            return jsonify({"Error": -4214})

        try:
            MAIN.Validate_leverage()
        except Leverage_Rediction_NotSupported:
            return jsonify({"Error": -4531})
        except Leverage_Unknown_Error:
            return jsonify({"Error": -4218})

        try:
            MAIN.change_Margin()
        except Margin_Wrong:
            return jsonify({"Error": -5421})
        except Margin_Couldnt_Change:
            return jsonify({"Error": -7424})

        try:
            MAIN.ORDER()
        except Market_Error:
            return jsonify({"Error": -6431})
        except MARKET_Margin_Insufficient:
            return jsonify({"Error": -2643})
        except Market_Not_OneWayMode:
            return jsonify({"Error": -2676})
        except Market_Amount_InSufficient:
            return jsonify({"Error": -6753})

        try:
            MAIN.submit_Order()
            return jsonify({"Success": "True"})
        except:
            return jsonify({"Error": -7532})

    elif Req['type'].upper() == 'MARKET':
        try:
            Token: str = Req['token']
            Pair: str = Req['pair'].upper()
            Side: str = Req['side'].upper()
            Amount: float = float(Req['amount'])
            Leverage: int = int(Req['leverage'])
            Margin: str = Req['margin'].upper()
            Price: float = float(Req['price'])
        except:
            return jsonify({"Error": -2415})

        try:
            MAIN = ORDERS(TOKEN=Token, PAIR=Pair,
                          TYPE="MARKET", SIDE=Side,
                          AMOUNT=Amount, MARGIN=Margin,
                          LEVERAGE=Leverage)
        except AK_SK_Database:
            return jsonify({"Error": -2543})
        except AK_SK_Invalid:
            return jsonify({"Error": -2543})
        except Leverage_Wrong:
            return jsonify({"Error": -4214})

        try:
            MAIN.Validate_leverage()
        except Leverage_Rediction_NotSupported:
            return jsonify({"Error": -4531})
        except Leverage_Unknown_Error:
            return jsonify({"Error": -4218})

        try:
            MAIN.change_Margin()
        except Margin_Wrong:
            return jsonify({"Error": -5421})
        except Margin_Couldnt_Change:
            return jsonify({"Error": -7424})

        try:
            MAIN.ORDER()
        except Market_Error:
            return jsonify({"Error": -6431})
        except MARKET_Margin_Insufficient:
            return jsonify({"Error": -2643})
        except Market_Not_OneWayMode:
            return jsonify({"Error": -2676})
        except Market_Amount_InSufficient:
            return jsonify({"Error": -6753})

        try:
            MAIN.submit_Order()
            return jsonify({"Success": "True"})
        except:
            return jsonify({"Error": -7532})
    else:
        return jsonify({"Error": -8213})


@app.route('/balance', methods=['POST'])
def Balance():
    try:
        Req = request.get_json()
        print(Req)
    except:
        return jsonify({"Error": -2340})
    try:
        Token: str = Req['token']
    except:
        return jsonify({"Error": -1341})
    try:
        MAIN = Account(TOKEN=Token)
    except Token_Wrong:
        return jsonify({"Error": -1342})
    try:
        BB = MAIN.get_Balance()
        return jsonify({"balance": BB})
    except AK_SK_Invalid:
        return jsonify({"Error": -1343})


@app.route('/positions', methods=['POST'])
def Positions():
    try:
        Req = request.get_json()
    except:
        return jsonify({"Error": -2341})
    try:
        Token: str = Req['token']
    except:
        return jsonify({"Error": -9458})
    try:
        MAIN = Account(TOKEN=Token)
        return jsonify(MAIN.open_Positions())
    except AK_SK_Database:
        return jsonify({"Error": -4342})
    except AK_SK_Invalid:
        return jsonify({"Error": -5213})


@app.route('/close', methods=['POST'])
def Close():
    try:
        Req = request.get_json()
    except:
        return jsonify({"Error": -9314})
    try:
        Token = Req['token']
        Pair = Req['pair'].upper()
        Amount = Req['amount']
        Side = Req['side'].upper()
    except:
        return jsonify({"Error": -9331})
    try:
        MAIN = ORDERS(TOKEN=Token, PAIR=Pair,
                      TYPE="MARKET", SIDE=Side,
                      AMOUNT=Amount)
    except AK_SK_Database:
        return jsonify({"Error": -4342})
    except AK_SK_Invalid:
        return jsonify({"Error": -5213})
    try:
        MAIN.close_Order()
    except Close_Error:
        return jsonify({"Error": -9315})
    try:
        MAIN.submit_Order()
    except:
        return jsonify({"Error": -9315})
    return jsonify({"Success": "True"})


@app.route('/check', methods=['POST'])
def Check():
    try:
        Req = request.get_json()
    except:
        return jsonify({"Error": -8864})
    try:
        Token: str = Req['token']
    except:
        return jsonify({"Error": -5432})
    try:
        Account(TOKEN=Token)
    except Token_Wrong:
        return jsonify({"Error": -4262})
    except AK_SK_Database:
        return jsonify({"Error": -4342})
    except AK_SK_Invalid:
        return jsonify({"Error": -5213})

    return jsonify({"Success": "True"})


if __name__ == '__main__':
    app.run(host=SERVER, debug=False, port=PORT)
