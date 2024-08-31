from orm.crabmodel import CrabModel, ForeignKey
from orm.datatypes import DataTypes
from orm.serializer import Serializer


class Product(CrabModel):
    _column = {
        'title': DataTypes.varchar(max_length=30),
        'made_by': DataTypes.varchar(max_length=35),
        'created_at': DataTypes.datetimefield(auto_add_now=True)
    }


class User(CrabModel):
    _column = {
        'first_name': DataTypes.varchar(max_length=15),
        'last_name': DataTypes.varchar(max_length=15),
        'email': DataTypes.emailfield(unique=True),
        'password': DataTypes.varchar(),
        'review': 'TEXT'
    }
    
    
    def __init__(self, id, first_name, last_name, email, password, review):
        self.id = id
        self.first_name = first_name
        self.last_name = last_name
        self.email = email
        self.password = password
        self.review = review



class Review(CrabModel):
    _column = {
        'review_by': DataTypes.varchar(),
        'in_product': DataTypes.varchar(),
        'comments': 'TEXT',
        'created_at': DataTypes.datetimefield(auto_add_now=True)
    }
    foreign_keys = [
        ForeignKey.create_foreignkey('review_by', 'user', 'id'),
        ForeignKey.create_foreignkey('in_product', 'product', 'email')
    ]


        