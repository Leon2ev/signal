from data.data import Data
from pandas.core.series import Series
from ta.momentum import AwesomeOscillatorIndicator


class AOSignal():
    @staticmethod
    async def is_impulse(data: Data, symbol: str) -> bool:
        interval = str('1h')
        limit = int(36)
        ao_values = await AOSignal.get_ao_values(data, symbol, interval, limit)

        if ao_values.size < 35:
            print(f'New coin: {symbol}')
            return False

        if ao_values[34] > 0 and ao_values[33] < 0:
            interval = str('4h')
            ao_values = await AOSignal.get_ao_values(data, symbol, interval, limit)

            if ao_values[34] > 0:
                return True

            else:
                return False

        else:
            return False

    @staticmethod
    async def get_ao_values(data: Data, symbol: str, interval: str, limit: int) -> Series:
        klines_df = await data.get_klines_df(symbol, interval, limit)
        high = klines_df['High']
        low = klines_df['Low']
        ao_indicator = AwesomeOscillatorIndicator(high, low)
        return ao_indicator.awesome_oscillator()

    @staticmethod
    async def get_impulse_symbols(data: Data) -> list[str]:
        symbols = await data.usdt_market
        impulse_symbols: list[str] = list()

        for symbol in symbols:
            is_impulse = await AOSignal.is_impulse(data, symbol)

            if is_impulse:
                impulse_symbols.append(symbol)
        
        return impulse_symbols

    @staticmethod
    async def get_local_minimum(data: Data, symbols: list[str]):
        interval = str('1h')
        
        for symbol in symbols:
            limit = int(100)
            ao_values = await AOSignal.get_ao_values(data, symbol, interval, limit)
            index = AOSignal.get_index_of_last_positive_ao(ao_values)
            limit = limit - index + 1
            klines_df = await data.get_klines_df(symbol, interval, limit)
            min_low = klines_df['Low'].min()
            max_high = klines_df['High'].max()
            print(f'{symbol} min: {min_low} max: {max_high}')

    @staticmethod
    def get_index_of_last_positive_ao(ao_values: Series) -> int:

        '''Remove two last rows of Series because they are been used for signal.
        Remove from the Series all values less than zero. Return index of last row in Series'''

        zero_float = float(0)
        greater_than_zero = ao_values.iloc[:-2].where(ao_values > zero_float).dropna()
        
        return greater_than_zero.tail(1).index[0]