import asyncio
from typing import Any, Union

from binance.client import AsyncClient
from pandas import DataFrame as df
from pandas.core.frame import DataFrame
from ta.momentum import AwesomeOscillatorIndicator, RSIIndicator


class Data():
	def __init__(self, binance: AsyncClient) -> None:
		self.binance = binance
		self._usdt_market = list()
		self._klines_df_dict = dict()


	async def tickers(self) -> Union[list[dict[str, str]], None]:
		try:
			return await self.binance.get_all_tickers()
		except Exception as e:
			print(e)


	async def set_usdt_market(self) -> None:
		tickers = await self.tickers()
		if tickers:
			filtered_tickers = list(
				filter(lambda x: 
					x['symbol'][-4:] == 'USDT' and 
					x['symbol'][-8:-4] != 'DOWN' and
					x['symbol'][-8:-4] != 'BEAR' and
					x['symbol'][-8:-4] != 'BULL' and
					x['symbol'][-6:-4] != 'UP' and
					x['symbol'] != 'BCCUSDT' and
					x['symbol'] != 'BCHSVUSDT' and
					x['symbol'] != 'HCUSDT' and
					x['symbol'] != 'MCOUSDT' and
					x['symbol'] != 'EURUSDT' and
					x['symbol'] != 'USDSBUSDT' and
					x['symbol'] != 'USDPUSDT' and
					x['symbol'] != 'SUSDUSDT' and
					x['symbol'] != 'BUSDUSDT', tickers))

			self._usdt_market = [x['symbol'] for x in filtered_tickers]

	@property
	def usdt_market(self):
		return self._usdt_market

	
	async def klines(self, symbol: str, interval: str, limit: int) -> Union[dict[Any, Any], None]:
		try:
			return await self.binance.get_klines(
				symbol=symbol,
				interval=interval,
				limit=limit)
		except Exception as e:
			print(e)


	async def get_klines_df(self, symbol: str, interval: str, limit: int) -> DataFrame:
		klines = await self.klines(symbol, interval, limit)

		klines_df =  df(klines, columns=[
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

		klines_df['High'] = klines_df['High'].astype('float64')
		klines_df['Low'] = klines_df['Low'].astype('float64')
		klines_df['Close'] = klines_df['Close'].astype('float64')

		ao = AwesomeOscillatorIndicator(klines_df['High'], klines_df['Low'])
		klines_df['AO'] = ao.awesome_oscillator()
		klines_df['AO'] = klines_df['AO'].astype('float64')

		rsi = RSIIndicator(klines_df['High'])
		klines_df['RSI'] = rsi.rsi()
		klines_df['RSI'] = klines_df['RSI'].astype('float64')

		return klines_df


	async def set_klines_df_dict(self, symbol: str, interval: str, limit: int) -> None:
		self._klines_df_dict[symbol] = await self.get_klines_df(symbol, interval, limit)


	async def gather_klines_df(self, interval, limit):
		if self.usdt_market:
			try:
				await asyncio.gather(*[self.set_klines_df_dict(symbol, interval, limit) for symbol in self.usdt_market])
			except Exception as e:
				print(e)
		else:
			print('Market is empty')


	@property
	def klines_df_dict(self):
		return self._klines_df_dict
