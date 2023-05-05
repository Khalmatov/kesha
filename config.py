import pathlib

BASE_DIR = pathlib.Path(__file__).parent.absolute()

with open(pathlib.Path(BASE_DIR, '.env')) as file:
    ENV = {line.split('=')[0]: line.split('=')[1] for line in file.read().strip().split()}

# Tinkoff
TINKOFF_API_KEY = ENV.get('TINKOFF_API_KEY')
TINKOFF_SECRET_KEY = ENV.get('TINKOFF_SECRET_KEY')

# VK
VK_SERVICE_TOKEN = ENV.get('VK_SERVICE_TOKEN')
VK_CHUNK_PATH = pathlib.Path(BASE_DIR, 'assets', 'chunk.wav')

# Yandex
YANDEX_FOLDER_ID = ENV.get('YANDEX_FOLDER_ID')
YANDEX_OAUTH_TOKEN = ENV.get('YANDEX_OAUTH_TOKEN')
