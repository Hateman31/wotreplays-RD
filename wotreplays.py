
class Replay:
	def __init__(self,rec,keys=None):
		self.rec = rec
		self.buf = self.rec('a')[0].get('href').split('#')
	def data(self):
		buf = self.rec('ul')[0]('li',limit=4)	# damage,xp,frags
		return {'damage':buf[3].text,'frags':buf[0].text,'xp':buf[1].text}
	def name(self):
		return self.buf[1]
	def link(self):
		return self.buf[0].replace('/site/','/site/download/')
	def load(self,path):
		npath = path+self.name()+'.wotreplay'
		urlretrieve('http://wotreplays.ru'+self.link(), npath)
	def test(self, params):
		mass = self.data()
		return(all(mass[p]>=params[p] for p in params))
