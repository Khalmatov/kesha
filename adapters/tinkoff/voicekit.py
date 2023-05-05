from typing import NoReturn

import grpc
import pyaudio

from adapters.tinkoff.auth import authorization_metadata
from adapters.tinkoff.stt.v1 import stt_pb2_grpc, stt_pb2
from audio_recognizer import ISpeechRecognizer

import config


class VoiceKitRecognizer(ISpeechRecognizer):

    def listening(self) -> NoReturn:
        stub = stt_pb2_grpc.SpeechToTextStub(grpc.secure_channel("api.tinkoff.ai:443", grpc.ssl_channel_credentials()))
        metadata = authorization_metadata(config.TINKOFF_API_KEY, config.TINKOFF_SECRET_KEY, "tinkoff.cloud.stt")
        responses = stub.StreamingRecognize(self._generate_requests(), metadata=metadata)
        self._print_streaming_recognition_responses(responses)

    def _generate_requests(self):
        try:
            sample_rate_hertz, num_channels = 16000, 1
            pyaudio_lib = pyaudio.PyAudio()
            f = pyaudio_lib.open(input=True, channels=num_channels, format=pyaudio.paInt16, rate=sample_rate_hertz)
            yield self._build_first_request(sample_rate_hertz, num_channels)
            for data in iter(lambda: f.read(800), b''):  # Send 50ms at a time
                request = stt_pb2.StreamingRecognizeRequest()
                request.audio_content = data
                yield request
        except Exception as e:
            print("Got exception in generate_requests", e)
            raise

    @staticmethod
    def _build_first_request(sample_rate_hertz, num_channels):
        request = stt_pb2.StreamingRecognizeRequest()
        request.streaming_config.config.encoding = stt_pb2.AudioEncoding.LINEAR16
        request.streaming_config.config.sample_rate_hertz = sample_rate_hertz
        request.streaming_config.config.num_channels = num_channels
        return request

    @staticmethod
    def _print_streaming_recognition_responses(responses):
        for response in responses:
            for result in response.results:
                print("Channel", result.recognition_result.channel)
                print("Phrase start:", result.recognition_result.start_time.ToTimedelta())
                print("Phrase end:  ", result.recognition_result.end_time.ToTimedelta())
                for alternative in result.recognition_result.alternatives:
                    print('"' + alternative.transcript + '"')
                print("------------------")
