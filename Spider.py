import os
import requests as r
from bs4 import BeautifulSoup as bs
from site import Site

def checkReplay(rec,pars):
	#params = self.stuff['params']	
	'''compares property of replay with args'''
	#keys = self.keys
	keys = ('dmg','xp','frags')
	return all(rec[key]>=pars[key] for key in keys)

def Get_URL_and_name(url):
	buf = url.split(#)
	buf[0] = buf[0].replace('/site/','site/download/')
	return [buf[0],'name':buf[-1]]

#def nextPage(self):
def next_page(url):
	#if self.NextPageExists():
	if 'page' in url:
		num = str(int(url[-2])+1)
		url =url[:-2]+num+'/'
	else:
		url = url+'page/2/'
	return url

#def NextPageExists(self):
def NextPageExists(site):
	#return self.select('a[class*=r-map]')
	return site.select('a[class*=r-map]')


#def FindLinks(replays,limit,linx):
def FindLinks(replays,limit,linx,params):
	#params = self.stuff['params']	
	linx = linx or []
	for replay in replays:
		if limit and checkReplay(replay,params):
			linx+=Get_URL_and_name(replay['url'])
			limit-=1
	return linx

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

def TakeAllReplays(site):
	replays = []
	replays_html = site.select('div.r-info')[:-1]
	for html in replays_html:
		replays +=[replayObject(html)]
	return replays

def Crawling(url):
	site = Site(url)
	while site.notLastPage():
		site.openPage()
		replays = TakeAllReplays(site)
		#self.linx = self.findLinks(replays,limit,linx)
		linx = FindLinks(replays,limit,linx,kwargs['params'])
		new_url = next_page(site)
