from typing import NoReturn

import pyaudio
from speechkit import DataStreamingRecognition, Session

import config
from audio_recognizer import ISpeechRecognizer


class YandexSpeachKitRecognizer(ISpeechRecognizer):
    CHUNK_SIZE = 4000

    def __init__(self):
        oauth_session = Session.from_yandex_passport_oauth_token(config.YANDEX_OAUTH_TOKEN, config.YANDEX_FOLDER_ID)
        self.data_streaming_recognition = DataStreamingRecognition(
            oauth_session,
            language_code='ru-RU',
            audio_encoding='LINEAR16_PCM',
            sample_rate_hertz=8000,
            partial_results=False,
            single_utterance=True,
        )

    def listening(self) -> NoReturn:
        for text, final, end_of_utterance in self.data_streaming_recognition.recognize(
                self._gen_audio_capture_function, chunk_size=self.CHUNK_SIZE
        ):
            print(text[0])  # text is list of alternatives

            if final:  # Stop when final_flag set
                break

    def _gen_audio_capture_function(self, chunk_size=1024):
        p = pyaudio.PyAudio()
        stream = p.open(
            format=pyaudio.paInt16,
            channels=1,
            rate=8000,
            input=True,
            frames_per_buffer=chunk_size
        )
        try:
            while True:
                yield stream.read(chunk_size)
        finally:
            stream.stop_stream()
            stream.close()
            p.terminate()