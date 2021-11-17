## Jason Voice Assistant
___
Jason is a simple voice assistant made in Python that provides both unique and useful functions to make everyday computer easier. 

Jason responds every time his name is said. The rest of a command is then parsed, and sent to complete one of a growing number of functions.

Jason utilizes various libraries and APIs in order to function. Associated dependencies are listed next to functions.

The main dependencies of Jason, which are required for its most basic functionality, are [pyttsx3](https://github.com/nateshmbhat/pyttsx3) for text-to-speech and [SpeechRecognition](https://github.com/Uberi/speech_recognition) for speech-to-text.
Jason uses SpeechRecognition's included interface with the [Google Speech to Text API](https://cloud.google.com/speech-to-text/) for speech recognition.

In order to run Jason, the only required dependency is ffmpeg, which can be downloaded [here](https://www.ffmpeg.org/download.html). Once ffmpeg is properly installed and on the computer's PATH, the compiled executable should run properly.

Upon running, Jason will inquire a user's name; this and all other necessary

Basic Commands

|Name|Input|Output|
|---|---|---|
|Greet|Called on start; additionally, is called on `hi`, `hello`, `greetings` and `hey`.|Jason responds with `Hello!` On startup, he additionally says the name configured in SetName
|SetName|Called on `call me [name]`, `my name is [name]` and `my name's [name`.|