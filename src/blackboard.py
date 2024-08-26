from typing import Type
from .interfaces import Observer

class BlackBoard:
    def __init__(self):
        self.observers = []

    def subscribe(self, observer: Type[Observer]):
        self.observers.append(observer)

    def unsubscribe(self, observer: Type[Observer]):
        self.observers.remove(observer)

    def notify(self, observer: Type[Observer], memory):
        observer.update(memory)

    def notifyAll(self, memory):
        for observer in self.observers:
            observer.update(memory)
        #observers =  []


