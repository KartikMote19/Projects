#import instaloader
import pyautogui
import pyttsx3
import speech_recognition as sr
import datetime
import os
#import cv2
import random
import wikipedia
import time
import webbrowser
import smtplib
#import pyjokes
import requests
import sys
import tkinter as tk
from tkinter import ttk
import pyttsx3
from PIL import Image, ImageTk


def start_listening():
    engine = pyttsx3.init('sapi5')
    voices = engine.getProperty('voices')
    print(voices[0].id)
    engine.setProperty('voices', voices[0].id)

    # text to speech
    def speak(text):
        engine.say(text)
        response_text.set(text)
        engine.runAndWait()

    # to convert voice into text

    def wish():
        hour = int(datetime.datetime.now().hour)
        tt = time.strftime('%I:%M %p')
        speak("Hello Sir")
        if 0 <= hour < 12:
            speak(f"Good Morning,\n Its {tt}")
        elif 12 <= hour < 17:
            speak(f"Good Afternoon,\n Its {tt}")
        else:
            speak(f"Good Evening,\n Its {tt}")
        speak("I am Alex.\n How can I help you?")

    def takecommand():
        r = sr.Recognizer()
        with sr.Microphone() as source:
            speak("Listening...")
            r.pause_threshold = 1
            audio = r.listen(source, timeout=1.5, phrase_time_limit=5)

        try:
            speak("Recognizing...")
            query = r.recognize_google(audio, language='en-in')
            speak(f"user said:{query}")

        except Exception as e:
            speak("Can you repeat please...")
            return "none"
        return query

    def sendEmail(to, content):
        server = smtplib.SMTP('smtp.gmail.com', 587)
        server.ehlo()
        server.starttls()
        server.login('our email id', 'email id password')
        server.sendmail('our Email Id', to, content)

    if __name__ == '__main__':
        wish()
        while True:

            query = takecommand().lower()

            # logic for tasks

            if 'open chrome' in query:
                cpath = "C:\\Program Files\\Google\\Chrome\\Application\\chrome.exe"
                os.startfile(cpath)
                speak("opening chrome now")

            elif "close chrome" in query:
                speak("Okay Sir, closing chrome now")
                os.system("taskkill/f /im chrome.exe")

            elif 'open vs code' in query:
                vpath = "C:\\Users\\Admin\\AppData\\Local\\Programs\\Microsoft VS Code\\Code.exe"
                os.startfile(vpath)
                speak("opening visual studio code")

            elif 'open zoom' in query:
                zpath = 'C:\\Users\\Admin\\AppData\\Roaming\\Zoom\\bin\\Zoom.exe'
                os.startfile(zpath)
                speak("opening zoom now")

            elif 'open command prompt' in query:
                os.system("start cmd")

            elif 'open camera' in query:
                cap = cv2.VideoCapture(0)
                while True:
                    ret, img = cap.read()
                    cv2.imshow('webcam', img)
                    k = cv2.waitKey(50)
                    if k == 27:
                        break;
                cap.release()
                cv2.destroyAllWindows()

            elif "play the music" in query or 'play the song' in query:
                music_dir = 'G:\\pythonProject\\Music'
                songs = os.listdir(music_dir)
                rd = random.choice(songs)  # for random music from folder we use random module
                os.startfile(os.path.join(music_dir, rd))
                # for selected song
                # os.startfile(os.path.join(music_dir, songs[16]))

            elif "wikipedia" in query:
                speak("searching wikipedia...")
                query = query.replace("wikipedia", "")
                result = wikipedia.summary(query, sentences=2)
                speak(result)

            elif "open youtube" in query:
                webbrowser.open("www.youtube.com")

            elif "open instagram" in query:
                webbrowser.open("https://www.instagram.com/")

            elif "open whatsapp" in query:
                webbrowser.open("https://web.whatsapp.com/")

            elif "search on google" in query:
                speak("what should I search on google")
                ans = takecommand().lower()  # to search on google
                webbrowser.open(f"{ans}")

            elif "email to kartik" in query:
                try:
                    speak("what should I say?")
                    content = takecommand().lower()
                    to = "mk19171408@gmail.com"
                    sendEmail(to, content)
                    speak("Email has been sent to Kartik")

                except Exception as e:
                    print(e)
                    speak("Sorry Sir.I'm unable to sent this mail.")

            elif "tell me a joke" in query:
                joke = pyjokes.get_joke()
                speak(joke)

            elif 'switch the window' in query:
                pyautogui.keyDown('alt')
                pyautogui.press('tab')
                time.sleep(1)
                pyautogui.keyUp('alt')

            elif "where i am" in query or "where we are" in query:
                speak("wait sir, let me check")
                try:
                    ipAdd = requests.get('https://api.ipify.org').text
                    print(ipAdd)
                    url = 'https://get.geojs.io/v1/ip/geo' + ipAdd + '.json'
                    geo_requests = requests.get(url)
                    geo_data = geo_requests.json()
                    # print(geo_data)
                    city = geo_data['city']
                    state = geo_data['state']
                    country = geo_data['country']

                    speak(f"Sir,I think we are in{city} city of {state} state in {country}")
                except Exception as e:
                    speak("Sorry Sir,Due to network issue I'm unable to find our location")
                    pass

            elif 'exit' in query:
                speak("Thank you for using me.")
                sys.exit()

            elif "search instagram profile" in query:
                speak("Sir please enter username correctly")
                name = input("Enter the name here:")
                webbrowser.open(f"https://www.instagram.com/{name}")
                time.sleep(5)
                speak("Sir would you like to download profile picture of this account")
                condition = takecommand().lower()
                if 'yes' in condition:
                    mod = instaloader.Instaloader()
                    mod.download_profile(name, profile_pic_only=True)
                    speak("Profile picture is saved in main folder")

                else:
                    speak("Ok sir")

            elif 'shut down the system' in query:
                speak("Shutting down...")
                os.system("shutdown /s /t 5")

            elif 'restart the system' in query:
                speak("Restarting the system...")
                os.system("shutdown /r /t 5")

def exit_app():
    root.destroy()

root = tk.Tk()
root.title("Alex")
root.configure(bg='black')
root.geometry("800x600")

image_path ="G:\pythonProject\GUI\Alex.gif"
img = tk.PhotoImage(file=image_path)

image_label = tk.Label(root, image=img, bg="black")
image_label.image = img
image_label.place(relx=0.5, rely=0.3, anchor='center')

response_text = tk.StringVar()
response_label = tk.Label(root, textvariable=response_text, fg='White', bg='blue', font=('Arial', 14))
response_label.place(relx=0.5,rely=0.7, anchor='center')

start_button = tk.Button(root, text="RUN",fg="White", bg='green', width=4, height=1, font=('Arial',18), command=start_listening)
start_button.place(relx=0.15, rely=0.825, anchor="center")

exit_button = tk.Button(root, text="EXIT",fg='white', bg='red', width=4, height=1, font=('Arial',18), command=exit_app)
exit_button.place(relx=0.845, rely=0.825, anchor="center")

root.mainloop()
