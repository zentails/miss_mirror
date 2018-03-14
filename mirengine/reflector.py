import time

from kivy.app import App
from kivy.clock import Clock
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.floatlayout import FloatLayout
from kivy.uix.label import Label
from kivy.uix.progressbar import ProgressBar


class IncrediblyCrudeClock(Label):
    def update(self, *args):
        self.text = time.asctime()


class ReflectorWidget(FloatLayout):
    def __init__(self, **kwargs):
        # make sure we aren't overriding any important functionality
        super(ReflectorWidget, self).__init__(**kwargs)

        long_text = "lb A consultant is someone who takes a subject you understand and makes it sound confusing"

        bx_root = BoxLayout(orientation='vertical', padding=60)

        w_l = BoxLayout(orientation="horizontal", size_hint=(1, 0.2))
        wl_clock = IncrediblyCrudeClock(text_size=self.size, valign='top', halign='left', text=long_text, markup=True)
        wl_clock.bind(size=wl_clock.setter('text_size'))
        Clock.schedule_interval(wl_clock.update, 1)
        w_l.add_widget(wl_clock)

        bl_1 = BoxLayout(orientation="horizontal")
        lt_label = Label(text_size=self.size, valign='top', halign='left', text=long_text, markup=True)
        rt_label = Label(text_size=self.size, valign='top', halign='right', text=long_text, markup=True)
        lt_label.bind(size=lt_label.setter('text_size'))
        rt_label.bind(size=rt_label.setter('text_size'))
        bl_1.add_widget(lt_label)
        bl_1.add_widget(rt_label)

        bl_2 = BoxLayout(orientation="horizontal")
        ct_label = Label(valign='center', halign='right', text=long_text, markup=True)
        bl_2.add_widget(ct_label)

        bl_3 = BoxLayout(orientation="horizontal")
        rb_label = Label(text_size=self.size, valign='bottom', halign='right', text=long_text, markup=True)
        lb_label = Label(text_size=self.size, valign='bottom', halign='left', text=long_text, markup=True)
        rb_label.bind(size=rb_label.setter('text_size'))
        lb_label.bind(size=lb_label.setter('text_size'))
        bl_3.add_widget(lb_label)
        bl_3.add_widget(rb_label)

        bl_4 = BoxLayout(orientation="horizontal", size_hint=(1, 0.1))
        self.profile_label = Label(valign='center', halign='right', text="profile")
        self.current_label = Label(valign='center', halign='right', text='current')
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

    def set_profiler_text(self, new_profile_name):
        self.profile_label.text = str(new_profile_name)

    def set_current_text(self, new_current_name):
        self.current_label.text = str(new_current_name)


class ReflectorApp(App):
    def __init__(self, wdgt, **kwargs):
        # make sure we aren't overriding any important functionality
        super(ReflectorApp, self).__init__(**kwargs)
        self.widgt = wdgt

    def build(self):
        return self.widgt


if __name__ == '__main__':
    ReflectorApp(ReflectorWidget()).run()
