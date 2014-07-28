# -*- coding: utf-8 -*-
from bs4 import BeautifulSoup as bs
from urllib.request import urlopen,urlretrieve
import os
from time import ctime

#~ вынести в файл(закрытый от юзера) и при первом запуске создать его
#~ при последующих - брать значения из файла(пока на сайте всё в порядке)(sqlite? json?)
mass = bs(urlopen('http://wotreplays.ru'))('ul',{'class':'b-list b-filter__list'},limit=4)
def couples(couple):
	key,idx = couple
	out = {}
	for li in mass[idx]('li'):
		id_ = li.find('input').get(key) #id tank
		node = li.find('label').text
		out+={id_:node}
	return out
maps, tanks, types = map(couples,[('map_id',1),('tank_id',0),('battletype',-1)])

def Replay(record,params):
	trick = lambda x: x.text.strip()
	replay = {}
	buf = record('a')	#player
	buf1 = record('li')		# damage,xp,frags
	funcs = {'player':(lambda:buf[2].text),'damage':(lambda:trick(buf1[3])),
			'frags':(lambda:trick(buf1[0])),'xp':(lambda:trick(buf1[1])),
			'date':(lambda:record('span')[4].text)}
	params = [p for p in params if p in funcs]
	for p in params:
		replay[p]=funcs[p]()
	return(replay)

def Test(data, params):
	def Choice(x,y,flag):
		def less(x,y,eq):
			res = (x<=y) if eq==-1 else (x<y)
			return(res)
		def great(x,y,eq):
			res = (x>=y) if eq==-1 else (x>y)
			return(res)
		funcs = {'<':less,'>':great}
		eq = {'<':-1,'>':-1,'<=':1,'>=':1}
		res = funcs[flag](x,y,eq[flag])
		return(res)
	for p in params:
		if '<' in params[p]:
			flag = '<=' if '=' in params[p] else '<'
		else:
			flag = '>' if not '=' in params[p] else '>='
		if not Choice(data[p],params[p].split(flag)[-1],flag):
			return(False)
	return(True)

def GetUrl(params):
	url ='http://wotreplays.ru/site/index'
	args = params['filter']
	sort = params['sort']
	for a in args:
		substr = args[a].replace(',','%2C')
		url='{1}/{2}/{3}/sort'.format(url,a,substr) 
	choice = {
			'damage':'/inflicted_damage.desc',
			'frags':'/frags.desc',
			'xp':'/xp.desc'
			}
	dfx = sorted([a for a in choice])
	#~ for s in dfx:
		#~ url+=s
	return(url)

def Load(link,name,path):
	URL = 'http://wotreplays.ru'
	npath = os.path.join(path,name)
	if not os.path.exists(npath):
		os.mkdir(npath)
	urlretrieve(URL+link, npath)

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
		keys+=[x for x in params[k]] # лучше...но наверно можно еще короче ;)
	url = GetUrl(params)
	path = GetPath()
	os.mkdir(path)
	num = 1
	while limit:
		try:
			page = bs(urlopen(url))
		except:
			break
		for rec in page('div',class_='r-info')[:-1]:
			rep = Replay(rec,keys)
			if Test(rep,params['sort']):
				link = rec.find('a').get('href')
				name = link.split('#')[1]
				Load(link,name,path)
				limit-=1
			num+=1
			url = '{1}/page/{2}/'.format(url,num)
