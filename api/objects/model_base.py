from abc import ABCMeta, abstractmethod

class AbstractModel(metaclass=ABCMeta):
    @abstractmethod
    def __init__(self):
        pass
    
    @abstractmethod
    def get_table(self, meta):
        pass

