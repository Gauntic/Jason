from dotenv import load_dotenv
import pyttsx3

import Config
import Listener
from TTSEngine import TTSEngine
from Parser import Parser

load_dotenv()
va_name = 'Jason'
engine = TTSEngine(pyttsx3.init())

if __name__ == '__main__':
    parser = Parser(engine, va_name)
    run = True

    try:
        engine.greet(Config.get_config('name'))
        while run:
            run = parser.parse(Listener.listen() or '')
    except KeyboardInterrupt:
        run = False
        engine.end()
