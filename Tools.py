import requests as r
from bs4 import BeautifulSoup as bs
import json
import os
import wget
import Spider

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

def LoadingFiles(path,linx):
	'''save replays on disk'''
	base = 'http://wotreplays.ru/'

	if not os.path.exists(path):
		os.mkdir(path)

	for url,name in linx:
		fileName = os.path.join(path,name+'.wotreplay')		
		#print('\n','LoadingFiles',url_buf[0])
		wget.download(base+url,out=fileName)

#сделать частью класса Root	
def Action(kwargs):
	query = MakeQuery(*kwargs['query'])
	linx = []
	limit = kwargs['limit']
	
	Spider.Crawling(query,linx,limit)

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
