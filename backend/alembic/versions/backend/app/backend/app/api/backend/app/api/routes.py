from fastapi import APIRouter, Depends, HTTPException, Query, status
from fastapi.security import OAuth2PasswordBearer
from sqlalchemy import select
from sqlalchemy.orm import Session
from app.core.security import create_access_token, verify_access_token
from app.db.session import get_db
from app.models.product import Product
from app.schemas.product import ProductCreate, ProductRead
from app.services.suppliers.registry import get_supplier_connector

router = APIRouter()
oauth2_scheme = OAuth2PasswordBearer(tokenUrl="/api/auth/token")

def require_user(token: str = Depends(oauth2_scheme)) -> str:
    subject = verify_access_token(token)
    if not subject:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Invalid token")
    return subject

@router.post("/auth/token")
def token(username: str = Query(...)):
    return {"access_token": create_access_token(username), "token_type": "bearer"}

@router.get("/products", response_model=list[ProductRead])
def list_products(db: Session = Depends(get_db), q: str | None = None, supplier: str | None = None, limit: int = Query(50, le=200)):
    stmt = select(Product)
    if q:
        stmt = stmt.where(Product.title.ilike(f"%{q}%"))
    if supplier:
        stmt = stmt.where(Product.supplier == supplier)
    return db.scalars(stmt.order_by(Product.updated_at.desc()).limit(limit)).all()

@router.post("/products", response_model=ProductRead, dependencies=[Depends(require_user)])
def create_product(payload: ProductCreate, db: Session = Depends(get_db)):
    product = Product(**payload.model_dump(mode="json"))
    db.add(product)
    db.commit()
    db.refresh(product)
    return product

@router.post("/suppliers/{supplier}/sync", dependencies=[Depends(require_user)])
def sync_supplier(supplier: str, db: Session = Depends(get_db), q: str = "trending"):
    connector = get_supplier_connector(supplier)
    products = connector.search_products(q)
    upserted = 0
    for item in products:
        existing = db.scalar(select(Product).where(Product.supplier == item.supplier, Product.external_id == item.external_id))
        data = item.model_dump(mode="json")
        if existing:
            for key, value in data.items():
                setattr(existing, key, value)
        else:
            db.add(Product(**data))
        upserted += 1
    db.commit()
    return {"supplier": supplier, "upserted": upserted}
