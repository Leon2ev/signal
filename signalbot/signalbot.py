import asyncio
import time
from datetime import datetime

from binance import AsyncClient

from data.data import Data
from signals.ao_signal import AOSignal
from telegram_bot import TelegramBot


async def main() -> None:
    client = await AsyncClient.create()
    telegram_bot = TelegramBot()
    data = Data(client)

    while True:

        signal_symbols = await AOSignal.get_signal_symbols(data)
        msg = telegram_bot.compose_msg(signal_symbols)

        if msg:
            telegram_bot.send_msg(msg)

        # time.sleep(60 * (60 - datetime.now().minute))
        time.sleep(60 * ((60 - datetime.now().minute) % 15))


if __name__ == "__main__":

    loop = asyncio.get_event_loop()
    loop.run_until_complete(main())
