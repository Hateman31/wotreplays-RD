import requests as r
import json, os, wget
from bs4 import BeautifulSoup as bs
from ReplaysDownloader import ReplaysDownloader
from spider import Site
import toolkit

with open('data1') as f:
	DATA = json.loads(f.read())

def Action(**kwargs):
	query = MakeQuery(kwargs['query'])
	path = kwargs['path']
	if not path:
		path = GetPath()
	
	wotreplays = ReplaysDownloader(query)
	wotreplays.walking()
	
	LoadingFiles(path,wotreplays.targets)

if __name__ == "__main__":
	test_params = None
	Action(test_params)
