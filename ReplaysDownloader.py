import requests as r
from bs4 import BeautifulSoup as bs
import json
import os
import wget
from spider import Site
import toolkit
import time

class ReplaysDownloader:
	def __init__(self,url,params):
		self.url = url
		self.keys = ('dmg','xp','frags')
		self.params = params
		self.targets = []
		self.site = None
		self.replays = []
	
	def replayIsGood(self,replay):
		for field in self.keys:
			if replay[field]<self.params[field]:
				return 0
		return 1
	
	def findTargets(self):
		for replay in self.replays:
			if self.replayIsGood(replay):
				self.addNewTarget(replay['url'])
				#~ return
	
	def html_to_replays(self):
		replays_html = self.site.html.select('div.r-info')[:-1]
		for replay_div in replays_html:
			self.add_replay_object(replay_div)

	def add_replay_object(self,html):
		replayObject = {}
		for key in self.keys:
			replayObject[key] = toolkit.valueFromText(html,key)
		replayObject['url'] = html.find('a').get('href')
		self.replays += [replayObject]
	
	def walking(self):
		self.site = Site(self.url)
		#TODO: site.notLastPage() to property
		#while self.site.NotLastPage:
		while self.site.notLastPage():
			time.sleep(2)
			self.html_to_replays()
			self.findTargets()
			#~ return
			self.site.openPage()

	def addNewTarget(self,url):
		self.targets += [toolkit.get_URL_and_name(url)]
	
if __name__ == "__main__":
	test_url = 'https://wotreplays.ru/site/index/version/43/tank/837/map/5/battle_type/1/sort/uploaded_at.desc/'
	#site = ReplaysDownloader(test_url)
	#print(site.replays[0])
