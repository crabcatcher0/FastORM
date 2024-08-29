from .serializer import productserializer

def search_products(query: str):
    products = productserializer(
        model='product',
        fields=('title', 'made_by')
    )
    
    filtered_products = [
        product for product in products
        if query.lower() in product["title"].lower() or query.lower() in product["made_by"].lower()
    ]
    return filtered_products