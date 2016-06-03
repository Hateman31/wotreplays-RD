#вынести в класс Replay
def next_page(url):
	if 'page' in url:
		num = str(int(url[-2])+1)
		url =url[:-2]+num+'/'
	else:
		url = url+'page/2/'
	return url

def openPage(url):
	return bs(r.get(url,timeout=30).content,"html5lib")

def checkReplay(rec,pars):
	'''compares property of replay with args'''
	keys = ('dmg','xp','frags')
	return all(rec[key]>=pars[key] for key in keys)


def NextPageExists(site,flag):
	r_map = site.select('a[class*=r-map]')
		if r_map:
			if not flag:
				flag = r_map[0].get('href')
			else:
				flag1 = r_map[0].get('href')
				return flag1 == flag
		else:
			return 0

def Get_URL_and_name(url):
	buf = url.split(#)
	buf[0] = buf[0].replace('/site/','site/download/')
	return [buf[0],'name':buf[-1]]

def FindLinks(replays,limit,linx,params):	
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

def Crawling(url,linx,limit,flag = None):
	try:
		site = openPage(url)
	except:
		print('Loading crash! Try later')
		exit()
	while limit and NextPageExists(site,flag):
		replays = TakeAllReplays(site)
		#linx = FindLinks(replays,limit,linx,self.stuff['params'])
		linx = FindLinks(replays,limit,linx,kwargs['params'])
		url = next_page(url)
		#Если загрузка упала - вернуть сообщение об этом	
		try:
			site = openPage(url)
		except:
			print('Loading crash! Try later')
			exit()
