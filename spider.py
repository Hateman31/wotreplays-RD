import os
import requests as r
from bs4 import BeautifulSoup as bs
from site import Site

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
