import requests as r
from bs4 import BeautifulSoup as bs

def query(tank=None,_map=None,battle=None):
	'''make a url query'''
	dlist = (tank,_map,battle)
	keys = ['dmg','xp','frags']
	if all(dlist):
		q = 'wotreplays.ru/site/index/'
		for key,rec in zip(keys,dlist):
			q+='{0}/{1}/'.format(key,data[key][rec])
		#~ return r.get(q+'inflicted_damage.desc').content
		return q+'/sort/inflicted_damage.desc'
	else:
		print('Error! Some data is None!')
		return None
def load(path,linx):
	'''download replays'''
	for url in linx:
		bites = R.get(url).content
		name = os.path.join(path,url.split('/')[-1]+'.wotreplay')
		with open(name,'wb') as f:
			f.write(bites)

def isGood(rec,pars):
	'''compares property of replay with args'''
	for key in keys:
		x = 1 if rec[key]>=pars[key] else 0
	return x

def record(data):
	res,css = {},'i[class*="{0}"]'
	for x in ['frags','exp','dmg']:
		res[x] = int(data.select(css.format(x))[0].parent.text.strip())
	res['link'] = data.find('a').get('href')
	return res

def action(kwargs):
	url = query(kwargs['query'])
	linx = []
	flag = None
	while 1:
		site = bs(r.get(url).content)
		if not flag:
			flag = site.find('a').get('href')
		else:
			flag1 = site.find('a').get('href')
			if flag1 == flag: 
				break
		for replay in site.select('div.r-info')[:-1]:
			rec = record(replay)
			if isGood(rec,kwargs['params']):
				linx+=[rec['url']]
				if limit:
					limit-=1
				else:
					break
	last = os.listdir(kwargs['path'])
	folder = str(int(last[-1])+1) if last else '1'
	path = os.path.join(self.path,folder)
	load(path,linx)
	#some code

