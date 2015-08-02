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
	def attack(self):
		'''Main function. It start searching and loading goods'''
		#read the load-folder
		with open('data') as f1:
			self.fold = f.read()
		#some code
		#...
	def folder(self):
		'''записывает в конфиг папку для сохранений'''
		with open('data1','w') as f:
			f.write(self.fold)

class SummApp(App):
	def build(self):
		self.title = 'Replays Downloader'
		return Root()
	
if __name__ == '__main__':
	SummApp().run()
