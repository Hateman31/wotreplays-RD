from kivy.app import App
from kivy.uix.boxlayout	import BoxLayout
import json

with open('data') as f:
	data = json.loads(f.read())
class Foo(BoxLayout):
	tanks = [x['title'] for x in data['tank'][:5]]
	maps = [x['title'] for x in data['map'][:5]]
	battles = [x['title'] for x in data['battle_type'][:5]]
	
class SummApp(App):
	def build(self):
		return Foo()
	
if __name__ == '__main__':
	SummApp().run()

