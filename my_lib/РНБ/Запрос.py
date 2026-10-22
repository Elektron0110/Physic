try:
	import requests as r
	def спросить (url, месяца: int = 15):
		return r.get(url, headers={
			'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/58.0.3029.110 Safari/537.3',
			'Accept-Language': 'ru-RU,ru;q=0.9,en-US;q=0.8,en;q=0.7'}, timeout=месяца)
	Wifi_без_интернета = r.ConnectionError
except: pass