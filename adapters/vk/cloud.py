import wave
from typing import NoReturn

import pyaudio
import requests

from audio_recognizer import ISpeechRecognizer
from .dto import CreateTaskResponse, AddChunkResponse, ResultResponse

import config


class VKCloudAudioRecognizer(ISpeechRecognizer):
    pyaudio_lib = pyaudio.PyAudio()
    FORMAT = pyaudio.paInt16  # шестнадцати-битный формат задает значение амплитуды
    CHANNELS = 1  # канал записи звука
    SAMPLE_RATE = 16000  # частота

    def listening(self) -> NoReturn:
        task_response = self._create_task()
        self._generate_requests(task_response)
        result = self._get_result(task_response)
        print(f'{result=}')

    def _generate_requests(self, task_response: CreateTaskResponse):
        stream = self.pyaudio_lib.open(
            input=True,
            format=self.FORMAT,
            channels=self.CHANNELS,
            rate=self.SAMPLE_RATE
        )
        for index, frame in enumerate(iter(lambda: stream.read(1000), b'')):  # ~80ms
            chunk_wave = self._serialize_frame_to_wave(frame)
            is_last = index > 20
            self._add_chunk(
                task_response=task_response,
                chunk_num=index,
                data=chunk_wave,
                last=is_last
            )
            if is_last:
                break

    def _create_task(self) -> CreateTaskResponse:
        response = requests.post(
            'https://voice.mcs.mail.ru/asr_stream/create_task',
            headers={
                'Authorization': f'Bearer {config.VK_SERVICE_TOKEN}'
            }
        )
        response = CreateTaskResponse(**response.json())
        return response

    def _add_chunk(
            self,
            task_response: CreateTaskResponse,
            chunk_num: int,
            data: bytes,
            last: bool = False
    ) -> AddChunkResponse:
        response = requests.post(
            'https://voice.mcs.mail.ru/asr_stream/add_chunk',
            headers={
                'Content-Type': 'audio/wav',
                'Authorization': f'Bearer {task_response.result.task_token}'
            },
            params={
                'task_id': task_response.result.task_id,
                'chunk_num': chunk_num,
                'last': int(last)
            },
            data=data
        )
        print(f'{response.json()=}')
        response = AddChunkResponse(**response.json())
        return response

    def _get_result(self, task_response: CreateTaskResponse) -> ResultResponse:
        response = requests.get(
            'https://voice.mcs.mail.ru/asr_stream/get_result',
            headers={
                'Authorization': f'Bearer {task_response.result.task_token}'
            },
            params={
                'task_id': task_response.result.task_id
            }
        )
        response = ResultResponse(**response.json())
        return response

    def _serialize_frame_to_wave(self, frame: bytes) -> bytes:
        wf = wave.open(config.VK_CHUNK_PATH, "wb")
        wf.setnchannels(self.CHANNELS)
        wf.setsampwidth(self.pyaudio_lib.get_sample_size(self.FORMAT))
        wf.setframerate(self.SAMPLE_RATE)
        wf.writeframes(frame)
        wf.close()
        with open(config.VK_CHUNK_PATH, 'rb') as f:
            return f.read()
