"""Функции созданные лично мной."""
from datetime import datetime, timedelta
from time import sleep
from typing import Any, Iterable, Literal, overload, override

loadpage_name = None
loadpage_dir = ''

def file_to_list (name: str, sep: str = '\n', code='utf-8', sort=True) -> list[str]:
	"""Эта функция упращает превращение файла в список значений, разделённых в файле опледелённым разделителем."""
	f = open(name, 'r', encoding=code)
	f = f.read().split(sep)
	if sort:
		f.sort()
	return f
def list_to_str (list: list, sep = ' '):
	"""Эта функция упращает превращение файла в список значений, разделённых в файле опледелённым разделителем."""
	f = str(list)
	f = f.replace("'", '').replace('[', '').replace(']', '').replace(', ', sep)
	return f
def remainder(paper: list[Any], element: Any, timer: float | timedelta):
	i = paper.index(element)
	rem = (len({a for a in paper}) - i) * timer
	return rem
class Timer:
	def __init__(self):
		pass
	def start(self):
		self.start_time = datetime.now()
	def stop(self, sec=True):
		return (datetime.now()-self.start_time) if not sec else (datetime.now()-self.start_time).total_seconds()
	def __str__(self):
		return f'{datetime.now()} {self.start_time} {datetime.now()-self.start_time}'
	def __call__(self, sec=True):
		delta = (datetime.now()-self.start_time) if not sec else (datetime.now()-self.start_time).total_seconds()
		self.start_time = datetime.now()
		return delta
def loadpage(url, name=None, type='html', headers=None):
	import requests
	with requests.Session() as sess:
		web = sess.get(url, timeout=60, headers=headers)
		web.raise_for_status ()
		sleep(1)
		page = web.content
		if not name and not loadpage_name:
			if page.decode().find('<title>') != -1:
				name = page.decode()[page.decode().find('<title>')+7:page.decode().find('</title>')]
			else:
				name = url[8:]
		elif not name: name = loadpage_name
		name = name.replace('/','_').replace('?', '.').replace(':', '').replace('*', '').replace('|', '')
		print(f'{loadpage_dir}{name}.{type}')
		open(f'{loadpage_dir}{name}.{type}', 'wb').write(page)
	return f'{loadpage_dir}{name}.{type}'
class Log:
	def __init__(self, file: str = 'logger.log', method: str = "a") -> None:
		self.file, self.comm = file, f"open(file, 'a', encoding='utf-8')"
		open(file, method, encoding='utf-8').close()
	def log(self, *string: str, slice: str = ' ', fw: str | tuple[str, ...] = '', fp: str | tuple[str, ...] = '') -> str:
		if isinstance(fw, tuple): fw = ''.join(map(str, fw))
		if isinstance(fp, tuple): fp = ''.join(map(str, fp))
		if string is None: string = ''
		u_string = ''.join(map(str, string))
		eval(self.comm, {'file': self.file}).write(u_string+((slice+fw) if fw else '')+'\n')
		print(u_string+((slice+fp) if fp else ''))
		return f'Added: {u_string+((slice+fw) if fw else '')}\nPrint: {u_string+((slice+fp) if fw else '')}'
	def __str__(self) -> str:
		return f'Logger to {self.file}.'
@overload
def is_sublist(this: Iterable, into: Iterable, t: Literal['list']) -> list[bool]: ...
@overload
def is_sublist(this: Iterable, into: Iterable, t: Literal['bool']) -> bool: ...
def is_sublist(this: Iterable, into: Iterable, t: Literal['bool'] | Literal['list']) -> bool | list[bool]:
	if t == 'list': return [i in into for i in this]
	elif t == 'bool': return False not in [i in into for i in this]
	else: raise ValueError(f"Value of t must be 'bool' or 'list', not {t}.")

def singleton(cls):
	my_class = ''
	def get(*args, **kwargs):
		nonlocal my_class
		if not my_class:
			my_class = cls
		if args or kwargs:
			my_class = my_class(*args, **kwargs)
		return my_class
	return get