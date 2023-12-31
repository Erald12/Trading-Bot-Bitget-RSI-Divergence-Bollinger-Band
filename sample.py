import ccxt
import talib
import numpy as np
import time
import ta
import pandas as pd

# Bitget API credentials
api_key = ''
secret_key = ''
passphrase = ''

Finance = [15,15,15,15,15,15,15,15,15]
Balance = [15]
Opened_long = []
Open_long_price = []
Opened_short = []
Open_short_price = []
symbol_set = []

# Candlestick patterns to detect
long_patterns = ['hammer', 'inverted_hammer', 'bullish_engulfing', 'piercing_line', 'morning_star', 'three_white_soldiers']
short_patterns = ['hanging_man', 'shooting_star', 'bearish_engulfing', 'evening_star', 'three_black_crows', 'dark_cloud_cover']

# Function to check for a specific candlestick pattern
def detect_candlestick_pattern(ticker, pattern,current_price):
    # Fetch recent candlestick data
    candles = exchange.fetch_ohlcv(ticker, timeframe=timeframe, limit=10) #Specify you timeframe here

    # Check for the pattern
    if pattern == 'hammer':
        current_open = candles[-1][1]
        current_close = candles[-1][4]
        current_high = candles[-1][2]
        current_low = candles[-1][3]

        body_range = abs(current_close - current_open)
        upper_shadow = current_high - max(current_open, current_close)
        lower_shadow = min(current_open, current_close) - current_low

        if lower_shadow >= 2 * body_range and upper_shadow <= 0.1 * body_range:
            return True

    elif pattern == 'inverted_hammer':
        current_open = candles[-1][1]
        current_close = candles[-1][4]
        current_high = candles[-1][2]
        current_low = candles[-1][3]

        body_range = abs(current_close - current_open)
        upper_shadow = current_high - max(current_open, current_close)
        lower_shadow = min(current_open, current_close) - current_low

        if upper_shadow >= 2 * body_range and lower_shadow <= 0.1 * body_range:
            return True

    elif pattern == 'bullish_engulfing':
        previous_open = candles[-2][1]
        previous_close = candles[-2][4]
        current_open = candles[-1][1]
        current_close = candles[-1][4]

        if previous_close < previous_open and current_close > previous_open and current_open < previous_close:
            return True

    elif pattern == 'piercing_line':
        previous_open = candles[-2][1]
        previous_close = candles[-2][4]
        current_open = candles[-1][1]
        current_close = candles[-1][4]
        current_low = candles[-1][3]
        previous_high = candles[-2][2]

        if previous_close < previous_open and current_close > previous_open and current_open < previous_close and current_close > 0.5 * (
                previous_close + previous_open) and current_open < previous_open and current_low < previous_close:
            return True

    elif pattern == 'morning_star':
        first_open = candles[-3][1]
        first_close = candles[-3][4]
        second_open = candles[-2][1]
        second_close = candles[-2][4]
        current_open = candles[-1][1]
        current_close = candles[-1][4]

        if first_close < first_open and current_close > second_close and current_open < second_open and current_open > second_close and current_close > first_open:
            return True

    elif pattern == 'three_white_soldiers':
        first_open = candles[-3][1]
        first_close = candles[-3][4]
        second_open = candles[-2][1]
        second_close = candles[-2][4]
        current_open = candles[-1][1]
        current_close = candles[-1][4]

        if first_close < first_open and second_close < second_open and current_close > current_open and current_close > second_close and current_open > second_open and second_close > first_close and second_open > first_open:
            return True

    elif pattern == 'hanging_man':
        current_open = candles[-1][1]
        current_close = candles[-1][4]
        current_high = candles[-1][2]
        current_low = candles[-1][3]

        body_range = abs(current_close - current_open)
        upper_shadow = current_high - max(current_open, current_close)
        lower_shadow = min(current_open, current_close) - current_low

        if lower_shadow >= 2 * body_range and upper_shadow <= 0.1 * body_range:
            return True

    elif pattern == 'shooting_star':
        current_open = candles[-1][1]
        current_close = candles[-1][4]
        current_high = candles[-1][2]
        current_low = candles[-1][3]

        body_range = abs(current_close - current_open)
        upper_shadow = current_high - max(current_open, current_close)
        lower_shadow = min(current_open, current_close) - current_low

        if upper_shadow >= 2 * body_range and lower_shadow <= 0.1 * body_range:
            return True

    elif pattern == 'bearish_engulfing':
        previous_open = candles[-2][1]
        previous_close = candles[-2][4]
        current_open = candles[-1][1]
        current_close = candles[-1][4]

        if previous_close > previous_open and current_close < previous_open and current_open > previous_close:
            return True

    elif pattern == 'evening_star':
        first_open = candles[-3][1]
        first_close = candles[-3][4]
        second_open = candles[-2][1]
        second_close = candles[-2][4]
        current_open = candles[-1][1]
        current_close = candles[-1][4]

        if first_close > first_open and current_close < second_close and current_open > second_open and current_open < second_close and current_close < first_open:
            return True

    elif pattern == 'three_black_crows':
        first_open = candles[-3][1]
        first_close = candles[-3][4]
        second_open = candles[-2][1]
        second_close = candles[-2][4]
        current_open = candles[-1][1]
        current_close = candles[-1][4]

        if first_close > first_open and second_close > second_open and current_close < current_open and current_close < second_close and current_open < second_open and second_close < first_close and second_open < first_open:
            return True

    elif pattern == 'dark_cloud_cover':
        previous_open = candles[-2][1]
        previous_close = candles[-2][4]
        current_open = candles[-1][1]
        current_close = candles[-1][4]
        current_high = candles[-1][2]
        previous_low = candles[-2][3]

        if previous_close > previous_open and current_close < previous_open and current_open > previous_close and current_close < 0.5 * (
                previous_close + previous_open) and current_open > previous_open and current_high > previous_low:
            return True
    return False

#Function to check stochastic slow
def check_stochastic_strategy(ticker):

    # Fetch recent candlestick data
    candles = exchange.fetch_ohlcv(ticker, timeframe=timeframe, limit=50)

    # Extract OHLC prices
    opens = np.array([candle[1] for candle in candles], dtype=float)
    highs = np.array([candle[2] for candle in candles], dtype=float)
    lows = np.array([candle[3] for candle in candles], dtype=float)
    closes = np.array([candle[4] for candle in candles], dtype=float)

    # Convert to DataFrame
    df = pd.DataFrame({'open': opens, 'high': highs, 'low': lows, 'close': closes})

    # Calculate Stochastic Slow indicator
    stochastic = ta.momentum.StochasticOscillator(
        close=df['close'],
        high=df['high'],
        low=df['low'],
        window=14,
        smooth_window=3
    )
    slowk = stochastic.stoch()
    slowd = stochastic.stoch_signal()

    # Check for the strategy condition
    if slowk.iloc[-1] < 20 and slowd.iloc[-1] < 20 and slowk.iloc[-2] > slowd.iloc[-2] and slowk.iloc[-1] > slowd.iloc[-1]:
        return 'long'
    elif slowk.iloc[-1] > 80 and slowd.iloc[-1] > 80 and slowk.iloc[-2] < slowd.iloc[-2] and slowk.iloc[-1] < slowd.iloc[-1]:
        return 'short'

    return None


