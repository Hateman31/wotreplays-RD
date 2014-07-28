from RD import *
from tkinter import *
from tkinter.ttk import Combobox

def Action():
    params={}
    params['filter'] = {} # что..
    params['sort'] = {}	# за..??
    funcs = {}
    funcs['filter'] = dict(
							tank = tanks.get(El1.combobox.get(),''),
							map = maps.get(El2.combobox.get(),''), # Исправить map на card
							battle_type = types.get(El3.combobox.get(),'')
							)
    funcs['sort'] = dict(
							damage = ent1.get(),
							frags = ent2.get(),
							 xp = ent3.get()
							 )
    
    #~ for f in funcs:
      #~ for fc in funcs[f]:
        #~ if len(funcs[f][fc])!=0:
          #~ params[f][fc]=funcs[f][fc] <--- Исправить!!!
    
    for f in funcs:
        if any(funcs[f][fc] for fc in funcs[f]):
			SearchReplays(params)
			break
		else:
		  root1 = Tk()
		  Label(root1,text ='You do not choose! Search is over!').pack(side = TOP)
		  Button(root1,text ='start again', command=root1.destroy).pack(side = BOTTOM)
		  root1.title('Error!')
		  root1.mainloop()

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
		
	f = lambda mass : [x for x in mass]
	values1,values2,values3  = map(f,(tanks,maps,types))
	
	f = lambda x : Element(sorted(x[0]),x[1],frame1)
	El1,El2,El3 = map(f,[(values1,'Tank')(values2,'Map')(values3,'Battle type')])
	
	f = lambda x : Label(frame2,text='Inflicted damage')
	lb1,lb3,lb2 = map(f,['Inflicted damage','Expirience','Frags'])
	
	ent1=Entry(frame2)
	ent2=Entry(frame2)
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
