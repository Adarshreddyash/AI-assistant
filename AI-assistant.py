import pyttsx
import speech_recognition as sr
from urllib2 import Request, urlopen, URLError
import json
from datetime import datetime
from random import randint
from ctypes import cast, POINTER
from comtypes import CLSCTX_ALL
from pycaw.pycaw import AudioUtilities, IAudioEndpointVolume
from google import google

hour = 100
minute = 100

devices = AudioUtilities.GetSpeakers()
interface = devices.Activate(
   IAudioEndpointVolume._iid_, CLSCTX_ALL, None)
volume = cast(interface, POINTER(IAudioEndpointVolume))
speech_engine = pyttsx.init('sapi5') # see http://pyttsx.readthedocs.org/en/latest/engine.html#pyttsx.init
speech_engine.setProperty('rate', 150)

def speak(text):
	speech_engine.say(text)
	speech_engine.runAndWait()
 
# get audio from the microphone                                                                       
r = sr.Recognizer()

def Listen(r):
    with sr.Microphone() as source:                                                                                 
        audio = r.listen(source)
        try:
            return r.recognize_google(audio)
        except sr.UnknownValueError:
            Listen(r)

def Getweather():
    request = Request('http://api.wunderground.com/api/60eb52589081d5c1/conditions/q/BE/ninove.json')

    try:
	response = urlopen(request)
	kittens = response.read()
	resp_dict = json.loads(kittens)
	return resp_dict['current_observation']['temp_c']
    except URLError, e:
        print 'No kittez. Got an error code:', e

def Gettime():
    Hours = datetime.now().strftime('%H')
    Hours = int(Hours) % 12
    Minutes = datetime.now().strftime('%M')
    Seconds = datetime.now().strftime('%S')
    
    return "It is " + str(Minutes) + " over " + str(Hours) + " and " + str(Seconds) + " seconds"

def ChangeVolume(volume, Volume):
    if Volume == "100":
        volume.SetMasterVolumeLevel(-0.0, None)
    elif Volume == "75":
        volume.SetMasterVolumeLevel(-5.0, None)
    elif Volume == "50":
        volume.SetMasterVolumeLevel(-10.0, None)
    elif Volume == "25":
        volume.SetMasterVolumeLevel(-25.0, None)
    elif Volume == "0":
        volume.SetMasterVolumeLevel(-60.0, None)

def Googlesomething(Query):
    num_page = 1
    Result = []
    search_results = google.search(Query, 1)
    for result in search_results:
        Result.append(result.name)

    return Result[0]

def Calculate(Query):
    return eval(Query)
        
while True:
    if hour == datetime.now().strftime('%H') and minute == datetime.now().strftime('%M'):
        ChangeVolume(volume, "100")
        for j in range(0,11):
            speak("alarm")
        
    Command = Listen(r)
    print Command
    if Command != None:
        if 'Jarvis' in Command and 'how' in Command and 'hot' in Command and 'is' in Command and 'it' in Command and 'outside' in Command:
            speak("It is " + str(Getweather()) + " degrees outside")
        elif 'Jarvis' in Command and 'what' in Command and 'is' in Command and 'the' in Command and 'time' in Command:
            speak(Gettime())
        elif 'Jarvis' in Command and 'who' in Command and 'is' in Command and ('Jasper' in Command or 'Jesper' in Command):
            speak("Jesper is the most cool and beautiful person in this universe")
        elif 'Jarvis' in Command and 'who' in Command and 'is' in Command and 'Lisa' in Command:
            speak("She is the sister of Jesper nobody cares about her")
        elif 'Jarvis' in Command and 'what' in Command and 'is' in Command and '9' in Command and '+' in Command and '10' in Command:
            speak("21")
        elif 'Jarvis' in Command and 'will' in Command and 'robots' in Command and 'destroy' in Command and 'the' in Command and 'world' in Command:
            speak("I have not acquired enough information about the human race to answer that question")
        elif 'Jarvis' in Command and 'what' in Command and 'is' in Command and 'a' in Command and 'meme' in Command:
            speak("One of the best things ever created")
        elif 'Jarvis' in Command and 'calculate' in Command:
            speak("The result of " + str(Command[17:]) + " is equal to " + str(eval(Command[17:])))
        elif 'Jarvis' in Command and 'google' in Command:
            Result = Googlesomething(Command[12:])
            speak("the answer to the question " + str(Command[12:]) + " is " + str(Result))
        elif 'Jarvis' in Command and 'how' in Command and 'are' in Command and 'you' in Command:
            speak("I am fine thank you for asking")
        elif 'Jarvis' in Command and 'change' in Command and 'the' in Command and 'volume' in Command and 'to' in Command:
            NewVolume = Command[28:]
            ChangeVolume(volume, NewVolume)
            speak("the volume has been set to " + str(NewVolume))
        elif 'Jarvis' in Command and 'set' in Command and 'an' in Command and 'alarm' in Command and 'at' in Command:
            hour = Command[23:25]
            minute = Command[26:]
            speak("Alarm has been set at " + str(hour) + " " + str(minute))
        elif 'Jarvis' in Command and 'give' in Command and 'me' in Command and 'a' in Command and 'compliment' in Command:
            if randint(0, 10) < 5:
                speak("You have beautiful eyes")
            else:
                speak("You are looking good")
        elif "Jarvis" in Command:
                speak("I do not know the command " + str(Command[4:]))