# Bitget trading parameters
symbol = 'BNB/USDT'  # Trading symbol
symbol2 = 'XRP/USDT'
symbol3 = 'BTC/USDT'
symbol4 = 'BCH/USDT'
symbol5 = 'MATIC/USDT'
symbol6 = 'LTC/USDT'
symbol7 = 'DOT/USDT'
symbol8 = 'DOGE/USDT'
symbol9 = 'EOS/USDT'

leverage = 50  # Leverage for the futures contract
trade_amount = 7  # Amount to trade in each order (needs trade amount 5 USDT or more.)
profit_target = 0.08  # Profit target in decimal format (10% = 0.1)
stop_loss = -0.02  # Stop loss in decimal format (-10% = -0.1)
timeframe = '1m'  # Candlestick timeframe (e.g., '1m', '5m', '1h', '1d')
num_candles = 30  # number of candles for slope computation

# Bollinger Bands parameters
bb_period = 30  # Number of periods for the moving average and standard deviation
bb_deviation = 2  # Number of standard deviations for the Bollinger Bands

# RSI parameters
rsi_period = 14  # Number of periods for RSI calculation
rsi_upper_threshold = 70  # Upper threshold for overbought condition
rsi_lower_threshold = 30  # Lower threshold for oversold condition

# Create Bitget exchange instance
exchange = ccxt.bitget({
    'apiKey': api_key,
    'secret': secret_key,
    'password': passphrase,
})

#Perecentage_Gain
def gain(v1,v2):
    gain = (v2-v1)/v1
    return gain

# Enable testnet if needed (uncomment the line below for testnet)
# exchange.urls['api'] = exchange.urls['test']

#Function to find high points and low points on closed prices
def find_high_points_price(ticker, timeframe, period):
    """Finds the high points of the specified symbol's price data."""
    candles = exchange.fetch_ohlcv(ticker, timeframe=timeframe, limit=period)

    prices = [float(candle[4]) for candle in candles]  # Extract close prices
    high_points = []
    for i in range(1, len(prices) - 1):
        if prices[i] > prices[i - 1] and prices[i] > prices[i + 1]:
            high_points.append(prices[i])
    return high_points

def find_low_points_price(ticker, timeframe, period):
    """Finds the peak points of the specified symbol's price data."""
    candles = exchange.fetch_ohlcv(ticker, timeframe=timeframe, limit=period)

    prices = [float(candle[4]) for candle in candles]  # Extract close prices
    low_points = []
    for i in range(1, len(prices) - 1):
        if prices[i] < prices[i - 1] and prices[i] < prices[i + 1]:
            low_points.append(prices[i])
    return low_points

#Function to find high points and low points on the data
def high_points_data(data):
    """Finds the high points of the specified symbol's price data."""

    high_points = []
    for i in range(1, len(data) - 1):
        if data[i] > data[i - 1] and data[i] > data[i + 1]:
            high_points.append(data[i])
    return high_points


def low_points_data(data):
    """Finds the high points of the specified symbol's price data."""

    low_points = []
    for i in range(1, len(data) - 1):
        if data[i] < data[i - 1] and data[i] < data[i + 1]:
            low_points.append(data[i])
    return low_points


# Function to calculate Bollinger Bands
def calculate_bollinger_bands(ticker):
    # Fetch recent candlestick data
    candles = exchange.fetch_ohlcv(ticker, timeframe=timeframe, limit=bb_period+59)

    # Extract closing prices
    closes = np.array([candle[4] for candle in candles])

    # Calculate moving average and standard deviation
    ma = talib.SMA(closes, timeperiod=bb_period)
    std = talib.STDDEV(closes, timeperiod=bb_period)

    # Calculate upper and lower Bollinger Bands
    upper_band = ma + bb_deviation * std
    lower_band = ma - bb_deviation * std

    return ma, upper_band, lower_band

# Calculate Slope
def calculate_slope(x1,x2,y1,y2):
    slope = (y2-y1)/(x2-x1)
    return slope

# Function to calculate RSI
def calculate_rsi(ticker, timeframe, rsi_period):
    # Fetch recent candlestick data
    candles = exchange.fetch_ohlcv(ticker, timeframe=timeframe, limit=rsi_period+59)

    # Extract closing prices
    closes = [candle[4] for candle in candles]

    # Calculate RSI
    gains = []
    losses = []

    for i in range(1, len(closes)):
        diff = closes[i] - closes[i-1]
        if diff > 0:
            gains.append(diff)
            losses.append(0)
        else:
            gains.append(0)
            losses.append(-diff)

    avg_gain = sum(gains[:rsi_period]) / rsi_period
    avg_loss = sum(losses[:rsi_period]) / rsi_period

    rsi = []
    rsi.append(100 - (100 / (1 + (avg_gain / avg_loss))))

    for i in range(rsi_period, len(closes)):
        avg_gain = (avg_gain * (rsi_period - 1) + gains[i-1]) / rsi_period
        avg_loss = (avg_loss * (rsi_period - 1) + losses[i-1]) / rsi_period
        relative_strength = avg_gain / avg_loss
        rsi.append(100 - (100 / (1 + relative_strength)))

    return rsi


# Function to check if the price crosses upper Bollinger Band
def is_price_crosses_upper_band(ticker):
    ma, upper_band, _ = calculate_bollinger_bands(ticker)
    current_price = exchange.fetch_ticker(ticker)['last']
    candles = exchange.fetch_ohlcv(ticker, timeframe=timeframe, limit=bb_period + 59)

    # Extract closing prices
    closes = np.array([candle[4] for candle in candles])

    return (closes[-2] > upper_band[-2] or closes[-3] > upper_band[-3] or closes[-4] > upper_band[-4]) and current_price < upper_band[-1]

# Function to check if the price crosses to lower Bollinger Band
def is_price_crosses_lower_band(ticker):
    ma, _, lower_band = calculate_bollinger_bands(ticker)
    current_price = exchange.fetch_ticker(ticker)['last']
    candles = exchange.fetch_ohlcv(ticker, timeframe=timeframe, limit=bb_period + 59)

    # Extract closing prices
    closes = np.array([candle[4] for candle in candles])

    return (closes[-2] < lower_band[-2] or closes[-3] < lower_band[-3] or closes[-4] < lower_band[-4]) and current_price > lower_band[-1]



###############################################################################################
# Function to place a long order
def place_long_order(ticker, balance):
    ticker_price = exchange.fetch_ticker(ticker)['last']
    long = Opened_long.append(balance)
    New_Balance = Balance.clear()
    position = Open_long_price.append(ticker_price)
    new_symbol = symbol_set.append(ticker)

    return  long, position, New_Balance, new_symbol

# Function to place a short order
def place_short_order(ticker, balance):
    ticker_price = exchange.fetch_ticker(ticker)['last']
    short = Opened_short.append(balance)
    New_Balance = Balance.clear()
    position = Open_short_price.append(ticker_price)
    new_symbol = symbol_set.append(ticker)


    return short, position, New_Balance, new_symbol

