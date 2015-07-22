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
	def action(self,tank=None,_map=None,battle=None):
		pass
class Folders(BoxLayout):
	pass		
class SummApp(App):
	def build(self):
		self.title = 'Replays Downloader'
		return Root()
	
if __name__ == '__main__':
	SummApp().run()

