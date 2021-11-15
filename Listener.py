import speech_recognition as sr

from TTSEngine import TTSEngine


def listen():
    rec = sr.Recognizer()
    mic = sr.Microphone()
    rec.pause_threshold = 2
    with mic as source:
        print('Listening...')
        audio = rec.listen(source, phrase_time_limit=10)
    try:
        res = rec.recognize_google(audio, language='en-us')
        return res
    except sr.UnknownValueError as err:
        return None


def wait_for(param, engine: TTSEngine):
    engine.say(param)
    res = listen()
    while not res:
        res = listen()
    return res
