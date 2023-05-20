# Учебная программа для распознавания аудио

Программа записывает аудио с микрофона и распознает текст с помощью API различных российских сервисов

## Установка и запуск

Для запуска приложения потребуются:

1. виртуальное окружение с Python версии 3.8 или выше
2. установленные внешние зависимости
3. заполненный конфигурационный файл `.env`

### С помощью Poetry

```bash
poetry use python3.11 # создаем виртуальное окружение
poetry install # устанавливаем внешние зависимости в окружение
poetry shell # активируем окружение
```

### С помощью venv и pip

```bash
python3.11 -m venv env # создаем виртуальное окружение
source env/bin/activate # активируем окружение (или .\bin\Scripts\activate на Windows)
pip install requirements.txt # устанавливаем внешние зависимости в окружение
```

### Конфигурационный файл

Конфигурационный файл `.env` имеет следующую структуру:

| Переменная         | Значение                                                                                                      |
|--------------------|---------------------------------------------------------------------------------------------------------------|
| TINKOFF_API_KEY    | API-ключ [Tinkoff VoiceKit](https://www.tinkoff.ru/software/voicekit/)                                        |
| TINKOFF_SECRET_KEY | Секретный ключ [Tinkoff VoiceKit](https://www.tinkoff.ru/software/voicekit/)                                  |
| VK_SERVICE_TOKEN   | [Сервисный токен](https://mcs.mail.ru/docs/ml/cloud-voice/get-voice-token#servisnyy-token) VK Cloud           |
| YANDEX_ACCOUNT_ID  | [Идентификатор сервисного аккаунта](https://cloud.yandex.ru/docs/iam/operations/sa/get-id) Yandex Cloud       |
| YANDEX_FOLDER_ID   | [Идентификатор каталога](https://cloud.yandex.ru/docs/resource-manager/operations/folder/get-id) Yandex Cloud |
| YANDEX_OAUTH_TOKEN | [OAuth-токен](https://cloud.yandex.ru/docs/iam/concepts/authorization/oauth-token) Yandex Cloud               |

### Запуск приложения

```bash
python main.py
```

