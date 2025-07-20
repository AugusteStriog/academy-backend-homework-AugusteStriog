# Defines the abstract base class for discount rules.

from abc import ABC, abstractmethod

class DiscountRules(ABC):
    @abstractmethod
    def apply(self, transaction, discount_manager):
        pass
