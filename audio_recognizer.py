from abc import ABC, abstractmethod
from typing import NoReturn


class ISpeechRecognizer(ABC):

    @abstractmethod
    def listening(self) -> NoReturn:
        ...
