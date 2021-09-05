from data.data import Data
from pandas.core.series import Series


class AOSignal():
    @staticmethod
    async def get_signals(data: Data) -> str:
        impulse_symbols = await AOSignal.get_impulse_symbols(data)
        return await AOSignal.get_local_min_and_max(data, impulse_symbols)

    @staticmethod
    async def is_impulse(data: Data, symbol: str) -> bool:
        interval = str('1h')
        limit = int(36)
        klines_df = await data.get_klines_df(symbol, interval, limit)
        
        if klines_df['AO'].size < 35:
            print(f'Not enough history data for: {symbol}')
            return False
        
        if klines_df['AO'].gt(0).iloc[34] and klines_df['AO'].lt(0).iloc[33]:
            interval = str('4h')
            klines_df= await data.get_klines_df(symbol, interval, limit)
            
            if klines_df['AO'].size < 35:
                print(f'Not enough history data for: {symbol}')
                return False

            if klines_df['AO'].gt(0).iloc[34]:
                return True

            else:
                return False

        else:
            return False

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
    async def get_local_min_and_max(data: Data, symbols: list[str]) -> str:
        interval = str('1h')
        msg = f'\U0001F4C8 *BINGO*'
        
        for symbol in symbols:
            limit = int(100)
            klines_df = await data.get_klines_df(symbol, interval, limit)
            index = AOSignal.get_index_of_last_positive_ao(klines_df['AO'])
            min_low = klines_df['Low'].iloc[index:-1].min()
            max_high = klines_df['High'].iloc[-2:].max()
            msg = msg + f'\n\n*{symbol}* min: {min_low} max: {max_high}'

        return msg

    @staticmethod
    def get_index_of_last_positive_ao(ao_values: Series) -> int:

        '''Remove two last rows of Series because they are been used for signal.
        Remove from the Series all values less than zero. Return index of last row in Series'''
        
        greater_than_zero = ao_values.iloc[:-2].where(ao_values.gt(0)).dropna()
        
        return greater_than_zero.tail(1).index[0]
