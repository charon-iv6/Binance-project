
class AK_SK_Invalid(Exception):
    """
        ApiKeyOrSecretKey Is Invalid.
    """


class AK_SK_Database(Exception):
    """
        ApiKeyOrSecretKey Isn't In Database.
    """


class Token_Wrong(Exception):
    """
        Token Isn't In Database.
    """


class Leverage_Unknown_Error(Exception):
    """
        Leverage Func Sent an Unknown Error
    """


class Leverage_Wrong(Exception):
    """
        Leverage Is Higher Than 125 or Lower Than 1
    """


class Leverage_Rediction_NotSupported(Exception):
    """
        Leverage Reduction is not supported ]n Isolated Margin Mode with open positions
    """


class Margin_Wrong(Exception):
    """
        Margin Isn't Valid = CROSSED - ISOLATED.
    """


class Margin_Couldnt_Change(Exception):
    """
        Currently a Position Is Open On This Pair And Can't Change Margin For This Pair.
    """


class Limit_Error(Exception):
    """
        Limit Order Didn't Open Because Of an Error.
    """


class Limit_Margin_Insufficient(Exception):
    """
        Limit Order - Insufficient Cash.
    """


class Limit_Not_OneWayMode(Exception):
    """
        Limit Order - User Settings isn't on OneWayMode.
    """


class Limit_Amount_InSufficient(Exception):
    """
        Limit Order - Quantity Is Not Acceptable.
    """


class MARKET_Margin_Insufficient(Exception):
    """
        Market Order - Insufficient Cash.
    """


class Market_Not_OneWayMode(Exception):
    """
        Market Order - User Settings isn't on OneWayMode.
    """


class Market_Amount_InSufficient(Exception):
    """
        Limit Order - Quantity Is Not Acceptable.
    """


class Market_Error(Exception):
    """
        Market Order Didn't Open Because Of an Error.
    """


class Close_Error(Exception):
    """
        Close Order Didn't Work Because Of an Error.
    """


class INTERNAL_WrongKey(Exception):
    """
        Wrong Key Type in GET_KEYS Func.
    """


class INTERNAL_WrongType(Exception):
    """
        Wrong TYPE In ORDER Func.
    """


class INTERNAL_WrongSide(Exception):
    """
        Wrong SIDE In Close_order Func.
    """