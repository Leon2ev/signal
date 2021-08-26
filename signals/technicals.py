import time
from datetime import datetime

import pandas as pd
from binance import AsyncClient
from pandas import DataFrame as df
from ta.momentum import AwesomeOscillatorIndicator


class AwesomeOscillator():
    def __init__(
        self,
        symbols: list[str],
        client: AsyncClient
    ):
        self.symbols = symbols
        self.client = client

    async def run(self) -> None:

        '''Loop through the symbols and fetch candles every hour.
        Get Awesome Oscillator values for the last two closed candles
        in this case indexes 33 and 34. If the value of 33 is less
        than 0 and the value of 34 is greater than 0 signal is sent.'''

        while True:
            for symbol in self.symbols:
                candles = await self.client.get_klines(
                    symbol=symbol,
                    interval=self.client.KLINE_INTERVAL_1HOUR,
                    limit=36
                )

                candles_df = df(candles, columns=[
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
                'Ignore'
                ])

                high = pd.to_numeric(candles_df['High'])
                low = pd.to_numeric(candles_df['Low'])
                indicator = AwesomeOscillatorIndicator(high, low)
                ao_values = indicator.awesome_oscillator()
                if ao_values[34] > 0 and ao_values[33] < 0:
                    print(symbol, 'bingo')

            time.sleep(60 * (60 - datetime.now().minute))

    
    
    