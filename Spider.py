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

def FindLinks(replays,limit,linx,params):	
	linx = linx or []
	for replay in replays:
		rec = replayObject(replay)
		#TODO:
			#надо сделать linx списком словарей,
			#каждый элемент, это словарь вида
			#{'url':url.split(#)[0],'name':url.split(#)[-1]}
		if limit and checkReplay(rec,params):
			linx+=[rec['url']]
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


def Crawling(url,linx,limit,flag = None):
	try:
		site = openPage(url)
	except:
		print('Loading crash! Try later')
		exit()
	while limit and NextPageExists(site,flag):
		#Если загрузка упала - вернуть сообщение об этом	
		replays = site.select('div.r-info')[:-1]
		linx = FindLinks(replays,limit,linx,kwargs['params'])
		url = next_page(url)
		try:
			site = openPage(url)
		except:
			print('Loading crash! Try later')
			exit()
