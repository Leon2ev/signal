from typing import Union
import requests
from typing import Union

from config import telegram_chat_id, telegram_token


class TelegramBot():
    def __init__(self):
        self.token = telegram_token
        self.chat_id = telegram_chat_id

    def send_msg(self, msg: str) -> None:
        if self.token and self.chat_id:
            
            url = ( 
                'https://api.telegram.org/bot' + self.token +
                '/sendMessage?chat_id=' + self.chat_id +
                '&parse_mode=Markdown&text=' + msg +
                '&disable_web_page_preview=True'
            )

            requests.get(url)

        elif not self.token:
            print('Token missing')

        else:
            print('Chat id missing')

    def compose_msg(self, ao_signal) -> Union[str, None]:
        if ao_signal:
            msg = f'\u2705 *AO Signal*'
            for signal in ao_signal:
                msg += f'\n\n*{signal}* \U0001F4C8 [Chart](https://www.binance.com/en/trade/{signal[:-4]}_{signal[-4:]})'
            
            return msg