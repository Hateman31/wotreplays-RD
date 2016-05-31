import requests as r
from bs4 import BeautifulSoup as bs
import json
import os
import wget

with open('data1') as f:
	data = json.loads(f.read())

def query(tank=None,_map=None,battle=None):
	'''make a url query'''
	dlist = (tank,_map,battle)
	keys = ('tank','map','battle_type')
	if all(dlist):
		q = 'http://wotreplays.ru/site/index/version/43/'
		for key,rec in zip(keys,dlist):
			q+='{0}/{1}/'.format(key,data[key][rec])
		return q+'sort/inflicted_damage.desc/'
	else:
		print('Error! Some data is None!')
		return None

def load(path,linx):
	'''download replays'''
	q = 'http://wotreplays.ru/'
	for url in linx:
		buf = url.split('#')
		s = buf[0].replace('/site/','site/download/')
		if not os.path.exists(path):
			os.mkdir(path)
		name = os.path.join(path,buf[-1]+'.wotreplay')
		print('\n','Load',buf[0])
		wget.download(q+s,out=name)

def Checked(rec,pars):
	'''compares property of replay with args'''
	keys = ('dmg','xp','frags')
	for key in keys:
		x = 1 if rec[key]>=pars[key] else 0
	return x

def record(data):
	'''Take replay params from page'''
	res,css = {},'i[class*="{0}"]'
	for x in ['frags','xp','dmg']:
		res[x] = int(data.select(css.format(x))[0].parent.text.strip())
	res['url'] = data.find('a').get('href')
	return res

def next_page(url):
	if 'page' in url:
		num = str(int(url[-2])+1)
		url =url[:-2]+num+'/'
	else:
		url = url+'page/2/'
	return url
	
def action(kwargs):
	url = query(*kwargs['query'])
	linx = []
	flag = None
	limit = kwargs['limit']
	while 1:
		try:
			site = bs(r.get(url,timeout=30).content,"html5lib")
		except:
			print('Loading crash! Try later')
			exit()
		r_map = site.select('a[class*=r-map]')
		if r_map:
			if not flag:
				flag = r_map[0].get('href')
			else:
				flag1 = r_map[0].get('href')
				if flag1 == flag: 
					break
		else:
			break
		for replay in site.select('div.r-info')[:-1]:
			rec = record(replay)
			if Checked(rec,kwargs['params']):
				if limit:
					linx+=[rec['url']]
					limit-=1
					#print(limit)
				else:
					break
		url = next_page(url)

#TODO: 
	#1) папка для реплеев должна создаваться
	#2) Если папка пуста last = 0
	
	try:
		last = sorted(os.listdir(kwargs['path']),key=lambda x:int(x))
		fold = str(int(last[-1])+1) if last else '1'
		path = os.path.join(kwargs['path'],fold)
		load(path,linx)
		print('\n','<'*6,'Finish','>'*6)
	except ValueError:
		print(os.listdir(kwargs['path']) or 'List are empty')

if __name__ == "__main__":
	pass