# Function to calculate account balance
def get_account_balance():
    try:
        account_info = exchange.fetch_balance()
        balance = account_info['total']['USDT']
        return balance
    except Exception as e:
        print(f"Failed to fetch account balance: {e}")
        return None

# Function to close an open position
def close_position_long(ticker):
    # Fetch open orders
    ticker_price = exchange.fetch_ticker(ticker)['last']
    percent_long = (ticker_price - Open_long_price[0])/(Open_long_price[0])
    # Close open orders
    balance_clear_from_long = Balance.append((Opened_long[0]*percent_long*leverage)+Opened_long[0])
    clear_open_long_price = Open_long_price.clear()
    clear_open_long = Opened_long.clear()
    return balance_clear_from_long, clear_open_long_price, clear_open_long

def close_position_short(ticker):
    # Fetch open orders
    ticker_price = exchange.fetch_ticker(ticker)['last']
    percent_short = (ticker_price - Open_short_price[0]) / (Open_short_price[0])
    balance_clear_from_short = Balance.append((Opened_short[0] * (-percent_short) * leverage)+Opened_short[0])
    clear_open_short_price = Open_short_price.clear()
    clear_open_short = Opened_short.clear()
    return balance_clear_from_short, clear_open_short_price, clear_open_short


# Function to check if there is an open position
def is_position_open():
    # Fetch open orders
    orders = exchange.fetch_open_orders(symbol)

    return len(orders) > 0


#Determine if Bullish Divergence
def is_bullish_divergence_with_rsi(ticker, timeframe, rsi_period):
    close_candles = exchange.fetch_ohlcv(ticker, timeframe=timeframe, limit=60)
    close_prices2 = list(np.array([candle[4] for candle in close_candles], dtype=float))
    high_points_price = find_high_points_price(ticker, timeframe, 60)
    low_points_price = find_low_points_price(ticker, timeframe, 60)
    high_of_high_price = high_points_data(high_points_price)
    high_of_high_price_max = [max(high_of_high_price)]
    low_of_low_price = low_points_data(low_points_price)
    low_of_low_price_min = [min(low_of_low_price)]
    recent_rsi = calculate_rsi(ticker, timeframe, rsi_period)
    high_of_high_price_max.append(high_points_price[-1])
    low_of_low_price_min.append(low_points_price[-1])

    price_low_slope = calculate_slope(close_prices2.index(low_of_low_price_min[0]),close_prices2.index(low_of_low_price_min[1]), low_of_low_price_min[0],low_of_low_price_min[1])
    rsi_low_slope = calculate_slope(close_prices2.index(low_of_low_price_min[0]),close_prices2.index(low_of_low_price_min[1]),recent_rsi[close_prices2.index(low_of_low_price_min[0])],recent_rsi[close_prices2.index(low_of_low_price_min[1])])

    return price_low_slope < 0 and rsi_low_slope > 0


#Determine if Bearish Divergence:
def is_bearish_divergence_with_rsi(ticker, timeframe, rsi_period):
    close_candles = exchange.fetch_ohlcv(ticker, timeframe=timeframe, limit=60)
    close_prices2 = list(np.array([candle[4] for candle in close_candles], dtype=float))
    high_points_price = find_high_points_price(ticker, timeframe, 60)
    low_points_price = find_low_points_price(ticker, timeframe, 60)
    high_of_high_price = high_points_data(high_points_price)
    high_of_high_price_max = [max(high_of_high_price)]
    low_of_low_price = low_points_data(low_points_price)
    low_of_low_price_min = [min(low_of_low_price)]
    recent_rsi = calculate_rsi(ticker, timeframe, rsi_period)
    high_of_high_price_max.append(high_points_price[-1])
    low_of_low_price_min.append(low_points_price[-1])

    price_high_slope = calculate_slope(close_prices2.index(high_of_high_price_max[0]),close_prices2.index(high_of_high_price_max[1]), high_of_high_price_max[0],high_of_high_price_max[1])
    rsi_high_slope = calculate_slope(close_prices2.index(high_of_high_price_max[0]),close_prices2.index(high_of_high_price_max[1]),recent_rsi[close_prices2.index(high_of_high_price_max[0])],recent_rsi[close_prices2.index(high_of_high_price_max[1])])

    return price_high_slope > 0 and rsi_high_slope < 0


