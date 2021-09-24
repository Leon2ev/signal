from data.data import Data


class AOSignal(Data):
    @staticmethod
    async def get_signal_symbols(data: Data) -> list[str]:
        symbols = await data.usdt_market
        signal_symbols = list()

        for symbol in symbols:
            interval = str('15m')
            limit = int(100)
            klines_df = await data.get_klines_df(symbol, interval, limit)

            if klines_df['AO'].size < 99:
                print(f'Not enough history data for: {symbol}')
            else:
                less_than_zero = klines_df.where(klines_df['AO'].iloc[:-1].lt(0)).dropna()

                if less_than_zero.empty == True:
                    print('Empty DataFrame')
                else:
                    last_negative_ao_index = less_than_zero.tail(1).index[0]
                    high_period = klines_df['High'].iloc[last_negative_ao_index:]

                    if 10 > high_period.size > 4 and high_period.idxmax() == 97:
                        interval = str('1h')
                        limit = int(36)
                        klines_df = await data.get_klines_df(symbol, interval, limit)

                        if klines_df['AO'].size > 35 and klines_df['AO'].gt(0).iloc[34]:
                            signal_symbols.append(symbol)

        return signal_symbols
