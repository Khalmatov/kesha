import os
import threading
import time
import tkinter as tk
import wave

import pyaudio

from adapters.tinkoff.voicekit import VoiceKitRecognizer
from adapters.vk.cloud import VKCloudAudioRecognizer
# from adapters.yandex.speach_kit import YandexSpeachKitRecognizer


class SpeechRecorderApp:
    FORMAT = pyaudio.paInt16
    CHANNELS = 1
    RATE = 44100
    CHUNK = 2048

    def __init__(self):
        self.window = tk.Tk()
        self.window.title("Speech Recorder")
        self.window.geometry('1135x600')

        self.recording = False

        # Создание кнопки "Play"
        self.play_button = tk.Button(self.window, text="Play", command=self.toggle_recording)
        self.play_button.grid(row=0, column=1, pady=5)

        self.label = tk.Label(text='')
        self.label.grid(row=1, column=1)

        self.label1 = tk.Label(text='Яндекс')
        self.label1.grid(row=2, column=0)
        self.yandex_text_output = tk.Text(self.window, height=30, width=45)
        self.yandex_text_output.grid(row=3, column=0)

        self.label2 = tk.Label(text='Тинькофф')
        self.label2.grid(row=2, column=1)
        self.tinkoff_text_output = tk.Text(self.window, height=30, width=45)
        self.tinkoff_text_output.grid(row=3, column=1, padx=15)

        self.label3 = tk.Label(text='ВК')
        self.label3.grid(row=2, column=2)
        self.vk_text_output = tk.Text(self.window, height=30, width=45)
        self.vk_text_output.grid(row=3, column=2)

    def toggle_recording(self):
        if not self.recording:
            self.recording = True
            self.play_button.config(text="Stop")
            threading.Thread(target=self.start_recording).start()
        else:
            self.recording = False
            self.play_button.config(text="Play")
            self.stop_recording()

    def record(self):
        audio = pyaudio.PyAudio()
        stream = audio.open(
            format=self.FORMAT,
            channels=self.CHANNELS,
            rate=self.RATE,
            input=True,
            frames_per_buffer=self.CHUNK,
            # input_device_index=9
        )

        frames = []
        start = time.time()

        while self.recording:
            data = stream.read(self.CHUNK, exception_on_overflow=False)
            frames.append(data)

            passed = time.time() - start
            secs = passed % 60
            mins = passed // 60
            hours = mins // 60
            self.label.config(text=f"{int(hours):02d}:{int(mins):02d}:{int(secs):02d}")

        stream.stop_stream()
        stream.close()
        audio.terminate()

        exists = True
        i = 1

        while exists:
            if os.path.exists(f'recording{i}.wav'):
                i += 1
            else:
                exists = False

        sound_file = wave.open(f'recording.wav', 'wb')
        sound_file.setnchannels(self.CHANNELS)
        sound_file.setsampwidth(audio.get_sample_size(self.FORMAT))
        sound_file.setframerate(self.RATE)
        sound_file.writeframes(b''.join(frames))
        sound_file.close()

    def start_recording(self):
        # self.record()
        self.recognize()

    def recognize(self):
        self.label.config(text='Идет распознавание текста...')

        with open('recording.wav', 'rb') as f:
            audio = f.read()
            threads = []

            for func in (self.recognize_by_yandex, self.recognize_by_tinkoff, self.recognize_by_vk):
                thread = threading.Thread(target=func, args=[audio])
                thread.start()
                threads.append(thread)

            for thread in threads:
                thread.join()

        self.label.config(text='')

    def recognize_by_yandex(self, audio: bytes):
        # recognized_text_of_yandex = YandexSpeachKitRecognizer().recognize(audio)
        self.yandex_text_output.delete(1.0, tk.END)
        self.yandex_text_output.insert(tk.END, 'recognized_text_of_yandex')

    def recognize_by_tinkoff(self, audio: bytes):
        recognized_text_of_tinkoff = VoiceKitRecognizer().recognize(audio)  # Распознаем записанный звук в текст
        self.tinkoff_text_output.delete(1.0, tk.END)
        self.tinkoff_text_output.insert(tk.END, recognized_text_of_tinkoff)

    def recognize_by_vk(self, audio: bytes):
        recognized_text_of_vk = VKCloudAudioRecognizer().recognize(audio)
        recognized_text_of_vk = recognized_text_of_vk['result']['texts'][0]['punctuated_text']
        self.vk_text_output.delete(1.0, tk.END)
        self.vk_text_output.insert(tk.END, recognized_text_of_vk)

    def stop_recording(self):
        pass

    def run(self):
        self.window.mainloop()


if __name__ == "__main__":
    app = SpeechRecorderApp()
    app.run()
