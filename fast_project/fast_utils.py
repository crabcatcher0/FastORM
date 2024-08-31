from .serializer import productserializer
from fastapi.requests import Request

def search_products(query: str):
    products = productserializer(
        model='product',
        fields=('id', 'title', 'made_by')
    )
    
    filtered_products = [
        product for product in products
        if query.lower() in product["title"].lower() or query.lower() in product["made_by"].lower()
    ]
    return filtered_products


