import requests as r
from bs4 import BeautifulSoup as bs
import json
import os
import wget

def valueFromText(x): 
	css = 'i[class*="%s"]'
	text = html.select(css % x)[0].parent.text
	return int(text.strip())
	
class ReplaysDownloader:

	def __init__(self,url,params):
		self.keys = ('dmg','xp','frags')
		self.params = params
		self.targets = None
		self.html_to_replays()
	
	def checkValue(self,replay,field):
		return replay[field]>=self.params[field]
		
	def replayIsGood(self,replay):
		return all(checkValue(replay,field) for field in self.keys)
	
	def findTargets(self):
		for replay in self.replays:
			if self.replayIsGood(replay):
				self.addNewTarget(replay['url'])
	
	def html_to_replays(self):
		replays_html = self.site.select('div.r-info')[:-1]
		for replay_div in replays_html:
			self.add_replay_object(replay_div)

	def add_replay_object(self,html):
		replayObject = {}
		for key in self.keys:
			replayObject[key] = valueFromText(key)
		replayObject['url'] = html.find('a').get('href')
		self.replays += [replayObject]
	
	def crawling(self):
		self.site = Site(self.url)
		#TODO: site.notLastPage() to property
		#while self.site.NotLastPage:
		while self.site.notLastPage():
			self.html_to_replays()
			self.findTargets()

	def addNewTarget(self,url):
		self.targets += get_URL_and_name(url)

	def get_URL_and_name(url):
		buf = url.split('#')
		buf[0] = buf[0].replace('/site/','site/download/')
		return [buf[0],buf[-1]]
	
