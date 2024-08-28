from orm.serializer import Serializer
from .models import Product


def productserializer(model, fields):
    serialed = Serializer.all_data(model=model, fields=fields)
    return serialed