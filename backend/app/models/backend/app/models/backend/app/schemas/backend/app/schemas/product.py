from pydantic import BaseModel, ConfigDict, HttpUrl

class ProductBase(BaseModel):
    external_id: str
    supplier: str
    title: str
    description: str | None = None
    price: float
    currency: str = "USD"
    image_url: HttpUrl | None = None
    product_url: HttpUrl | None = None
    stock: int = 0

class ProductCreate(ProductBase):
    pass

class ProductRead(ProductBase):
    model_config = ConfigDict(from_attributes=True)
    id: int
