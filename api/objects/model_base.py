"""
Abstract model base
"""
from abc import ABCMeta, abstractmethod


class AbstractModel(metaclass=ABCMeta):
    """
    Abstract model base

    Args:
        metaclass ([type], optional): Abstracth meta class. Defaults to ABCMeta.
    """

    @abstractmethod
    def __init__(self):
        pass

    @abstractmethod
    def get_table(self, meta):
        """
        Get the table of the model
        Args:
            meta ([type]): The meta object
        """
