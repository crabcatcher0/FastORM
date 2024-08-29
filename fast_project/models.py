from orm.crabmodel import CrabModel, ForeignKey
from orm.datatypes import DataTypes


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
        'password': DataTypes.varchar()
    }