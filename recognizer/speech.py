import logging

import speech_recognition
import pyttsx

logger = logging.getLogger(__name__)
speech_engine = pyttsx.init()
speech_engine.setProperty('rate', 150)
recognizer = speech_recognition.Recognizer()


def listen(wav_file):
    with speech_recognition.WavFile(wav_file) as source:
        audio = recognizer.record(source)
        text = ""

        try:
            text = recognizer.recognize_sphinx(audio)
            logger.info("Sphinx thinks you said " + text)
        except speech_recognition.UnknownValueError:
            logger.warn("Sphinx could not understand audio")
        except speech_recognition.RequestError as e:
            logger.exception("Sphinx error; {0}".format(e))
        return text
