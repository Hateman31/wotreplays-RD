# -*- coding: utf-8 -*-
from bs4 import BeautifulSoup as bs
#~ import requests
from urllib.request import urlopen
from urllib.request import urlretrieve
import os
from time import ctime

#~ вынести в файл(закрытый от юзера) и при первом запуске создать его
#~ при последующих - брать значения из файла(пока на сайте всё в порядке)(json???)
mass = bs(urlopen('http://wotreplays.ru'))('ul')
maps = {x.text.strip():x.find('input').get('map_id') for x in mass[7]('li')}
tanks = {x.text.strip():x.find('input').get('tank_id') for x in mass[6]('li')}
types = { x.text.strip(): x.find('input').get('battletype') for x in mass[9]('li')}

def Replay(record,params):
	def trick(x):
		return(x.text.strip())
	replay = {}
	buf = record('a')	#player
	buf1 = record('li')		# damage,xp,frags
	funcs = {'player':(lambda:buf[2].text),'damage':(lambda:trick(buf1[3])),
			'frags':(lambda:trick(buf1[0])),'xp':(lambda:trick(buf1[1])),
			'date':(lambda:record('span')[4].text)}
	params = [p for p in params if p in list(funcs.keys())]
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
	args=params['filter']
	for a in args:
		url=''.join((url,'/',a,'/','%2C'.join(args[a].split(','))))
	url = ''.join((url,'/sort'))
	sort = params['sort']
	choice = {}
	if 'damage' in sort:
			url = ''.join((url,'/inflicted_damage.desc'))
	elif 'frags' in sort:
			url = ''.join((url,'/frags.desc'))
	elif 'xp' in sort:
			url = ''.join((url,'/xp.desc'))
	else:
			url=''.join((url,'/upload_at.desc'))
	return(url)

def Load(link,name,path):
	t_path = os.path.join(path,name)
	if not os.path.exists(t_path):
		os.mkdir(path)
	urlretrieve(link, t_path)

def SearchReplays(params,limit=25):
	keys = []
	for k in params:
		for x in params[k]:
			keys+=[x]
	url = GetUrl(params)
	path=''.join(('C:\\Users\\',os.environ.get('USERNAME'),'\\Desktop\\Downloaded Replays\\'))
	if not os.path.exists(path):
		os.mkdir(path)
	path=''.join((path,ctime().replace(':','-'),'\\'))
	os.mkdir(path)
	while limit:
		# Use the Force!!!
		# Seriously!
		# Use the PyQuery
		page = bs(urlopen(url))
		for rec in [x for x in page('li')[-150:-20] if len(x)==13]:
			rep = Replay(rec,keys)
			if Test(rep,params['sort']):
				link = rec('a')[3].get('href')
				name = rec('a')[0].get('href').split('#')[1]
				Load(link,name,path)
				limit-=1
		url = ''.join(('http://wotreplays.ru',page('a')[-6].get('href')))
