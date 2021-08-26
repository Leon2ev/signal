import asyncio
import time
from datetime import datetime, timedelta
from typing import Any

from binance import AsyncClient
from bson.objectid import ObjectId

from backup import Signals
from config import telegram_chat_id, telegram_token
from marker_filter import MarketFilter
from technicals import AwesomeOscillator
from telegram_bot import TelegramBot


async def main() -> None:
    client = await AsyncClient.create()
    
    market_filter = MarketFilter(client)
    usdt_symbols = await market_filter.usdt

    awesome_oscilator = AwesomeOscillator(usdt_symbols, client)
    await awesome_oscilator.run()

    telegram_bot = TelegramBot(telegram_token, telegram_chat_id)

    def rounder(time: datetime) -> datetime:
        # Example: Round time from 16:31:49 to 16:00:00
        return time.replace(second=0, microsecond=0, minute=0)

    def getPastTime() -> int:
        # Get last hour in milliseconds
        lastHourDateTime = datetime.now() - timedelta(hours=1)
        roundedDateTime = rounder(lastHourDateTime)
        return int(roundedDateTime.timestamp() * 1000)

    signals = Signals()

    while True:
        start_time_ts = getPastTime()
        signal = signals.get_item()
        
        if not signal:
            print('Signal time added to DB')
            signals.insert_item(dict(start_date_ts=start_time_ts))
        else:
            if signal['start_date_ts'] == start_time_ts:
                minutes_left = 60 - datetime.now().minute
                print(f'Wait for new signal: {minutes_left} min')
                time.sleep(60 * minutes_left)
                print('Update signal time in DB')
                signal_filter = dict(_id=ObjectId(signal['_id']))
                signals.update_item(signal_filter, {'$set': {'start_date_ts': start_time_ts}})
                
        start_date_time = datetime.fromtimestamp(start_time_ts / 1000)
        start_date = start_date_time.date()
        start_time = start_date_time.time()
        msg_time = f'\U0001F4C5{start_date} \u23F0{start_time}'
        msg_buy = f'\n\n\U0001F4C8 *BUY*'
        msg_sell = f'\n\n\U0001F4C9 *SELL*'

        # Fetch last hour candle for each USDT pair
        # Filter candles by BUY or SELL market power
        for symbol in usdt_symbols:
            candles = await client.get_klines(symbol=symbol, interval=client.KLINE_INTERVAL_1HOUR, startTime=start_time_ts, limit=1)
            if candles:
                candle = candles[0]
                candlesticks: dict[str, Any] = dict()
                candlesticks['quote_volume']=float(candle[7])
                candlesticks['buy_quote']=float(candle[10])
                candlesticks['signal']=candlesticks['buy_quote'] / candlesticks['quote_volume']
                signal = round(candlesticks['signal'], 2)
                if candlesticks['signal'] > 0.7:
                    msg = f'\n*{symbol}* _{signal}_'
                    msg_buy = msg_buy + msg
                elif candlesticks['signal'] < 0.3:
                    msg = f'\n*{symbol}* _{signal}_'
                    msg_sell = msg_sell + msg

        msg = msg_time + msg_buy + msg_sell
        telegram_bot.send_msg(msg)
        time.sleep(60 * (60 - datetime.now().minute))


if __name__ == "__main__":

    loop = asyncio.get_event_loop()
    loop.run_until_complete(main())
