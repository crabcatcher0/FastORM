from orm.serializer import Serializer


def studentserializer(model: str, fields: tuple):
    data = Serializer.all_data(
        model=model,
        fields=fields
    )
    return data


def courseserializer(model: str, fields: tuple):
    course_data = Serializer.all_data(
        model= model,
        fields=fields
    )
    return course_data
