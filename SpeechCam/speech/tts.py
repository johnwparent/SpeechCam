import pyttsx3 as ptts 


class TTS:
    def __init__(self):
        self.engine = self._create_tts()

    def _create_tts(self):
        return ptts.init()

    def set_rate(self, rate):
        self.engine.setProperty('rate', rate)

    def get_rate(self):
        return self.engine.getProperty('rate')

    def get_volume(self):
        return self.engine.getProperty('volume')

    def set_volume(self, level):
        self.engine.setProperty('volume', level)

    def set_voice(self, gender):
        voices = self.engine.getProperty('voices')
        self.engine.setProperty('voice',voices[gender].id)

    def speak(self, speech):
        self.engine.say(speech)
        self.engine.runAndWait()
        self.engine.stop()