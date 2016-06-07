import os
import requests as r
from bs4 import BeautifulSoup as bs

class Site:
	def __init__(self,url):
		self.url = url
		self.start_url = url
		self.new_url = None
		
	def openPage(self):
		#Если загрузка упала - вернуть сообщение об этом	
		try:
			self.html = bs(r.get(url,timeout=30).content,"html5lib")
			self.url = self.new_url = self.nextPage()
		except:
			print('Loading crash! Try later')
			return
		
	def notLastPage(self):
		return (self.start_url != self.new_url)
	
	def nextPage(self):
		# something do ...
		return url
