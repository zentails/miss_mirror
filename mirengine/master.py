import multiprocessing
import threading

import time

import gasdetect
import mirtools
import mirbase
import recogniser
import reflector
import web_interfaces


def printMan(m=2, text="---------------------------------------------------"):
    while True:
        print("{}_{}".format(text, m))
        time.sleep(m)


class Master():
    def __init__(self):
        print("________MASTER UP________")

        # Faace Reccogniser Part
        self.rec_obj = recogniser.Recogniser()
        self.reload_face_sig_q = self.rec_obj.reload_face_sig_q
        self.profile_change_to_q = self.rec_obj.profile_change_to_q
        self.current_front_q = self.rec_obj.current_front_q

        # Reflector Recognition Part
        self.reflector_widget = reflector.ReflectorWidget()

        # Mirabase
        self.mirbase_obj = mirbase.Mirbase(self.rec_obj.reload_face_sig_q)

        # Web interface objects
        self.web_weather = web_interfaces.WebWeather()
        self.web_news = web_interfaces.WebNews()
        self.web_quote = web_interfaces.WebQuote()

    def start(self):
        threading.Thread(target=self.current_update_man).start()
        threading.Thread(target=self.profile_update_man).start()
        threading.Thread(target=printMan).start()
        self.rec_obj.start_recogniser()

        # Smoke Detction
        gas_detector_obj = gasdetect.GasDetector(self)
        gas_detector_obj.run_detector()

        reflector.ReflectorApp(self.reflector_widget).run()

    def update_reflector(self, user):
        print(user)
        self.reflector_widget.set_right_bottom(self.web_quote)
        if not user:
            print("returning")
            self.reflector_widget.set_left_bottom(None)
            self.reflector_widget.set_right_top(None)
            return
        print("updating")
        pref = user['preferences']
        if pref['news']:
            self.reflector_widget.set_left_bottom(self.web_news)
        else:
            self.reflector_widget.set_left_bottom(None)
        if pref['weather']:
            self.reflector_widget.set_right_top(self.web_weather)
        else:
            self.reflector_widget.set_right_top(None)

    def show_log(self, text, time_hold=8, send_notification=False):
        threading.Thread(target=self.reflector_widget.log_man, args=(text, time_hold)).start()
        if send_notification:
            self.mirbase_obj.push_notification("Warning", text)

    def dump_delete_me(self):
        print("?>>>>dump_delete man in ")
        self.reflector_widget.set_right_top(self.web_weather)
        print("left bottom up????????????????????????????????")
        time.sleep(1)
        self.reflector_widget.set_left_bottom(self.web_news)
        time.sleep(1)
        self.reflector_widget.set_right_bottom(self.web_quote)

    def profile_update_man(self):
        print(">>Profile Update Man in")
        while True:
            id = self.profile_change_to_q.get(block=True)
            user = mirtools.get_name(self.mirbase_obj.get_users(), id)
            if user:
                name = user['username']
                self.update_reflector(user)
            else:
                name = "Stranger"
                self.update_reflector(user)
                self.mirbase_obj.push_notification("Stranger Detected", "A stranger has been detected",
                                                   self.mirbase_obj.capture_upload_photo())
            print("--##-{}----------->{}".format(id, name))
            self.reflector_widget.set_profiler_text(name)
            self.reflector_widget.greet_master(name)

    def current_update_man(self):
        print(">>Current Update Man in")
        while True:
            tx = self.current_front_q.get(block=True)
            if not tx:
                tx = "Stranger"
            print("--##------------>{}".format(tx))
            self.reflector_widget.set_current_text(tx)

    def profile_update_reflector(self, profile_id):
        self.reflector_widget.set_left_bottom(profile_id)


if __name__ == '__main__':
    Master().start()
