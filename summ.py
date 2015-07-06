from kivy.app import App
from kivy.uix.boxlayout	import BoxLayout
import json
import os

with open('data1') as f:
	data = json.loads(f.read())
class Root(BoxLayout):
	keys = ('tank','map','battle_type')
	tanks,maps,battles = map(sorted,(data[x] for x in keys))
	def action(self,tank=None,_map=None,battle=None):
		pass
	def query(self,tank=None,_map=None,battle=None):
		#~ продумать обработку комбинаций tank-map-battle
		dlist = (tank,_map,battle)
		if all(dlist):
			q= 'wotreplays.ru/site/index/version/37/'
			for key,rec in zip(self.keys,dlist):
				q+='{0}/{1}/'.format(key,data[key][rec])
			print(q+'inflicted_damage.desc')
			#~ 0)обернуть создание адреса в отдельную ф-ю
			#~ 1)загрузка страницы с реплеями по адресу q
			#~ 2)обернуть (1) в отдельную функцию
			#~ 3)создание папки с именем date/tank-map-battle
			#~ 4)если папка уже есть то:
				#~ а)создать папку ./1
				#~ б)перенести старое содержимое в нее
				#~ в)результаты нового поиска - в ./2, потом в ./3 etc.
			#~ 5)сохранять выбранную для работы папку в конфе  
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

