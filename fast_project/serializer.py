from orm.serializer import Serializer


def productserializer(model, fields):
    serialed = Serializer.all_data(model=model, fields=fields)
    return serialed


def for_review():
    serialized = Serializer.all_data(model='product', fields=('id', 'title'))
    return serialized



def oneserializer(model, fields, pk):
    serialized = Serializer.one_data(model=model, fields=fields, pk=pk)
    return serialized




