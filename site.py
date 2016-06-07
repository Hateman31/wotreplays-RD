import os
import requests as r
from bs4 import BeautifulSoup as bs

class Site:
	def __init__(self,url):
		self.url = url
		self.start_url = url
		self.page = 1
		self.new_url = None
		
	def openPage(self):
		#Если загрузка упала - вернуть сообщение об этом	
		try:
			self.html = bs(r.get(url,timeout=30).content,"html5lib")
			self.prepare_next_URL()
		except:
			print('Loading crash! Try later')
			return
	
	#@property	
	#def NotLastPage(self):
	def notLastPage(self):
		return (self.start_url != self.new_url)
	
	def prepare_next_URL(self):
		# something do ...
		if 'page' in self.url:
			num = str(int(url[-2])+1)
			self.url =url[:-2]+num+'/'
		else:
			url = url+'page/2/'
		return url
