from kivy.app import App
from kivy.uix.anchorlayout import AnchorLayout
from kivy.uix.label import Label
from kivy.uix.widget import Widget
from kivy.graphics import Color, Line
from kivy.uix.floatlayout import FloatLayout
from math import cos, sin, pi
from kivy.clock import Clock
from kivy.lang import Builder
from kivy.properties import NumericProperty

import datetime

kv = '''
#:import math math

[ClockNumber@Label]:
    text: str(ctx.i)
    pos_hint: {"center_x": 0.5+0.42*math.sin(math.pi/6*(ctx.i-12)), "center_y": 0.5+0.42*math.cos(math.pi/6*(ctx.i-12))}
    font_size: self.height/16

<MyClockWidget>:
    face: face
    FloatLayout:
        id: face
        size_hint: None, None
        pos_hint: {"center_x":0.5, "center_y":0.5}
        size: 0.9*min(root.size), 0.9*min(root.size)
        canvas:
            Color:
                rgb: 0.1, 0.1, 0.1
            Ellipse:
                size: self.size     
                pos: self.pos
        ClockNumber:
            i: 1
        ClockNumber:
            i: 2
        ClockNumber:
            i: 3
        ClockNumber:
            i: 4
        ClockNumber:
            i: 5
        ClockNumber:
            i: 6
        ClockNumber:
            i: 7
        ClockNumber:
            i: 8
        ClockNumber:
            i: 9
        ClockNumber:
            i: 10
        ClockNumber:
            i: 11
        ClockNumber:
            i: 12
'''
Builder.load_string(kv)


class MyClockWidget(FloatLayout):
    pass


class Ticks(Widget):
    def __init__(self, root, **kwargs):
        super(Ticks, self).__init__(**kwargs)
        # print(root.size)
        self.root=root
        self.r = min(root.size)
        self.center_x = root.center_x
        self.center_y = root.center_y
        # print(self.r)
        self.bind(pos=self.update_clock)
        self.bind(size=self.update_clock)

    def update_clock(self, *args):
        self.canvas.clear()
        with self.canvas:
            time = datetime.datetime.now()
            # print("TICKS Center :{} {}".format(self.center_x,self.center_y))
            # print("Root Center :{} {}".format(self.root.center_x,self.root.center_y))

            # Here this mortals I'm a DemiGod, Atleast feeling like right now. :mojo jojo laughs:

            self.r = min(self.root.size)*0.9/2
            self.set_center_x(self.root.center_x)
            self.set_center_y(self.root.center_y)
            Color(0.2, 0.5, 0.2)
            Line(points=[self.center_x, self.center_y, self.center_x + 0.8 * self.r * sin(pi / 30 * time.second),
                         self.center_y + 0.8 * self.r * cos(pi / 30 * time.second)], width=1, cap="round")
            Color(0.3, 0.6, 0.3)
            Line(points=[self.center_x, self.center_y, self.center_x + 0.7 * self.r * sin(pi / 30 * time.minute),
                         self.center_y + 0.7 * self.r * cos(pi / 30 * time.minute)], width=2, cap="round")
            Color(0.4, 0.7, 0.4)
            th = time.hour * 60 + time.minute
            Line(points=[self.center_x, self.center_y, self.center_x + 0.5 * self.r * sin(pi / 360 * th),
                         self.center_y + 0.5 * self.r * cos(pi / 360 * th)], width=3, cap="round")


class MyClockApp(App):
    def build(self):
        clock = MyClockWidget()
        ticks = Ticks(clock)
        clock.add_widget(ticks)
        Clock.schedule_interval(ticks.update_clock, 1)
        return clock


if __name__ == '__main__':
    MyClockApp().run()
