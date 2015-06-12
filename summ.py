from kivy.app import App
from kivy.uix.boxlayout	import BoxLayout
import json

with open('data') as f:
	data = json.loads(f.read())
class Foo(BoxLayout):
	tanks = [x['title'] for x in data['tank']]
	maps = [x['title'] for x in data['map']]
	battles = [x['title'] for x in data['battle_type']]
	
class SummApp(App):
	def build(self):
		return Foo()
	
if __name__ == '__main__':
	SummApp().run()

