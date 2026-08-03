from app.core.config import settings
from app.schemas.product import ProductCreate
from app.services.suppliers.base import SupplierConnector
from app.services.suppliers.http import SupplierHTTPClient

class SpocketConnector(SupplierConnector):
    name = "spocket"

    def __init__(self):
        self.client = SupplierHTTPClient("https://api.spocket.co", settings.spocket_api_key)

    def search_products(self, query: str) -> list[ProductCreate]:
        data = self.client.get("v1/products", {"q": query})
        items = data.get("products", [])
        return [ProductCreate(external_id=str(i.get("id")), supplier=self.name, title=i.get("name", "Untitled"), description=i.get("description"), price=float(i.get("price", 0)), currency=i.get("currency", "USD"), image_url=i.get("image"), product_url=i.get("url"), stock=int(i.get("inventory", 0))) for i in items]
