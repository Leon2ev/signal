from signals.data import Data


class AOSignal():
	@staticmethod
	async def get(data: Data):
		signal_symbols = list()
		for symbol, df in data.klines_df_dict.items():
			if len(df.index) + 1 < 100:
				print(f'Not enough history data for: {symbol}')
			else:
				less_than_zero = df.where(df['AO'].iloc[:-1].lt(0)).dropna()

				if less_than_zero.empty == True:
					print('Empty DataFrame')
				else:
					last_negative_ao_index = less_than_zero.tail(1).index[0]
					high_period = df['High'].iloc[last_negative_ao_index:]

					if 10 > high_period.size > 4 and high_period.idxmax() == 97:
						interval = str('1d')
						limit = int(36)

						df = await data.get_klines_df(symbol, interval, limit)
						if df['AO'].size > 35 and df['AO'].gt(0).iloc[34]:
							signal_symbols.append(symbol)

		signal_symbols.sort()
		return signal_symbols
