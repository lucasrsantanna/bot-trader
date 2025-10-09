import pandas as pd

def calculate_rsi(df, window=14):
    delta = df["close"].diff()
    gain = (delta.where(delta > 0, 0)).rolling(window=window).mean()
    loss = (-delta.where(delta < 0, 0)).rolling(window=window).mean()

    rs = gain / loss
    rsi = 100 - (100 / (1 + rs))
    df["rsi"] = rsi
    return df

def calculate_macd(df, fast_period=12, slow_period=26, signal_period=9):
    exp1 = df["close"].ewm(span=fast_period, adjust=False).mean()
    exp2 = df["close"].ewm(span=slow_period, adjust=False).mean()
    macd = exp1 - exp2
    signal = macd.ewm(span=signal_period, adjust=False).mean()
    histogram = macd - signal

    df["macd"] = macd
    df["macd_signal"] = signal
    df["macd_hist"] = histogram
    return df

def calculate_moving_average(df, window=20, type='sma'):
    if type == 'sma':
        df[f"sma_{window}"] = df["close"].rolling(window=window).mean()
    elif type == 'ema':
        df[f"ema_{window}"] = df["close"].ewm(span=window, adjust=False).mean()
    return df

def calculate_volume_ma(df, window=20):
    df[f"volume_ma_{window}"] = df["volume"].rolling(window=window).mean()
    return df

# Exemplo de uso
if __name__ == '__main__':
    # Criar um DataFrame de exemplo
    data = {
        'close': [10, 11, 12, 13, 14, 15, 14, 13, 12, 11, 10, 9, 10, 11, 12, 13, 14, 15, 16, 17, 18, 19, 20, 21, 22, 23, 24, 25, 26, 27],
        'volume': [100, 110, 120, 130, 140, 150, 140, 130, 120, 110, 100, 90, 100, 110, 120, 130, 140, 150, 160, 170, 180, 190, 200, 210, 220, 230, 240, 250, 260, 270]
    }
    df_test = pd.DataFrame(data)

    df_test = calculate_rsi(df_test)
    df_test = calculate_macd(df_test)
    df_test = calculate_moving_average(df_test, window=10, type='sma')
    df_test = calculate_moving_average(df_test, window=10, type='ema')
    df_test = calculate_volume_ma(df_test)

    print(df_test.tail())

