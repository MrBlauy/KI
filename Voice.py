import datetime
import os
import subprocess
import time
import webbrowser
from pydub import AudioSegment
from pydub.playback import play
import pyjokes
import pyttsx3
import requests
import speech_recognition as sr
import wikipedia
import wolframalpha
from deep_translator import GoogleTranslator
from word2number import w2n
import wave
import pyaudio
import pygetwindow as gw

engine = pyttsx3.init('sapi5')
voices = engine.getProperty('voices')
engine.setProperty('voice', voices[1].id)


file_path = os.path.realpath(__file__)

start_sound = AudioSegment.from_wav(file_path.replace("Voice.py", "/audios/computerbeep_44.wav"))
stop_sound = AudioSegment.from_wav(file_path.replace("Voice.py", "/audios/computerbeep_43.wav"))


def translate(text, lang):
    if "german" in target_language:
        target_lang = "de"
    elif "english" in target_language:
        target_lang = "en"
    result = GoogleTranslator(source="en", target=target_lang).translate(text=to_be_translated)
    if target_lang == "de":
        speak(f"In {target_language} that is ")
        engine.setProperty("voice", voices[0].id)
        speak(result)
        engine.setProperty("voice", voices[1].id)
        speak("Sir")
    elif target_lang == "en":
        speak(f"In {target_language} that is {result}, Sir")


def record(time):
    hours = 0
    minutes = 0
    seconds = 0


    if ("hour" in time) or ("hours" in time):
        try:
            indx = time.lower().split().index("hours")
        except:
            indx = time.lower().split().index("hour")
        hours = w2n.word_to_num(time.lower().split()[indx - 1])

    if ("minute" in time) or ("minutes" in time):
        try:
            indx = time.lower().split().index("minutes")
        except:
            indx = time.lower().split().index("minute")
        minutes = w2n.word_to_num(query.lower().split()[indx - 1])

    if ("seconds" in time) or ("second" in time):
        print("test 1 passed")
        try:
            indx = time.lower().split().index("seconds")
        except:
            indx = time.lower().split().index("second")
        seconds = w2n.word_to_num(time.lower().split()[indx - 1])

    total_seconds = hours * 3600 + minutes * 60 + seconds    
    
    
    filename = "recorded.wav"
    chunk = 1024
    FORMAT = pyaudio.paInt16
    channels = 2
    sample_rate = 44100
    record_seconds = total_seconds
    p = pyaudio.PyAudio()

    stream = p.open(format=FORMAT,
                channels=channels,
                rate=sample_rate,
                input=True,
                output=True,
                frames_per_buffer=chunk)
    frames = []
    print("Recording...")
    for i in range(int(sample_rate / chunk * record_seconds)):
        data = stream.read(chunk)
        stream.write(data)
        frames.append(data)
    print("Finished recording.")
    stream.stop_stream()
    stream.close()
    p.terminate()

    wf = wave.open(filename, "wb")
    wf.setnchannels(channels)
    wf.setsampwidth(p.get_sample_size(FORMAT))
    wf.setframerate(sample_rate)
    wf.writeframes(b"".join(frames))
    wf.close()


