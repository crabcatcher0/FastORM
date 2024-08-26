from .get_data import GetData

"""

Database result it converted into list of dict   

"""

class Serializer:

    @staticmethod
    def all_data(model: str, fields: tuple):
        data = GetData.get_data(model, fields=fields)
        tup_data = tuple(data)

        final_result = []
        for tup in tup_data:
            zip_data = dict(zip(fields, tup))
            final_result.append(zip_data)

        return final_result
    
    
    @staticmethod
    def one_data(model: str, fields: tuple, pk: int):
        data = GetData.get_one_or_404(model, fields, pk=pk)
        result = dict(zip(fields, data))
        return result
        





    
    
    











