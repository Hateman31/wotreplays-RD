# -*- coding: utf-8 -*-
from bs4 import BeautifulSoup as bs
from urllib.request import urlopen,urlretrieve
import os
from time import strftime
from random import randint
from wotreplays import *

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
	return {f2(x):f1(x) for x in m('li')}
foo = {'tank_id':0,'map_id':1,'battletype':-1}
tanks, maps, types = [couples(key,mass[idx]) for key,idx in foo.items()]

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
	s =[set(choice)^set(sort)][0]
	return url+сhoice[s]

def GetPath(): # Выполняется при каждом поиске реплея - не экономно!!!
	path=''.join((os.environ['HOME'],'\\Desktop\\Downloaded Replays\\'))
	if not os.path.exists(path): 
		os.mkdir(path)
	return path

def SearchReplays(params,limit=25, best = False,path = None): #best - выбор лучшего реплея из отысканных
	url = URL = GetUrl(params)
	path = path+strftime('\\%H-%M_%d_%m') # ''.join((path,strftime('%H-%M_%d_%m'),'\\'))
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

def GetRandomFight():
	page = bs(urlopen('http://wotreplays.ru'))('div',class_='r-info')[:-1]
	path = '/home/vlad/wot/'
	Replay(page[randint(0,9)]).load(path)
	
if __name__=='__main__':
	GetRandomFight()
