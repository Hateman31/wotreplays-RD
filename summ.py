from kivy.app import App
from kivy.uix.boxlayout	import BoxLayout

class Foo(BoxLayout):
	pass
class SummApp(App):
	def build(self):
		return Foo()
	
if __name__ == '__main__':
	SummApp().run()
