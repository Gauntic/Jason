import difflib
import os
import re
import subprocess
import threading
import time
import webbrowser
from datetime import timedelta
from tkinter import ttk, PhotoImage, Tk, filedialog, StringVar

import geocoder
import requests
from PIL import Image
from plyer import notification
from pyautogui import press
from wikipedia import wikipedia

import Config
import Listener
from TTSEngine import TTSEngine


class Parser:
    def __init__(self, engine: TTSEngine, va_name):
        self.engine = engine
        self.va_name = va_name

    def parse(self, command):
        command = command.lower()
        if self.va_name.lower() not in command:
                return True
        command = command.replace(self.va_name.lower(), '').strip()
        if command.startswith('please'):
            command = command.replace('please', '').strip()

        if re.compile('call me .*$').match(command):
            self.set_name(command.replace('call me', '').strip().title())
        elif re.compile('my name is .*$').match(command):
            self.set_name(command.replace('my name is', '').strip().title())
        elif re.compile('my name\'s .*$').match(command):
            self.set_name(command.replace('my name\'s', '').strip().title())
        elif re.compile('my name .*$').match(command):
            self.set_name(command.replace('my name', '').strip().title())
        elif ('hi' in command or 'hello' in command or 'greetings' in command
              or 'hey' in command):
            self.engine.greet()
        elif command.startswith('open '):
            self.open_app(command[5:])
        elif command == 'add app':
            self.prompt_alias('app')
        elif command.startswith('news'):
            self.get_news(command.replace('news', '').strip())
        elif command == 'pause' or command == 'paz':
            self.pause_media()
        elif command == 'volume up':
            self.vol_up()
        elif command == 'volume down':
            self.vol_down()
        elif command == 'censor jokes':
            Config.set_config('joke_censor', True)
        elif command == 'remove joke censor':
            Config.set_config('joke_censor', False)
        elif 'joke' in command:
            self.get_joke(censor=Config.get_config('joke_censor'))
        elif command == 'add site' or command == 'adsight':
            self.prompt_alias('site')
        elif command.startswith('search '):
            self.search(command[7:])
        elif command.startswith('wiki '):
            self.search(command[5:])
        elif command.startswith('calculate '):
            self.calc(command.replace('calculate', '').strip())
        elif command.startswith('define '):
            self.define(command.replace('define', '').strip())
        elif 'notify' in command or 'notification' in command:
            self.notification_gui()
        elif command == 'what\'s your name' or command == 'who are you':
            self.engine.say('I\'m ' + self.va_name + ', a voice assistant created by Gauntic.')
        elif command.startswith('thank you') or command.startswith('thanks'):
            self.engine.say('You\'re welcome.')
        elif command == 'exit' or command == 'close' or command == 'bye' or command == 'goodbye':
            self.engine.end()
            return False
        else:
            self.engine.say('Sorry, I didn\'t understand you')
        return True

    # Makes a prompt to add either an app or site alias (tkinter, difflib)
    def prompt_alias(self, t):
        root = Tk()
        frame = ttk.Frame(root, padding=10)
        root.iconphoto(False, PhotoImage(file='logo.png'))
        root.title(t.title() + ' alias')
        frame.grid()

        def cancel_alias():
            root.destroy()
            self.engine.say('alias discarded')

        def save_alias(n, p):
            root.destroy()
            if not deleted == [True, True] or n == '' or p == '':
                self.engine.say('alias discarded')
                return
            self.engine.say('alias saved')
            Config.set_config_alias(n, p, t)

        def file_search():
            filetypes = (
                ('executable files', '*.exe'),
                ('All files', '*.*')
            )
            deleted[0] = True
            filename = filedialog.askopenfilename(
                title='Open a file',
                initialdir='/',
                filetypes=filetypes)
            entry.delete(0, len(path.get()))
            entry.insert(0, filename)

        path = StringVar()
        entry = ttk.Entry(frame, textvariable=path, width=50)
        deleted = [False, False]
        entry.insert(10, "File location:" if t == 'app' else 'URL:')

        def delHint(e, sv, deleted_vars, i, start_text):
            diff = [li for li in difflib.ndiff(sv.get(), start_text) if li[0] != ' ']
            if not deleted_vars[i]:
                e.delete(0, len(sv.get()))
                deleted_vars[i] = True
                if diff[0].startswith('-'):
                    e.insert(1000, ''.join([d[-1] for d in diff]))

        path.trace('w', lambda n, index, mode, sv=path: delHint(entry, path, deleted, 0,
                                                                ("File location:" if t == 'app' else 'URL:')))
        entry.grid(row=0, column=0)
        if t == 'app':
            button = ttk.Button(frame, text="Find file", command=file_search)
            button.grid(row=0, column=1, columnspan=2, sticky='NESW')
        name = StringVar()
        entry2 = ttk.Entry(frame, textvariable=name)
        entry2.insert(10, "Alias name:")
        name.trace('w', lambda n, index, mode, sv=name: delHint(entry2, name, deleted, 1, 'Alias name:'))
        entry2.grid(row=1, column=0)
        button = ttk.Button(frame, text="Add Alias", command=lambda: save_alias(name.get(), path.get()))
        button.grid(row=1, column=1)
        button = ttk.Button(frame, text="Discard Alias", command=cancel_alias)
        button.grid(row=1, column=2)
        root.protocol('WM_DELETE_WINDOW', cancel_alias)

        root.mainloop()

    # Creates a GUI prompt to schedule an OS notification (tkinter)
    def notification_gui(self):
        root = Tk()
        frame = ttk.Frame(root, padding=10)
        root.iconphoto(False, PhotoImage(file='logo.png'))
        root.title('New Notification')
        frame.grid()
        file_name = StringVar()

        def cancel_notif():
            root.destroy()
            self.engine.say('Notification discarded')

        def save_notif(t, m, dt):
            root.destroy()
            if t == '' or m == '' or not file_name.get():
                self.engine.say('Notification discarded')
                return
            self.engine.say('Notification saved')
            self.set_notification(t, m, file_name.get(), dt)

        def file_search():
            filetypes = (
                ('png file', '*.png'),
                ('jpg file', '*.jpg'),
            )
            filename = filedialog.askopenfilename(
                title='Open a file',
                initialdir='/',
                filetypes=filetypes)
            file_name.set(filename)

        label1 = ttk.Label(frame, text="Notification Title")
        title = StringVar()
        entry = ttk.Entry(frame, textvariable=title, width=50)
        entry.grid(row=1, column=0, columnspan=3)
        label1.grid(row=0, column=0, columnspan=3)

        label2 = ttk.Label(frame, text="Notification Message")
        message = StringVar()
        entry2 = ttk.Entry(frame, textvariable=message, width=50)
        entry2.grid(row=3, column=0, columnspan=3)
        label2.grid(row=2, column=0, columnspan=3)

        def val_changed():
            time_label.set(
                f'Notification Time ({int(hr_entry.get()):02d}:{int(min_entry.get()):02d}:{int(sec_entry.get()):02d})'
            )

        time_label = StringVar()
        time_label.set("Notification Time (00:00:00)")
        label3 = ttk.Label(frame, textvariable=time_label)
        hr_entry = ttk.Spinbox(frame, from_=0, to=24, command=val_changed)
        hr_entry.grid(row=5, column=0)
        hr_entry.set(0)
        min_entry = ttk.Spinbox(frame, from_=0, to=59, command=val_changed)
        min_entry.grid(row=5, column=1)
        min_entry.set(0)
        sec_entry = ttk.Spinbox(frame, from_=0, to=59, command=val_changed)
        sec_entry.grid(row=5, column=2)
        sec_entry.set(0)

        icon_label = ttk.Label(frame, textvariable=file_name)
        icon_label.grid(row=6, column=0, columnspan=2)
        file_picker = ttk.Button(frame, text="Select icon", command=file_search)
        file_picker.grid(row=6, column=2)

        label3.grid(row=4, column=0, columnspan=3)

        button1 = ttk.Button(
            frame,
            text="Save Notification",
            command=lambda: save_notif(title.get(), message.get(), timedelta(seconds=int(sec_entry.get()),
                                                                             minutes=int(min_entry.get()),
                                                                             hours=int(hr_entry.get())))
        )
        button1.grid(row=0, column=3, rowspan=6, sticky='NESW')
        button2 = ttk.Button(frame, text="Discard Notification", command=cancel_notif)
        button2.grid(row=0, column=4, rowspan=6, sticky='NESW')
        root.protocol('WM_DELETE_WINDOW', cancel_notif)

        root.mainloop()

    # Schedules then deploys an OS notification. (threading, plyer)
    def set_notification(self, title, message, icon_file, delta_time: timedelta):
        def notify():
            time.sleep(delta_time.total_seconds())
            icon = Image.open(icon_file)
            new_file = '.'.join(icon_file.split('.')[:-1]) + '.ico'
            icon.save(new_file)
            notification.notify(
                title=title,
                message=message,
                timeout=10,
                app_icon=new_file,
                app_name=self.va_name + ' Voice Assistant',
            )

        threading.Thread(target=notify).start()

    # Opens either an app or website based on a parameter and the config file. (subprocess, webbrowser)
    def open_app(self, string):
        app_aliases = Config.get_config('app_aliases')
        site_aliases = Config.get_config('site_aliases')
        if not app_aliases and not site_aliases:
            return
        for key in app_aliases:
            if key.lower() == string.lower():
                def try_open():
                    try:
                        subprocess.call(app_aliases[key], shell=False)
                    except OSError:
                        self.engine.say('sorry, that is not an executable file')

                threading.Thread(target=try_open).start()
                return
        for key in site_aliases:
            if key.lower() == string.lower():
                def try_open():
                    if not webbrowser.open(site_aliases[key]):
                        self.engine.say('sorry, that is not a valid URL')

                threading.Thread(target=try_open).start()
                return
        self.engine.say('Sorry, I can\'t find a program or site by that name.')

    # Sets the configured user name
    def set_name(self, val):
        Config.set_config('name', val)
        self.engine.greet()

    # Searches Wikipedia for a topic and says the first few lines of the result. (wikipedia)
    def search(self, param):
        try:
            summary = wikipedia.summary(param, sentences=3, redirect=True)
            self.engine.say(f'According to Wikipedia,')
            self.engine.say(summary)
        except wikipedia.DisambiguationError:
            self.engine.say('Sorry, I could not find a Wikipedia article.')

    run = True

    # Defines a word or phrase using the Wolfram Alpha API (requests)
    def define(self, param):
        url = 'https://api.wolframalpha.com/v2/query?input=' + param + '&appid=' + os.environ.get('WOLFRAM_APP_ID') + \
              '&format=plaintext&output=json'
        res = requests.get(url).json()
        if not res['queryresult']['pods']:
            self.engine.say('Not found.')
            return
        title = res['queryresult']['pods'][0]['subpods'][0]['plaintext']
        info = res['queryresult']['pods'][1]['subpods'][0]['plaintext']

        self.engine.say(title)
        self.engine.say(info)

    # Calculates a result using the Wolfram Alpha API (requests)
    def calc(self, param):
        url = 'https://api.wolframalpha.com/v2/query?input=' + param + '&appid=' + os.environ.get('WOLFRAM_APP_ID') + \
              '&format=plaintext&output=json'
        try:
            res = requests.get(url).json()
            if not res['queryresult']['pods']:
                self.engine.say('Not found.')
                return
            title = res['queryresult']['pods'][0]['subpods'][0]['plaintext']
            answer = res['queryresult']['pods'][1]['subpods'][0]['plaintext']
        except Exception:
            print('Bad request.')
            self.engine.say('Sorry, try again later.')
            return

        self.engine.say(title + ' is ' + answer)

    # Returns local news from NewsAPI, with a possible query (geocoder, requests, webbrowser)
    def get_news(self, q='', i=1):
        loc = geocoder.ip('me').country
        if loc:
            url = f'https://newsapi.org/v2/top-headlines?country={loc}&q={q}&apiKey={os.environ.get("NEWS_API_KEY")}'
        else:
            url = f'https://newsapi.org/v2/top-headlines?q={q}&apiKey={os.environ.get("NEWS_API_KEY")}'
        try:
            res = requests.get(url).json()
            for n in range(i):
                if len(res['articles']) <= n:
                    self.engine.say(f'No news was found for {q}')
                    return
                article = res['articles'][n]
                self.engine.say('top article: ' + article['title'])
                response = Listener.wait_for('Would you like me to read a description?', self.engine).lower()
                if response == 'yes':
                    self.engine.say(article['description'])
                    response = Listener.wait_for('Would you like me to open the article?', self.engine).lower()
                    if response == 'yes':
                        webbrowser.open(article['url'])
        except Exception:
            print('Bad request.')
            self.engine.say('Sorry, try again later.')
            return

    # Media controls (pyautogui)
    @staticmethod
    def vol_down():
        press('volumedown')

    @staticmethod
    def vol_up():
        press('volumeup')

    @staticmethod
    def pause_media():
        press('playpause')

    # Returns and reads a joke using the JokeAPI, using safe mode if set in config.yaml (requests)
    def get_joke(self, censor=True):
        if censor is None:
            censor = True
        url = 'https://v2.jokeapi.dev/joke/Any' + ('?safe-mode' if censor else '')
        try:
            res = requests.get(url).json()
            if res['error']:
                raise Exception
            if res['type'] == 'twopart':
                joke = res['setup'] + " " + res['delivery']
            else:
                joke = res['joke']
            self.engine.say(joke)
        except Exception:
            print('Bad request.')
            self.engine.say('Sorry, try again later.')
