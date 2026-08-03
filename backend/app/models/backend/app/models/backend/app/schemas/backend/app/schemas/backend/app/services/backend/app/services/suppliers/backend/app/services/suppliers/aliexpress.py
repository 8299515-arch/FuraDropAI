from app.core.config import settings
from app.schemas.product import ProductCreate
from app.services.suppliers.base import SupplierConnector
from app.services.suppliers.http import SupplierHTTPClient

class AliExpressConnector(SupplierConnector):
    name = "aliexpress"

    def __init__(self):
        self.client = SupplierHTTPClient("https://api-sg.aliexpress.com", settings.aliexpress_api_key)

    def search_products(self, query: str) -> list[ProductCreate]:
        data = self.client.get("sync", {"method": "aliexpress.ds.text.search", "keywords": query})
        items = data.get("products") or data.get("result", {}).get("products", [])
        return [ProductCreate(external_id=str(i.get("product_id")), supplier=self.name, title=i.get("title", "Untitled"), description=i.get("description"), price=float(i.get("price", 0)), currency=i.get("currency", "USD"), image_url=i.get("image_url"), product_url=i.get("product_url"), stock=int(i.get("stock", 0))) for i in items]
