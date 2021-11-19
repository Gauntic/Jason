## Jason Voice Assistant

Jason is a simple voice assistant made in Python that provides both unique and useful functions to make everyday computer easier. 

Jason utilizes various libraries and APIs in order to function. Associated dependencies are listed next to functions, or a complete list can be found [here](#dependencies).

The main dependencies of Jason, which are required for its most basic functionality, are [pyttsx3](https://pypi.org/project/pyttsx3/) for text-to-speech and [SpeechRecognition](https://pypi.org/project/SpeechRecognition/) for speech-to-text.
Jason uses SpeechRecognition's included interface with the Google Speech to Text API for speech recognition.

In order to run Jason, the only required dependency is ffmpeg, which can be downloaded [here](https://www.ffmpeg.org/download.html). Once ffmpeg is properly installed and on the computer's PATH, the compiled executable should run properly.

Upon running, Jason will inquire a user's name; this and all other necessary configuration information are stored using [PyYAML](https://pypi.org/project/PyYAML/) into a config.yaml file in the same directory as the program.

### Commands

Jason responds every time his name is said. The rest of a command is then parsed, and sent to complete one of a growing number of functions.

#### Basic Commands

|Name|Input|Output|
|:---|:---|:---|
|Greet|Called on start; "hi", "hello", "greetings", "hey"|Jason replies, "Hello!"; On startup, Jason additionally repeats the name configured in `Set Name`|
|Set Name|"call me [name]", "my name is [name]", "my name's [name]"|Sets the `name` config property to [name], and then `Greet`s the user.|
|8Ball|"8 ball [query]"|Jason replies with a random standard Magic 8 Ball response.|
|Roll Dice|"roll [query]", where [query] is in the format of either a number or "[value] times [number]"|Simulates rolling a [value]-sided die [number] (defaults to 1) times; Jason replies with the sum of all results.|
|Timer|"timer [time in seconds]"|After [time in seconds] seconds, as long as Jason is still running, he will notify the user that a timer has finished.|
|Questions|any of a set number of questions about Jason|Jason responds to the question if he has an answer.|
|Thank|"thanks", "thank you"|Jason replies, "You're welcome."|
|Set Joke Censor|"censor jokes"|Sets the `joke_censor` value in the config file to true, turning on safe mode in calls to JokeAPI.|
|Remove Joke Censor|"remove joke censor"|Sets the `joke_censor` value in the config file to false, turning off safe mode in calls to JokeAPI.|
|Quit|"exit", "close", "bye", "goodbye"|Jason replies, "Goodbye" and shuts down.|

#### Applications and Website Commands
|Name|Input|Output|
|:---|:---|:---|
|Add App|"add app"|Displays a GUI allowing an app to be added to the config file for opening through Jason.|
|Add Site|"add site"|Displays a GUI allowing a website link to be added to the config file for opening through Jason.|
|Open|"open [app/site name]"|Searches the configuration file for an app then a website with the requested name, and opens it if found.|

#### Hardware functions
|Name|Input|Output|
|:---|:---|:---|
|Take Photo|"take photo"|Opens a new window using OpenCV which displays a camera feed. `Space` will take a photo and `q` will quit. Once a photo has been taken, it is copied to the user's clipboard for any use that is desired.|
|Take Video|"take video"|Opens a new window using OpenCV which displays a camera feed, which begins recording immediately. `Space` or `q` will end a recording, and closing the window will prevent the video from being saved. Once a photo has been taken, it is saved to the path `./output/output.mp4` relative to the location of Jason.|
|Notify|any phrase containing "notify" or "notification"|Displays a GUI with several options for scheduling a desktop notification with a custom title, message, and logo.|

#### Media Controls (using [PyAutoGUI](https://pypi.org/project/PyAutoGUI/))
|Name|Input|Output|
|:---|:---|:---|
|Volume Up|"volume up"|Increases media volume.|
|Volume Down|"volume down"|Decreases media volume.|
|Pause/Play|"pause"|Toggles pause on any currently playing media.|

#### API Calls
|Name|Input|Output|
|:---|:---|:---|
|Link Shortener|"shorten url"|Displays a GUI, which calls the [Bitly API](https://dev.bitly.com/) with an inputted value and returns a shortened bit.ly link.
|Joke|any phrase containing "joke"|Calls the [JokeAPI](https://v2.jokeapi.dev/) using the config value of `joke_censor` (default true) and Jason replies with the joke.|
|Calculate|"calculate [expression]"|Calls the [Wolfram&#124;Alpha API](https://products.wolframalpha.com/api/) with [expression] and Jason says the result.|
|Define|"define [word/phrase]"|Calls the [Wolfram&#124;Alpha API](https://products.wolframalpha.com/api/) with [word/phrase] and Jason says the result.|
|Wikipedia|"search [query]", "wiki [query]", "wikipedia [query]"|Calls the [MediaWiki Action API](https://www.mediawiki.org/wiki/API:Main_page) with [query] and Jason says the first few lines of the resulting article.|
|News|"news {buzzword}"|Calls the [NewsAPI](https://newsapi.org/) and searches with an optional buzzword, Jason saying the first article returned. Jason also provides options for the user to hear about the article in more detail, and will open the article inm a web browser.|

### Dependencies

##### Here is an alphabetized list of all modules and APIs used to build Jason.

- [Bitly API](https://dev.bitly.com/)
- [FFmpeg](https://www.ffmpeg.org/)
- [ffmpeg-python](https://pypi.org/project/ffmpeg-python/)
- [geocoder](https://pypi.org/project/geocoder/)
- [JokeAPI](https://v2.jokeapi.dev/)
- [MediaWiki Action API](https://www.mediawiki.org/wiki/API:Main_page)
- [NewsAPI](https://newsapi.org/)
- [numpy](https://pypi.org/project/numpy/)
- [opencv-python](https://pypi.org/project/opencv-python/)
- [Pillow](https://pypi.org/project/Pillow/)
- [plyer](https://pypi.org/project/plyer/)
- [PyAudio](https://pypi.org/project/PyAudio/)
- [PyAutoGUI](https://pypi.org/project/PyAutoGUI/)
- [python-dotenv](https://pypi.org/project/python-dotenv/)
- [pyttsx3](https://pypi.org/project/pyttsx3/)
- [pywin32](https://pypi.org/project/pywin32/)
- [PyYAML](https://pypi.org/project/PyYAML/)
- [requests](https://pypi.org/project/requests/)
- [SpeechRecognition](https://pypi.org/project/SpeechRecognition/)
- [wikipedia module](https://pypi.org/project/wikipedia/)
- [Wolfram|Alpha API](https://products.wolframalpha.com/api/)

Jason was created by Gauntic Team under the [MIT License](LICENSE)
