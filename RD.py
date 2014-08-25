# -*- coding: utf-8 -*-
from bs4 import BeautifulSoup as bs
from urllib.request import urlopen,urlretrieve
import os
from time import strftime

#~ Создать объект из которого будут извлекаться maps, tanks, types
#~ Если версия сайта другая - проверить валидность
#~ полей класса и данных с сайта
#~ При несовпадении вызвать исключение и прекратить работу программы
#~ Если версия прежняя, то maps, tanks, types извлечь из объекта
#~ (см. Лутц стр.501)

mass = bs(urlopen('http://wotreplays.ru'))('ul',class_='b-list b-filter__list',limit=4)
def couples(key,m):
	f1 = lambda x: x.find('input').get(key)
	f2 = lambda x: x.find('label').text
	return {f1(x):f2(x) for x in m('li')}
foo = {'map_id':1,'tank_id':0,'battletype':-1}
maps, tanks, types = [couples(key,mass[idx]) for key,idx in foo.items()]

class Replay:
	def __init__(self,rec,path):
		self = rec
		self.buf = self('a')[0].get('href').split('#')
		self.path = path # and something else
	def data(self):
		buf = self('ul')[0]('li',limit=4)	# damage,xp,frags
		return {'damage':buf[3].text,'frags':buf[0].text,'xp':buf[1].text}
	def name(self):
		return self.buf[1]
	def link(self):
		return self.buf[0].replace('/site/','/site/download/')
	def load(self,path):
		npath = '/'.join(path,self.name()+'.wotreplay')
		urlretrieve('http://wotreplays.ru'+self.link(), npath)
	def test(self, params):
		mass = self.data()
		return(all(mass[p]>=params[p] for p in params))

def GetUrl(params):
	url ='http://wotreplays.ru/site/index'
	args,sort = params.values()
	for a,b in args.items():
		url='%s/%s/%s/' % url,a,b.replace(',','%2C')
	choice = {
			'damage':'sort/inflicted_damage.desc',
			'frags':'sort/frags.desc',
			'xp':'sort/xp.desc'
			}
	s =list(set(choice)^set(sort))[0]
	return url+сhoice[s]

def GetPath(): # Выполняется при каждом поиске реплея - не экономно!!!
	path=''.join((os.environ['HOME'],'\\Desktop\\Downloaded Replays\\'))
	if not os.path.exists(path): 
		os.mkdir(path)
	return path+strftime('\\%H-%M_%d_%m')

def SearchReplays(params,limit=25, best = False): #best - выбор лучшего реплея из отысканных
	url = URL = GetUrl(params)
	#~ url = URL(params)
	path = GetPath() # ''.join((path,strftime('%H-%M_%d_%m'),'\\'))
	os.mkdir(path)
	num = 1
	while limit:
		try:
			page = bs(urlopen(url))('div',class_='r-info')[:-1]
		except Exception:
			break
		for rec in page:
			replay = Replay(rec,path)
			if replay.test(params['sort']):
				replay.load(path) 
				limit-=1
			del replay
		num+=1
		url = '%s/page/%s/' % URL,num
		#~ url = URL(num)
