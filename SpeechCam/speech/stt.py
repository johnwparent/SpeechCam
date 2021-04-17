# Defining python TTS interface for speech cam
import speech_recognition as sr

def get_interpreter():
    return sr.Recognizer()

def get_sphinx_interp(recognizer):
    return recognizer.recognize_sphinx

def get_google_interp(recognizer):
    return recognizer.recognize_google

def get_mic(mic_idx=None):
    if not mic_idx:
        return sr.Microphone()
    else:
        return sr.Microphone(device_index=mic_idx)

def get_mic_list():
    return sr.Microphone.list_microphone_names()

RequestError = sr.RequestError
UnknownValueError = sr.UnknownValueError
