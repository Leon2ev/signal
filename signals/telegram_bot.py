import requests
from typing import Union


class TelegramBot():
    def __init__(
        self,
        token: Union[str, None],
        chat_id: Union[str, None]
    ):
        self.token = token
        self.chat_id = chat_id

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