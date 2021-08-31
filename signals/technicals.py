import time
from datetime import datetime

import pandas as pd
from binance import AsyncClient
from pandas import DataFrame as df
from ta.momentum import AwesomeOscillatorIndicator
from telegram_bot import TelegramBot


class AwesomeOscillator():
    def __init__(
        self,
        symbols: list[str],
        client: AsyncClient,
        telegram_bot: TelegramBot
    ):
        self.symbols = symbols
        self.client = client
        self.telegram_bot = telegram_bot

    async def get_ao(self, symbol: str, interval: str) -> None:

        '''Get Awesome Oscillator(AO) values for the last two closed candles
        on 1h time frame(TF) in this case indexes 33 and 34. If the value of 
        33 is less than 0 and the value of 34 is greater than 0 then we confirm 
        signal on 4h TF. If the last closed candle on 4h has AO value greater
        than 0 then signal is sent'''

        candles = await self.client.get_klines(
            symbol=symbol,
            interval=interval,
            limit=36)

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
            'Ignore'])

        high = pd.to_numeric(candles_df['High'])
        low = pd.to_numeric(candles_df['Low'])
        indicator = AwesomeOscillatorIndicator(high, low)
        ao_values = indicator.awesome_oscillator()
        if ao_values[34] > 0 and ao_values[33] < 0:
            if interval == '1h':
                interval = str(self.client.KLINE_INTERVAL_4HOUR)
                await self.get_ao(symbol, interval)
            else:
                self.telegram_bot.send_msg(f'{symbol} BINGO!')

    async def run(self) -> None:
        interval = str(self.client.KLINE_INTERVAL_1HOUR)
        while True:
            for symbol in self.symbols:
                await self.get_ao(symbol, interval)

            time.sleep(60 * (60 - datetime.now().minute))