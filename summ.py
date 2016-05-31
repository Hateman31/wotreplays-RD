from kivy.app import App
from kivy.uix.boxlayout	import BoxLayout
from kivy.config import Config
from kivy.core.window import Window
import json
import os
import tools

PARAMS = {
		'fullscreen': '0',
		'resizable': '0'
		}

Config.setall('graphics',PARAMS)

with open('data1') as f:
	data = json.loads(f.read())

class Root(BoxLayout):

	keys,path = ('tank','map','battle_type'),''
	tanks,maps,battles = map(sorted,(data[x] for x in keys))
	if os.path.exists('data.txt'):
		with open('data.txt') as f:
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
				exit()
		return True
			
	def attack(self):
		'''Main function. It start searching and loading goods'''
		self.stuff['path'] = self.path
		tools.action(self.stuff)
		#...

	def folder(self,path):
		'''Remember folder to save replays'''
		cwd = os.path.join(os.getcwd(),'data.txt')
		if not os.path.exists(cwd):
			with open(cwd,'w') as f:
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
