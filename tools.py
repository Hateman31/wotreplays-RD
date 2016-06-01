import requests as r
from bs4 import BeautifulSoup as bs
import json
import os
import wget

with open('DATA1') as f:
	DATA = json.Loadings(f.read())

def query(tank=None,_map=None,battle=None):
	'''make a url for query'''
	dataList = (tank,_map,battle)
	keys = ('tank','map','battle_type')
	if all(dataList):
		q = 'http://wotreplays.ru/site/index/version/43/'
		for key,rec in zip(keys,dataList):
			q+='{0}/{1}/'.format(key,DATA[key][rec])
		return q+'sort/inflicted_damage.desc/'
	else:
		print('Error! Some DATA is None!')
		return None

def Loading(path,linx):
	'''downLoading replays'''
	q = 'http://wotreplays.ru/'
	for url in linx:
		buf = url.split('#')
		s = buf[0].replace('/site/','site/downLoading/')
		if not os.path.exists(path):
			os.mkdir(path)
		name = os.path.join(path,buf[-1]+'.wotreplay')
		print('\n','Loading',buf[0])
		wget.downLoading(q+s,out=name)

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
	limit = kwargs['limit']
	Crawling(url,linx,limit)

def Crawling(url,linx,limit,flag = None):
	while limit:
		#Если загрузка упала - вернуть в окно сообщение об этом
		try:
			site = openPage(url)
		except:
			print('Loadinging crash! Try later')
			exit()
		r_map = site.select('a[class*=r-map]')
		#breakin is BAD!!! VERY VERY BAD!!!
		if r_map:
			if not flag:
				flag = r_map[0].get('href')
			else:
				flag1 = r_map[0].get('href')
				if flag1 == flag: 
					break
		else:
			break
		
		replays = site.select('div.r-info')[:-1]
		
		linx = FindLinks(replays,limit,linx,kwargs['params'])
		url = next_page(url)

	#TODO: 
		#1) папка для реплеев должна создаваться
	
	try:
		folder_list = os.listdir(kwargs['path'])
		folder_list.sort()
		LastNum = folder_list[-1] if folder_list else '0'
	except ValueError:
		print(os.listdir(kwargs['path']) or 'List are empty')
	
	new_fold = int(LastNum)+1
	path = os.path.join(kwargs['path'],str(new_fold))
	Loading(path,linx)

	print('\n','<'*6,'Finish','>'*6)

def openPage(url):
	return bs(r.get(url,timeout=30).content,"html5lib")

def FindLinks(replays,limit,linx,params):	
	linx = linx or []
	for replay in replays:
		rec = record(replay)
		if Checked(rec,params):
			if limit:
				linx+=[rec['url']]
				limit-=1
			#breakin is BAD!!! VERY VERY BAD!!!
			else:
				break
	return linx
	
if __name__ == "__main__":
	test_url = 'https://wotreplays.ru/site/index/version/43/tank/837/map/5/battle_type/1/sort/upLoadinged_at.desc/'
	site = openPage(test_url)
	print(site.select('div.r-info')[:-1])
