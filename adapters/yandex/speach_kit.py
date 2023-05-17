from speechkit import Session, ShortAudioRecognition

import config
from audio_recognizer import ISpeechRecognizer


class YandexSpeachKitRecognizer(ISpeechRecognizer):
    CHUNK_SIZE = 4000

    def recognize(self, audio: bytes) -> str:
        oauth_session = Session.from_yandex_passport_oauth_token(config.YANDEX_OAUTH_TOKEN, config.YANDEX_FOLDER_ID)
        recognizeShortAudio = ShortAudioRecognition(oauth_session)
        text = recognizeShortAudio.recognize(
            audio, format='lpcm', sampleRateHertz='48000')
        return text
