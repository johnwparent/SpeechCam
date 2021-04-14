import sys, os
import argparse
import speech.stt as stt
import speech.tts as tts

def detect_speech():
    language_processor = stt.get_interpreter()
    default_mic = stt.get_mic()
    with default_mic as audio_src:
        language_processor.adjust_for_ambient_noise(audio_src, duration=0.3)
        audio_capture = language_processor.listen(audio_src)

    sphinx = stt.get_sphinx_interp(language_processor)
    try:
        text_from_speech = sphinx(audio_capture)
    except stt.RequestError:
        raise RuntimeError("Unable to access speech recognition runtime, please install Sphinx")
    except stt.UnknownValueError:
        print("Sorry, we're having trouble understanding you, please try to say that again, this time waiting for just a moment before speaking")



def speak(speaker,direction):
    def left():
        speaker.speak("Move left")
    def right():
        speaker.speak("Move right")
    def up():
        speaker.speak("Move up")
    def down():
        speaker.speak("Move down")
    return return locals()[direction]


def main(argv=None):


if __name__ == '__main__':
    main()