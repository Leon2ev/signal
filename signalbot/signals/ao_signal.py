import time
from datetime import datetime

from data.data import Data
from pandas.core.series import Series
from ta.momentum import AwesomeOscillatorIndicator


class AOSignal():
    @staticmethod
    async def is_impulse(data: Data, symbol: str) -> bool:
        interval = '1h'
        ao_values = await AOSignal.get_ao_values(data, symbol, interval)

        if ao_values.size < 35:
            print(f'New coin: {symbol}')
            return False

        if ao_values[34] > 0 and ao_values[33] < 0:
            interval = '4h'
            ao_values = await AOSignal.get_ao_values(data, symbol, interval)

            if ao_values[34] > 0:
                return True

            else:
                return False

        else:
            return False

    @staticmethod
    async def get_ao_values(data, symbol, interval) -> Series:
        limit = str('36')
        klines_df = await data.get_klines_df(symbol, interval, limit)
        high = klines_df['High']
        low = klines_df['Low']
        ao_indicator = AwesomeOscillatorIndicator(high, low)
        return ao_indicator.awesome_oscillator()

    @staticmethod
    async def get_impulse_symbols(data: Data) -> list[str]:
        usdt_symbols = await data.usdt_market
        impulse_symbols: list[str] = list()

        for symbol in usdt_symbols:
            is_impulse = await AOSignal.is_impulse(data, symbol)

            if is_impulse:
                impulse_symbols.append(symbol)
        
        return impulse_symbols