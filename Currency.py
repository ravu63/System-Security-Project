import pyttsx3
import cv2
import threading

videoCaptureObject = cv2.VideoCapture(0)

import win32com.client as wincl
speak = wincl.Dispatch("SAPI.SpVoice")

def instruct():
    speak.Speak("Hello World")


def capture():
    instruct()
    while (True):
        ret, frame = videoCaptureObject.read()
        cv2.imshow('Capturing Video', frame)
        if (cv2.waitKey(1) & 0xFF == ord('q')):
            videoCaptureObject.release()
            cv2.destroyAllWindows()

capture()


