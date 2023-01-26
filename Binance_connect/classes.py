from pydantic import BaseModel


class Order(BaseModel):
    s: str  # Symbol
    c: str  # Client Order Id
    S: str  # Side
    o: str  # Order Type
    f: str  # Time in Force
    q: float  # Original Quantity
    p: float  # Original Price
    ap: float  # Average Price
    x: str  # Execution Type
    X: str  # Order Status
    i: int  # Order Id
    l: float  # Order Last Filled Quantity
    z: float  # Order Filled Accumulated Quantity
    L: float  # Last Filled Price
    T: int  # Order Trade Time
    t: int  # Trade Id
    b: float  # Bids Notional
    a: float  # Ask Notional
    m: bool  # Is this trade the maker side?
    R: bool  # Is this reduce only
    wt: str  # Stop Price Working Type
    ot: str  # Original Order Type
    ps: str  # Position Side
    cp: bool  # If Close-All, pushed with conditional order
    pP: bool  # ignore
    si: float  # ignore
    ss: float  # ignore
    rp: float  # Realized Profit of the trade
    N: str = None  # Commission Asset, will not push if no commission
    n: float = None  # Commission, will not push if no commission
    AP: float = None  # Activation Price, only puhed with TRAILING_STOP_MARKET order
    cr: float = None  # Callback Rate, only puhed with TRAILING_STOP_MARKET order
    sp: float = None  # Stop Price. Please ignore with TRAILING_STOP_MARKET order


class OpenOrder(BaseModel):
    avgPrice: float
    clientOrderId: str
    cumQuote: float
    executedQty: float
    orderId: int
    origQty: float
    origType: str
    price: float
    reduceOnly: bool
    side: str
    positionSide: str
    status: str
    stopPrice: float  # please ignore when order type is TRAILING_STOP_MARKET
    closePosition: bool
    symbol: str
    timeInForce: str
    type: str
    updateTime: int
    workingType: str
    time: int = None
    priceProtect: bool  # if conditional order trigger is protected
    # activation price, only return with TRAILING_STOP_MARKET order
    activatePrice: float = None
    priceRate: float = None  # callback rate, only return with TRAILING_STOP_MARKET order


class ORDER_TRADE_UPDATE(BaseModel):
    e: str  # Event Type
    E: int  # Event Time
    T: int  # Transaction Time
    o: Order

class ACCOUNT_UPDATE(BaseModel):
    e: str  # Event Type
    E: int  # Event Time
    T: int  # Transaction Time
    m: str

class ChangeLeverage(BaseModel):
    s: str  # symbol
    l: int  # leverage


class ChangeConfiguration(BaseModel):
    j: bool


class ACCOUNT_CONFIG_UPDATE(BaseModel):
    e: str  # Event Type
    E: int  # Event Time
    T: int  # Transaction Time
    ac: ChangeLeverage = None
    ai: ChangeConfiguration = None


class ACCOUNT_UPDATE_EventTypes:
    MARGIN_TYPE_CHANGE = 'MARGIN_TYPE_CHANGE'

class ExecutioTypes:
    NEW = 'NEW'
    CANCELED = "CANCELED"


class OrderTypes:
    TRAILING_STOP_MARKET = 'TRAILING_STOP_MARKET'
    LIMIT = 'LIMIT'
    MARKET = 'MARKET'
    TAKE_PROFIT_MARKET = 'TAKE_PROFIT_MARKET'
    STOP_MARKET = 'STOP_MARKET'
    TAKE_PROFIT = 'TAKE_PROFIT'
    STOP = 'STOP'


class PositionModes(BaseModel):
    symbol:str
    positionAmt:float
    entryPrice:float
    markPrice:float
    unRealizedProfit:float
    liquidationPrice:float
    leverage:int
    maxNotionalValue:int
    marginType:str
    isolatedMargin:float
    isAutoAddMargin:bool
    positionSide:str
    notional:float
    isolatedWallet:float
    updateTime:int

class EventTypes:
    ORDER_TRADE_UPDATE = "ORDER_TRADE_UPDATE"
    ACCOUNT_CONFIG_UPDATE = 'ACCOUNT_CONFIG_UPDATE'
    ACCOUNT_UPDATE = 'ACCOUNT_UPDATE'
