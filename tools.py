import requests as r
import json, os, wget
from bs4 import BeautifulSoup as bs
from ReplaysDownloader import ReplaysDownloader
from spider import Site

with open('data1') as f:
	DATA = json.loads(f.read())

#оставить здесь
def MakeQuery(tank=None,_map=None,battle=None):
	'''make a url for query'''
	valueList = (tank,_map,battle)
	keys = ('tank','map','battle_type')
	if all(valueList):
		#добавить фукнцию проверки версии сайта
		q = 'http://wotreplays.ru/site/index/version/43/'
		for key,value in zip(keys,valueList):
			q+='{0}/{1}/'.format(key,DATA[key][field])
		return q+'sort/inflicted_damage.desc/'
	else:
		print('Error! Some DATA is None!')
		return None

def LoadingFiles(path,targets):
	'''save replays on disk'''
	base = 'http://wotreplays.ru/'

	if not os.path.exists(path):
		os.mkdir(path)

	for url,name in targets:
		fileName = os.path.join(path,name+'.wotreplay')		
		wget.download(base+url,out=fileName)

#сделать частью класса Root	
def Action(**kwargs):
	query = MakeQuery(kwargs['query'])
	
	#wotreplays = ReplaysDownloader(query)
	#wotreplays.walking()
	Spider.Crawling(query,linx,limit)

	#TODO: 
		#папка для реплеев должна создаваться	
	try:
		folder_list = os.listdir(kwargs['path']).sort()
		LastNum = folder_list[-1] if folder_list else '0'
	except ValueError:
		print(os.listdir(kwargs['path']) or 'List are empty')
	
	new_fold = int(LastNum)+1
	path = os.path.join(kwargs['path'],str(new_fold))
	
	LoadingFiles(path,wotreplays.targets)
	
if __name__ == "__main__":
	test_url = 'https://wotreplays.ru/site/index/version/43/tank/837/map/5/battle_type/1/sort/uploaded_at.desc/'
	#site = ReplaysDownloader(test_url)
	#print(site.replays[0])
