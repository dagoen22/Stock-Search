from abc import ABC, abstractmethod

class StockData(ABC):
    '''Abstract class to define all stock datas method'''
    @property
    @abstractmethod
    def URL() -> str:
        ...

    @abstractmethod
    def get_info():
        ...

    @abstractmethod
    def to_dict():
        ...