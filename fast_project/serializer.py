from orm.serializer import Serializer


def productserializer(model, fields):
    serialed = Serializer.all_data(model=model, fields=fields)
    return serialed


def oneserializer(model, fields, pk):
    serialized = Serializer.one_data(model=model, fields=fields, pk=pk)
    return serialized


def reviewserializere():
    serialized = Serializer.all_data(
        model='review',
        fields=('id', 'review_by', 'in_product', 'comments')
    )
    return serialized