# Main trading loop
while True:
    try:
        if len(Balance)>0:
            my_balance =Balance[0]
        else:
            my_balance = 0
        if my_balance == 0 and (len(Opened_short) == 0 and len(Opened_long) == 0):
            Balance.append(Finance.pop())
            print('Amount to trade was added')
            print('Wallet Balance : ', sum(Finance))
        else:
            print('')


        currency_price_symbol = exchange.fetch_ticker(symbol)['last']
        if len(Balance)>0:
            print('Amount to trade : ', my_balance)
            # Fetch current price
            ticker = exchange.fetch_ticker(symbol)
            current_price = ticker['last']
            # Check for candlestick patterns
            for pattern in long_patterns:
                if detect_candlestick_pattern(symbol, pattern, current_price) and is_bullish_divergence_with_rsi(symbol,timeframe,rsi_period) and check_stochastic_strategy(symbol) == 'long':
                    print(pattern)
                    place_long_order(symbol, my_balance)
                    break

            for pattern in short_patterns:
                if detect_candlestick_pattern(symbol, pattern, current_price) and is_bearish_divergence_with_rsi(symbol,timeframe,rsi_period) and check_stochastic_strategy(symbol) == 'short':
                    print(pattern)
                    place_short_order(symbol, my_balance)
                    break
            if (len(Opened_long)) == 0 and (len(Opened_short)) == 0:
                if is_bullish_divergence_with_rsi(symbol, timeframe, rsi_period):
                    print('####################################################')
                    close_candles_symbol = exchange.fetch_ohlcv(symbol, timeframe=timeframe, limit=60)
                    close_prices_symbol = list(np.array([candle[4] for candle in close_candles_symbol], dtype=float))
                    print('Price: ', close_prices_symbol[-1], symbol)
                    print('Bullish Divergence Confirmed')
                    print('####################################################')
                elif is_bearish_divergence_with_rsi(symbol, timeframe, rsi_period):
                    print('####################################################')
                    close_candles_symbol = exchange.fetch_ohlcv(symbol, timeframe=timeframe, limit=60)
                    close_prices_symbol = list(np.array([candle[4] for candle in close_candles_symbol], dtype=float))
                    print('Price: ', close_prices_symbol[-1], symbol)
                    print('Bearish Divergence Confirmed')
                    print('####################################################')
                else:
                    print('')
                if is_price_crosses_lower_band(symbol) and is_bullish_divergence_with_rsi(symbol, timeframe,rsi_period) and (my_balance >= 10):
                    place_long_order(symbol, my_balance)
                    print('Long position taken')
                elif is_price_crosses_upper_band(symbol) and is_bearish_divergence_with_rsi(symbol, timeframe,rsi_period) and (my_balance >= 10):
                    place_short_order(symbol, Balance[0])
                    print('Short position taken')
            else:
                print('')
        else:
            print('Amount to Trade: ', '0')


        if len(Opened_long) > 0 and (symbol_set[0] == symbol):

            print('Opened Position: ', Open_long_price, symbol, '   Amount: ','LONG', Opened_long, 'PNL: ',gain(Open_long_price[0], currency_price_symbol))
            if (gain(Open_long_price[0], currency_price_symbol) >= 0.0032) or (gain(Open_long_price[0], currency_price_symbol) <= -0.001):
                close_position_long(symbol)
                symbol_set.clear()
                if my_balance <= 5:
                    Balance[0] = Balance[0]+float(Finance.pop())
                    print('Amount to trade was added')
                    print('Wallet Balance : ', sum(Finance), 'Amount to trade: ', Balance[0])
                else:
                    print('')
                print('Position Closed')
            else:
                print('No Close')
        elif len(Opened_short) > 0 and (symbol_set[0] == symbol):
            print('Opened Position: ', Open_short_price, symbol, '   Amount: ','SHORT', Opened_short, 'PNL: ',-gain(Open_short_price[0], currency_price_symbol))
            if (gain(Open_short_price[0], currency_price_symbol) >= 0.001) or (gain(Open_short_price[0], currency_price_symbol) <= -0.0032):
                close_position_short(symbol)
                symbol_set.clear()
                if my_balance <= 5:
                    Balance[0] = Balance[0]+float(Finance.pop())
                    print('Amount to trade was added')
                    print('Wallet Balance : ', sum(Finance), 'Amount to trade: ', Balance[0])
                else:
                    print('')
                print('Position Closed')
            else:
                print('No Close')
        else:
            print('No Opened Trades')



        ##########################################################################
        currency_price_symbol2 = exchange.fetch_ticker(symbol2)['last']
        if len(Balance)>0:
            print('Amount to trade: ', my_balance)
            # Fetch current price
            ticker = exchange.fetch_ticker(symbol2)
            current_price = ticker['last']
            # Check for candlestick patterns
            for pattern in long_patterns:
                if detect_candlestick_pattern(symbol2, pattern, current_price) and is_bullish_divergence_with_rsi(symbol2, timeframe, rsi_period) and check_stochastic_strategy(symbol2) == 'long':
                    print(pattern)
                    place_long_order(symbol2, my_balance)
                    break

            for pattern in short_patterns:
                if detect_candlestick_pattern(symbol2, pattern, current_price) and is_bearish_divergence_with_rsi(symbol2, timeframe, rsi_period) and check_stochastic_strategy(symbol2) == 'short':
                    print(pattern)
                    place_short_order(symbol2, my_balance)
                    break
            if (len(Opened_long)) == 0 and (len(Opened_short)) == 0:
                if is_bullish_divergence_with_rsi(symbol2, timeframe, rsi_period):
                    print('####################################################')
                    close_candles_symbol2 = exchange.fetch_ohlcv(symbol2, timeframe=timeframe, limit=60)
                    close_prices_symbol2 = list(np.array([candle[4] for candle in close_candles_symbol2], dtype=float))
                    print('Price: ', close_prices_symbol2[-1], symbol2)
                    print('Bullish Divergence Confirmed')
                    print('####################################################')
                elif is_bearish_divergence_with_rsi(symbol2, timeframe, rsi_period):
                    print('####################################################')
                    close_candles_symbol2 = exchange.fetch_ohlcv(symbol2, timeframe=timeframe, limit=60)
                    close_prices_symbol2 = list(np.array([candle[4] for candle in close_candles_symbol2], dtype=float))
                    print('Price: ', close_prices_symbol2[-1], symbol2)
                    print('Bearish Divergence Confirmed')
                    print('####################################################')
                else:
                    print('')

                if is_price_crosses_lower_band(symbol2) and is_bullish_divergence_with_rsi(symbol2, timeframe,rsi_period) and (my_balance >= 10):
                    place_long_order(symbol2, my_balance)
                    print('Long position taken')
                elif is_price_crosses_upper_band(symbol2) and is_bearish_divergence_with_rsi(symbol2, timeframe,rsi_period) and (my_balance >= 10):
                    place_short_order(symbol2, Balance[0])
                    print('Short position taken')
            else:
                print('')

        else:
            print('Amount to trade: ', '0')

        if len(Opened_long) > 0 and (symbol_set[0] == symbol2):
            print('Opened Position: ', Open_long_price, symbol2, '   Amount: ','LONG', Opened_long, 'PNL: ',gain(Open_long_price[0], currency_price_symbol2))
            if (gain(Open_long_price[0], currency_price_symbol2) >= 0.0032) or (gain(Open_long_price[0], currency_price_symbol2) <= -0.001):
                close_position_long(symbol2)
                symbol_set.clear()
                if my_balance <= 5:
                    Balance[0] = Balance[0]+float(Finance.pop())
                    print('Amount to trade was added')
                    print('Wallet Balance : ', sum(Finance), 'Amount to trade: ', Balance[0])
                else:
                    print('')
                print('Position Closed')
            else:
                print('No Close')
        elif len(Opened_short) > 0 and (symbol_set[0] == symbol2):
            print('Opened Position: ', Open_short_price, symbol2, '   Amount: ','SHORT', Opened_short, 'PNL: ',-gain(Open_short_price[0], currency_price_symbol2))
            if (gain(Open_short_price[0], currency_price_symbol2) >= 0.001) or (gain(Open_short_price[0], currency_price_symbol2) <= -0.0032):
                close_position_short(symbol2)
                symbol_set.clear()
                if my_balance <= 5:
                    Balance[0] = Balance[0]+float(Finance.pop())
                    print('Amount to trade was added')
                    print('Wallet Balance : ', sum(Finance), 'Amount to trade: ', Balance[0])
                else:
                    print('')
                print('Position Closed')
            else:
                print('No Close')
        else:
            print('No Opened Trades')

        ##########################################################################
        currency_price_symbol3 = exchange.fetch_ticker(symbol3)['last']
        if len(Balance)>0:
            print('Amount to trade: ',my_balance)
            # Fetch current price
            ticker = exchange.fetch_ticker(symbol3)
            current_price = ticker['last']
            # Check for candlestick patterns
            for pattern in long_patterns:
                if detect_candlestick_pattern(symbol3, pattern, current_price) and is_bullish_divergence_with_rsi(symbol3, timeframe, rsi_period) and check_stochastic_strategy(symbol3) == 'long':
                    print(pattern)
                    place_long_order(symbol3, my_balance)
                    break

            for pattern in short_patterns:
                if detect_candlestick_pattern(symbol3, pattern, current_price) and is_bearish_divergence_with_rsi(symbol3, timeframe, rsi_period) and check_stochastic_strategy(symbol3) == 'short':
                    print(pattern)
                    place_short_order(symbol3, my_balance)
                    break
            if (len(Opened_long)) == 0 and (len(Opened_short)) == 0:
                if is_bullish_divergence_with_rsi(symbol3, timeframe, rsi_period):
                    print('####################################################')
                    close_candles_symbol3 = exchange.fetch_ohlcv(symbol3, timeframe=timeframe, limit=60)
                    close_prices_symbol3 = list(np.array([candle[4] for candle in close_candles_symbol3], dtype=float))
                    print('Price: ', close_prices_symbol3[-1], symbol3)
                    print('Bullish Divergence Confirmed')
                    print('####################################################')
                elif is_bearish_divergence_with_rsi(symbol3, timeframe, rsi_period):
                    print('####################################################')
                    close_candles_symbol3 = exchange.fetch_ohlcv(symbol3, timeframe=timeframe, limit=60)
                    close_prices_symbol3 = list(np.array([candle[4] for candle in close_candles_symbol3], dtype=float))
                    print('Price: ', close_prices_symbol3[-1], symbol3)
                    print('Bearish Divergence Confirmed')
                    print('####################################################')
                else:
                    print('')

                if is_price_crosses_lower_band(symbol3) and is_bullish_divergence_with_rsi(symbol3, timeframe,rsi_period) and (my_balance >= 10):
                    place_long_order(symbol3, my_balance)
                    print('Long position taken')
                elif is_price_crosses_upper_band(symbol3) and is_bearish_divergence_with_rsi(symbol3, timeframe,rsi_period) and (my_balance >= 10):
                    place_short_order(symbol3, Balance[0])
                    print('Short position taken')
            else:
                print('')
        else:
            print('Amount to trade : ', '0')

        if len(Opened_long) > 0 and (symbol_set[0] == symbol3):
            print('Opened Position: ', Open_long_price, symbol3, '   Amount: ','LONG', Opened_long,'PNL: ',gain(Open_long_price[0], currency_price_symbol3))
            if (gain(Open_long_price[0], currency_price_symbol3) >= 0.0032) or (gain(Open_long_price[0], currency_price_symbol3) <= -0.001):
                close_position_long(symbol3)
                symbol_set.clear()
                if my_balance <= 5:
                    Balance[0] = Balance[0]+float(Finance.pop())
                    print('Amount to trade was added')
                    print('Wallet Balance : ', sum(Finance), 'Amount to trade: ', Balance[0])
                else:
                    print('')
                print('Position Closed')
            else:
                print('No Close')
        elif len(Opened_short) > 0 and (symbol_set[0] == symbol3):
            print('Opened Position: ', Open_short_price, symbol3, '   Amount: ','SHORT', Opened_short, 'PNL: ',-gain(Open_short_price[0], currency_price_symbol3))
            if (gain(Open_short_price[0], currency_price_symbol3) >= 0.001) or (gain(Open_short_price[0], currency_price_symbol3) <= -0.0032):
                close_position_short(symbol3)
                symbol_set.clear()
                if my_balance <= 5:
                    Balance[0] = Balance[0]+float(Finance.pop())
                    print('Amount to trade was added')
                    print('Wallet Balance : ', sum(Finance), 'Amount to trade: ', Balance[0])
                else:
                    print('')
                print('Position Closed')
            else:
                print('No Close')
        else:
            print('No Opened Trades')

        ##########################################################################
        currency_price_symbol4 = exchange.fetch_ticker(symbol4)['last']
        if len(Balance)>0:
            print('Amount to trade ', my_balance)
            # Fetch current price
            ticker = exchange.fetch_ticker(symbol4)
            current_price = ticker['last']
            # Check for candlestick patterns
            for pattern in long_patterns:
                if detect_candlestick_pattern(symbol4, pattern, current_price) and is_bullish_divergence_with_rsi(symbol4, timeframe, rsi_period) and check_stochastic_strategy(symbol4) == 'long':
                    print(pattern)
                    place_long_order(symbol4, my_balance)
                    break

            for pattern in short_patterns:
                if detect_candlestick_pattern(symbol4, pattern, current_price) and is_bearish_divergence_with_rsi(symbol4, timeframe, rsi_period) and check_stochastic_strategy(symbol4) == 'short':
                    print(pattern)
                    place_short_order(symbol4, my_balance)
                    break

            if (len(Opened_long)) == 0 and (len(Opened_short)) == 0:
                if is_bullish_divergence_with_rsi(symbol4, timeframe, rsi_period):
                    print('####################################################')
                    close_candles_symbol4 = exchange.fetch_ohlcv(symbol4, timeframe=timeframe, limit=60)
                    close_prices_symbol4 = list(np.array([candle[4] for candle in close_candles_symbol4], dtype=float))
                    print('Price: ', close_prices_symbol4[-1], symbol4)
                    print('Bullish Divergence Confirmed')
                    print('####################################################')
                elif is_bearish_divergence_with_rsi(symbol4, timeframe, rsi_period):
                    print('####################################################')
                    close_candles_symbol4 = exchange.fetch_ohlcv(symbol4, timeframe=timeframe, limit=60)
                    close_prices_symbol4 = list(np.array([candle[4] for candle in close_candles_symbol4], dtype=float))
                    print('Price: ', close_prices_symbol4[-1], symbol4)
                    print('Bearish Divergence Confirmed')
                    print('####################################################')
                else:
                    print('')

                if is_price_crosses_lower_band(symbol4) and is_bullish_divergence_with_rsi(symbol4, timeframe,rsi_period) and (my_balance >= 10):
                    place_long_order(symbol4, my_balance)
                    print('Long position taken')
                elif is_price_crosses_upper_band(symbol4) and is_bearish_divergence_with_rsi(symbol4, timeframe,rsi_period) and (my_balance >= 10):
                    place_short_order(symbol4, Balance[0])
                    print('Short position taken')
            else:
                print('')
        else:
            print('Amount to trade: ', '0')

        if len(Opened_long) > 0 and (symbol_set[0] == symbol4):
            print('Opened Position: ', Open_long_price, symbol4, '   Amount: ','LONG', Opened_long, 'PNL: ',gain(Open_long_price[0], currency_price_symbol4))
            if (gain(Open_long_price[0], currency_price_symbol4) >= 0.0032) or (gain(Open_long_price[0], currency_price_symbol4) <= -0.001):
                close_position_long(symbol4)
                symbol_set.clear()
                if my_balance <= 5:
                    Balance[0] = Balance[0]+float(Finance.pop())
                    print('Amount to trade was added')
                    print('Wallet Balance : ', sum(Finance), 'Amount to trade: ', Balance[0])
                else:
                    print('')
                print('Position Closed')
            else:
                print('No Close')
        elif len(Opened_short) > 0 and (symbol_set[0] == symbol4):
            print('Opened Position: ', Open_short_price, symbol4, '   Amount: ','SHORT', Opened_short,'PNL: ',-gain(Open_short_price[0], currency_price_symbol4))
            if (gain(Open_short_price[0], currency_price_symbol4) >= 0.001) or (gain(Open_short_price[0], currency_price_symbol4) <= -0.0032):
                close_position_short(symbol4)
                symbol_set.clear()
                if my_balance <= 5:
                    Balance[0] = Balance[0]+float(Finance.pop())
                    print('Amount to trade was added')
                    print('Wallet Balance : ', sum(Finance), 'Amount to trade: ', Balance[0])
                else:
                    print('')
                print('Position Closed')
            else:
                print('No Close')
        else:
            print('No Opened Trades')

        ##########################################################################
        currency_price_symbol5 = exchange.fetch_ticker(symbol5)['last']
        if len(Balance)>0:
            print('Amount to trade: ', my_balance)
            # Fetch current price
            ticker = exchange.fetch_ticker(symbol5)
            current_price = ticker['last']
            # Check for candlestick patterns
            for pattern in long_patterns:
                if detect_candlestick_pattern(symbol5, pattern, current_price) and is_bullish_divergence_with_rsi(symbol5, timeframe, rsi_period) and check_stochastic_strategy(symbol5) == 'long':
                    print(pattern)
                    place_long_order(symbol5, my_balance)
                    break

            for pattern in short_patterns:
                if detect_candlestick_pattern(symbol5, pattern, current_price) and is_bearish_divergence_with_rsi(symbol5, timeframe, rsi_period) and check_stochastic_strategy(symbol5) == 'short':
                    print(pattern)
                    place_short_order(symbol5, my_balance)
                    break

            if (len(Opened_long)) == 0 and (len(Opened_short)) == 0:
                if is_bullish_divergence_with_rsi(symbol5, timeframe, rsi_period):
                    print('####################################################')
                    close_candles_symbol5 = exchange.fetch_ohlcv(symbol5, timeframe=timeframe, limit=60)
                    close_prices_symbol5 = list(np.array([candle[4] for candle in close_candles_symbol5], dtype=float))
                    print('Price: ', close_prices_symbol5[-1], symbol5)
                    print('Bullish Divergence Confirmed')
                    print('####################################################')
                elif is_bearish_divergence_with_rsi(symbol5, timeframe, rsi_period):
                    print('####################################################')
                    close_candles_symbol5 = exchange.fetch_ohlcv(symbol5, timeframe=timeframe, limit=60)
                    close_prices_symbol5 = list(np.array([candle[4] for candle in close_candles_symbol5], dtype=float))
                    print('Price: ', close_prices_symbol5[-1], symbol5)
                    print('Bearish Divergence Confirmed')
                    print('####################################################')
                else:
                    print('')

                if is_price_crosses_lower_band(symbol5) and is_bullish_divergence_with_rsi(symbol5, timeframe,rsi_period) and (my_balance >= 10):
                    place_long_order(symbol5, my_balance)
                    print('Long position taken')
                elif is_price_crosses_upper_band(symbol5) and is_bearish_divergence_with_rsi(symbol5, timeframe,rsi_period) and (my_balance >= 10):
                    place_short_order(symbol5, Balance[0])
                    print('Short position taken')
            else:
                print('')

        else:
            print('Amount to trade: ', '0')

        if len(Opened_long) > 0 and (symbol_set[0] == symbol5):
            print('Opened Position: ', Open_long_price, symbol5, '   Amount: ','LONG', Opened_long, 'PNL: ',gain(Open_long_price[0], currency_price_symbol5))
            if (gain(Open_long_price[0], currency_price_symbol5) >= 0.0032) or (gain(Open_long_price[0], currency_price_symbol5) <= -0.001):
                close_position_long(symbol5)
                symbol_set.clear()
                if my_balance <= 5:
                    Balance[0] = Balance[0]+float(Finance.pop())
                    print('Amount to trade was added')
                    print('Wallet Balance : ', sum(Finance), 'Amount to trade: ', Balance[0])
                else:
                    print('')
                print('Position Closed')
            else:
                print('No Close')
        elif len(Opened_short) > 0 and (symbol_set[0] == symbol5):
            print('Opened Position: ', Open_short_price, symbol5, '   Amount: ','SHORT', Opened_short, 'PNL: ',-gain(Open_short_price[0], currency_price_symbol5))
            if (gain(Open_short_price[0], currency_price_symbol5) >= 0.001) or (gain(Open_short_price[0], currency_price_symbol5) <= -0.032):
                close_position_short(symbol5)
                symbol_set.clear()
                if my_balance <= 5:
                    Balance[0] = Balance[0]+float(Finance.pop())
                    print('Amount to trade was added')
                    print('Wallet Balance : ', sum(Finance), 'Amount to trade: ', Balance[0])
                else:
                    print('')
                print('Position Closed')
            else:
                print('No Close')
        else:
            print('No Opened Trades')

        ##########################################################################
        currency_price_symbol6 = exchange.fetch_ticker(symbol6)['last']
        if len(Balance)>0:
            print('Amount to trade: ', my_balance)
            # Fetch current price
            ticker = exchange.fetch_ticker(symbol6)
            current_price = ticker['last']
            # Check for candlestick patterns
            for pattern in long_patterns:
                if detect_candlestick_pattern(symbol6, pattern, current_price) and is_bullish_divergence_with_rsi(symbol6, timeframe, rsi_period) and check_stochastic_strategy(symbol6) == 'long':
                    print(pattern)
                    place_long_order(symbol6, my_balance)
                    break

            for pattern in short_patterns:
                if detect_candlestick_pattern(symbol6, pattern, current_price) and is_bearish_divergence_with_rsi(symbol6, timeframe, rsi_period) and check_stochastic_strategy(symbol6) == 'short':
                    print(pattern)
                    place_short_order(symbol6, my_balance)
                    break

            if (len(Opened_long)) == 0 and (len(Opened_short)) == 0:
                if is_bullish_divergence_with_rsi(symbol6, timeframe, rsi_period):
                    print('####################################################')
                    close_candles_symbol6 = exchange.fetch_ohlcv(symbol6, timeframe=timeframe, limit=60)
                    close_prices_symbol6 = list(np.array([candle[4] for candle in close_candles_symbol6], dtype=float))
                    print('Price: ', close_prices_symbol6[-1], symbol6)
                    print('Bullish Divergence Confirmed')
                    print('####################################################')
                elif is_bearish_divergence_with_rsi(symbol6, timeframe, rsi_period):
                    print('####################################################')
                    close_candles_symbol6 = exchange.fetch_ohlcv(symbol6, timeframe=timeframe, limit=60)
                    close_prices_symbol6 = list(np.array([candle[4] for candle in close_candles_symbol6], dtype=float))
                    print('Price: ', close_prices_symbol6[-1], symbol6)
                    print('Bearish Divergence Confirmed')
                    print('####################################################')
                else:
                    print('')

                if is_price_crosses_lower_band(symbol6) and is_bullish_divergence_with_rsi(symbol6, timeframe,rsi_period) and (my_balance >= 10):
                    place_long_order(symbol6, my_balance)
                    print('Long position taken')
                elif is_price_crosses_upper_band(symbol6) and is_bearish_divergence_with_rsi(symbol6, timeframe,rsi_period) and (my_balance >= 10):
                    place_short_order(symbol6, Balance[0])
                    print('Short position taken')
            else:
                print('')
        else:
            print('Amount to trade: ', '0')

        if len(Opened_long) > 0 and (symbol_set[0] == symbol6):
            print('Opened Position: ', Open_long_price, symbol6, '   Amount: ','LONG', Opened_long, 'PNL: ',gain(Open_long_price[0], currency_price_symbol6))
            if (gain(Open_long_price[0], currency_price_symbol6) >= 0.0032) or (gain(Open_long_price[0], currency_price_symbol6) <= -0.001):
                close_position_long(symbol6)
                symbol_set.clear()
                if my_balance <= 5:
                    Balance[0] = Balance[0]+float(Finance.pop())
                    print('Amount to trade was added')
                    print('Wallet Balance : ', sum(Finance), 'Amount to trade: ', Balance[0])
                else:
                    print('')
                print('Position Closed')
            else:
                print('No Close')
        elif len(Opened_short) > 0 and (symbol_set[0] == symbol6):
            print('Opened Position: ', Open_short_price, symbol6, '   Amount: ','SHORT', Opened_short, 'PNL: ',-gain(Open_short_price[0], currency_price_symbol6))
            if (gain(Open_short_price[0], currency_price_symbol6) >= 0.001) or (gain(Open_short_price[0], currency_price_symbol6) <= -0.032):
                close_position_short(symbol6)
                symbol_set.clear()
                if my_balance <= 5:
                    Balance[0] = Balance[0]+float(Finance.pop())
                    print('Amount to trade was added')
                    print('Wallet Balance : ', sum(Finance), 'Amount to trade: ', Balance[0])
                else:
                    print('')
                print('Position Closed')
            else:
                print('No Close')
        else:
            print('No Opened Trades')

        ##########################################################################
        currency_price_symbol7 = exchange.fetch_ticker(symbol7)['last']
        if len(Balance)>0:
            print('Amount to trade: ', my_balance)
            # Fetch current price
            ticker = exchange.fetch_ticker(symbol7)
            current_price = ticker['last']
            # Check for candlestick patterns
            for pattern in long_patterns:
                if detect_candlestick_pattern(symbol7, pattern, current_price) and is_bullish_divergence_with_rsi(symbol7, timeframe, rsi_period) and check_stochastic_strategy(symbol7) == 'long':
                    print(pattern)
                    place_long_order(symbol7, my_balance)
                    break

            for pattern in short_patterns:
                if detect_candlestick_pattern(symbol7, pattern, current_price) and is_bearish_divergence_with_rsi(symbol7, timeframe, rsi_period) and check_stochastic_strategy(symbol7) == 'short':
                    print(pattern)
                    place_short_order(symbol7, my_balance)
                    break

            if (len(Opened_long)) == 0 and (len(Opened_short)) == 0:
                if is_bullish_divergence_with_rsi(symbol7, timeframe, rsi_period):
                    print('####################################################')
                    close_candles_symbol7 = exchange.fetch_ohlcv(symbol7, timeframe=timeframe, limit=60)
                    close_prices_symbol7 = list(np.array([candle[4] for candle in close_candles_symbol7], dtype=float))
                    print('Price: ', close_prices_symbol7[-1], symbol7)
                    print('Bullish Divergence Confirmed')
                    print('####################################################')
                elif is_bearish_divergence_with_rsi(symbol7, timeframe, rsi_period):
                    print('####################################################')
                    close_candles_symbol7 = exchange.fetch_ohlcv(symbol7, timeframe=timeframe, limit=60)
                    close_prices_symbol7 = list(np.array([candle[4] for candle in close_candles_symbol7], dtype=float))
                    print('Price: ', close_prices_symbol7[-1], symbol7)
                    print('Bearish Divergence Confirmed')
                    print('####################################################')
                else:
                    print('')

                if is_price_crosses_lower_band(symbol7) and is_bullish_divergence_with_rsi(symbol7, timeframe,rsi_period) and (my_balance >= 10):
                    place_long_order(symbol7, my_balance)
                    print('Long position taken')
                elif is_price_crosses_upper_band(symbol7) and is_bearish_divergence_with_rsi(symbol7, timeframe,rsi_period) and (my_balance >= 10):
                    place_short_order(symbol7, Balance[0])
                    print('Short position taken')
            else:
                print('')
        else:
            print('Amount to trade: ', '0')

        if len(Opened_long) > 0 and (symbol_set[0] == symbol7):
            print('Opened Position: ', Open_long_price, symbol7, '   Amount: ','LONG', Opened_long, 'PNL: ',gain(Open_long_price[0], currency_price_symbol7))
            if (gain(Open_long_price[0], currency_price_symbol7) >= 0.0032) or (gain(Open_long_price[0], currency_price_symbol7) <= -0.001):
                close_position_long(symbol7)
                symbol_set.clear()
                if my_balance <= 5:
                    Balance[0] = Balance[0]+float(Finance.pop())
                    print('Amount to trade was added')
                    print('Wallet Balance : ', sum(Finance), 'Amount to trade: ', Balance[0])
                else:
                    print('')
                print('Position Closed')
            else:
                print('No Close')
        elif len(Opened_short) > 0 and (symbol_set[0] == symbol7):
            print('Opened Position: ', Open_short_price, symbol7, '   Amount: ','SHORT', Opened_short, 'PNL: ',-gain(Open_short_price[0], currency_price_symbol7))
            if (gain(Open_short_price[0], currency_price_symbol7) >= 0.001) or (gain(Open_short_price[0], currency_price_symbol7) <= -0.0032):
                close_position_short(symbol7)
                symbol_set.clear()
                if my_balance <= 5:
                    Balance[0] = Balance[0]+float(Finance.pop())
                    print('Amount to trade was added')
                    print('Wallet Balance : ', sum(Finance), 'Amount to trade: ', Balance[0])
                else:
                    print('')
                print('Position Closed')
            else:
                print('No Close')
        else:
            print('No Opened Trades')

        ##########################################################################
        currency_price_symbol8 = exchange.fetch_ticker(symbol8)['last']
        if len(Balance)>0:
            print('Amount to trade: ', my_balance)
            # Fetch current price
            ticker = exchange.fetch_ticker(symbol8)
            current_price = ticker['last']
            # Check for candlestick patterns
            for pattern in long_patterns:
                if detect_candlestick_pattern(symbol8, pattern, current_price) and is_bullish_divergence_with_rsi(symbol8, timeframe, rsi_period) and check_stochastic_strategy(symbol8) == 'long':
                    print(pattern)
                    place_long_order(symbol8, my_balance)
                    break

            for pattern in short_patterns:
                if detect_candlestick_pattern(symbol8, pattern, current_price) and is_bearish_divergence_with_rsi(symbol8, timeframe, rsi_period) and check_stochastic_strategy(symbol8) == 'short':
                    print(pattern)
                    place_short_order(symbol8, my_balance)
                    break

            if (len(Opened_long)) == 0 and (len(Opened_short)) == 0:
                if is_bullish_divergence_with_rsi(symbol8, timeframe, rsi_period):
                    print('####################################################')
                    close_candles_symbol8 = exchange.fetch_ohlcv(symbol8, timeframe=timeframe, limit=60)
                    close_prices_symbol8 = list(np.array([candle[4] for candle in close_candles_symbol8], dtype=float))
                    print('Price: ', close_prices_symbol8[-1], symbol8)
                    print('Bullish Divergence Confirmed')
                    print('####################################################')
                elif is_bearish_divergence_with_rsi(symbol8, timeframe, rsi_period):
                    print('####################################################')
                    close_candles_symbol8 = exchange.fetch_ohlcv(symbol8, timeframe=timeframe, limit=60)
                    close_prices_symbol8 = list(np.array([candle[4] for candle in close_candles_symbol8], dtype=float))
                    print('Price: ', close_prices_symbol8[-1], symbol8)
                    print('Bearish Divergence Confirmed')
                    print('####################################################')
                else:
                    print('')

                if is_price_crosses_lower_band(symbol8) and is_bullish_divergence_with_rsi(symbol8, timeframe,rsi_period) and (my_balance >= 10):
                    place_long_order(symbol8, my_balance)
                    print('Long position taken')
                elif is_price_crosses_upper_band(symbol8) and is_bearish_divergence_with_rsi(symbol8, timeframe,rsi_period) and (my_balance >= 10):
                    place_short_order(symbol8, Balance[0])
                    print('Short position taken')
            else:
                print('')

        else:
            print('Amount to trade: ', '0')

        if len(Opened_long) > 0 and (symbol_set[0] == symbol8):
            print('Opened Position: ', Open_long_price, symbol8, '   Amount: ','LONG', Opened_long, 'PNL: ',gain(Open_long_price[0], currency_price_symbol8))
            if (gain(Open_long_price[0], currency_price_symbol8) >= 0.0032) or (gain(Open_long_price[0], currency_price_symbol8) <= -0.001):
                close_position_long(symbol8)
                symbol_set.clear()
                if my_balance <= 5:
                    Balance[0] = Balance[0]+float(Finance.pop())
                    print('Amount to trade was added')
                    print('Wallet Balance : ', sum(Finance), 'Amount to trade: ','SHORT', Balance[0])
                else:
                    print('')
                print('Position Closed')
            else:
                print('No Close')
        elif len(Opened_short) > 0 and (symbol_set[0] == symbol8):
            print('Opened Position: ', Open_short_price, symbol8, '   Amount: ', Opened_short, 'PNL: ',-gain(Open_short_price[0], currency_price_symbol8))
            if (gain(Open_short_price[0], currency_price_symbol8) >= 0.001) or (gain(Open_short_price[0], currency_price_symbol8) <= -0.0032):
                close_position_short(symbol8)
                symbol_set.clear()
                if my_balance <= 5:
                    Balance[0] = Balance[0]+float(Finance.pop())
                    print('Amount to trade was added')
                    print('Wallet Balance : ', sum(Finance), 'Amount to trade: ', Balance[0])
                else:
                    print('')
                print('Position Closed')
            else:
                print('No Close')
        else:
            print('No Opened Trades')

        ##########################################################################
        currency_price_symbol9 = exchange.fetch_ticker(symbol9)['last']
        if len(Balance)>0:
            print('Amount to trade: ', my_balance)
            # Fetch current price
            ticker = exchange.fetch_ticker(symbol9)
            current_price = ticker['last']
            # Check for candlestick patterns
            for pattern in long_patterns:
                if detect_candlestick_pattern(symbol9, pattern, current_price) and is_bullish_divergence_with_rsi(symbol9, timeframe, rsi_period) and check_stochastic_strategy(symbol9) == 'long':
                    print(pattern)
                    place_long_order(symbol9, my_balance)
                    break

            for pattern in short_patterns:
                if detect_candlestick_pattern(symbol9, pattern, current_price) and is_bearish_divergence_with_rsi(symbol9, timeframe, rsi_period) and check_stochastic_strategy(symbol9) == 'short':
                    print(pattern)
                    place_short_order(symbol9, my_balance)
                    break

            if (len(Opened_long)) == 0 and (len(Opened_short)) == 0:
                if is_bullish_divergence_with_rsi(symbol9, timeframe, rsi_period):
                    print('####################################################')
                    close_candles_symbol9 = exchange.fetch_ohlcv(symbol9, timeframe=timeframe, limit=60)
                    close_prices_symbol9 = list(np.array([candle[4] for candle in close_candles_symbol9], dtype=float))
                    print('Price: ', close_prices_symbol9[-1], symbol9)
                    print('Bullish Divergence Confirmed')
                    print('####################################################')
                elif is_bearish_divergence_with_rsi(symbol9, timeframe, rsi_period):
                    print('####################################################')
                    close_candles_symbol9 = exchange.fetch_ohlcv(symbol9, timeframe=timeframe, limit=60)
                    close_prices_symbol9 = list(np.array([candle[4] for candle in close_candles_symbol9], dtype=float))
                    print('Price: ', close_prices_symbol9[-1], symbol9)
                    print('Bearish Divergence Confirmed')
                    print('####################################################')
                else:
                    print('')

                if is_price_crosses_lower_band(symbol9) and is_bullish_divergence_with_rsi(symbol9, timeframe,
                                                                                           rsi_period) and (
                        my_balance >= 10):
                    place_long_order(symbol9, my_balance)
                    print('Long position taken')
                elif is_price_crosses_upper_band(symbol9) and is_bearish_divergence_with_rsi(symbol9, timeframe,
                                                                                             rsi_period) and (
                        my_balance >= 10):
                    place_short_order(symbol9, Balance[0])
                    print('Short position taken')
            else:
                print('')
        else:
            print('Amount to trade: ', '0')

        if len(Opened_long) > 0 and (symbol_set[0] == symbol9):
            print('Opened Position: ', Open_long_price, symbol9, '   Amount: ','LONG', Opened_long, 'PNL: ',gain(Open_long_price[0], currency_price_symbol9))
            if (gain(Open_long_price[0], currency_price_symbol9) >= 0.0032) or (gain(Open_long_price[0], currency_price_symbol9) <= -0.001):
                close_position_long(symbol9)
                symbol_set.clear()
                if my_balance <= 5:
                    Balance[0] = Balance[0]+float(Finance.pop())
                    print('Amount to trade was added')
                    print('Wallet Balance : ', sum(Finance), 'Amount to trade: ', Balance[0])
                else:
                    print('')
                print('Position Closed')
            else:
                print('No Close')
        elif len(Opened_short) > 0 and (symbol_set[0] == symbol9):
            print('Opened Position: ', Open_short_price, symbol9, '   Amount: ','SHORT', Opened_short, 'PNL: ',-gain(Open_short_price[0], currency_price_symbol9))
            if (gain(Open_short_price[0], currency_price_symbol9) >= 0.001) or (gain(Open_short_price[0], currency_price_symbol9) <= -0.0032):
                close_position_short(symbol9)
                symbol_set.clear()
                if my_balance <= 5:
                    Balance[0] = Balance[0]+float(Finance.pop())
                    print('Amount to trade was added')
                    print('Wallet Balance : ', sum(Finance), 'Amount to trade: ', Balance[0])
                else:
                    print('')
                print('Position Closed')
            else:
                print('No Close')
        else:
            print('No Opened Trades')

        if my_balance> 30:
            Finance.append(Balance.pop())
        else:
            print('')

        print('New Wallet Balance: ', sum(Finance))

        ##########################################################################



    except Exception as e:
        print('An error occurred:', str(e))


    time.sleep(60)  # Sleep for 1 minute before checking the strategy again

