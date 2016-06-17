import requests as r
import json, os, wget
from bs4 import BeautifulSoup as bs
from ReplaysDownloader import ReplaysDownloader
from spider import Site
import toolkit
import time
with open('data1') as f:
	DATA = json.loads(f.read())

def Search_and_Save(kwargs):
	query = toolkit.MakeQuery(DATA,*kwargs['query'])
	path = kwargs['path']
	if not path:
		path = GetPath()
	wotreplays = ReplaysDownloader(query,kwargs['params'])
	wotreplays.walking()
	toolkit.LoadingFiles(path,wotreplays.targets)
	
if __name__ == "__main__":
	test_params = None
	Search_and_Save(test_params)
