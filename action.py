import requests as r
import json, os, wget
from bs4 import BeautifulSoup as bs
from ReplaysDownloader import ReplaysDownloader
from spider import Site
import toolkit

with open('data1') as f:
	DATA = json.loads(f.read())

def Search_and_Save(kwargs):
	query = toolkit.MakeQuery(DATA,*kwargs['query'])
	path = kwargs['path']
	if not path:
		path = GetPath()
	wotreplays = ReplaysDownloader(query,kwargs['params'])
	print('Start walking...')
	wotreplays.walking()
	print('Loading files...')
	toolkit.LoadingFiles(path,wotreplays.targets)
	print('Completed!')
	
if __name__ == "__main__":
	test_params = None
	Action(test_params)
