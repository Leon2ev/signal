import os
from typing import Any, Union

from pymongo import MongoClient

db_url = os.getenv("MONGO_DB")
client: MongoClient
if db_url:
    client = MongoClient(db_url)
else:
    client = MongoClient('localhost', 27017)

db = client['signals']
signals = db['signals']

class Signals():

    def insert_item(self, time: dict[str,Any]) -> None:
        signals.insert_one(time)

    def get_item(self) -> Union[dict[str,Any], None]:
        return signals.find_one()

    def update_item(self, filter, value):
        signals.update_one(filter, value)

    
