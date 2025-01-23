'''import json

import products
from cart import dao
from products import Product


class Cart:
    def __init__(self, id: int, username: str, contents: list[Product], cost: float):
        self.id = id
        self.username = username
        self.contents = contents
        self.cost = cost

    def load(data):
        return Cart(data['id'], data['username'], data['contents'], data['cost'])


def get_cart(username: str) -> list:
    cart_details = dao.get_cart(username)
    if cart_details is None:
        return []
    
    items = []
    for cart_detail in cart_details:
        contents = cart_detail['contents']
        evaluated_contents = eval(contents)  
        for content in evaluated_contents:
            items.append(content)
    
    i2 = []
    for i in items:
        temp_product = products.get_product(i)
        i2.append(temp_product)
    return i2

    


def add_to_cart(username: str, product_id: int):
    dao.add_to_cart(username, product_id)


def remove_from_cart(username: str, product_id: int):
    dao.remove_from_cart(username, product_id)

def delete_cart(username: str):
    dao.delete_cart(username)'''


import json
from typing import List
from products import Product, get_product
from cart import dao


class Cart:
    def __init__(self, id: int, username: str, contents: List[Product], cost: float):
        self.id = id
        self.username = username
        self.contents = contents
        self.cost = cost

    @staticmethod
    def load(data: dict) -> 'Cart':
        return Cart(
            id=data.get('id', 0),
            username=data.get('username', ''),
            contents=data.get('contents', []),
            cost=data.get('cost', 0.0)
        )


def get_cart(username: str) -> List[Product]:
    """Retrieve a user's cart details."""
    cart_details = dao.get_cart(username)
    if not cart_details:
        return []

    items = []
    for cart_detail in cart_details:
        contents = cart_detail.get('contents', '[]')
        try:
            product_ids = json.loads(contents)  # Parse safely as JSON
        except json.JSONDecodeError:
            product_ids = []  # Handle invalid JSON gracefully

        items.extend(product_ids)

    # Fetch products in one loop
    return [get_product(product_id) for product_id in items]


def add_to_cart(username: str, product_id: int) -> None:
    """Add a product to a user's cart."""
    dao.add_to_cart(username, product_id)


def remove_from_cart(username: str, product_id: int) -> None:
    """Remove a product from a user's cart."""
    dao.remove_from_cart(username, product_id)


def delete_cart(username: str) -> None:
    """Delete a user's cart."""
    dao.delete_cart(username)
