from fastapi import FastAPI, HTTPException, Depends
from sqlalchemy.orm import Session
from typing import List
from datetime import datetime
import requests

from app.database import get_db
from app.models import Order
from app import schemas
from app.utils import calculate_total_price, create_order_in_db


app = FastAPI()


@app.post("/orders/", response_model=schemas.Order, status_code=201)
def create_order(order: schemas.OrderCreate, db: Session = Depends(get_db)):
    """
    Create an order, accepts a list of products and quantities, calculates the total price and saves the order in the database
    """

    # Prepare the list of products for the order
    order_items = [{"id": item.id, "quantity": item.quantity} for item in order.products]

    # Calculate the total price
    total_price = calculate_total_price(order)

    # Create the order in the database
    db_order = create_order_in_db(db, order_items, total_price)

    return db_order


@app.get("/orders/", response_model=List[schemas.Order], status_code=200)
def list_orders(db: Session = Depends(get_db)):
    orders = db.query(Order).all()
    return orders


@app.delete("/orders/{order_id}", status_code=204)
def delete_order(order_id: int, db: Session = Depends(get_db)):
    """
    Delete an order
    """
    order = db.query(Order).filter(Order.id == order_id).first()
    if order:
        db.delete(order)
        db.commit()
        return
    raise HTTPException(status_code=404, detail="Order not found")



@app.get("/orders/{order_id}", response_model=schemas.Order, status_code=200)
def get_order(order_id: int, db: Session = Depends(get_db)):
    """
    Get order details
    """
    order = db.query(Order).filter(Order.id == order_id).first()
    if order:
        return order
    raise HTTPException(status_code=404, detail="Order not found")


@app.put("/orders/{order_id}", response_model=schemas.Order, status_code=200)
def update_order(order_id: int, order: schemas.OrderUpdate, db: Session = Depends(get_db)):
    """
    Update an order, ensure the total price is recalculated, item quantities and item id can be updated
    """
    db_order = db.query(Order).filter(Order.id == order_id).first()
    if db_order:
        order_items = [{"id": item.id, "quantity": item.quantity} for item in order.products]
        total_price = calculate_total_price(order)
        db_order.products = order_items
        db_order.total_price = total_price
        db.commit()
        return db_order
    raise HTTPException(status_code=404, detail="Order not found")