def timer(query):
    hours = 0
    minutes = 0
    seconds = 0


    if ("hour" in query) or ("hours" in query):
        try:
            indx = query.lower().split().index("hours")
        except:
            indx = query.lower().split().index("hour")
        hours = w2n.word_to_num(query.lower().split()[indx - 1])

    if ("minute" in query) or ("minutes" in query):
        try:
            indx = query.lower().split().index("minutes")
        except:
            indx = query.lower().split().index("minute")
        minutes = w2n.word_to_num(query.lower().split()[indx - 1])

    if ("seconds" in query) or ("second" in query):
        print("test 1 passed")
        try:
            indx = query.lower().split().index("seconds")
        except:
            indx = query.lower().split().index("second")
        seconds = w2n.word_to_num(query.lower().split()[indx - 1])

    timer_time = [hours, minutes, seconds]


    if (timer_time[0] == 0) and (timer_time[1] == 0) and (timer_time[2] == 0):
        speak("Time invalid, Sir")
        input()

    else:
        total_seconds = timer_time[0] * 3600 + timer_time[1] * 60 + timer_time[2]
        speak("Timer is set.")
        while total_seconds > 0:
            timer = datetime.timedelta(seconds=total_seconds)

            print(timer, end="\r")

            time.sleep(1)

            total_seconds -= 1

            if total_seconds == 3600:
                speak("1 hour left, Sir")

            if total_seconds == 1800:
                speak("30 minutes left, Sir")

            if total_seconds == 900:
                speak("15 minutes left, Sir")

            if total_seconds == 300:
                speak("5 minutes left, Sir")    

        speak("Time is over, Sir")
        

def speak(audio):
    engine.say(audio)
    engine.runAndWait()


def wishMe():
    hour = int(datetime.datetime.now().hour)
    if hour >= 0 and hour < 12:
        speak("Good Morning Sir !")

    elif hour >= 12 and hour < 18:
        speak("Good Afternoon Sir !")

    else:
        speak("Good Evening Sir !")

    assname = ("Computer")
    speak((assname, "started succesfully, Sir"))


def takeCommand():
    r = sr.Recognizer()

    with sr.Microphone() as source:

        r.pause_threshold = 0.5
        audio = r.listen(source)

    try:
        query = r.recognize_google(audio, language='en-in')
        print(f"User said: {query}\n")

    except:
        pass
        return "None"

    return query


