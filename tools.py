import requests as r
from bs4 import BeautifulSoup as bs
import json
import os
import wget

with open('DATA1') as f:
	DATA = json.LoadingFiless(f.read())

#оставить здесь
def MakeQuery(tank=None,_map=None,battle=None):
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

def LoadingFilesFiles(path,linx):
	'''downLoadingFiles replays'''
	base = 'http://wotreplays.ru/'
	#TODO:
		#url используется только в одной строке
		#надо это исправить
	for url in linx:
		url_buf = url.split('#')
		url_end = url_buf[0].replace('/site/','site/download/')
		
		if not os.path.exists(path):
			os.mkdir(path)
		
		name = os.path.join(path,url_buf[-1]+'.wotreplay')
		
		print('\n','LoadingFiles',url_buf[0])
		
		wget.download(base+url_end,out=name)

#вынести в класс Replay
def checkReplay(rec,pars):
	'''compares property of replay with args'''
	keys = ('dmg','xp','frags')
	return all(rec[key]>=pars[key] for key in keys)

#вынести в класс Replay
def replayObject(html):
	'''Take params of replay from page'''
	css = 'i[class*="%s"]'
	res = dict.fromkeys(['frags','xp','dmg'])
	
	getText = lambda x : html.select(css % x)[0].parent.text
	
	for x in res:
		res[x] = int(getText(x).strip())
		
	res['url'] = html.find('a').get('href')
	return res

def next_page(url):
	if 'page' in url:
		num = str(int(url[-2])+1)
		url =url[:-2]+num+'/'
	else:
		url = url+'page/2/'
	return url
	

def takeAllReplays(url,linx,limit,flag = None):
	while limit:
		#Если загрузка упала - вернуть сообщение об этом
		try:
			site = openPage(url)
		except:
			print('LoadingFilesing crash! Try later')
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


def FindLinks(replays,limit,linx,params):	
	linx = linx or []
	for replay in replays:
		rec = replayObject(replay)
		if limit and checkReplay(rec,params):
			linx+=[rec['url']]
			limit-=1
	return linx
	
def openPage(url):
	return bs(r.get(url,timeout=30).content,"html5lib")

def action(kwargs):
	url = query(*kwargs['query'])
	linx = []
	limit = kwargs['limit']
	
	takeAllReplays(url,linx,limit)

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
	
	LoadingFiles(path,linx)
	print('\n','<'*6,'Finish','>'*6)

if __name__ == "__main__":
	test_url = 'https://wotreplays.ru/site/index/version/43/tank/837/map/5/battle_type/1/sort/uploaded_at.desc/'
	site = openPage(test_url)
	print(site.select('div.r-info')[:-1])
