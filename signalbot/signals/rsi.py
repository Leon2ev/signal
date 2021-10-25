from signals.data import Data


class RSISignal():
	@staticmethod
	async def get(data: Data):
		signal_symbols = list()
		for symbol, df in data.klines_df_dict.items():
			if len(df.index) + 1 < 100:
				print(f'Not enough history data for: {symbol}')
			elif df['RSI'].gt(30).iloc[-3] and df['RSI'].lt(30).iloc[-2]:
				signal_symbols.append(symbol)

		signal_symbols.sort()
		return signal_symbols