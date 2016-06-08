import requests as r
from bs4 import BeautifulSoup as bs
import json
import os
import wget

class ReplaysDownloader:

	def __init__(self,url,params):
		self.keys = ('dmg','xp','frags')
		self.params = params
		self.targets = None
		self.takeAllReplays()
	
	def checkValue(self,replay,field):
		return replay[field]>=self.params[field]
		
	def replayIsGood(self,replay):
		return all(checkValue(replay,field) for field in self.keys)
	
	def findTargets(self):
		params = self.stuff['params']	
		for replay in self.replays:
			if self.replayIsGood(replay):
				self.addNewTarget(replay['url'])
	
	def takeAllReplays(self):
		replays_html = self.site.select('div.r-info')[:-1]
		for replay_div in replays_html:
			self.replays +=[replayObject(replay_div)]

	def crawling(self):
		self.site = Site(self.url)
		#while self.site.NotLastPage:
		while self.site.notLastPage():
			self.takeAllReplays()
			self.linx = self.findLinks()

	def addNewTarget(self,url):
		pass

	def Get_URL_and_name(url):
		buf = url.split(#)
		buf[0] = buf[0].replace('/site/','site/download/')
		return [buf[0],'name':buf[-1]]
	
