from kivy.app import App
from kivy.uix.textinput import TextInput
from kivy.uix.label	import Label
from kivy.uix.floatlayout	import FloatLayout

class Foo(FloatLayout):
	def bar(self,in1,in2):
		return str(int(in1.text)+int(in2.text))

class SummApp(App):
	def build(self):
		return Foo()
	
if __name__ == '__main__':
	SummApp().run()
