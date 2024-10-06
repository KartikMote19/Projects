import pyttsx3
import datetime
import speech_recognition as sr
import webbrowser
import wikipedia
import pywhatkit
import pyautogui
from pygame import mixer
from plyer import notification
from PIL import Image, ImageTk
import tkinter as tk
from tkinter import ttk
import threading
from itertools import count
import os
import time

# Initialize the speech engine
engine = pyttsx3.init('sapi5')
voices = engine.getProperty('voices')
engine.setProperty('voice', voices[0].id)

# Flag to control the process_commands loop
is_listening = False

def start_listening():
    global is_listening
    is_listening = True

    def speak(audio):
        engine.say(audio)
        response_text.set(audio)
        engine.runAndWait()

    def wishMe():
        hour = int(datetime.datetime.now().hour)

        if 0 < hour < 12:
            speak("Good Morning Sir")
        elif 12 <= hour <= 18:
            speak("Good Afternoon Sir")
        else:
            speak("Good Evening Sir")

        speak("How may I help you?")

    def takeCommand():
        r = sr.Recognizer()
        m = sr.Microphone()

        try:
            with m as source:
                print("Listening... ")
                r.pause_threshold = 1
                audio = r.listen(source)
                print("Recognizing...")
                query = r.recognize_google(audio, language='en-in')
                print(f'User said: {query}')

        except sr.RequestError:
            print("API unavailable or unresponsive")
            return "None"
        
        except sr.UnknownValueError:
            print("Unable to recognize speech")
            return "None"

        return query

    def searchGoogle(query):
        if "google" in query:
            query = query.replace('jarvis', "").replace('search', "").replace('google', "").replace('on', "").replace('open', "")
            speak("This is what I found on google...")

            try:
                pywhatkit.search(query)
                result = wikipedia.summary(query, sentences=2)
                speak(result)

            except:
                speak("No output...")

    def searchYoutube(query):
        if "youtube" in query:
            speak("This is what I found online...")
            query = query.replace('jarvis', "").replace('youtube search', "").replace('youtube', "").replace('search', "").replace('on', "").replace('open', "")
            web = "https://www.youtube.com/results?search_query=" + query
            webbrowser.open(web)
            pywhatkit.playonyt(query)

    def searchWikipedia(query):
        if "wikipedia" in query:
            speak("Here's what I found from wikipedia...")
            query = query.replace('jarvis', "").replace('search', "").replace('wikipedia', "")
            results = wikipedia.summary(query, sentences=2)
            speak("According to wikipedia...")
            print(results)
            speak(results)

    def process_commands():
        global is_listening
        speak('Hello I am Jarvis')
        wishMe()
        while is_listening:
            command = takeCommand()
            command1 = command.lower()

            if 'the time' in command1:
                strfTime = datetime.datetime.now().strftime("%H:%M:%S")
                speak(f'Sir the time is {strfTime}')

            elif 'google' in command1:
                searchGoogle(command1)

            elif 'youtube' in command1:
                searchYoutube(command1)

            elif 'wikipedia' in command1:
                searchWikipedia(command1)

            elif 'open' in command1:
                command1 = command1.replace('open', "")
                command1 = command1.replace('jarvis', "")
                pyautogui.press('super')
                pyautogui.typewrite(command1)
                pyautogui.sleep(2)
                pyautogui.press('enter')

            elif 'alarm' in command1:
                speak("Enter the time: ")
                time_input = input("Enter time in HH:MM:SS format")

                while True:
                    Time_Ac = datetime.datetime.now()
                    now = Time_Ac.strftime("%H:%M:%S")

                    if now == time_input:
                        speak("Time to wake up sir!!")
                        mixer.init()
                        mixer.music.load("C:/Users/nisch/Downloads/Alarm Clock Ringing   Free Sound Effect Ringtones.mp3")
                        mixer.music.play()

                    elif now > time_input:
                        break

            elif 'shutdown the system' in command1:
                speak("Shutting down...")
                os.system("shutdown /s /t 5")

            elif 'restart the system' in command1:
                speak("Restarting the system...")
                os.system("shutdown /r /t 5")

            elif "search instagram profile" in command1:
                speak("Sir, please enter username correctly")
                name = input("Enter the name here: ")
                webbrowser.open(f"https://www.instagram.com/{name}")
                time.sleep(5)

            elif 'switch the window' in command1:
                pyautogui.keyDown('alt')
                pyautogui.press('tab')
                time.sleep(1)
                pyautogui.keyUp('alt')

            elif 'shutdown' in command1:
                speak("Going offline sir...")
                break

    # Run command processing in a separate thread
    command_thread = threading.Thread(target=process_commands)
    command_thread.start()

def exit_application():
    global is_listening
    def speak(audio):
        engine.say(audio)
        response_text.set(audio)
        engine.runAndWait()

    # Stop the listening loop
    is_listening = False

    # Speak the exit message before closing the application
    speak("Exiting the application. Goodbye!")
    
    # Close the application
    root.destroy()

# Class to handle animated GIF
class AnimatedGIF(tk.Label):
    def __init__(self, root, path, delay=100):
        tk.Label.__init__(self, root)
        self.root = root
        self.path = path
        self.delay = delay
        self.frames = []
        self.load_gif()

    def load_gif(self):
        img = Image.open(self.path)
        try:
            for i in count(1):
                self.frames.append(ImageTk.PhotoImage(img.copy()))
                img.seek(i)
        except EOFError:
            pass

        self.frame_index = 0
        self.update_gif()

    def update_gif(self):
        frame = self.frames[self.frame_index]
        self.config(image=frame)
        self.frame_index = (self.frame_index + 1) % len(self.frames)
        self.root.after(self.delay, self.update_gif)

# Set up the main GUI window
root = tk.Tk()
root.title("JARVIS")
root.configure(bg="black")
root.geometry("1260x700")

# Animated GIF setup
image_path = "JarvisGUI-ezgif.com-resize.gif"  # Path to your GIF file
animated_label = AnimatedGIF(root, image_path, delay=100)
animated_label.place(relx=0.5, rely=0.5, anchor="center")

# Display response text in the GUI
response_text = tk.StringVar()
response_label = tk.Label(root, textvariable=response_text, fg="white", bg="black", font=("Arial", 18))
response_label.place(relx=0.5, rely=0.9, anchor='center')

# Buttons to start listening and exit the program
start_button = ttk.Button(root, text="Start Listening", command=start_listening)
start_button.place(relx=0.3, rely=0.8, anchor="center")

exit_button = ttk.Button(root, text="Exit", command=exit_application)
exit_button.place(relx=0.7, rely=0.8, anchor="center")

root.mainloop()
