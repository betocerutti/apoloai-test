from fastapi import FastAPI, HTTPException, Depends
from sqlalchemy.orm import Session
from typing import List
from datetime import datetime
import requests

from app import models, schemas

PRODUCTS_SERVICE_URL = "http://172.22.0.2:8000/api"


def validate_product_and_update_stock(product_id: int, quantity: int) -> float:
    """
    Validate a product and update its stock in the products service.
    Returns the price of the product if successful.
    """
    if quantity < 1:
        raise HTTPException(status_code=400, detail="Product quantity must be at least 1")

    # Check if product exists
    response = requests.get(f"{PRODUCTS_SERVICE_URL}/products/{product_id}")
    if response.status_code == 404:
        raise HTTPException(status_code=404, detail=f"Product with id {product_id} not found")

    product_data = response.json()
    if product_data["stock"] < quantity:
        raise HTTPException(
            status_code=400,
            detail=f"Insufficient stock for product with id {product_id}",
        )

    # Update product stock
    new_stock = product_data["stock"] - quantity
    update_stock_response = requests.patch(
        f"{PRODUCTS_SERVICE_URL}/products/{product_id}/update-stock/",
        json={"stock": new_stock},
    )

    if update_stock_response.status_code != 200:
        raise HTTPException(
            status_code=update_stock_response.status_code,
            detail=f"Failed to update stock for product with id {product_id}",
        )

    # Return the product price
    return float(product_data["price"])

def calculate_total_price(order: schemas.OrderCreate) -> float:
    """
    Calculate the total price of an order by validating products and summing their prices.
    """
    total_price = 0.0
    for product_item in order.products:
        product_price = validate_product_and_update_stock(product_item.id, product_item.quantity)
        total_price += product_price * product_item.quantity
    return total_price

def create_order_in_db(db: Session, products: List[dict], total_price: float) -> models.Order:
    """
    Create an order in the database.
    """
    db_order = models.Order(
        products=products,  # Store the list of products as JSON
        total_price=total_price,
        created_at=datetime.now(),
    )
    try:
        db.add(db_order)
        db.commit()
        db.refresh(db_order)
        return db_order
    except Exception as e:
        db.rollback()
        raise HTTPException(status_code=400, detail=str(e))
