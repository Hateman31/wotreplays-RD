import requests as R

def query(tank=None,_map=None,battle=None):
	#~ продумать обработку комбинаций tank-map-battle
	dlist = (tank,_map,battle)
	if all(dlist):
		q = 'wotreplays.ru/site/index/version/37/'
		for key,rec in zip(self.keys,dlist):
			q+='{0}/{1}/'.format(key,data[key][rec])
		return r.get(q+'inflicted_damage.desc').content
	else:
		print('Error! Some data is None!')
		return None
def load(url,path):
	'''download replay'''
	bites = R.get(url).content
	name = os.path.join(path,url.split('/')[-1]+'.wotreplay')
	with open(name,'wb') as f:
		f.write(bites)

