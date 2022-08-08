import pyttsx3
import cv2
import threading

videoCaptureObject = cv2.VideoCapture(0)

engine = pyttsx3.init()
voices = engine.getProperty('voices')
engine.setProperty('voice', voices[1].id)
rate = engine.getProperty('rate')
engine.setProperty('rate', 120)


def instruct():
    engine.say("Hi! I am Ravu")


def capture():
    instruct()
    while (True):
        ret, frame = videoCaptureObject.read()
        cv2.imshow('Capturing Video', frame)
        if (cv2.waitKey(1) & 0xFF == ord('q')):
            videoCaptureObject.release()
            cv2.destroyAllWindows()

capture()


