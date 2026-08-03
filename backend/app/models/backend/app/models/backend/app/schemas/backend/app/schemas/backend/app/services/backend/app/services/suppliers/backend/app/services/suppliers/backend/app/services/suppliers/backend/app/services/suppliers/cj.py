from app.core.config import settings
from app.schemas.product import ProductCreate
from app.services.suppliers.base import SupplierConnector
from app.services.suppliers.http import SupplierHTTPClient

class CJDropshippingConnector(SupplierConnector):
    name = "cj"

    def __init__(self):
        self.client = SupplierHTTPClient("https://developers.cjdropshipping.com/api2.0/v1", settings.cj_dropshipping_api_key)

    def search_products(self, query: str) -> list[ProductCreate]:
        data = self.client.get("product/list", {"productName": query})
        items = data.get("data", {}).get("list", [])
        return [ProductCreate(external_id=str(i.get("pid")), supplier=self.name, title=i.get("productName", "Untitled"), description=i.get("description"), price=float(i.get("sellPrice", 0)), currency="USD", image_url=i.get("productImage"), product_url=i.get("productUrl"), stock=int(i.get("productStock", 0))) for i in items]
