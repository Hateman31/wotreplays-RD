# -*- coding: utf-8 -*-
from bs4 import BeautifulSoup as bs
from urllib.request import urlopen,urlretrieve
import os
from time import ctime

#~ вынести в файл(закрытый от юзера) и 
#~ при первом запуске создать его
#~ при последующих - брать значения из файла
#~ (пока на сайте всё в порядке)(sqlite? json?)
mass = bs(urlopen('http://wotreplays.ru'))('ul',class_='b-list b-filter__list',limit=4)
def couples(key,m):
	out = {}
	for li in m('li'):
		id_ = li.find('input').get(key) #id tank
		node = li.find('label').text
		out+={id_:node}
	return out
maps, tanks, types = [couples(key,mass[idx]) for key,idx in (('map_id',1),('tank_id',0),('battletype',-1))]

def Replay(record,keys):
	buf = record('li',limit=4)	# damage,xp,frags
	data = {
			'damage':buf[3].text,
			'frags':buf[0].text,
			'xp':buf[1].text
			}
	return({k:data[k] for k in keys})

#~ def less(x,y,eq):
	#~ res = (x<=y) if eq==-1 else (x<y)
	#~ return(res)
	
#~ def great(x,y,eq):
	#~ res = (x>=y) if eq==-1 else (x>y)
	#~ return(res)
	
#~ def Choice(x,y,flag):
	#~ funcs = {'<':less,'>':great}
	#~ eq = {('<','>'):-1,('<=','>='):1}
	#~ res = funcs[flag](x,y,eq[flag])
	#~ return(res)

def Test(data, params):
	rerturn(all(data[p]>=params[p] for p in params))

def GetUrl(params):
	url ='http://wotreplays.ru/site/index'
	args = params['filter']
	sort = params['sort']
	for a in args:
		substr = args[a].replace(',','%2C')
		url='{1}/{2}/{3}/'.format(url,a,substr)
	url+='sort' 
	choice = {
			'damage':'/inflicted_damage.desc',
			'frags':'/frags.desc',
			'xp':'/xp.desc'
			}
	dfx = sorted(list(choice))
	for s in dfx:
		if s in sort:
			url+=сhoice[s]
			break
	return(url)

def Load(link,name,path):
	URL = 'http://wotreplays.ru'
	npath = os.path.join(path,name)
	if not os.path.exists(npath):
		os.mkdir(npath)
	urlretrieve(URL+link, npath+'.wotreplay')

def GetPath():
	substr = '\\Desktop\\Downloaded Replays\\'
	path=''.join(os.environ['HOME'],substr))
	if not os.path.exists(path):
		os.mkdir(path)
	Time = ctime().replace(':','-')
	path=''.join((path,Time,'\\'))
	return path	

def SearchReplays(params,limit=25):
	keys = [] # избавиться от этого!!!
	for k in params:
		keys+=list(params[k]) # лучше...но наверно можно еще короче ;)
	url = URL = GetUrl(params)
	path = GetPath()
	os.mkdir(path)
	num = 1
	while limit:
		try:
			page = bs(urlopen(url))
		except Exception:
			break
		for rec in page('div',class_='r-info')[:-1]:
			if Test(Replay(rec('ul')[0],keys),params['sort']):
				buf = rec('a')[0].get('href').split('#')
				name = buf[1]
				link = buf[0].replace('/site/','/site/download/')
				Load(link,name,path)
				limit-=1
		num+=1
		url = '{1}/page/{2}/'.format(URL,num)
