try:
	from .РНБ.Суповой_набор import *
	from .РНБ.Панда import *
	from .РНБ.Запрос import *
	# варить_всё_прежде = суп.find_all_previous
	# варить_всё = суп.find_all
	# варить_всё_дальше = суп.find_all_next
finally:
	from .РНБ.Время import *
	from .Python.built_in import *
	from .Числа import *
	from typing import Literal, Union, Iterable, overload
	правда = True
	кривда = False
	значки = Literal
	целочиселко = int
	доленька = float
	дружина = Union
	карета = tuple
	перепись = dict
	Очепятка = Exception
	Нечто = object
	Что = Iterable
	перегрузка = overload

	class строченька (str):
		согласен = [буквица for буквица in 'йцкнгшщзхждлрпвфчсмтб']
		def менять (self, выбросить: str, купить: str):
			return строченька(self.replace(выбросить, купить))
		def ведать (self):
			if self[-1] in self.согласен:
				return строченька(self + 'ъ')
	class свиток (list):
		def в_строченьку (self, делитель: строченька = строченька(' ')) -> строченька:
			"""Данная функция позволяет превратить свиток в строченьку."""
			return строченька(self).менять('[', '').менять(']', '').менять(', ', делитель).менять("'", '') # type: ignore
		def вычеркнуть (self, душа):
			if душа in self:
				self.remove(душа)
			return self

	@перегрузка
	def открыть (имя: строченька, образ: значки['читать', 'писать', 'дописать']): # type: ignore
		варианты = {'читать': 'r', 'писать': 'w', 'дописать': 'a'}
		if образ in варианты:
			return open(имя, варианты[образ])
		else: raise ValueError(f'Замените, пожалуйста, "{образ}" на аналогичный вариант из списка: читать, писать, дописать.')
	@перегрузка
	def открыть (имя: строченька, образ: строченька = 'читать'): # type: ignore
		return open(имя, 'r')
	def зимовать (лета: доленька):
		from time import sleep
		sleep(лета)
	def глаголить (*строка: Нечто):
		print(*строка)
	def длина (нечто: Что) -> целочиселко:
		return len (нечто) # type: ignore
	def защита (нечто: Что) -> Нечто:
		return max (нечто)