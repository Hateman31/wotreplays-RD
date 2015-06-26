from kivy.app import App
from kivy.uix.boxlayout	import BoxLayout
import json

with open('data1') as f:
	data = json.loads(f.read())
class Root(BoxLayout):
	keys = ('tank','map','battle_type')
	tanks,maps,battles = map(sorted,(data[x] for x in keys))
	def action(self,tank=None,_map=None,battle=None):
		#~ продумать обработку комбинаций tank-map-battle
		dlist = (tank,_map,battle)
		if all(dlist):
			q= 'wotreplays.ru/site/index/version/37/'
			for key,rec in zip(self.keys,dlist):
				q+='{0}/{1}/'.format(key,data[key][rec])
			print(q)
		else:
			print('Error! Some data is None!')
class Folders(BoxLayout):
	pass		
class SummApp(App):
	def build(self):
		self.title = 'Replays Downloader'
		return Root()
	
if __name__ == '__main__':
	SummApp().run()

