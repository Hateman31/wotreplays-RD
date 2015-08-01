from kivy.app import App
from kivy.uix.boxlayout	import BoxLayout
import json
import os
import requests as r
from bs4 import BeautifulSoup as bs
import tools

with open('data1') as f:
	data = json.loads(f.read())

class Root(BoxLayout):
	keys = ('tank','map','battle_type')
	tanks,maps,battles = map(sorted,(data[x] for x in keys))
	# def action(self,tank=None,_map=None,battle=None):
	def action(self,*args):
		#как внутри функции использовать поля
		#объектов из kv
		url = query('???')
		linx = []
		flag = None
		while 1:
			site = bs(r.get(url).content)
			if not flag:
				flag = site.find('a').get('href')
			else:
				flag1 = site.find('a').get('href')
				if flag1 == flag: 
					break
			for replay in site.select('div.r-info')[:-1]:
				rec = tools.record(replay)
				if tools.isGood(rec,pars):
					linx+=[rec['url']]
					if limit:
						limit-=1
					else:
						break
			#try:
			 #'...' - some args
				#url = site('...').get('href')
			#except:
				 #break if not pages
				#break
		last = os.listdir(self.path)
		folder = str(int(last[-1])+1) if last else '1'
		path = os.path.join(self.path,folder)
		for l in linx:
			tools.load(path,l)
		#some code
	def folder(self,):
		'''записывает в конфиг папку для сохранений'''
		pass
class Folders(BoxLayout):
	pass		
class SummApp(App):
	def build(self):
		self.title = 'Replays Downloader'
		return Root()
	
if __name__ == '__main__':
	SummApp().run()

