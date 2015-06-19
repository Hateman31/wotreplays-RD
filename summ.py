from kivy.app import App
from kivy.uix.boxlayout	import BoxLayout
import json

with open('data1') as f:
	data = json.loads(f.read())
class Foo(BoxLayout):
	tanks,maps,battles = map(sorted,(data[x] for x in ['tank','map','battle_type']))
	def action(self,tank,_map,battle):
		s = 'tank\{0}\map\{1}\\battle_type\{2}'
		#~ продумать обработку комбинаций tank-map-battle
		print(s.format(	data['tank'][tank],
						data['map'][_map],
						data['battle_type'][battle]))
class SummApp(App):
	def build(self):
		self.title = 'Replays Downloader'
		return Foo()
	
if __name__ == '__main__':
	SummApp().run()

