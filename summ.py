from kivy.app import App
from kivy.uix.boxlayout	import BoxLayout
import json

with open('data1') as f:
	data = json.loads(f.read())
class Foo(BoxLayout):
	keys = ('tank','map','battle_type')
	tanks,maps,battles = map(sorted,(data[x] for x in keys))
	def action(self,tank,_map,battle):
		#~ продумать обработку комбинаций tank-map-battle
		dlist = (tank,_map,battle)
		q= 'wotreplays.ru/site/index/version/37/'
		for key,rec in zip(self.keys,dlist):
			#~ print(key,data[key][rec])
			q+='{0}/{1}/'.format(key,data[key][rec])
		print(q)
class SummApp(App):
	def build(self):
		self.title = 'Replays Downloader'
		return Foo()
	
if __name__ == '__main__':
	SummApp().run()

