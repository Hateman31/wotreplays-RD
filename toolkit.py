import requests as r
import json, os, wget,sys
from bs4 import BeautifulSoup as bs
from spider import Site
import time

appdata = os.environ['APPDATA']
Config_Folder = os.path.join(appdata,'ReplaysDownloader')

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
	if not os.path.exists(path):
		os.mkdir(path)
	subfolder = GetPath(path)
	print(subfolder)
	if not os.path.exists(subfolder):
		os.mkdir(subfolder)
	for target in targets:
	#~ for target in targets[:1]:
		url,name = target
		fileName = os.path.join(subfolder,name+'.wotreplay')		
		wget.download(base+url,out=fileName)
		time.sleep(1.5)
		
def GetPath(folder):
	folder_list = os.listdir(folder)
	folder_list.sort()
	try:
		LastNum = folder_list[-1]
	except IndexError:
		LastNum = '0'
	new_fold = int(LastNum)+1
	return os.path.join(folder,str(new_fold))

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

def RelativePath(fname):
	return os.path.join(os.path.dirname(sys.executable),fname)

def AnotherRelativePath(fname,script = __file__):
	basedir = os.path.abspath(os.path.dirname(script))
	return os.path.join(basedir,fname)
	
if __name__ == "__main__":
	path = 'C:\\users\\vlad\\desktop\\WOT_Replays'
	subfolder = GetPath(path)
	print(subfolder)
