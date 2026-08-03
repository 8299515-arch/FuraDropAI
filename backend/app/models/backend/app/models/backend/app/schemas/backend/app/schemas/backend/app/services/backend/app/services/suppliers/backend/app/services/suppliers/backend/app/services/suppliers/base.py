from abc import ABC, abstractmethod
from app.schemas.product import ProductCreate

class SupplierConnector(ABC):
    name: str

    @abstractmethod
    def search_products(self, query: str) -> list[ProductCreate]:
        """Fetch normalized products from a real supplier API."""
