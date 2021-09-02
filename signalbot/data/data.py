import pandas as pd
from binance import AsyncClient
from pandas import DataFrame as df


class Data():
    def __init__(self, client: AsyncClient):
        self.client = client

    async def tickers(self) -> list[dict[str, str]]:
        return await self.client.get_all_tickers()

    async def get_klines_df(self, symbol: str, interval: str, limit: int) -> df:
        klines = await self.client.get_klines(
            symbol=symbol,
            interval=interval,
            limit=limit)

        klines_df =  df(klines, columns=[
            'Open Time',
            'Open',
            'High',
            'Low',
            'Close',
            'Volume',
            'Close Time',
            'Quote Volume',
            'Trades',
            'Taker buy base',
            'Taker buy quote',
            'Ignore'])

        klines_df['High'] = pd.to_numeric(klines_df['High'])
        klines_df['Low'] = pd.to_numeric(klines_df['High'])

        return klines_df

    @property
    async def usdt_market(self) -> list[str]:
        tickers = await self.tickers()

        filtered_tickers = list(
            filter(lambda x: 
                x['symbol'][-4:] == 'USDT' and 
                x['symbol'][-8:-4] != 'DOWN' and
                x['symbol'][-8:-4] != 'BEAR' and
                x['symbol'][-8:-4] != 'BULL' and
                x['symbol'][-6:-4] != 'UP' and
                x['symbol'] != 'USDSBUSDT' and
                x['symbol'] != 'BUSDUSDT', tickers))
        
        symbols = [x['symbol'] for x in filtered_tickers]
        symbols.sort()
        return symbols
