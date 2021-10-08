from pandas.core.frame import DataFrame
from pandas import DataFrame
from signals.data import Data

class RSIDivergence():
	def __init__(self, data: Data) -> None:
		self.data = data
		self.lower_barrier = 30
		self.width = 100
			
	async def get(self) -> list[dict[str, str]]:
		signals = list()
		for symbol, df in self.data.klines_df_dict.items():
			signal = self.bullish_divergence(symbol, df)
			if signal:
				signals.append(signal)

		return signals

	def bullish_divergence(self, symbol, df: DataFrame) -> dict[str, str]:
		signal= dict()
		data_length = len(df['RSI'])
		for i in range(data_length):
			
			try:
				if df['RSI'].lt(self.lower_barrier).iloc[i]:

					for a in range(i + 1, i + self.width):

						if a > 75 and df['RSI'].gt(self.lower_barrier).iloc[a]:
							
							for r in range(a + 1, a + self.width):
								
								if df['RSI'].lt(self.lower_barrier).iloc[r] and \
									df['RSI'].iloc[r] > df['RSI'].iloc[i] and \
									df['Close'].iloc[r] < df['Close'].iloc[i]:
									
									for s in range(r + 1, r + self.width):
										
										if df['RSI'].gt(self.lower_barrier).iloc[s]:
											time = data_length - s
											signal = dict(symbol=symbol, time=time)
											break
										
										else:
											continue
								else:
									continue
						else:
							continue
				else:
					continue
			
			except IndexError:
				pass

		return signal
 # Bearish Divergence
#  for i in range(len(Data)):
    
#     try:
#         if Data[i, 4] > upper_barrier:
            
#             for a in range(i + 1, i + width): 
#                 if Data[a, 4] < upper_barrier:
#                     for r in range(a + 1, a + width):
#                         if Data[r, 4] > upper_barrier and \
#                         Data[r, 4] < Data[i, 4] and Data[r, 3] >                 43                        Data[i, 3]:
#                             for s in range(r + 1, r + width):
#                                 if Data[s, 4] < upper_barrier:
#                                     Data[s + 1, 6] = -1
#                                     break
#                                 else:
#                                     continue
#                         else:
#                             continue
#                     else:
#                         continue
#                 else:
#                     continue
#     except IndexError:
#         pass