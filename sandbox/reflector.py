import os
import threading
from tkinter import *


master = os.path.abspath(os.path.join(__file__, '..', '..'))
sys.path.append(master)


from sandbox import news, quotes, weather


def set_weather_and_quote(weather_label_text, quote_label_text, newsaa):
    quote_label_text.set(quotes.get_quote())
    weather_label_text.set(weather.get_details())
    newsaa.set(news.get_news())


def set_current_front(current_front_label_text, currennt_front):
    while True:
        current_front_label_text.set(str(currennt_front.get()))


def set_active_profile(active_profile_label_text, profile_change_to):
    while True:
        active_profile_label_text.set(str(profile_change_to.get()))


def start_reflector(current_front, profile_change_to):
    root = Tk()
    root.configure(background='black')

    root.attributes('-fullscreen', True)

    f1 = Frame(root, bg="black")
    f2 = Frame(root, bg="black")
    f3 = Frame(root, bg="black")
    f4 = Frame(root, bg="black")

    f41profile = Frame(f4, bg="black")

    f1.pack(side="top", fill="both", expand=True)
    f2.pack(side="top", fill="both", expand=True)
    f3.pack(side="top", fill="both", expand=True)
    f4.pack(side="top", fill="both", expand=True)
    f41profile.pack(side="bottom", fill=X)

    active_profile_label_text = StringVar()
    weather_label_text = StringVar()
    quote_label_text = StringVar()
    riddle_label_text = StringVar()
    news_label_text = StringVar()
    current_front_label_text = StringVar()

    Label(f41profile, textvariable=active_profile_label_text, font=("Helvetica", 15), fg="white", bg='black').pack(
        side='right', fill='none', padx=14)
    Label(f1, textvariable=weather_label_text, font=("Helvetica", 15), fg="white", bg='black').pack(side='right',
                                                                                                    fill='none',
                                                                                                    padx=14)
    Label(f1, textvariable=quote_label_text, font=("Helvetica", 15), fg="white", bg='black').pack(side='left',
                                                                                                  fill='none', padx=14)
    Label(f2, textvariable=riddle_label_text, font=("Helvetica", 15), fg="white", bg='black').pack(side='left',
                                                                                                   fill='none', padx=14)
    Label(f4, textvariable=news_label_text, font=("Helvetica", 8), fg="white", bg='black').pack(side='left',
                                                                                                fill='none',
                                                                                                padx=14)
    Label(f41profile, textvariable=current_front_label_text, font=("Helvetica", 15), fg="white", bg='black').pack(
        side='left',
        fill='none',
        padx=14)
    Label(f41profile, textvariable=active_profile_label_text, font=("Helvetica", 15), fg="white", bg='black').pack(
        side='left',
        fill='none',
        padx=14)

    active_profile_label_text.set("Sylveryte")

    # THREADS
    weather_and_quotes_thread = threading.Thread(name='weather', target=set_weather_and_quote,
                                                 args=(weather_label_text, quote_label_text, news_label_text))
    weather_and_quotes_thread.start()

    current_front_thread = threading.Thread(name='current_front', target=set_current_front,
                                            args=(current_front_label_text, current_front))
    current_front_thread.start()

    current_front_thread = threading.Thread(name='current_front', target=set_active_profile,
                                            args=(active_profile_label_text, profile_change_to))
    current_front_thread.start()

    root.mainloop()
