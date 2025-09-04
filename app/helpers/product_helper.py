from ..schemas import product_schema


def update_product_fields(db_product, product: product_schema.ProductCreate):
    db_product.name = product.name
    db_product.description = product.description
    db_product.price = product.price
    db_product.quantity = product.quantity
    return db_product
