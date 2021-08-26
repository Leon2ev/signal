from binance import AsyncClient


class MarketFilter():
    def __init__(
        self,
        client: AsyncClient
    ):
        self.client = client

    async def tickers(self):
        return await self.client.get_all_tickers()


    @property
    async def usdt(self) -> list[str]:
        tickers = await self.tickers()

        filtered_tickers = list(
            filter(lambda x: 
                x['symbol'][-4:] == 'USDT' and 
                x['symbol'][-8:-4] != 'DOWN' and
                x['symbol'][-8:-4] != 'BEAR' and
                x['symbol'][-8:-4] != 'BULL' and
                x['symbol'][-6:-4] != 'UP' and
                x['symbol'] != 'USDSBUSDT', tickers
            )
        )
        
        symbols = [x['symbol'] for x in filtered_tickers]
        symbols.sort()
        return symbols
