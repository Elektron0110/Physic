try:
	from bs4 import BeautifulSoup as bs
	from bs4 import Tag
	class Суп(bs):
		def варить (
				self,
				name = None,
				attrs = {},
				recursive: bool = True,
				string = None,
				**kwargs):
			return self.find(name, attrs, recursive, string, **kwargs)
	# class Бульон (Tag):
	# 	def варить_дальше (
	# 			self,
	# 			name = None,
	# 			attrs = {},
	# 			string = None,
	# 			**kwargs):
	# 		return self.find_previous(name, attrs, string, **kwargs)
	# 	def варить (
	# 			self,
	# 			name = None,
	# 			attrs = {},
	# 			recursive: bool = True,
	# 			string = None,
	# 			**kwargs):
	# 		return self.find(name, attrs, recursive, string, **kwargs)
	# 	def варить_дальше (
	# 			self,
	# 			name = None,
	# 			attrs = {},
	# 			string = None,
	# 			**kwargs):
	# 		return self.find_next(self, name, attrs, string, **kwargs)
	# 	def читать (self,
	# 				separator: str = "",
	# 				strip: bool = True) -> str:
	# 		return self.get_text(separator, strip)
except: pass