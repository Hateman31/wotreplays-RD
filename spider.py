import os
import requests as r
from bs4 import BeautifulSoup as bs

class Site:
	def __init__(self,url):
		self.url = url
		self.start_url = url
		self.page = 0
		self.new_url = None
		self.html = None
		self.max_page_number = 0
		
	def openPage(self):
		#Если загрузка упала - вернуть сообщение об этом	
		try:
			self.html = bs(r.get(self.url,timeout=30).content,"html5lib")
		except:
			print('Loading crash! Try later')
			raise
		print('prepare_next_URL')
		if not self.page:
			self.max_page_number = self.last_page_number()
		self.page+=1
		self.prepare_next_URL()
	
	#@property	
	#def NotLastPage(self):
	def notLastPage(self):
		return self.page < self.max_page_number
		#return (self.start_url != self.new_url)
	
	def prepare_next_URL(self):
		print('Old URL: ',self.url)
		if 'page' in self.url:
			num = int(self.url[-2])+1
			self.url = self.new_url = self.url[:-2]+str(num)+'/'
		else:
			self.url = self.new_url = self.url+'page/2/'
		print('New URL: ',self.url)
	
	def next_page_exists(self):
		pass

	def last_page_number(self):
		css = 'script[type="text/javascript"]'
		text = self.html.select(css)[-1].text
		text = text.split('total:')[-1]
		return int(text.split(',')[0])
		
if __name__ == "__main__":
	test_url = 'https://wotreplays.ru/site/index/version/43/tank/837/map/5/battle_type/1/sort/uploaded_at.desc/'
	test = Site(test_url)
	test.openPage()
	print(test.last_page_number())
