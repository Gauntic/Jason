import pyttsx3


class TTSEngine:
    def __init__(self, engine: pyttsx3.Engine):
        self.engine = engine

    def say(self, phrase):
        self.engine.say(phrase)
        print(phrase)
        self.engine.runAndWait()

    def greet(self, name=None):
        self.say(f'Hello{", " + name if name else ""}!')

    def end(self):
        if self.engine.isBusy():
            self.engine.endLoop()
        self.say('Goodbye')
