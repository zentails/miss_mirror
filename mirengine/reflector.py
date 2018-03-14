import random
import time

from kivy.app import App
from kivy.clock import Clock
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.floatlayout import FloatLayout
from kivy.uix.label import Label
from kivy.uix.progressbar import ProgressBar
from kivy.uix.widget import Widget

import myclock


class IncrediblyCrudeClock(Label):
    def update(self, *args):
        self.text = time.asctime()


class ReflectorWidget(FloatLayout):
    def __init__(self, **kwargs):
        # make sure we aren't overriding any important functionality
        super(ReflectorWidget, self).__init__(**kwargs)

        long_text = "make sure we aren't overriding any important functionality"
        # long_text = "-"
        self.lable_font_size='20dp'
        self.lable_center_font_size='40dp'

        bx_root = BoxLayout(orientation='vertical', padding=60)

        w_l = BoxLayout(orientation="horizontal", size_hint=(1, 0.2))
        wl_clock = IncrediblyCrudeClock(font_size='25dp', valign='top', halign='left', markup=True)
        wl_clock.bind(size=wl_clock.setter('text_size'))
        Clock.schedule_interval(wl_clock.update, 1)
        w_l.add_widget(wl_clock)

        bl_1 = BoxLayout(orientation="horizontal")
        self.lt_clock = myclock.MyClockWidget(size_hint=(1, 0.8))
        self.lt_clock_ticks = myclock.Ticks(self.lt_clock)
        self.lt_clock.add_widget(self.lt_clock_ticks)
        Clock.schedule_interval(self.lt_clock_ticks.update_clock, 1)
        lt_bl = BoxLayout(orientation="horizontal")
        lt_bl.add_widget(self.lt_clock)
        lt_bl.add_widget(Widget())

        # self.lt_label = Label(text_size=self.size, valign='top', halign='left', text=long_text, markup=True)
        self.rt_label = Label(text_size=self.size, valign='top', halign='right', text=long_text, markup=True)
        # self.lt_label.bind(size=self.lt_label.setter('text_size'))
        self.rt_label.bind(size=self.rt_label.setter('text_size'))
        self.rt_label.font_size=self.lable_font_size
        bl_1.add_widget(lt_bl)
        bl_1.add_widget(self.rt_label)

        bl_2 = BoxLayout(orientation="horizontal")
        self.ct_label = Label(valign='center', halign='right', text=long_text, markup=True)
        self.ct_label.font_size=self.lable_center_font_size
        bl_2.add_widget(self.ct_label)

        bl_3 = BoxLayout(orientation="horizontal")
        self.rb_label = Label(text_size=self.size, valign='bottom', halign='right', text=long_text, markup=True)
        self.lb_label = Label(text_size=self.size, valign='bottom', halign='left', text=long_text, markup=True)
        self.rb_label.bind(size=self.rb_label.setter('text_size'))
        self.lb_label.bind(size=self.lb_label.setter('text_size'))
        self.lb_label.font_size=self.lable_font_size
        self.rb_label.font_size=self.lable_font_size
        bl_3.add_widget(self.lb_label)
        bl_3.add_widget(self.rb_label)

        bl_4 = BoxLayout(orientation="horizontal", size_hint=(1, 0.1))
        self.profile_label = Label(valign='center', halign='right', text="profile")
        self.current_label = Label(valign='center', halign='right', text='current')
        self.profile_label.font_size=self.lable_font_size
        self.current_label.font_size=self.lable_font_size
        bl_4.add_widget(self.profile_label)
        bl_4.add_widget(self.current_label)

        progress_bar = ProgressBar(value=0, max=100, size_hint=(1, 0.02))

        bl_5 = BoxLayout(orientation="horizontal", size_hint=(1, 0.05))
        log_label = Label(valign='center', halign='left')
        bl_5.add_widget(log_label)

        bx_root.add_widget(w_l)
        bx_root.add_widget(bl_1)
        bx_root.add_widget(bl_2)
        bx_root.add_widget(bl_3)
        bx_root.add_widget(bl_4)
        bx_root.add_widget(progress_bar)
        bx_root.add_widget(bl_5)
        self.add_widget(bx_root)

    def set_center(self, web_get):
        self.ct_label.text = str(web_get)

    def set_left_bottom(self, web_get):
        self.lb_label.text = str(web_get)

    def set_right_bottom(self, web_get):
        self.rb_label.text = str(web_get)

    def set_right_top(self, web_get):
        self.rt_label.text = str(web_get)

    def set_profiler_text(self, new_profile_name):
        self.profile_label.text = str(new_profile_name)

    def set_current_text(self, new_current_name):
        self.current_label.text = str(new_current_name)

    def greet_master(self, name):
        greet = ["hi, ", "hello, ", "Master "]

        self.ct_label.text = random.choice(greet) + name +"!"
        time.sleep(2)
        self.ct_label.text = ""


class ReflectorApp(App):
    def __init__(self, wdgt, **kwargs):
        # make sure we aren't overriding any important functionality
        super(ReflectorApp, self).__init__(**kwargs)
        self.widgt = wdgt

    def build(self):
        return self.widgt


if __name__ == '__main__':
    ReflectorApp(ReflectorWidget()).run()
