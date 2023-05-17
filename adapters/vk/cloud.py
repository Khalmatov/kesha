import pyaudio
import requests

import config
from audio_recognizer import ISpeechRecognizer


class VKCloudAudioRecognizer(ISpeechRecognizer):
    pyaudio_lib = pyaudio.PyAudio()
    FORMAT = pyaudio.paInt16  # шестнадцати-битный формат задает значение амплитуды
    CHANNELS = 1  # канал записи звука
    SAMPLE_RATE = 16000  # частота

    def recognize(self, audio: bytes) -> dict:
        result = self._asr(audio)
        return result

    def _asr(
            self,
            audio: bytes,
    ) -> str:
        response = requests.post(
            'https://voice.mcs.mail.ru/asr',
            headers={
                'Content-Type': 'audio/wav',
                'Authorization': f'Bearer {config.VK_SERVICE_TOKEN}'
            },
            data=audio
        )
        print(f'{response.json()=}')
        response = response.json()
        return response
