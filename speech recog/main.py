from asyncio import IocpProactor
from email import message
from email.mime import audio
from operator import ipow, truediv
import re
from sunau import AUDIO_FILE_ENCODING_LINEAR_16
from tokenize import Special
from neuralintents import GenericAssistant
import speech_recognition
import pyttsx3 as tts
import sys
import nltk
nltk.download('omw-1.4')

recognizer =speech_recognition.Recognizer()

speaker =tts.init()
speaker.setProperty('rate',150)

todo_list =[ 'fo shopping'  , 'clean room']

def create_note():
    global recognizer

    speaker.say("what do you want to write onto your note")
    speaker.runAndWait()

    done =False

    while not done:

        try:
            with speech_recognition.Microphone() as mic:
                recognizer.adjust_for_ambient_noise(mic,duration=0.2)
                audio =recognizer.listen(mic)
                note =recognizer.recognize_google(audio)
                note=note.lower()

                speaker.say("choose a filename! ")
                speaker.runAndWait()
                recognizer.adjust_for_ambient_noise(mic,duration=0.2)
                audio =recognizer.listen(mic)


                filename=recognizer.recognize_google(audio)
                filename=filename.lower()


                with open(filename,'w') as f:
                    f.write(note)
                    done = True
                    speaker.say(f"successfully created note {filename}")
                    speaker.runAndWait()

        except speech_recognition.UnknownValueError:
            recognizer =speech_recognition.Recognizer()
            speaker.say(" i did not understand you : please try again !!")
            speaker.runAndWait()


def add_todo():
    global recognizer
    speaker.say("what do you want to  do")
    speaker.runAndWait()

    done =False
    while not done:
        try:

            with speech_recognition.Microphone() as mic:
                recognizer.adjust_for_ambient_noise(mic,duration=0.2)
                audio =recognizer.listen(mic)
                item =recognizer.recognize_google(audio)
                item=item.lower()

                todo_list.append(item)
                done =True

                speaker.say(f"i added {item} to the to do list ")
                speaker.runAndWait()
        except speech_recognition.UnknownValueError:
            recognizer =speech_recognition.Recognizer()
            speaker.say(" i did not understand you : please try again !!")
            speaker.runAndWait()


def show_todo():
    speaker.say(" the items on your todo are the following")
    for item in todo_list:
        speaker.say(item)
    speaker.runAndWait()


def hello():
    speaker.say("hello what can i do for you ?")
    speaker.runAndWait()

def quit():
    speaker.say("bye")
    speaker.runAndWait()
    sys.exit(0)

mappings = {
    "greeting":hello,
    "create_note":create_note,
    "add_todo":add_todo,
    "show_todo":show_todo,
    "exit":quit


 }   


assistant= GenericAssistant('intents.json',intent_methods=mappings)
assistant.train_model()

while True:
    try:

        with speech_recognition.Microphone() as mic:
            recognizer.adjust_for_ambient_noise(mic,duration=0.2)
            audio =recognizer.listen(mic)
            message =recognizer.recognize_google(audio)
            message=message.lower()
        assistant.request(message)
    
    except speech_recognition.UnknownValueError:
        recognizer =speech_recognition.Recognizer()
