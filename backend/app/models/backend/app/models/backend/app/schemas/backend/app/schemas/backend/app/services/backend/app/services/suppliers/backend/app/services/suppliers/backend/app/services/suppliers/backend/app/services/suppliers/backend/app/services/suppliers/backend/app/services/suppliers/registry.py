from fastapi import HTTPException
from app.services.suppliers.aliexpress import AliExpressConnector
from app.services.suppliers.cj import CJDropshippingConnector
from app.services.suppliers.spocket import SpocketConnector

CONNECTORS = {"aliexpress": AliExpressConnector, "cj": CJDropshippingConnector, "spocket": SpocketConnector}

def get_supplier_connector(name: str):
    connector = CONNECTORS.get(name.lower())
    if not connector:
        raise HTTPException(status_code=404, detail=f"Unknown supplier '{name}'")
    return connector()
