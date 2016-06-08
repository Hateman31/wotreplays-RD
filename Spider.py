import os
import requests as r
from bs4 import BeautifulSoup as bs
from site import Site

#def replayIsGood(self,replay):
def checkReplay(rec,pars):
	keys = ('dmg','xp','frags')
	#return all(rec[key]>=self.pars[key] for key in self.keys)
	return all(rec[key]>=pars[key] for key in keys)

def Get_URL_and_name(url):
	buf = url.split(#)
	buf[0] = buf[0].replace('/site/','site/download/')
	return [buf[0],'name':buf[-1]]

#def findTargets(self):
def FindLinks(replays,limit,linx,params):
	#params = self.stuff['params']	
	linx = linx or []
	#for replay in self.replays:
	for replay in replays:
		#if self.replayIsGood(replay):
		if limit and checkReplay(replay,params):
			#self.addNewTarget(replay['url'])
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

#def TakeAllReplays(self.site):
def TakeAllReplays(site):
	replays = []
	#replays_html = self.site.select('div.r-info')[:-1]
	replays_html = site.select('div.r-info')[:-1]
	for html in replays_html:
		replays +=[replayObject(html)]
	return replays

#def Crawling(self):
def Crawling(url):
	#self.site = Site(url)
	site = Site(url)
	#while self.site.NotLastPage:
	while site.notLastPage():
		site.openPage()
		#self.takeAllReplays()
		replays = TakeAllReplays(site)
		#self.linx = self.findLinks()
		linx = FindLinks(replays,limit,linx,kwargs['params'])
		new_url = next_page(site)
