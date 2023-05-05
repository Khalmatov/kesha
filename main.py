from adapters.tinkoff.voicekit import VoiceKitRecognizer
from adapters.vk.cloud import VKCloudAudioRecognizer
from adapters.yandex.speach_kit import YandexSpeachKitRecognizer


def main():
    YandexSpeachKitRecognizer().listening()


if __name__ == '__main__':
    main()
