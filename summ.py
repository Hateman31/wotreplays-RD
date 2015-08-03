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
	path = ''
	if os.path.exists('data'):
		with open('data') as f:
			path = f.read()
	def attack(self):
		'''Main function. It start searching and loading goods'''
		#read the load-folder
		tools.action(self.stuff)
		#some code
		#...
	def folder(self,path):
		'''записывает в конфиг папку для сохранений'''
		cwd = os.getcwd()
		s = os.path.join(cwd,'data')
		if not os.path.exists(s):
			os.mkdir(s)
		with open('data','w') as f:
			f.write(path)
		self.path = path

class SummApp(App):
	def build(self):
		self.title = 'Replays Downloader'
		return Root()
	
if __name__ == '__main__':
	SummApp().run()
