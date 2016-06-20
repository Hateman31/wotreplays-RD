import requests as r
import json, os, wget
from bs4 import BeautifulSoup as bs
from spider import Site
import time

def MakeQuery(DATA,tank=None,_map=None,battle=None):
	valueList = (tank,_map,battle)
	keys = ('tank','map','battle_type')
	if all(valueList):
		#добавить фукнцию проверки версии сайта
		q = 'http://wotreplays.ru/site/index/version/43/'
		for key,field in zip(keys,valueList):
			q+='{0}/{1}/'.format(key,DATA[key][field])
		return q+'sort/inflicted_damage.desc/'
	else:
		print('Error! Some DATA is None!')
		return None

def LoadingFiles(path,targets):
	'''save replays on disk'''
	base = 'http://wotreplays.ru/'
	for target in targets:
		url,name = target
		fileName = os.path.join(path,name+'.wotreplay')		
		wget.download(base+url,out=fileName)
		time.sleep(1.5)
		
def GetPath(folder):
	print(folder)
	#TODO: 
	#папка для реплеев должна создаваться	
	folder_list = os.listdir(folder).sort()
	try:
		LastNum = folder_list[-1] if folder_list else '0'
	except ValueError:
		print(os.listdir(folder) or 'List are empty')
	
	new_fold = int(LastNum)+1
	path = os.path.join(folder,str(new_fold))

def valueFromText(html,key): 
	css = 'i[class*="%s"]'
	text = html.select(css % key)[0].parent.text
	return int(text.strip())

def get_URL_and_name(url):
	buf = url.split('#')
	buf[0] = buf[0].replace('/site/','site/download/')
	return (buf[0],buf[-1])

def SaveReplaysFolder(path):
	directory = 'WOT_Replays'
	return os.path.join(path,directory)
	
def GetUnicode(text):
	return text.encode('cp1251').decode('utf-8')	
	
if __name__ == "__main__":
	pass
