from RD import *
from tkinter import *
from tkinter.ttk import Combobox

def Action():
    params={}
    params['filter'] = {}
    params['sort'] = {}
    funcs = {}
    funcs['filter'] = dict(tank = tanks.get(El1.combobox.get(),''),
						Map = maps.get(El2.combobox.get(),''),
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

def Main(Action):
	root = Tk()
	root.title("Replays Downloader v 0.1")
	frame3 = Frame(root)
	frame4 = Frame(root)
	frame1 = Frame(frame3)
	frame2 = Frame(frame3)
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

