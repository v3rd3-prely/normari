# from kivy.app import App
# from kivy.uix.widget import Widget
# from kivy.graphics import Color, Ellipse, Line


# class MyPaintWidget(Widget):

#     def on_touch_down(self, touch):
#         with self.canvas:
#             Color(1, 1, 0)
#             d = 30.
#             Ellipse(pos=(touch.x - d / 2, touch.y - d / 2), size=(d, d))
#             touch.ud['line'] = Line(points=(touch.x, touch.y))

#     def on_touch_move(self, touch):
#         touch.ud['line'].points += [touch.x, touch.y]


# class MyPaintApp(App):

#     def build(self):
#         return MyPaintWidget()


# if __name__ == '__main__':
#     MyPaintApp().run()



# # Program to create a calculator

# from datetime import datetime

# # Program to Show how to create a switch
# # import kivy module
# import kivy

# # base Class of your App inherits from the App class.
# # app:always refers to the instance of your application
# from kivy.app import App

# # this restrict the kivy version i.e
# # below this kivy version you cannot
# # use the app or software
# kivy.require('1.9.0')

# # for making multiple buttons to arranging
# # them we are using this
# from kivy.uix.gridlayout import GridLayout

# # for the size of window
# from kivy.config import Config

# # Setting size to resizable
# Config.set('graphics', 'resizable', 1)
# ## Config.set('graphics', 'width', '400')
# ## Config.set('graphics', 'height', '400')

# class TimerGridLayout(GridLayout):
#     def __init__(self):
#         self.hasStarted = False
#         super(TimerGridLayout, self).__init__()
#     def start(self):
#         self.startTime = datetime.now()
#         self.hasStarted = True
#     def stop(self):
#         self.endTime = datetime.now()
#         self.hasStarted = False
#         print(self.endTime-self.startTime)
#         return self.endTime-self.startTime
#     def now(self):
#         if(self.hasStarted):
#             return (datetime.now()-self.startTime).strftime('%H:%M:%S')
#         else:
#             return '0'


# # Creating Layout class
# class CalcGridLayout(GridLayout):

#     # Function called when equals is pressed
#     def calculate(self, calculation):
#         if calculation:
#             try:
#                 # Solve formula and display it in entry
#                 # which is pointed at by display
#                 self.display.text = str(eval(calculation))
#             except Exception:
#                 self.display.text = "Error"

#  # Creating App class
# class TimerApp(App):

#     def build(self):
#         return TimerGridLayout()

# # creating object and running it
# calcApp = TimerApp()
# calcApp.run()







import time

from kivy.app import App
from kivy.clock import Clock
from kivymd.uix.label import Label
from kivy.core.window import Window
from kivy.uix.boxlayout import BoxLayout

Window.size = (400, 700)


class myclock(Label):
	def update(self, *args):
		self.text = time.asctime()


class myclock2(Label):
	def update(self, *args):
		t = time.gmtime()
		self.text = time.asctime(t)


class TimeApp(App):

	def build(self):
		layout = BoxLayout(orientation='vertical')

		clock1 = myclock()
		Clock.schedule_interval(clock1.update, 1)
		layout.add_widget(clock1)
		layout.add_widget(Label(text='INDIA'))

		clock2 = myclock2()
		Clock.schedule_interval(clock2.update, 1)
		layout.add_widget(clock2)
		layout.add_widget(Label(text='LONDON'))

		return layout


root = TimeApp()
root.run()
