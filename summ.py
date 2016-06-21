# -*- coding: utf-8 -*- 
from kivy.app import App
from kivy.uix.boxlayout	import BoxLayout
from kivy.config import Config
from kivy.core.window import Window
import json
import os
import action
#~ from action import DATA as data
import toolkit
import requests as r
import sys

PARAMS = {
		'fullscreen': '0',
		'resizable': '0'
		}

Config.setall('graphics',PARAMS)

#~ with open(toolkit.RelativePath('data1')) as f:
with open(toolkit.AnotherRelativePath('data1')) as f:
	data = json.loads(f.read())

class Root(BoxLayout):

	keys,path = ('tank','map','battle_type'),''
	tanks,maps,battles = map(sorted,(data[x] for x in keys))
	#~ configPath = toolkit.RelativePath('config.txt')
	configPath = toolkit.AnotherRelativePath('config.txt')
	if os.path.exists(configPath):
		with open(configPath) as f:
			path = f.read()

	def keyPressed(self, keyboard, keycode, text, modifiers):
		if keycode[1] == 'right':
			self.sm.current = self.sm.next()
		if keycode[1] == 'left':
			self.sm.current = self.sm.previous()
			#Продумать при нажатии esc 
			#подтверждения выхода,
			#если идет загрузка
		if keycode[1] == 'escape'and not self.disabled:
				sys.exit()
				#~ exit()
		return True
			
	def attack(self):
		'''Main function. It start searching and loading replays'''
		self.stuff['path'] = self.path
		#print(self.path or 'Path not exists!')
		try:
			action.Search_and_Save(self.stuff)
		except r.exceptions.ConnectionError:
			self.popup.open()

	def folder(self,path):
		'''Remember folder to save replays'''
		path = toolkit.SaveReplaysFolder(path)
		#~ configPath = toolkit.RelativePath('config.txt')
		configPath = toolkit.AnotherRelativePath('config.txt')
		if not os.path.exists(path):
			os.mkdir(path)
		if not os.path.exists(configPath):
			os.mkdir(configPath)
		with open(configPath,'w') as f:
			f.write(path)
		self.path = path

class SummApp(App):	
	def build(self):
		config = self.config
		root = Root()
		Window.size = (500,400)
		MyKeyboard = Window.request_keyboard(None, root)
		MyKeyboard.bind(on_key_down=root.keyPressed)
		self.title = 'Replays Downloader'
		return root
		
if __name__ == '__main__':
	SummApp().run()
