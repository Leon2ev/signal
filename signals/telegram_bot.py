import requests

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
                '&parse_mode=Markdown&text=' + msg
            )

            requests.get(url)

        elif not self.token:
            print('Token missing')

        else:
            print('Chat id missing')
