from abc import ABC, abstractmethod

class Observer(ABC):
    @abstractmethod
    def update(self, *args, **kwargs):
        pass
    @abstractmethod
    def verify(self, *args, **kwargs) -> bool:
        pass