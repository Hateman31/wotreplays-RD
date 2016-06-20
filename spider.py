import os
import requests as r
import bs4
from bs4 import BeautifulSoup as bs

class ConnectionError(r.exceptions.ConnectionError):
	pass
	
class Site:
	def __init__(self,url):
		self.url = url
		self.page = 1
		self.max_page_number = 0
		self.html = None
		self.openPage()
		
	def openPage(self):
		#Если загрузка упала - вернуть сообщение об этом	
		try:
			self.html = bs(r.get(self.url,timeout=30).content,"html5lib")
		#~ except:
			#~ print('Loading crash! Try later')
			#~ raise
		except bs4.FeatureNotFound:
			#~ self.html = bs(r.get(self.url,timeout=30).content)
			self.html = bs(r.get(self.url,timeout=30).content,"html.parser")
		if self.page == 1:
			self.max_page_number = self.last_page_number()
		self.page+=1
		self.prepare_next_URL()
	
	#@property	
	#def NotLastPage(self):
	def notLastPage(self):
		return self.page < self.max_page_number
	
	def prepare_next_URL(self):
		if 'page' in self.url:
			num = int(self.url[-2])+1
			self.url = self.url[:-2]+str(num)+'/'
		else:
			self.url = self.url+'page/2/'
		#self.url = self.url[:-2]+str(self.page)+'/'
	
	def last_page_number(self):
		css = 'script[type="text/javascript"]'
		text = self.html.select(css)[-1].text
		text = text.split('total:')[-1]
		return int(text.split(',')[0])
		
if __name__ == "__main__":
	test_url = 'https://wotreplays.ru/site/index/version/43/tank/837/map/5/battle_type/1/sort/uploaded_at.desc/'
	test = Site(test_url)
	test.openPage()
	print('last_page_number: ',test.last_page_number())
