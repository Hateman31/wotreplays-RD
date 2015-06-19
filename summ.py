from kivy.app import App
from kivy.uix.boxlayout	import BoxLayout
import json

with open('data1') as f:
	data = json.loads(f.read())
class Foo(BoxLayout):
	tanks,maps,battles = map(sorted,(data[x] for x in ['tank','map','battle_type']))
	def action(self,tank,_map,battle):
		print(tank, data['tank'][tank])
		print(_map, data['map'][_map])
		print(battle, data['battle_type'][battle])
	
class SummApp(App):
	def build(self):
		self.title = 'Replays Downloader'
		return Foo()
	
if __name__ == '__main__':
	SummApp().run()