if __name__ == "__main__":
    clear = lambda: os.system("cls")

    clear()
    wishMe()

    WAKE = "computer"
    while True:
        waking = takeCommand().lower()

        if waking.count(WAKE) > 0:
            play(start_sound)
            while True:
                query = takeCommand().lower()

                if 'wikipedia' in query:
                    speak('Searching Wikipedia...')
                    query = query.replace("wikipedia", "")
                    results = wikipedia.summary(query, sentences=3)
                    speak("According to Wikipedia")
                    speak(results)

                elif 'open youtube' in query:
                    speak("Here you go to Youtube\n")
                    webbrowser.open("youtube.com", new=2, autoraise=True)

                elif 'open google' in query:
                    speak("Here you go to Google\n")
                    webbrowser.open("google.com")

                elif 'the time' in query:
                    named_tuple = time.localtime() # get struct_time
                    time_string = time.strftime("%I:%M %p", named_tuple)

                    speak(("It is", time_string))
                    
                elif "change name" in query:
                    speak("What would you like to call me, Sir ")
                    assname = takeCommand()
                    speak("Thanks for naming me")
                    
                elif "calculate" in query:
                    app_id = "85T9L6-P8T935LXE2"
                    client = wolframalpha.Client(app_id)
                    indx = query.lower().split().index('calculate')
                    query = query.split()[indx + 1:]
                    res = client.query(' '.join(query))
                    answer = next(res.results).text
                    speak("The answer is " + answer)

                elif 'search' in query or 'play' in query:
                    query = query.replace("search", "")
                    query = query.replace("play", "")
                    webbrowser.open(query)

                elif "what is" in query or "who is" in query:
                    client = wolframalpha.Client("85T9L6-P8T935LXE2")
                    res = client.query(query)

                    try:
                        print(next(res.results).text)
                        speak(next(res.results).text)
                    except StopIteration:
                        print("No results")

                elif "restart" in query:
                    subprocess.call(["shutdown", "/r"])

                elif "hibernate" in query or "sleep" in query:
                    speak("Hibernating")
                    subprocess.call("shutdown / h")

                elif "log off" in query or "sign out" in query:
                    speak("Make sure all the application are closed before sign-out")
                    time.sleep(5)
                    subprocess.call(["shutdown", "/l"])

                elif "write a note" in query:
                    speak("What should i write, sir")
                    note = takeCommand()
                    speak("Do you want me to keep the Other Notes in the file, Sir?")
                    keep = takeCommand()
                    now = time.localtime() # get struct_time
                    dt_string = time.strftime("%d/%m/%Y %H:%M %p", now)
                    if "yes" in keep:
                        file = open('computer.txt', 'a')
                        file.write(dt_string + note)
                    else:
                        file = open('computer.txt', 'w')
                        file.write(dt_string + note)
                    file.close()
                    speak("Note has been written, Sir")

                elif "show note" in query:
                    speak("Showing Notes")
                    file = open("computer.txt", "r")
                    speak(file.read())
                    file.close()

                elif "delete note" in query:
                    speak("Are you sure, Sir?")
                    if takeCommand() == "yes":
                        file = open("computer.txt", "w")
                        file.write("")
                        file.close()
                        speak("Content deleted, Sir.")
                    

                elif "translate" in query:
                    to_be_translated = query.replace("translate", "")
                    speak("What Language do you want it to be translated to?")
                    target_language = takeCommand().lower()
                    translate(to_be_translated, target_language)

                elif "joke" in query:
                    speak(pyjokes.get_joke())

                elif "date" in query:
                    today = datetime.date.today()
                    speak(f"Today'S Date is {today}")

                elif "timer" in query:
                    timer(query)

                elif "weather" in query:
                    city = "dresden"
                    url = 'https://wttr.in/{}'.format(city)
                    result = requests.get(url)

                    print(result.text)
                    speak("Look to the Console. I have displayed the weatherreport for {}".format(city))
                    time.sleep(10)

                elif "pip" in query:
                    speak("Enter in the Terminal which Module you want to Install")
                    module = input("Module: ")
                    speak("Module is being installed, Sir")
                    os.system("pip install --upgrade pip")
                    os.system(f"pip install --upgrade {module}")
                    speak("Module has been succesfully installed, Sir")

                elif ("open" in query) or ("start" in query):
                    if "destiny" in query:
                        subprocess.call("D:\Steam\Steam.exe -applaunch 1085660")
                    elif "valorant" in query:
                        subprocess.call('"C:\Riot Games\Riot Client\RiotClientServices.exe" --launch-product=valorant --launch-patchline=live"')
                    elif "steam" in query:
                        subprocess.call("D:\Steam\Steam.exe")
                    elif "epic games" in query:
                        subprocess.call('"D:\Epic Games\Launcher\Portal\Binaries\Win32\EpicGamesLauncher.exe"')
                    elif "browser" in query:
                        subprocess.call('"C:/Users/beate/AppData/Local/Programs/Opera GX/launcher.exe"')
                    speak("Start succesful, Sir")

                elif ("close" in query) or ("end" in query):
                    if "destiny" in query:
                        title = "Destiny 2"
                    elif "valorant" in query:
                        title = "Valorant"
                    elif "steam" in query:
                        title = "Steam"
                    elif "epic games" in query:
                        title = "Epic Games"
                    elif "browser" in query:
                        title = "opera"
                    window = gw.getWindowsWithTitle(title)[0]
                    window.close()
                    speak("Closing succesful, Sir")
                
                elif "record" in query:
                    speak("how long do you want me to record,sir")
                    duartion = takeCommand()
                    record(duartion)
                    speak("recorded sucessfully, sir")

                elif "maximize" in query:
                    if "destiny" in query:
                        title = "Destiny 2"
                    elif "valorant" in query:
                        title = "Valorant"
                    elif "steam" in query:
                        title = "Steam"
                    elif "epic games" in query:
                        title = "Epic Games"
                    elif "browser" in query:
                        title = "opera"

                    window = gw.getWindowsWithTitle(title)[0]
                    window.maximize()
                    


                else:
                    clear()
                    play(stop_sound)
                    break
