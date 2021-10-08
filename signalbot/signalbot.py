import asyncio
import time
from datetime import datetime

from binance import AsyncClient

from signals.awesome import AOSignal
from signals.data import Data
from signals.rsi_divergence import RSIDivergence
from telegram_bot import TelegramBot


async def main() -> None:
    binance_client = await AsyncClient.create()
    data = Data(binance_client)
    telegram_bot = TelegramBot()

    await data.set_usdt_market()

    while True:
        await data.gather_klines_df('1h', 100)

        ao_signals = await AOSignal.get(data)
        rsi = RSIDivergence(data)
        rsi_signals = await rsi.get()
        
        messages = telegram_bot.compose_msg(ao_signals, rsi_signals)
        if messages:
            telegram_bot.send_msg(messages)

        time.sleep(60 * (60 - datetime.now().minute))


if __name__ == "__main__":
    loop = asyncio.get_event_loop()
    loop.run_until_complete(main())
