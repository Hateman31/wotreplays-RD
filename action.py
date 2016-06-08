import requests as r
import json, os, wget
from bs4 import BeautifulSoup as bs
from ReplaysDownloader import ReplaysDownloader
from spider import Site

def Action(**kwargs):
	query = MakeQuery(kwargs['query'])
	
	wotreplays = ReplaysDownloader(query)
	wotreplays.walking()

	#TODO: 
		#папка для реплеев должна создаваться	
	folder_list = os.listdir(kwargs['path']).sort()
	try:
		LastNum = folder_list[-1] if folder_list else '0'
	except ValueError:
		print(os.listdir(kwargs['path']) or 'List are empty')
	
	new_fold = int(LastNum)+1
	path = os.path.join(kwargs['path'],str(new_fold))
	
	LoadingFiles(path,wotreplays.targets)
