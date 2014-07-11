# -*- coding: utf-8 -*-
from bs4 import BeautifulSoup as bs
#~ import requests
from urllib.request import urlopen
from urllib.request import urllretrieve
import os
from time import ctime
from tkinter import *
from tkinter.ttk import Combobox

mass = bs(urlopen('http://wotreplays.ru'))('ul')
maps = {x.text.strip():x.find('input').get('map_id') for x in mass[7]('li')}
tanks = {x.text.strip():x.find('input').get('tank_id') for x in mass[6]('li')}
types = { x.text.strip(): x.find('input').get('battletype') for x in mass[9]('li')}

def Replay(record,params):
	def trick(x):
		return(x.text.strip())
	replay = {}
	buf = record('a')	#player 
	buf1 = record('li')		# damage,xp,frags		
	funcs = {'player':(lambda:buf[2].text),'damage':(lambda:trick(buf1[3])),
			'frags':(lambda:trick(buf1[0])),'xp':(lambda:trick(buf1[1])),
			'date':(lambda:record('span')[4].text)}		
	params = [p for p in params if p in list(funcs.keys())]
	for p in params:
		replay[p]=funcs[p]()
	return(replay)
	
def Test(data, params):
	def Choice(x,y,flag):
		def less(x,y,eq):
			res = (x<=y) if eq==-1 else (x<y)
			return(res)
		def great(x,y,eq):
			res = (x>=y) if eq==-1 else (x>y)
			return(res)
		funcs = {'<':less,'>':great}
		eq = {'<':-1,'>':-1,'<=':1,'>=':1}
		res = funcs[flag](x,y,eq[flag])
		return(res)
	for p in params:
		if '<' in params[p]:
			flag = '<=' if '=' in params[p] else '<'
		else:
			flag = '>' if not '=' in params[p] else '>='		
		if not Choice(data[p],params[p].split(flag)[-1],flag):
			return(False)
	return(True)
		
def GetUrl(params):
	url ='http://wotreplays.ru/site/index'
	args=params['filter']
	for a in args:
		url=''.join((url,'/',a,'/','%2C'.join(args[a].split(','))))
	url = ''.join((url,'/sort'))
	sort = params['sort']
	choice = {}
	#~ if 'damage' in sort:
			#~ url = ''.join((url,'/inflicted_damage.desc'))
	#~ elif 'frags' in sort:
			#~ url = ''.join((url,'/frags.desc'))
	#~ elif 'xp' in sort:
			#~ url = ''.join((url,'/xp.desc'))
	#~ else:
			#~ url=''.join((url,'/upload_at.desc'))
	return(url)
    
def Load(link,name,path):
	t_path = os.path.join(path,name)
	if not os.path.exists(t_path):
		urllib.urlretrieve(link, t_path)
            
def SearchReplays(params,limit=25):
	keys = []
	for k in params:
		for x in params[k]:
			keys+=[x]
	url = GetUrl(params)
	y=0
	path=''.join(('C:\\Users\\',os.environ.get('USERNAME'),'\\Desktop\\Downloaded Replays\\'))
	if not os.path.exists(path):
		os.mkdir(path)
	path=''.join((path,ctime().replace(':','-'),'\\'))
	print(path)
	os.mkdir(path)
	while y<limit:
		page = bs(urlopen(url))
		for rec in [x for x in page('li')[-150:-20] if len(x)==13]:
			rep = Replay(rec,keys)
			if Test(rep,params['sort']):
				link = rec('a')[3].get('href')
				name = rec('a')[0].get('href').split('#')[1]    
				Load(link,name,path)
				y+=1
		url = ''.join(('http://wotreplays.ru',page('a')[-6].get('href')))
	print('Поиск и загрузка завершены!')


root = Tk()
root.title("Replays Downloader v 0.1")
frame3 = Frame(root)
frame4 = Frame(root)
frame1 = Frame(frame3)
frame2 = Frame(frame3)

def Action():
		params={}
		params['filter'] = {}
		params['sort'] = {}
		funcs = {}
		funcs['filter'] = dict(tank = tanks.get(El1.combobox.get(),''),map = maps.get(El2.combobox.get(),''),
					battle_type = types.get(El3.combobox.get(),''))
		funcs['sort'] = dict(damage = ent1.get(),frags = ent2.get(), xp = ent3.get())
		c = 0
		for f in funcs:
			for fc in funcs[f]:
				if len(funcs[f][fc])!=0:
					params[f][fc]=funcs[f][fc]
					c = 1
		if c == 0:
			root1 = Tk()
			Label(root1,text ='You do not choose! Search is over!').pack(side = TOP)
			Button(root1,text ='start again', command=root1.destroy).pack(side = BOTTOM)
			root1.title('Error!')
			root1.mainloop()
		else:
			SearchReplays(params)
			
			
			
class Element(Frame):
	def __init__(self,values,name,parent=None):
		Frame.__init__(self,parent)
		self.pack()
		self.makeWidgets(values,name)
	def makeWidgets(self,values,name):
		self.combobox = Combobox(self,values=values,height=8)
		self.labl = Label(self,text=name)
		self.labl.grid(row=0,column=0)
		self.combobox.grid(row=1,column=0)
	
values1 = [x for x in tanks]
El1 = Element(sorted(values1),'Tank',frame1)
values2 = [x for x in maps]
El2 = Element(sorted(values2),'Map',frame1)
values3 = [x for x in types]
El3 = Element(sorted(values3),'Battle type',frame1)
lb1 = Label(frame2,text='Inflicted damage')
ent1=Entry(frame2)
lb2 = Label(frame2,text='Frags')
ent2=Entry(frame2)
lb3 = Label(frame2,text='Expirience')
ent3=Entry(frame2)
for x in (El1,El2,El3,lb1,ent1,lb2,ent2,lb3,ent3):
		x.pack()
Button(frame4,text='Close',command=root.destroy).pack(side=RIGHT)
Button(frame4,text='Search', command=Action).pack(side=RIGHT)
frame1.grid(row=0,column=0)
frame2.grid(row=0,column=1)
frame3.grid(row=0,column=0)
frame4.grid(row=1,column=0)
root.mainloop()
