import requests as R
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
def load(url,path):
	'''download replay'''
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
		res[x] = data.select(css.format(x))[0].parent.text.strip()
	res['link'] = data.find('a').get('href')
	return res
